# 智码引擎数据库表结构设计（MySQL版本）

## 1. 核心用户与组织表

```sql
-- 用户表
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url TEXT,
    role VARCHAR(50) DEFAULT 'user', -- 'user', 'admin', 'super_admin'
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'suspended'
    email_verified BOOLEAN DEFAULT FALSE,
    phone_number VARCHAR(50),
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_status (status),
    INDEX idx_users_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 团队表
CREATE TABLE teams (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL, -- 团队URL标识
    description TEXT,
    logo_url TEXT,
    subscription_plan VARCHAR(50) DEFAULT 'free', -- 'free', 'team', 'enterprise'
    subscription_status VARCHAR(20) DEFAULT 'active', -- 'active', 'canceled', 'past_due'
    subscription_ends_at TIMESTAMP NULL,
    created_by_user_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_teams_subscription_status (subscription_status),
    INDEX idx_teams_created_by (created_by_user_id),
    FOREIGN KEY (created_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 团队成员表
CREATE TABLE team_members (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    team_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    role VARCHAR(50) DEFAULT 'member', -- 'owner', 'admin', 'member', 'viewer'
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    invited_by_user_id CHAR(36),
    invited_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_team_members_team_user (team_id, user_id),
    INDEX idx_team_members_user (user_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (invited_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 邀请表
CREATE TABLE invitations (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    team_id CHAR(36) NOT NULL,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'member',
    invited_by_user_id CHAR(36),
    expires_at TIMESTAMP NOT NULL,
    accepted_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_invitations_team_email (team_id, email),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (invited_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 2. 项目与蓝图管理表

```sql
-- 项目表
CREATE TABLE projects (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    team_id CHAR(36) NOT NULL,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) NOT NULL, -- 项目标识，团队内唯一
    description TEXT,
    tech_stack JSON, -- {"frontend": "vue3", "backend": "nestjs", "ui": "ant-design-vue"}
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'archived', 'deleted'
    is_public BOOLEAN DEFAULT FALSE,
    storage_quota_mb INTEGER DEFAULT 1024,
    created_by_user_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_projects_team_slug (team_id, slug),
    INDEX idx_projects_team (team_id),
    INDEX idx_projects_status (status),
    INDEX idx_projects_created_by (created_by_user_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 蓝图表（存储在独立文档存储，这里只存储元数据）
CREATE TABLE blueprints (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    version_tag VARCHAR(50) NOT NULL, -- 如 "v1.0.0", "draft-1"
    spec_document_id VARCHAR(100), -- 独立文档存储中的文档ID
    spec_summary JSON, -- 蓝图的摘要信息，用于快速查询
    is_draft BOOLEAN DEFAULT TRUE,
    parent_blueprint_id CHAR(36),
    created_by_user_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_blueprints_project_version (project_id, version_tag),
    INDEX idx_blueprints_project (project_id),
    INDEX idx_blueprints_is_draft (is_draft),
    INDEX idx_blueprints_created_at (created_at),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_blueprint_id) REFERENCES blueprints(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 蓝图变更记录
CREATE TABLE blueprint_changes (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    blueprint_id CHAR(36) NOT NULL,
    change_type VARCHAR(50), -- 'create', 'update', 'delete'
    field_path VARCHAR(500), -- 如 "dataModels.User.fields"
    old_value JSON,
    new_value JSON,
    changed_by_user_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_blueprint_changes_blueprint (blueprint_id),
    FOREIGN KEY (blueprint_id) REFERENCES blueprints(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 3. 生成与任务管理表

```sql
-- 生成任务表
CREATE TABLE generation_jobs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL,
    blueprint_id CHAR(36) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'generating', 'qa', 'success', 'failed'
    target_tech_stack JSON, -- 目标技术栈配置
    trigger_type VARCHAR(50) DEFAULT 'manual', -- 'manual', 'api', 'webhook', 'schedule'
    triggered_by_user_id CHAR(36),
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    error_message TEXT,
    logs JSON, -- 存储生成过程中的关键日志
    qa_report JSON, -- 质量检查报告
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_generation_jobs_project (project_id),
    INDEX idx_generation_jobs_status (status),
    INDEX idx_generation_jobs_created_at (created_at),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (blueprint_id) REFERENCES blueprints(id) ON DELETE CASCADE,
    FOREIGN KEY (triggered_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 生成产物表
CREATE TABLE generated_artifacts (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    job_id CHAR(36) NOT NULL,
    artifact_type VARCHAR(50) NOT NULL, -- 'source_zip', 'qa_report', 'deploy_config', 'api_docs'
    artifact_name VARCHAR(255) NOT NULL,
    storage_type VARCHAR(50) DEFAULT 's3', -- 's3', 'oss', 'local'
    storage_path TEXT NOT NULL,
    storage_url TEXT, -- 访问URL
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    checksum VARCHAR(255),
    is_compressed BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_generated_artifacts_job (job_id),
    FOREIGN KEY (job_id) REFERENCES generation_jobs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 部署配置表
CREATE TABLE deployment_configs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL,
    name VARCHAR(200) NOT NULL,
    environment VARCHAR(50) NOT NULL, -- 'development', 'staging', 'production'
    config JSON NOT NULL, -- 具体的部署配置
    is_active BOOLEAN DEFAULT TRUE,
    deployed_job_id CHAR(36),
    deployed_at TIMESTAMP NULL,
    deployed_by_user_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_deployment_configs_project_env_name (project_id, environment, name),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (deployed_job_id) REFERENCES generation_jobs(id) ON DELETE SET NULL,
    FOREIGN KEY (deployed_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 4. 模板与插件管理表

```sql
-- 模板表
CREATE TABLE templates (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL, -- 'ui_component', 'api_layer', 'project_scaffold', 'workflow'
    target_framework VARCHAR(100), -- 'vue3', 'react', 'nestjs', 'spring_boot'
    complexity_level VARCHAR(20) DEFAULT 'basic', -- 'basic', 'intermediate', 'advanced'
    is_official BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT TRUE,
    author_user_id CHAR(36),
    download_count INTEGER DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0,
    version VARCHAR(50) DEFAULT '1.0.0',
    tags JSON, -- 标签数组存储为JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_templates_category (category),
    INDEX idx_templates_target_framework (target_framework),
    INDEX idx_templates_is_public (is_public),
    FOREIGN KEY (author_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 模板版本表
CREATE TABLE template_versions (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    template_id CHAR(36) NOT NULL,
    version VARCHAR(50) NOT NULL,
    changelog TEXT,
    template_content JSON NOT NULL, -- 模板的JSON定义
    example_blueprint JSON, -- 示例蓝图
    is_active BOOLEAN DEFAULT TRUE,
    published_at TIMESTAMP NULL,
    published_by_user_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_template_versions_template_version (template_id, version),
    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
    FOREIGN KEY (published_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插件表
CREATE TABLE plugins (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(200) NOT NULL,
    plugin_type VARCHAR(50) NOT NULL, -- 'code_generator', 'qa_checker', 'deployer'
    target_framework VARCHAR(100),
    version VARCHAR(50) DEFAULT '1.0.0',
    author_user_id CHAR(36),
    is_approved BOOLEAN DEFAULT FALSE,
    install_count INTEGER DEFAULT 0,
    config_schema JSON, -- 插件配置的JSON Schema
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 5. 资产管理表

```sql
-- API访问令牌表
CREATE TABLE api_tokens (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    team_id CHAR(36),
    name VARCHAR(200) NOT NULL,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    token_prefix VARCHAR(10) NOT NULL,
    scopes JSON NOT NULL, -- 权限范围数组存储为JSON
    expires_at TIMESTAMP NULL,
    last_used_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_api_tokens_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 文件资源表
CREATE TABLE resources (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    project_id CHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    resource_type VARCHAR(50) NOT NULL, -- 'image', 'file', 'json', 'sql'
    storage_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    uploaded_by_user_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_resources_project (project_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 订阅与支付表
CREATE TABLE subscriptions (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    team_id CHAR(36) NOT NULL,
    plan VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    current_period_start TIMESTAMP NULL,
    current_period_end TIMESTAMP NULL,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    canceled_at TIMESTAMP NULL,
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_subscriptions_team (team_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 6. 日志与审计表

```sql
-- 系统日志表
CREATE TABLE system_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    level VARCHAR(20) NOT NULL, -- 'info', 'warn', 'error', 'debug'
    service_name VARCHAR(100), -- 服务名称
    user_id CHAR(36),
    team_id CHAR(36),
    project_id CHAR(36),
    action VARCHAR(200) NOT NULL, -- 操作描述
    details JSON,
    ip_address VARCHAR(45), -- 支持IPv6
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_system_logs_created_at (created_at),
    INDEX idx_system_logs_level (level),
    INDEX idx_system_logs_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- API请求日志表
CREATE TABLE api_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    api_token_id CHAR(36),
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER,
    request_body JSON,
    response_body JSON,
    duration_ms INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_api_logs_created_at (created_at),
    INDEX idx_api_logs_endpoint (endpoint(100)),
    INDEX idx_api_logs_status_code (status_code),
    FOREIGN KEY (api_token_id) REFERENCES api_tokens(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 审计日志表
CREATE TABLE audit_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36),
    team_id CHAR(36),
    action_type VARCHAR(100) NOT NULL, -- 'create', 'update', 'delete', 'login', 'logout'
    resource_type VARCHAR(100) NOT NULL, -- 'project', 'blueprint', 'user', 'team'
    resource_id CHAR(36),
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_logs_created_at (created_at),
    INDEX idx_audit_logs_resource (resource_type, resource_id),
    INDEX idx_audit_logs_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 7. 消息与通知表

```sql
-- 通知表
CREATE TABLE notifications (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'system', 'team', 'project', 'generation'
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    metadata JSON,
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notifications_user (user_id),
    INDEX idx_notifications_is_read (is_read),
    INDEX idx_notifications_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 站内消息表
CREATE TABLE messages (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    sender_user_id CHAR(36) NOT NULL,
    recipient_user_id CHAR(36),
    recipient_team_id CHAR(36),
    subject VARCHAR(200),
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    parent_message_id CHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_messages_recipient_user (recipient_user_id),
    INDEX idx_messages_recipient_team (recipient_team_id),
    INDEX idx_messages_sender (sender_user_id),
    FOREIGN KEY (sender_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_message_id) REFERENCES messages(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 数据库设计说明

### MySQL适配要点：

1. **主键类型**：使用`CHAR(36)`存储UUID，默认值使用`UUID()`函数生成
2. **JSON类型**：MySQL 5.7+支持JSON类型，替代PostgreSQL的JSONB
3. **时间戳**：使用`TIMESTAMP`类型，`ON UPDATE CURRENT_TIMESTAMP`自动更新
4. **字符集**：使用`utf8mb4`支持完整的Unicode字符（包括emoji）
5. **外键约束**：明确指定`ON DELETE`规则（CASCADE/SET NULL）
6. **索引优化**：为频繁查询的字段创建索引，JSON列不支持普通索引
7. **存储引擎**：统一使用`InnoDB`支持事务和外键

### 表关系说明：

- **用户(users)**：系统基础用户
- **团队(teams)**：用户组织单位
- **项目(projects)**：团队下的具体项目
- **蓝图表(blueprints)**：项目的应用蓝图版本
- **生成任务(generation_jobs)**：蓝图到代码的生成任务
- **模板系统(templates/template_versions)**：可复用的代码生成模板

### 性能优化建议：

1. **分区表**：对于日志类大表（如`system_logs`, `api_logs`），可按时间分区
2. **归档策略**：定期归档历史数据，保持生产表数据量合理
3. **读写分离**：将日志和审计类写入与核心业务读取分离
4. **连接池**：应用层使用数据库连接池管理连接

这套MySQL表结构支持智码引擎的所有核心功能，同时保持了良好的性能和扩展性。

