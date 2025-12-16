# API接口设计文档

## 1. 接口规范概述

### 1.1 规范版本
采用OpenAPI 3.0规范进行API接口设计。

### 1.2 基础URL
```
/api/v1
```

### 1.3 响应格式
统一使用JSON格式响应，标准格式如下：

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {}
}
```

## 2. 核心接口设计

### 2.1 项目结构

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py              # 认证接口（原RuoYi）
│   │   │   ├── users.py             # 用户接口（原RuoYi）
│   │   │   ├── teams.py             # 团队接口（新增）
│   │   │   ├── projects.py          # 项目接口（新增）
│   │   │   ├── blueprints.py        # 蓝图接口（新增）
│   │   │   ├── generation.py        # 生成接口（新增）
│   │   │   ├── templates.py         # 模板接口（新增）
│   │   │   └── deployment.py        # 部署接口（新增）
```

### 2.2 团队管理接口

#### 创建团队
```python
@router.post("/teams", response_model=TeamResponse)
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建团队"""
    return TeamService.create_team(db, team, current_user.user_id)
```

#### 获取团队列表
```python
@router.get("/teams", response_model=List[TeamResponse])
async def get_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取团队列表"""
    return TeamService.get_user_teams(db, current_user.user_id, skip, limit)
```

#### 添加团队成员
```python
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
```

### 2.3 项目管理接口

#### 创建项目
```python
@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建项目"""
    return ProjectService.create_project(db, project, current_user.user_id)
```

#### 获取项目列表
```python
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
```

#### 克隆项目
```python
@router.post("/projects/{project_id}/clone")
async def clone_project(
    project_id: int,
    new_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """克隆项目"""
    return ProjectService.clone_project(db, project_id, new_name, current_user.user_id)
```

### 2.4 蓝图管理接口

#### 创建蓝图
```python
@router.post("/projects/{project_id}/blueprints", response_model=BlueprintResponse)
async def create_blueprint(
    project_id: int,
    blueprint: BlueprintCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建蓝图"""
    return BlueprintService.create_blueprint(db, project_id, blueprint, current_user.user_id)
```

#### 解析需求
```python
@router.post("/blueprints/{blueprint_id}/parse")
async def parse_requirements(
    blueprint_id: int,
    requirements: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """解析需求"""
    return BlueprintService.parse_requirements(db, blueprint_id, requirements, current_user.user_id)
```

## 3. 安全规范

### 3.1 认证机制
- 使用JWT Token进行认证
- Token有效期：24小时

### 3.2 权限控制
- 基于角色的访问控制（RBAC）
- 每个接口都需要验证用户权限

### 3.3 接口限流
- 防止API滥用
- 根据接口重要性设置不同的限流策略

## 4. 错误处理

### 4.1 错误码定义
| 错误码 | 描述 |
|-------|------|
| 200   | 操作成功 |
| 400   | 请求参数错误 |
| 401   | 未认证 |
| 403   | 无权限 |
| 404   | 资源不存在 |
| 500   | 服务器内部错误 |

### 4.2 错误响应格式

```json
{
  "code": 400,
  "msg": "请求参数错误",
  "data": null
}
```
