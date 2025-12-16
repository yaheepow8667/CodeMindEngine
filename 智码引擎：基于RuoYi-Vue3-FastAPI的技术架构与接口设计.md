# **智码引擎：基于RuoYi-Vue3-FastAPI的技术架构与接口设计**

## **一、 基于RuoYi-Vue3-FastAPI的架构适配**

### **1.1 现有技术栈分析**

**RuoYi-Vue3-FastAPI 技术栈：**
- 前端：Vue 3 + Element Plus + Vite + TypeScript
- 后端：Python FastAPI + SQLAlchemy + Pydantic
- 数据库：MySQL 8.0
- 认证：JWT Token
- 权限：基于角色的访问控制（RBAC）

**智码引擎适配调整：**
```yaml
保留部分：
  - 用户认证与权限系统
  - 基础的后台管理框架
  - 前端组件库（Element Plus）
  - 项目结构和构建工具

扩展部分：
  - 新增AI服务集成模块
  - 新增代码生成引擎
  - 新增蓝图管理模块
  - 增强任务调度系统
```

### **1.2 架构升级方案**

```
┌─────────────────────────────────────────────────────────────┐
│                   智码引擎增强架构                            │
├─────────────────────────────────────────────────────────────┤
│  前端层 (Vue 3 + Element Plus)                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  标准管理后台 │ │ 智能生成工作台 │ │ 蓝图可视化编辑器 │      │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│  接口层 (FastAPI + JWT)                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          原有RuoYi接口          │    智码引擎新接口      │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  服务层 (Python Microservices)                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  智能规划服务 │ │  代码生成服务 │ │  质量保障服务 │         │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  LLM网关服务 │ │  模板管理服务 │ │  任务调度服务 │         │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│  数据层 (MySQL + Redis + MinIO/S3)                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  关系型数据   │ │    缓存     │ │  文件存储    │         │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## **二、 数据库表结构（基于RuoYi的Sys表扩展）**

### **2.1 用户与权限表（原表扩展）**

```sql
-- 1. 用户表（基于sys_user扩展）
ALTER TABLE sys_user ADD (
    api_token VARCHAR(255) COMMENT 'API访问令牌',
    subscription_level VARCHAR(50) DEFAULT 'free' COMMENT '订阅等级：free/team/enterprise',
    subscription_end_time DATETIME COMMENT '订阅到期时间',
    monthly_generation_limit INT DEFAULT 10 COMMENT '月生成次数限制',
    monthly_generation_used INT DEFAULT 0 COMMENT '本月已使用次数',
    total_generation_count INT DEFAULT 0 COMMENT '总生成次数'
);

