-- 智码引擎数据库表结构 (基于RuoYi-FastAPI扩展)
-- 生成时间: 2025-12-16

-- ===========================================
-- 1. 扩展现有用户表 (sys_user)
-- ===========================================
ALTER TABLE sys_user
ADD COLUMN display_name VARCHAR(100) COMMENT '显示名称',
ADD COLUMN avatar_url TEXT COMMENT '头像地址',
ADD COLUMN role VARCHAR(50) DEFAULT 'user' COMMENT '用户角色 (user, admin, super_admin)',
ADD COLUMN email_verified BOOLEAN DEFAULT FALSE COMMENT '邮箱是否验证',
ADD COLUMN uuid CHAR(36) UNIQUE DEFAULT (UUID()) COMMENT 'UUID 标识',
ADD COLUMN last_login_at DATETIME COMMENT '最后登录时间';

-- ===========================================
-- 2. 团队与组织管理表
-- ===========================================

-- 团队表
CREATE TABLE teams (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(200) NOT NULL COMMENT '团队名称',
    slug VARCHAR(100) UNIQUE NOT NULL COMMENT '团队URL标识',
    description TEXT COMMENT '团队描述',
    logo_url TEXT COMMENT '团队logo',
    subscription_plan VARCHAR(50) DEFAULT 'free' COMMENT '订阅计划 (free, team, enterprise)',
    subscription_status VARCHAR(20) DEFAULT 'active' COMMENT '订阅状态 (active, canceled, past_due)',
    subscription_ends_at DATETIME NULL COMMENT '订阅到期时间',
    created_by_user_id BIGINT(20) COMMENT '创建者用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_teams_subscription_status (subscription_status),
    INDEX idx_teams_created_by (created_by_user_id),
    FOREIGN KEY (created_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '团队表';

-- 团队成员表
CREATE TABLE team_members (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    team_id CHAR(36) NOT NULL COMMENT '团队ID',
    user_id BIGINT(20) NOT NULL COMMENT '用户ID',
    role VARCHAR(50) DEFAULT 'member' COMMENT '成员角色 (owner, admin, member, viewer)',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    invited_by_user_id BIGINT(20) COMMENT '邀请者用户ID',
    invited_at DATETIME NULL COMMENT '邀请时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_team_members_team_user (team_id, user_id),
    INDEX idx_team_members_user (user_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES sys_user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (invited_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '团队成员表';

-- 邀请表
CREATE TABLE invitations (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    team_id CHAR(36) NOT NULL COMMENT '团队ID',
    email VARCHAR(255) NOT NULL COMMENT '邀请邮箱',
    token VARCHAR(255) UNIQUE NOT NULL COMMENT '邀请令牌',
    role VARCHAR(50) DEFAULT 'member' COMMENT '邀请角色',
    invited_by_user_id BIGINT(20) COMMENT '邀请者用户ID',
    expires_at DATETIME NOT NULL COMMENT '邀请过期时间',
    accepted_at DATETIME NULL COMMENT '接受时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_invitations_team_email (team_id, email),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (invited_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '邀请表';

-- ===========================================
-- 3. 项目与蓝图管理表
-- ===========================================

-- 项目表
CREATE TABLE projects (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    team_id CHAR(36) NOT NULL COMMENT '团队ID',
    name VARCHAR(200) NOT NULL COMMENT '项目名称',
    slug VARCHAR(100) NOT NULL COMMENT '项目标识（团队内唯一）',
    description TEXT COMMENT '项目描述',
    tech_stack JSON COMMENT '技术栈配置 {"frontend": "vue3", "backend": "nestjs", "ui": "ant-design-vue"}',
    status VARCHAR(20) DEFAULT 'active' COMMENT '项目状态 (active, archived, deleted)',
    is_public BOOLEAN DEFAULT FALSE COMMENT '是否公开',
    storage_quota_mb INTEGER DEFAULT 1024 COMMENT '存储配额 (MB)',
    created_by_user_id BIGINT(20) COMMENT '创建者用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_projects_team_slug (team_id, slug),
    INDEX idx_projects_team (team_id),
    INDEX idx_projects_status (status),
    INDEX idx_projects_created_by (created_by_user_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '项目表';

-- 蓝图表
CREATE TABLE blueprints (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL COMMENT '项目ID',
    name VARCHAR(200) NOT NULL COMMENT '蓝图名称',
    description TEXT COMMENT '蓝图描述',
    version_tag VARCHAR(50) NOT NULL COMMENT '版本标签（如 v1.0.0, draft-1）',
    spec_document_id VARCHAR(100) COMMENT '独立文档存储中的文档ID',
    spec_summary JSON COMMENT '蓝图摘要信息',
    is_draft BOOLEAN DEFAULT TRUE COMMENT '是否为草稿',
    parent_blueprint_id CHAR(36) COMMENT '父蓝图ID',
    created_by_user_id BIGINT(20) COMMENT '创建者用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_blueprints_project_version (project_id, version_tag),
    INDEX idx_blueprints_project (project_id),
    INDEX idx_blueprints_is_draft (is_draft),
    INDEX idx_blueprints_created_at (created_at),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_blueprint_id) REFERENCES blueprints(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '蓝图表';

-- 蓝图变更记录表
CREATE TABLE blueprint_changes (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    blueprint_id CHAR(36) NOT NULL COMMENT '蓝图ID',
    change_type VARCHAR(50) COMMENT '变更类型 (create, update, delete)',
    field_path VARCHAR(500) COMMENT '变更字段路径 如 "dataModels.User.fields"',
    old_value JSON COMMENT '旧值',
    new_value JSON COMMENT '新值',
    changed_by_user_id BIGINT(20) COMMENT '变更者用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_blueprint_changes_blueprint (blueprint_id),
    FOREIGN KEY (blueprint_id) REFERENCES blueprints(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '蓝图变更记录表';

-- ===========================================
-- 4. 生成与任务管理表
-- ===========================================

-- 生成任务表
CREATE TABLE generation_jobs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL COMMENT '项目ID',
    blueprint_id CHAR(36) NOT NULL COMMENT '蓝图ID',
    status VARCHAR(50) DEFAULT 'pending' COMMENT '任务状态 (pending, generating, qa, success, failed)',
    target_tech_stack JSON COMMENT '目标技术栈配置',
    trigger_type VARCHAR(50) DEFAULT 'manual' COMMENT '触发类型 (manual, api, webhook, schedule)',
    triggered_by_user_id BIGINT(20) COMMENT '触发者用户ID',
    started_at DATETIME NULL COMMENT '开始时间',
    completed_at DATETIME NULL COMMENT '完成时间',
    error_message TEXT COMMENT '错误信息',
    logs JSON COMMENT '生成日志',
    qa_report JSON COMMENT '质量检查报告',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_generation_jobs_project (project_id),
    INDEX idx_generation_jobs_status (status),
    INDEX idx_generation_jobs_created_at (created_at),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (blueprint_id) REFERENCES blueprints(id) ON DELETE CASCADE,
    FOREIGN KEY (triggered_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '生成任务表';

-- 生成产物表
CREATE TABLE generated_artifacts (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    job_id CHAR(36) NOT NULL COMMENT '生成任务ID',
    artifact_type VARCHAR(50) NOT NULL COMMENT '产物类型 (source_zip, qa_report, deploy_config, api_docs)',
    artifact_name VARCHAR(255) NOT NULL COMMENT '产物名称',
    storage_type VARCHAR(50) DEFAULT 'local' COMMENT '存储类型 (s3, oss, local)',
    storage_path TEXT NOT NULL COMMENT '存储路径',
    storage_url TEXT COMMENT '访问URL',
    file_size_bytes BIGINT COMMENT '文件大小 (字节)',
    mime_type VARCHAR(100) COMMENT '文件类型',
    checksum VARCHAR(255) COMMENT '校验和',
    is_compressed BOOLEAN DEFAULT TRUE COMMENT '是否压缩',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_generated_artifacts_job (job_id),
    FOREIGN KEY (job_id) REFERENCES generation_jobs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '生成产物表';

-- 部署配置表
CREATE TABLE deployment_configs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL COMMENT '项目ID',
    name VARCHAR(200) NOT NULL COMMENT '配置名称',
    environment VARCHAR(50) NOT NULL COMMENT '部署环境 (development, staging, production)',
    config JSON NOT NULL COMMENT '部署配置内容',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    deployed_job_id CHAR(36) COMMENT '已部署的任务ID',
    deployed_at DATETIME NULL COMMENT '部署时间',
    deployed_by_user_id BIGINT(20) COMMENT '部署者用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_deployment_configs_project_env_name (project_id, environment, name),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (deployed_job_id) REFERENCES generation_jobs(id) ON DELETE SET NULL,
    FOREIGN KEY (deployed_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '部署配置表';

-- ===========================================
-- 5. 模板与插件管理表
-- ===========================================

-- 模板表
CREATE TABLE templates (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(200) NOT NULL COMMENT '模板名称',
    slug VARCHAR(100) UNIQUE NOT NULL COMMENT '模板标识',
    description TEXT COMMENT '模板描述',
    category VARCHAR(100) NOT NULL COMMENT '模板分类 (ui_component, api_layer, project_scaffold, workflow)',
    target_framework VARCHAR(100) COMMENT '目标框架 (vue3, react, nestjs, spring_boot)',
    complexity_level VARCHAR(20) DEFAULT 'basic' COMMENT '复杂度 (basic, intermediate, advanced)',
    is_official BOOLEAN DEFAULT FALSE COMMENT '是否官方模板',
    is_public BOOLEAN DEFAULT TRUE COMMENT '是否公开',
    author_user_id BIGINT(20) COMMENT '作者用户ID',
    download_count INTEGER DEFAULT 0 COMMENT '下载次数',
    rating DECIMAL(3,2) DEFAULT 0 COMMENT '评分',
    version VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本',
    tags JSON COMMENT '标签数组',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_templates_category (category),
    INDEX idx_templates_target_framework (target_framework),
    INDEX idx_templates_is_public (is_public),
    FOREIGN KEY (author_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '模板表';

-- 模板版本表
CREATE TABLE template_versions (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    template_id CHAR(36) NOT NULL COMMENT '模板ID',
    version VARCHAR(50) NOT NULL COMMENT '版本号',
    changelog TEXT COMMENT '更新日志',
    template_content JSON NOT NULL COMMENT '模板JSON定义',
    example_blueprint JSON COMMENT '示例蓝图',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    published_at DATETIME NULL COMMENT '发布时间',
    published_by_user_id BIGINT(20) COMMENT '发布者用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_template_versions_template_version (template_id, version),
    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
    FOREIGN KEY (published_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '模板版本表';

-- 插件表
CREATE TABLE plugins (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(200) NOT NULL COMMENT '插件名称',
    plugin_type VARCHAR(50) NOT NULL COMMENT '插件类型 (code_generator, qa_checker, deployer)',
    target_framework VARCHAR(100) COMMENT '目标框架',
    version VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本',
    author_user_id BIGINT(20) COMMENT '作者用户ID',
    is_approved BOOLEAN DEFAULT FALSE COMMENT '是否已审核',
    install_count INTEGER DEFAULT 0 COMMENT '安装次数',
    config_schema JSON COMMENT '插件配置JSON Schema',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (author_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '插件表';

-- ===========================================
-- 6. 资产管理表
-- ===========================================

-- API访问令牌表
CREATE TABLE api_tokens (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id BIGINT(20) NOT NULL COMMENT '用户ID',
    team_id CHAR(36) COMMENT '团队ID',
    name VARCHAR(200) NOT NULL COMMENT '令牌名称',
    token_hash VARCHAR(255) UNIQUE NOT NULL COMMENT '令牌哈希值',
    token_prefix VARCHAR(10) NOT NULL COMMENT '令牌前缀',
    scopes JSON NOT NULL COMMENT '权限范围',
    expires_at DATETIME NULL COMMENT '过期时间',
    last_used_at DATETIME NULL COMMENT '最后使用时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_api_tokens_user (user_id),
    FOREIGN KEY (user_id) REFERENCES sys_user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = 'API访问令牌表';

-- 文件资源表
CREATE TABLE resources (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL COMMENT '项目ID',
    name VARCHAR(255) NOT NULL COMMENT '资源名称',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型 (image, file, json, sql)',
    storage_path TEXT NOT NULL COMMENT '存储路径',
    file_size_bytes BIGINT COMMENT '文件大小 (字节)',
    uploaded_by_user_id BIGINT(20) COMMENT '上传者用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_resources_project (project_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by_user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '文件资源表';

-- 订阅与支付表
CREATE TABLE subscriptions (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    team_id CHAR(36) NOT NULL COMMENT '团队ID',
    plan VARCHAR(50) NOT NULL COMMENT '订阅计划',
    status VARCHAR(20) DEFAULT 'active' COMMENT '订阅状态',
    current_period_start DATETIME NULL COMMENT '当前订阅周期开始时间',
    current_period_end DATETIME NULL COMMENT '当前订阅周期结束时间',
    cancel_at_period_end BOOLEAN DEFAULT FALSE COMMENT '是否在周期结束时取消',
    canceled_at DATETIME NULL COMMENT '取消时间',
    stripe_customer_id VARCHAR(255) COMMENT 'Stripe客户ID',
    stripe_subscription_id VARCHAR(255) COMMENT 'Stripe订阅ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_subscriptions_team (team_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '订阅与支付表';

-- ===========================================
-- 7. 日志与审计表
-- ===========================================

-- 系统日志表
CREATE TABLE system_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    level VARCHAR(20) NOT NULL COMMENT '日志级别 (info, warn, error, debug)',
    service_name VARCHAR(100) COMMENT '服务名称',
    user_id BIGINT(20) COMMENT '用户ID',
    team_id CHAR(36) COMMENT '团队ID',
    project_id CHAR(36) COMMENT '项目ID',
    action VARCHAR(200) NOT NULL COMMENT '操作描述',
    details JSON COMMENT '操作详情',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_system_logs_created_at (created_at),
    INDEX idx_system_logs_level (level),
    INDEX idx_system_logs_user (user_id),
    FOREIGN KEY (user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '系统日志表';

-- API请求日志表
CREATE TABLE api_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    api_token_id CHAR(36) COMMENT 'API令牌ID',
    endpoint VARCHAR(500) NOT NULL COMMENT '请求端点',
    method VARCHAR(10) NOT NULL COMMENT '请求方法',
    status_code INTEGER COMMENT '响应状态码',
    request_body JSON COMMENT '请求体',
    response_body JSON COMMENT '响应体',
    duration_ms INTEGER COMMENT '请求耗时 (ms)',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_api_logs_created_at (created_at),
    INDEX idx_api_logs_endpoint (endpoint(100)),
    INDEX idx_api_logs_status_code (status_code),
    FOREIGN KEY (api_token_id) REFERENCES api_tokens(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = 'API请求日志表';

-- 审计日志表
CREATE TABLE audit_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id BIGINT(20) COMMENT '用户ID',
    team_id CHAR(36) COMMENT '团队ID',
    action_type VARCHAR(100) NOT NULL COMMENT '操作类型 (create, update, delete, login, logout)',
    resource_type VARCHAR(100) NOT NULL COMMENT '资源类型 (project, blueprint, user, team)',
    resource_id CHAR(36) COMMENT '资源ID',
    old_values JSON COMMENT '旧值',
    new_values JSON COMMENT '新值',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_audit_logs_created_at (created_at),
    INDEX idx_audit_logs_resource (resource_type, resource_id),
    INDEX idx_audit_logs_user (user_id),
    FOREIGN KEY (user_id) REFERENCES sys_user(user_id) ON DELETE SET NULL,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '审计日志表';

-- ===========================================
-- 8. 消息与通知表
-- ===========================================

-- 通知表
CREATE TABLE notifications (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id BIGINT(20) NOT NULL COMMENT '用户ID',
    type VARCHAR(50) NOT NULL COMMENT '通知类型 (system, team, project, generation)',
    title VARCHAR(200) NOT NULL COMMENT '通知标题',
    message TEXT NOT NULL COMMENT '通知内容',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    metadata JSON COMMENT '附加信息',
    expires_at DATETIME NULL COMMENT '过期时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_notifications_user (user_id),
    INDEX idx_notifications_is_read (is_read),
    INDEX idx_notifications_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES sys_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '通知表';

-- 站内消息表
CREATE TABLE messages (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    sender_user_id BIGINT(20) NOT NULL COMMENT '发送者用户ID',
    recipient_user_id BIGINT(20) COMMENT '接收者用户ID',
    recipient_team_id CHAR(36) COMMENT '接收者团队ID',
    subject VARCHAR(200) COMMENT '消息主题',
    content TEXT NOT NULL COMMENT '消息内容',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    parent_message_id CHAR(36) COMMENT '父消息ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_messages_recipient_user (recipient_user_id),
    INDEX idx_messages_recipient_team (recipient_team_id),
    INDEX idx_messages_sender (sender_user_id),
    FOREIGN KEY (sender_user_id) REFERENCES sys_user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_user_id) REFERENCES sys_user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_message_id) REFERENCES messages(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT = '站内消息表';

-- ===========================================
-- 数据库配置说明
-- ===========================================
/*
MySQL适配要点：
1. 主键类型：使用CHAR(36)存储UUID，默认值使用UUID()函数生成
2. JSON类型：MySQL 5.7+支持JSON类型，用于存储结构化配置数据
3. 时间戳：使用DATETIME类型，ON UPDATE CURRENT_TIMESTAMP自动更新
4. 字符集：使用utf8mb4支持完整的Unicode字符（包括emoji）
5. 外键约束：明确指定ON DELETE规则（CASCADE/SET NULL）
6. 索引优化：为频繁查询的字段创建索引
7. 存储引擎：统一使用InnoDB支持事务和外键

表关系说明：
- 用户(sys_user)：系统基础用户，已扩展字段
- 团队(teams)：用户组织单位
- 项目(projects)：团队下的具体项目
- 蓝图表(blueprints)：项目的应用蓝图版本
- 生成任务(generation_jobs)：蓝图到代码的生成任务
- 模板系统(templates/template_versions)：可复用的代码生成模板
*/