-- 2. 团队表（新表）
CREATE TABLE sys_team (
    team_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(100) NOT NULL COMMENT '团队名称',
    team_code VARCHAR(50) UNIQUE NOT NULL COMMENT '团队编码',
    team_owner BIGINT NOT NULL COMMENT '团队所有者',
    description VARCHAR(500) COMMENT '团队描述',
    max_members INT DEFAULT 10 COMMENT '最大成员数',
    max_projects INT DEFAULT 50 COMMENT '最大项目数',
    storage_quota_mb INT DEFAULT 1024 COMMENT '存储配额(MB)',
    subscription_plan VARCHAR(50) DEFAULT 'free' COMMENT '订阅计划',
    status CHAR(1) DEFAULT '0' COMMENT '状态（0正常 1停用）',
    create_by VARCHAR(64) DEFAULT '' COMMENT '创建者',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_by VARCHAR(64) DEFAULT '' COMMENT '更新者',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    remark VARCHAR(500) COMMENT '备注',
    FOREIGN KEY (team_owner) REFERENCES sys_user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='团队信息表';

-- 3. 团队成员表
CREATE TABLE sys_team_member (
    member_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    team_id BIGINT NOT NULL COMMENT '团队ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    role_code VARCHAR(50) DEFAULT 'member' COMMENT '角色编码：owner/admin/member/viewer',
    join_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    invited_by BIGINT COMMENT '邀请人',
    status CHAR(1) DEFAULT '0' COMMENT '状态（0正常 1退出）',
    UNIQUE KEY uk_team_user (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES sys_team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES sys_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='团队成员表';
```

### **2.2 项目与蓝图表**

```sql
-- 4. 项目表
CREATE TABLE sys_project (
    project_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    team_id BIGINT NOT NULL COMMENT '所属团队',
    project_name VARCHAR(200) NOT NULL COMMENT '项目名称',
    project_code VARCHAR(100) UNIQUE NOT NULL COMMENT '项目编码',
    description TEXT COMMENT '项目描述',
    tech_stack JSON COMMENT '技术栈配置',
    project_type VARCHAR(50) DEFAULT 'web' COMMENT '项目类型：web/mobile/desktop',
    project_status VARCHAR(20) DEFAULT 'active' COMMENT '项目状态：active/archived/deleted',
    visibility CHAR(1) DEFAULT '0' COMMENT '可见性：0私有 1团队可见 2公开',
    storage_used_mb INT DEFAULT 0 COMMENT '已使用存储(MB)',
    create_by VARCHAR(64) DEFAULT '' COMMENT '创建者',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_by VARCHAR(64) DEFAULT '' COMMENT '更新者',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    remark VARCHAR(500) COMMENT '备注',
    FOREIGN KEY (team_id) REFERENCES sys_team(team_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目信息表';

-- 5. 应用蓝图表
CREATE TABLE app_blueprint (
    blueprint_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    project_id BIGINT NOT NULL COMMENT '所属项目',
    blueprint_name VARCHAR(200) NOT NULL COMMENT '蓝图名称',
    version_tag VARCHAR(50) NOT NULL COMMENT '版本标签',
    spec_data JSON NOT NULL COMMENT '蓝图规格数据',
    spec_summary JSON COMMENT '蓝图摘要',
    is_draft BOOLEAN DEFAULT TRUE COMMENT '是否为草稿',
    parent_id BIGINT COMMENT '父蓝图ID',
    generation_count INT DEFAULT 0 COMMENT '生成次数',
    status CHAR(1) DEFAULT '0' COMMENT '状态（0正常 1废弃）',
    create_by VARCHAR(64) DEFAULT '' COMMENT '创建者',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_by VARCHAR(64) DEFAULT '' COMMENT '更新者',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_project_version (project_id, version_tag),
    FOREIGN KEY (project_id) REFERENCES sys_project(project_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES app_blueprint(blueprint_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='应用蓝图表';

-- 6. 蓝图变更历史表
CREATE TABLE app_blueprint_history (
    history_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    blueprint_id BIGINT NOT NULL COMMENT '蓝图ID',
    version_from VARCHAR(50) COMMENT '源版本',
    version_to VARCHAR(50) COMMENT '目标版本',
    change_type VARCHAR(50) COMMENT '变更类型',
    change_summary JSON COMMENT '变更摘要',
    diff_data JSON COMMENT '差异数据',
    create_by VARCHAR(64) DEFAULT '' COMMENT '操作者',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    FOREIGN KEY (blueprint_id) REFERENCES app_blueprint(blueprint_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='蓝图变更历史表';
```

### **2.3 生成任务与产物表**

```sql
-- 7. 生成任务表
CREATE TABLE gen_task (
    task_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    project_id BIGINT NOT NULL COMMENT '项目ID',
    blueprint_id BIGINT NOT NULL COMMENT '蓝图ID',
    task_name VARCHAR(200) NOT NULL COMMENT '任务名称',
    task_type VARCHAR(50) DEFAULT 'full' COMMENT '任务类型：full/incremental/test',
    target_stack JSON COMMENT '目标技术栈',
    status VARCHAR(50) DEFAULT 'pending' COMMENT '状态',
    progress INT DEFAULT 0 COMMENT '进度(0-100)',
    start_time DATETIME COMMENT '开始时间',
    end_time DATETIME COMMENT '结束时间',
    error_message TEXT COMMENT '错误信息',
    log_path VARCHAR(500) COMMENT '日志路径',
    qa_report JSON COMMENT '质量报告',
    create_by VARCHAR(64) DEFAULT '' COMMENT '创建者',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (project_id) REFERENCES sys_project(project_id) ON DELETE CASCADE,
    FOREIGN KEY (blueprint_id) REFERENCES app_blueprint(blueprint_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生成任务表';

-- 8. 生成产物表
CREATE TABLE gen_artifact (
    artifact_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_id BIGINT NOT NULL COMMENT '任务ID',
    artifact_type VARCHAR(50) NOT NULL COMMENT '产物类型',
    artifact_name VARCHAR(255) NOT NULL COMMENT '产物名称',
    storage_type VARCHAR(50) DEFAULT 'local' COMMENT '存储类型',
    file_path VARCHAR(500) COMMENT '文件路径',
    file_url VARCHAR(500) COMMENT '文件URL',
    file_size BIGINT COMMENT '文件大小',
    checksum VARCHAR(128) COMMENT '文件校验和',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (task_id) REFERENCES gen_task(task_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生成产物表';

-- 9. 部署配置表
CREATE TABLE sys_deployment (
    deploy_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    project_id BIGINT NOT NULL COMMENT '项目ID',
    env_name VARCHAR(50) NOT NULL COMMENT '环境名称',
    config_data JSON NOT NULL COMMENT '配置数据',
    deployed_version VARCHAR(50) COMMENT '已部署版本',
    deployed_time DATETIME COMMENT '部署时间',
    status VARCHAR(20) DEFAULT 'idle' COMMENT '状态',
    create_by VARCHAR(64) DEFAULT '' COMMENT '创建者',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_project_env (project_id, env_name),
    FOREIGN KEY (project_id) REFERENCES sys_project(project_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='部署配置表';
```

### **2.4 模板与插件表**

```sql
-- 10. 代码模板表
CREATE TABLE code_template (
    template_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    template_name VARCHAR(200) NOT NULL COMMENT '模板名称',
    template_code VARCHAR(100) UNIQUE NOT NULL COMMENT '模板编码',
    template_type VARCHAR(50) NOT NULL COMMENT '模板类型',
    target_framework VARCHAR(100) COMMENT '目标框架',
    category VARCHAR(100) COMMENT '分类',
    version VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本',
    template_content JSON NOT NULL COMMENT '模板内容',
    example_data JSON COMMENT '示例数据',
    is_official BOOLEAN DEFAULT FALSE COMMENT '是否官方模板',
    is_public BOOLEAN DEFAULT TRUE COMMENT '是否公开',
    author_id BIGINT COMMENT '作者ID',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    rating DECIMAL(3,2) DEFAULT 0 COMMENT '评分',
    tags JSON COMMENT '标签',
    status CHAR(1) DEFAULT '0' COMMENT '状态',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (author_id) REFERENCES sys_user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='代码模板表';

-- 11. LLM配置表
CREATE TABLE sys_llm_config (
    config_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    provider_name VARCHAR(100) NOT NULL COMMENT '提供商',
    model_name VARCHAR(100) NOT NULL COMMENT '模型名称',
    api_key VARCHAR(500) COMMENT 'API密钥',
    base_url VARCHAR(500) COMMENT '基础URL',
    max_tokens INT DEFAULT 4000 COMMENT '最大token数',
    temperature DECIMAL(3,2) DEFAULT 0.7 COMMENT '温度参数',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    priority INT DEFAULT 1 COMMENT '优先级',
    monthly_limit INT DEFAULT 1000 COMMENT '月调用限制',
    monthly_used INT DEFAULT 0 COMMENT '本月已使用',
    cost_per_1k DECIMAL(10,4) DEFAULT 0.02 COMMENT '每1k token成本',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='LLM配置表';
```

## **三、 FastAPI接口设计**

### **3.1 项目结构**

```
app/
├── main.py                          # 应用入口
├── config/                          # 配置文件
├── core/                            # 核心模块
│   ├── security.py                  # 安全认证
│   ├── dependencies.py              # 依赖注入
│   └── exceptions.py                # 异常处理
├── api/                             # API接口
│   ├── v1/                          # API版本1
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── auth.py              # 认证接口（原RuoYi）
│   │   │   ├── users.py             # 用户接口（原RuoYi）
│   │   │   ├── teams.py             # 团队接口（新增）
│   │   │   ├── projects.py          # 项目接口（新增）
│   │   │   ├── blueprints.py        # 蓝图接口（新增）
│   │   │   ├── generation.py        # 生成接口（新增）
│   │   │   ├── templates.py         # 模板接口（新增）
│   │   │   └── deployment.py        # 部署接口（新增）
│   │   └── api.py                   # API路由注册
├── models/                          # 数据模型
│   ├── sys_user.py                  # 用户模型（扩展）
│   ├── sys_team.py                  # 团队模型
│   ├── sys_project.py               # 项目模型
│   ├── app_blueprint.py             # 蓝图模型
│   ├── gen_task.py                  # 任务模型
│   └── code_template.py             # 模板模型
├── schemas/                         # Pydantic模式
├── services/                        # 业务服务
│   ├── user_service.py              # 用户服务
│   ├── team_service.py              # 团队服务
│   ├── project_service.py           # 项目服务
│   ├── blueprint_service.py         # 蓝图服务
│   ├── generation_service.py        # 生成服务
│   ├── template_service.py          # 模板服务
│   ├── llm_service.py               # LLM服务
│   └── task_queue.py                # 任务队列
├── utils/                           # 工具函数
│   ├── llm_helper.py                # LLM辅助函数
│   ├── code_generator.py            # 代码生成器
│   └── template_engine.py           # 模板引擎
└── tasks/                           # 异步任务
    ├── celery_app.py                # Celery配置
    ├── generation_tasks.py          # 生成任务
    └── qa_tasks.py                  # 质量检查任务
```

### **3.2 核心接口设计**

#### **1. 团队管理接口**

```python
# app/api/v1/endpoints/teams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse
from app.services.team_service import TeamService

router = APIRouter()

@router.post("/teams", response_model=TeamResponse)
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建团队"""
    return TeamService.create_team(db, team, current_user.user_id)

@router.get("/teams", response_model=List[TeamResponse])
async def get_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取团队列表"""
    return TeamService.get_user_teams(db, current_user.user_id, skip, limit)

@router.post("/teams/{team_id}/members")
async def add_team_member(
    team_id: int,
    user_id: int,
    role: str = "member",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """添加团队成员"""
    return TeamService.add_member(db, team_id, user_id, role, current_user.user_id)

@router.get("/teams/{team_id}/projects")
async def get_team_projects(
    team_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取团队项目"""
    return TeamService.get_team_projects(db, team_id, current_user.user_id)
```

#### **2. 项目管理接口**

```python
# app/api/v1/endpoints/projects.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建项目"""
    return ProjectService.create_project(db, project, current_user.user_id)

@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(
    team_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取项目列表"""
    return ProjectService.list_projects(db, current_user.user_id, team_id, skip, limit)

@router.post("/projects/{project_id}/clone")
async def clone_project(
    project_id: int,
    new_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """克隆项目"""
    return ProjectService.clone_project(db, project_id, new_name, current_user.user_id)

@router.get("/projects/{project_id}/stats")
async def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取项目统计"""
    return ProjectService.get_project_stats(db, project_id, current_user.user_id)
```

#### **3. 蓝图管理接口**

```python
# app/api/v1/endpoints/blueprints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user
from app.schemas.blueprint import BlueprintCreate, BlueprintUpdate, BlueprintResponse
from app.services.blueprint_service import BlueprintService

router = APIRouter()

@router.post("/projects/{project_id}/blueprints", response_model=BlueprintResponse)
async def create_blueprint(
    project_id: int,
    blueprint: BlueprintCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建蓝图"""
    return BlueprintService.create_blueprint(db, project_id, blueprint, current_user.user_id)

@router.post("/blueprints/{blueprint_id}/parse")
async def parse_requirements(
    blueprint_id: int,
    requirements: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """解析需求并更新蓝图"""
    return BlueprintService.parse_and_update_blueprint(db, blueprint_id, requirements, current_user.user_id)

@router.get("/blueprints/{blueprint_id}/preview")
async def preview_blueprint(
    blueprint_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """预览蓝图"""
    return BlueprintService.preview_blueprint(db, blueprint_id, current_user.user_id)

@router.get("/blueprints/{blueprint_id}/history")
async def get_blueprint_history(
    blueprint_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取蓝图变更历史"""
    return BlueprintService.get_history(db, blueprint_id, current_user.user_id)
```

#### **4. 代码生成接口**

```python
# app/api/v1/endpoints/generation.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user
from app.schemas.generation import GenerationRequest, TaskResponse
from app.services.generation_service import GenerationService
from app.tasks.generation_tasks import start_generation_task

router = APIRouter()

@router.post("/generate", response_model=TaskResponse)
async def generate_code(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """启动代码生成任务"""
    # 验证用户生成配额
    if not GenerationService.check_quota(db, current_user.user_id):
        raise HTTPException(status_code=402, detail="生成次数已用完")
    
    # 创建任务记录
    task = GenerationService.create_task(db, request, current_user.user_id)
    
    # 异步执行生成任务
    background_tasks.add_task(start_generation_task, task.task_id)
    
    return task

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取任务状态"""
    return GenerationService.get_task(db, task_id, current_user.user_id)

@router.get("/tasks/{task_id}/artifacts")
async def get_task_artifacts(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取任务产物"""
    return GenerationService.get_artifacts(db, task_id, current_user.user_id)

@router.post("/tasks/{task_id}/regenerate")
async def regenerate_code(
    task_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """重新生成代码"""
    return GenerationService.regenerate(db, task_id, current_user.user_id, background_tasks)
```

#### **5. 模板管理接口**

```python
# app/api/v1/endpoints/templates.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateResponse
from app.services.template_service import TemplateService

router = APIRouter()

@router.get("/templates", response_model=List[TemplateResponse])
async def list_templates(
    category: Optional[str] = None,
    framework: Optional[str] = None,
    is_official: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取模板列表"""
    return TemplateService.list_templates(db, category, framework, is_official, skip, limit)

@router.post("/templates", response_model=TemplateResponse)
async def create_template(
    template: TemplateCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建模板"""
    return TemplateService.create_template(db, template, current_user.user_id)

@router.post("/templates/{template_id}/upload")
async def upload_template_content(
    template_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """上传模板文件"""
    content = await file.read()
    return TemplateService.update_content(db, template_id, content, current_user.user_id)

@router.post("/templates/{template_id}/apply")
async def apply_template(
    template_id: int,
    blueprint_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """应用模板到蓝图"""
    return TemplateService.apply_to_blueprint(db, template_id, blueprint_id, current_user.user_id)
```

### **3.3 异步任务设计**

```python
# app/tasks/celery_app.py
from celery import Celery
from app.config import settings

celery_app = Celery(
    "codemind",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.generation_tasks", "app.tasks.qa_tasks"]
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_routes={
        'app.tasks.generation_tasks.*': {'queue': 'generation'},
        'app.tasks.qa_tasks.*': {'queue': 'qa'},
    }
)

# app/tasks/generation_tasks.py
from app.tasks.celery_app import celery_app
from app.services.generation_service import GenerationService
from app.services.llm_service import LLMService
from app.services.code_generator import CodeGenerator
from app.utils.template_engine import TemplateEngine
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
import json

@celery_app.task(bind=True, name="generation.full_generation")
def full_generation_task(self, task_id: int):
    """完整生成任务"""
    db = SessionLocal()
    try:
        # 获取任务信息
        task = GenerationService.get_task_internal(db, task_id)
        
        # 更新任务状态
        GenerationService.update_task_status(db, task_id, "generating", 10)
        
        # 1. 获取蓝图
        blueprint = GenerationService.get_blueprint_for_task(db, task_id)
        
        # 2. 调用LLM进行优化（如果需要）
        if task.task_type == "full":
            self.update_state(state="PROGRESS", meta={"current": 20, "status": "优化蓝图中..."})
            optimized_blueprint = LLMService.optimize_blueprint(blueprint.spec_data)
            GenerationService.update_task_progress(db, task_id, 30)
        
        # 3. 代码生成
        self.update_state(state="PROGRESS", meta={"current": 30, "status": "生成代码中..."})
        code_result = CodeGenerator.generate_from_blueprint(
            optimized_blueprint if task.task_type == "full" else blueprint.spec_data,
            task.target_stack
        )
        GenerationService.update_task_progress(db, task_id, 70)
        
        # 4. 保存产物
        self.update_state(state="PROGRESS", meta={"current": 70, "status": "保存产物中..."})
        artifact = GenerationService.save_artifact(
            db, task_id, "source_zip", 
            "generated_code.zip", code_result["zip_path"]
        )
        
        # 5. 触发质量检查
        self.update_state(state="PROGRESS", meta={"current": 80, "status": "启动质量检查..."})
        from app.tasks.qa_tasks import run_qa_check
        run_qa_check.delay(task_id, artifact.artifact_id)
        
        GenerationService.update_task_status(db, task_id, "qa_checking", 90)
        
    except Exception as e:
        GenerationService.update_task_status(db, task_id, "failed", error=str(e))
        db.close()
        raise
    finally:
        db.close()
```

## **四、 前端组件扩展**

### **4.1 智能生成工作台组件**

```vue
<!-- src/views/generation/GenerationWorkbench.vue -->
<template>
  <div class="generation-workbench">
    <el-row :gutter="20">
      <!-- 左侧：需求输入区 -->
      <el-col :span="8">
        <el-card class="input-panel">
          <template #header>
            <span>需求描述</span>
          </template>
          <el-form :model="requirementForm" label-width="80px">
            <el-form-item label="项目类型">
              <el-select v-model="requirementForm.projectType" placeholder="请选择">
                <el-option label="管理后台" value="admin" />
                <el-option label="数据看板" value="dashboard" />
                <el-option label="电商平台" value="ecommerce" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="需求描述">
              <el-input
                v-model="requirementForm.description"
                type="textarea"
                :rows="8"
                placeholder="请详细描述您的需求，例如：我需要一个用户管理系统，包含用户注册、登录、权限管理、用户列表展示和编辑功能..."
              />
            </el-form-item>
            
            <el-form-item label="附加文件">
              <el-upload
                class="upload-demo"
                action="#"
                :on-change="handleFileUpload"
                :auto-upload="false"
                multiple
              >
                <el-button type="primary">上传草图或文档</el-button>
              </el-upload>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="parseRequirements" :loading="parsing">
                智能解析
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 中间：蓝图预览区 -->
      <el-col :span="8">
        <el-card class="blueprint-panel">
          <template #header>
            <span>应用蓝图</span>
            <el-button style="float: right" size="small" @click="editBlueprint">
              编辑
            </el-button>
          </template>
          
          <el-tabs v-model="activeBlueprintTab">
            <el-tab-pane label="数据模型" name="dataModels">
              <BlueprintDataModels :models="blueprint.dataModels" />
            </el-tab-pane>
            <el-tab-pane label="页面设计" name="pages">
              <BlueprintPages :pages="blueprint.pages" />
            </el-tab-pane>
            <el-tab-pane label="API接口" name="apis">
              <BlueprintApis :apis="blueprint.apis" />
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
      
      <!-- 右侧：生成配置区 -->
      <el-col :span="8">
        <el-card class="config-panel">
          <template #header>
            <span>生成配置</span>
          </template>
          
          <el-form :model="generationConfig" label-width="100px">
            <el-form-item label="前端框架">
              <el-select v-model="generationConfig.frontend">
                <el-option label="Vue 3" value="vue3" />
                <el-option label="React" value="react" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="UI库">
              <el-select v-model="generationConfig.uiLibrary">
                <el-option label="Element Plus" value="element-plus" />
                <el-option label="Ant Design Vue" value="ant-design-vue" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="后端框架">
              <el-select v-model="generationConfig.backend">
                <el-option label="FastAPI" value="fastapi" />
                <el-option label="NestJS" value="nestjs" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="数据库">
              <el-select v-model="generationConfig.database">
                <el-option label="MySQL" value="mysql" />
                <el-option label="PostgreSQL" value="postgresql" />
              </el-select>
            </el-form-item>
            
            <el-divider />
            
            <el-form-item>
              <el-button 
                type="primary" 
                @click="startGeneration" 
                :loading="generating"
                :disabled="!blueprint.valid"
              >
                开始生成
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 生成进度对话框 -->
    <el-dialog
      v-model="progressDialogVisible"
      title="代码生成中"
      width="600px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
    >
      <el-progress
        :percentage="generationProgress"
        :status="generationStatus"
        :text-inside="true"
        :stroke-width="20"
      />
      <div class="progress-message">{{ generationMessage }}</div>
      
      <template #footer>
        <el-button @click="cancelGeneration" :disabled="!canCancel">
          取消
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import BlueprintDataModels from '@/components/blueprint/DataModels.vue'
import BlueprintPages from '@/components/blueprint/Pages.vue'
import BlueprintApis from '@/components/blueprint/Apis.vue'
import { parseRequirements, startGenerationTask } from '@/api/generation'

const requirementForm = reactive({
  projectType: 'admin',
  description: '',
  attachments: []
})

const blueprint = reactive({
  dataModels: [],
  pages: [],
  apis: [],
  valid: false
})

const generationConfig = reactive({
  frontend: 'vue3',
  uiLibrary: 'element-plus',
  backend: 'fastapi',
  database: 'mysql'
})

const parsing = ref(false)
const generating = ref(false)
const progressDialogVisible = ref(false)
const generationProgress = ref(0)
const generationMessage = ref('')
const generationStatus = ref('')
const canCancel = ref(true)
const activeBlueprintTab = ref('dataModels')

const handleFileUpload = (file) => {
  requirementForm.attachments.push(file)
}

const parseRequirements = async () => {
  if (!requirementForm.description.trim()) {
    ElMessage.warning('请输入需求描述')
    return
  }
  
  parsing.value = true
  try {
    const response = await parseRequirements({
      description: requirementForm.description,
      projectType: requirementForm.projectType,
      attachments: requirementForm.attachments
    })
    
    blueprint.dataModels = response.data.dataModels || []
    blueprint.pages = response.data.pages || []
    blueprint.apis = response.data.apis || []
    blueprint.valid = true
    
    ElMessage.success('需求解析成功')
  } catch (error) {
    ElMessage.error('需求解析失败：' + error.message)
  } finally {
    parsing.value = false
  }
}

const startGeneration = async () => {
  if (!blueprint.valid) {
    ElMessage.warning('请先完成需求解析')
    return
  }
  
  generating.value = true
  progressDialogVisible.value = true
  generationProgress.value = 0
  generationMessage.value = '任务提交中...'
  
  try {
    const taskId = await startGenerationTask({
      blueprint: blueprint,
      config: generationConfig
    })
    
    // 开始轮询任务状态
    pollTaskStatus(taskId)
    
  } catch (error) {
    ElMessage.error('启动生成失败：' + error.message)
    generating.value = false
    progressDialogVisible.value = false
  }
}

const pollTaskStatus = async (taskId) => {
  const interval = setInterval(async () => {
    try {
      const response = await getTaskStatus(taskId)
      const task = response.data
      
      generationProgress.value = task.progress
      generationMessage.value = task.message || `当前进度：${task.progress}%`
      generationStatus.value = task.status === 'failed' ? 'exception' : ''
      
      if (task.status === 'success') {
        clearInterval(interval)
        generationMessage.value = '生成完成！'
        setTimeout(() => {
          progressDialogVisible.value = false
          ElMessage.success('代码生成成功')
          // 跳转到结果页面
          router.push(`/generation/results/${taskId}`)
        }, 1000)
      } else if (task.status === 'failed') {
        clearInterval(interval)
        canCancel.value = false
        generationMessage.value = `生成失败：${task.error_message}`
      }
    } catch (error) {
      console.error('轮询任务状态失败:', error)
    }
  }, 2000)
}

const cancelGeneration = () => {
  // 取消生成逻辑
  ElMessage.info('已取消生成任务')
  progressDialogVisible.value = false
  generating.value = false
}

const editBlueprint = () => {
  // 跳转到蓝图编辑器
  router.push({
    name: 'BlueprintEditor',
    params: { blueprintData: blueprint }
  })
}
</script>
```

### **4.2 蓝图可视化编辑器组件**

```vue
<!-- src/components/blueprint/VisualEditor.vue -->
<template>
  <div class="visual-editor">
    <div class="editor-toolbar">
      <el-button-group>
        <el-button @click="switchView('data')" :type="activeView === 'data' ? 'primary' : ''">
          <el-icon><DataLine /></el-icon> 数据模型
        </el-button>
        <el-button @click="switchView('page')" :type="activeView === 'page' ? 'primary' : ''">
          <el-icon><Monitor /></el-icon> 页面设计
        </el-button>
        <el-button @click="switchView('api')" :type="activeView === 'api' ? 'primary' : ''">
          <el-icon><Connection /></el-icon> API设计
        </el-button>
      </el-button-group>
      
      <div class="toolbar-actions">
        <el-button @click="saveBlueprint">
          <el-icon><Save /></el-icon> 保存
        </el-button>
        <el-button @click="validateBlueprint">
          <el-icon><Checked /></el-icon> 验证
        </el-button>
        <el-button @click="exportBlueprint">
          <el-icon><Download /></el-icon> 导出
        </el-button>
      </div>
    </div>
    
    <div class="editor-main">
      <!-- 左侧：组件库 -->
      <div class="component-library">
        <el-collapse v-model="activeCollapse">
          <el-collapse-item title="数据实体" name="entities">
            <draggable
              v-model="entityComponents"
              :group="{ name: 'components', pull: 'clone', put: false }"
              :clone="cloneComponent"
              item-key="id"
            >
              <template #item="{ element }">
                <div class="component-item" :data-type="element.type">
                  <el-icon><component :is="element.icon" /></el-icon>
                  <span>{{ element.name }}</span>
                </div>
              </template>
            </draggable>
          </el-collapse-item>
          
          <el-collapse-item title="UI组件" name="ui">
            <draggable
              v-model="uiComponents"
              :group="{ name: 'components', pull: 'clone', put: false }"
              :clone="cloneComponent"
              item-key="id"
            >
              <template #item="{ element }">
                <div class="component-item" :data-type="element.type">
                  <el-icon><component :is="element.icon" /></el-icon>
                  <span>{{ element.name }}</span>
                </div>
              </template>
            </draggable>
          </el-collapse-item>
        </el-collapse>
      </div>
      
      <!-- 中间：画布 -->
      <div class="editor-canvas" @drop="handleDrop" @dragover.prevent>
        <div v-if="activeView === 'data'" class="data-model-canvas">
          <EntityDiagram :entities="blueprint.dataModels" />
        </div>
        
        <div v-else-if="activeView === 'page'" class="page-canvas">
          <PageCanvas :pages="blueprint.pages" />
        </div>
        
        <div v-else class="api-canvas">
          <ApiFlowChart :apis="blueprint.apis" />
        </div>
      </div>
      
      <!-- 右侧：属性面板 -->
      <div class="property-panel">
        <el-tabs v-model="activePropertyTab">
          <el-tab-pane label="属性" name="properties">
            <PropertyEditor 
              :selected-item="selectedItem" 
              @update="updateItemProperty"
            />
          </el-tab-pane>
          <el-tab-pane label="样式" name="styles">
            <StyleEditor :selected-item="selectedItem" />
          </el-tab-pane>
          <el-tab-pane label="数据绑定" name="binding">
            <DataBindingEditor :selected-item="selectedItem" />
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>
```

## **五、 核心服务实现**

### **5.1 LLM服务封装**

```python
# app/services/llm_service.py
from typing import Dict, Any, List, Optional
import openai
from openai import OpenAI
import anthropic
import json
from app.config import settings
from app.models.sys_llm_config import LLMConfig
from app.db.session import SessionLocal
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """LLM服务封装"""
    
    @staticmethod
    def get_llm_client(config: LLMConfig):
        """获取LLM客户端"""
        if config.provider_name == "openai":
            return OpenAI(
                api_key=config.api_key,
                base_url=config.base_url or "https://api.openai.com/v1"
            )
        elif config.provider_name == "anthropic":
            return anthropic.Anthropic(api_key=config.api_key)
        else:
            # 支持国内大模型
            return OpenAI(
                api_key=config.api_key,
                base_url=config.base_url
            )
    
    @staticmethod
    async def parse_requirements(requirements: str, project_type: str = "admin") -> Dict[str, Any]:
        """解析需求生成蓝图"""
        db = SessionLocal()
        try:
            # 获取最优的LLM配置
            config = db.query(LLMConfig).filter(
                LLMConfig.is_active == True
            ).order_by(LLMConfig.priority).first()
            
            if not config:
                raise ValueError("没有可用的LLM配置")
            
            client = LLMService.get_llm_client(config)
            
            # 构建提示词
            prompt = LLMService.build_parse_prompt(requirements, project_type)
            
            # 调用LLM
            if config.provider_name == "openai":
                response = client.chat.completions.create(
                    model=config.model_name,
                    messages=[
                        {"role": "system", "content": "你是一个资深的全栈架构师，擅长将业务需求转化为技术设计方案。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=config.temperature,
                    max_tokens=config.max_tokens,
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content)
                
            elif config.provider_name == "anthropic":
                response = client.messages.create(
                    model=config.model_name,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                result = json.loads(response.content[0].text)
            
            # 更新使用量
            config.monthly_used += 1
            db.commit()
            
            return result
            
        except Exception as e:
            logger.error(f"解析需求失败: {str(e)}")
            raise
        finally:
            db.close()
    
    @staticmethod
    def build_parse_prompt(requirements: str, project_type: str) -> str:
        """构建解析需求的提示词"""
        return f"""
        请将以下需求转化为一个完整的应用蓝图（Application Blueprint）。

        项目类型：{project_type}
        用户需求：{requirements}

        请按照以下JSON格式输出蓝图：
        {{
          "dataModels": [
            {{
              "name": "实体名称",
              "description": "实体描述",
              "fields": [
                {{"name": "字段名", "type": "字段类型", "required": true/false, "unique": true/false}}
              ],
              "relations": [
                {{"type": "OneToMany/ManyToOne/ManyToMany", "target": "关联实体"}}
              ]
            }}
          ],
          "pages": [
            {{
              "name": "页面名称",
              "path": "/路由路径",
              "layout": "页面布局",
              "components": [
                {{
                  "type": "组件类型",
                  "name": "组件标识",
                  "props": {{}},
                  "dataBinding": {{"entity": "实体名", "action": "操作"}},
                  "events": []
                }}
              ]
            }}
          ],
          "apis": [
            {{
              "path": "/api/路径",
              "method": "GET/POST/PUT/DELETE",
              "description": "接口描述",
              "parameters": [],
              "responses": {{}}
            }}
          ],
          "businessFlows": []
        }}

        请确保蓝图的结构完整、合理，能够直接用于代码生成。
        """
    
    @staticmethod
    async def optimize_blueprint(blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """优化应用蓝图"""
        # 实现蓝图优化逻辑
        pass
```

### **5.2 代码生成服务**

```python
# app/services/code_generator.py
import os
import json
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, Any, List
import jinja2
from app.utils.template_engine import TemplateEngine

class CodeGenerator:
    """代码生成器"""
    
    @staticmethod
    def generate_from_blueprint(blueprint: Dict[str, Any], config: Dict[str, str]) -> Dict[str, Any]:
        """从蓝图生成代码"""
        # 创建临时目录
        temp_dir = tempfile.mkdtemp(prefix="codemind_")
        
        try:
            # 1. 生成项目结构
            project_structure = CodeGenerator.generate_project_structure(
                blueprint, config, temp_dir
            )
            
            # 2. 生成数据模型代码
            CodeGenerator.generate_data_models(blueprint, config, temp_dir)
            
            # 3. 生成API代码
            CodeGenerator.generate_apis(blueprint, config, temp_dir)
            
            # 4. 生成前端代码
            CodeGenerator.generate_frontend(blueprint, config, temp_dir)
            
            # 5. 生成配置文件
            CodeGenerator.generate_config_files(blueprint, config, temp_dir)
            
            # 6. 打包为ZIP
            zip_path = CodeGenerator.create_zip_package(temp_dir)
            
            return {
                "success": True,
                "temp_dir": temp_dir,
                "zip_path": zip_path,
                "file_count": CodeGenerator.count_files(temp_dir)
            }
            
        except Exception as e:
            # 清理临时目录
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise
    
    @staticmethod
    def generate_project_structure(blueprint: Dict[str, Any], config: Dict[str, str], base_dir: str):
        """生成项目结构"""
        project_name = blueprint.get("projectName", "generated_app")
        
        # 根据技术栈创建不同的目录结构
        if config["frontend"] == "vue3":
            frontend_dir = os.path.join(base_dir, "frontend")
            os.makedirs(frontend_dir, exist_ok=True)
            
            # Vue3项目结构
            dirs = [
                "src/components",
                "src/views",
                "src/api",
                "src/router",
                "src/store",
                "src/utils",
                "public"
            ]
            
            for dir_path in dirs:
                os.makedirs(os.path.join(frontend_dir, dir_path), exist_ok=True)
        
        if config["backend"] == "fastapi":
            backend_dir = os.path.join(base_dir, "backend")
            os.makedirs(backend_dir, exist_ok=True)
            
            # FastAPI项目结构
            dirs = [
                "app/api/v1/endpoints",
                "app/models",
                "app/schemas",
                "app/services",
                "app/utils",
                "tests"
            ]
            
            for dir_path in dirs:
                os.makedirs(os.path.join(backend_dir, dir_path), exist_ok=True)
        
        return {
            "project_name": project_name,
            "frontend_dir": frontend_dir if 'frontend_dir' in locals() else None,
            "backend_dir": backend_dir if 'backend_dir' in locals() else None
        }
    
    @staticmethod
    def generate_data_models(blueprint: Dict[str, Any], config: Dict[str, str], base_dir: str):
        """生成数据模型代码"""
        data_models = blueprint.get("dataModels", [])
        
        if config["backend"] == "fastapi":
            # 生成SQLAlchemy模型
            for model in data_models:
                template_data = {
                    "model_name": model["name"],
                    "fields": model.get("fields", []),
                    "relations": model.get("relations", [])
                }
                
                # 使用模板引擎生成代码
                model_code = TemplateEngine.render(
                    "fastapi_model.py.j2", 
                    template_data
                )
                
                # 保存到文件
                model_file = os.path.join(
                    base_dir, "backend", "app", "models", 
                    f"{model['name'].lower()}.py"
                )
                
                with open(model_file, "w", encoding="utf-8") as f:
                    f.write(model_code)
        
        if config["frontend"] == "vue3":
            # 生成TypeScript接口
            types_code = TemplateEngine.render(
                "vue3_types.ts.j2",
                {"models": data_models}
            )
            
            types_file = os.path.join(
                base_dir, "frontend", "src", "types", "models.ts"
            )
            
            os.makedirs(os.path.dirname(types_file), exist_ok=True)
            with open(types_file, "w", encoding="utf-8") as f:
                f.write(types_code)
    
    @staticmethod
    def create_zip_package(source_dir: str) -> str:
        """创建ZIP包"""
        zip_path = os.path.join(tempfile.gettempdir(), f"codemind_{os.path.basename(source_dir)}.zip")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        
        return zip_path
```

## **六、 部署与配置**

### **6.1 Docker Compose配置**

```yaml
# docker-compose.yml
version: '3.8'

services:
  # MySQL数据库
  mysql:
    image: mysql:8.0
    container_name: codemind-mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - codemind-network

  # Redis缓存
  redis:
    image: redis:7-alpine
    container_name: codemind-redis
    ports:
      - "6379:6379"
    networks:
      - codemind-network

  # MinIO对象存储（用于文件存储）
  minio:
    image: minio/minio
    container_name: codemind-minio
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
    networks:
      - codemind-network

  # FastAPI后端
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: codemind-backend
    environment:
      - DATABASE_URL=mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mysql:3306/${MYSQL_DATABASE}
      - REDIS_URL=redis://redis:6379/0
      - MINIO_ENDPOINT=minio:9000
    ports:
      - "8000:8000"
    depends_on:
      - mysql
      - redis
      - minio
    volumes:
      - ./backend:/app
    networks:
      - codemind-network

  # Celery Worker（处理异步任务）
  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: codemind-celery-worker
    command: celery -A app.tasks.celery_app worker --loglevel=info -Q generation,qa
    environment:
      - DATABASE_URL=mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mysql:3306/${MYSQL_DATABASE}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
      - mysql
    volumes:
      - ./backend:/app
    networks:
      - codemind-network

  # Vue3前端
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: codemind-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - codemind-network

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    container_name: codemind-nginx
    ports:
      - "8080:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - frontend
      - backend
    networks:
      - codemind-network

networks:
  codemind-network:
    driver: bridge

volumes:
  mysql_data:
  minio_data:
```

### **6.2 环境变量配置**

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "智码引擎"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/codemind"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 文件存储配置
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "codemind"
    
    # AI服务配置
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # 生成限制
    FREE_USER_DAILY_LIMIT: int = 10
    TEAM_USER_DAILY_LIMIT: int = 100
    ENTERPRISE_USER_DAILY_LIMIT: int = 1000
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## **七、 总结**

基于RuoYi-Vue3-FastAPI的智码引擎技术架构实现了以下核心特性：

### **7.1 技术优势**
1. **快速启动**：基于成熟的开源框架，快速搭建企业级应用
2. **前后端分离**：清晰的API接口设计，便于扩展和维护
3. **异步任务处理**：使用Celery处理耗时的代码生成任务
4. **模块化设计**：每个功能模块独立，便于开发和测试
5. **容器化部署**：支持Docker部署，便于扩展和运维

### **7.2 关键改进点**
1. **用户系统扩展**：在原有RuoYi用户系统基础上增加团队、项目、配额管理
2. **蓝图管理**：实现应用蓝图的全生命周期管理
3. **智能生成流水线**：集成LLM服务，实现从需求到代码的自动化
4. **模板引擎**：支持可扩展的代码模板系统
5. **质量保障**：集成自动化代码检查和测试生成

### **7.3 部署要求**
- 服务器：最低2核4GB内存
- 数据库：MySQL 8.0+
- 缓存：Redis 6.0+
- 存储：MinIO或兼容S3的对象存储
- Python：3.9+
- Node.js：18+

该架构既保留了RuoYi-Vue3-FastAPI的成熟稳定特性，又扩展了AI驱动低代码开发的核心功能，是一个平衡了开发效率和系统稳定性的技术方案。

