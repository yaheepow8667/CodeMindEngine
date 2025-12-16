-- 数据库表结构示例

-- 1. 用户扩展表（扩展RuoYi的sys_user表）
ALTER TABLE `sys_user`
ADD COLUMN `display_name` VARCHAR(50) NOT NULL COMMENT '显示名称' AFTER `nick_name`,
ADD COLUMN `avatar_url` VARCHAR(255) COMMENT '头像URL' AFTER `avatar`;

-- 2. 团队表
CREATE TABLE `teams` (
  `team_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '团队ID',
  `name` VARCHAR(100) NOT NULL COMMENT '团队名称',
  `description` TEXT COMMENT '团队描述',
  `created_by` BIGINT NOT NULL COMMENT '创建人ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`team_id`),
  UNIQUE KEY `uk_name` (`name`),
  KEY `idx_created_by` (`created_by`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='团队表';

-- 3. 团队成员表
CREATE TABLE `team_members` (
  `member_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '成员ID',
  `team_id` BIGINT NOT NULL COMMENT '团队ID',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  `role` VARCHAR(20) NOT NULL COMMENT '角色（owner/manager/member）',
  `joined_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `uk_team_user` (`team_id`, `user_id`),
  KEY `idx_team_id` (`team_id`),
  KEY `idx_user_id` (`user_id`),
  FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='团队成员表';

-- 4. 项目表
CREATE TABLE `projects` (
  `project_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '项目ID',
  `team_id` BIGINT NOT NULL COMMENT '所属团队ID',
  `name` VARCHAR(100) NOT NULL COMMENT '项目名称',
  `description` TEXT COMMENT '项目描述',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '项目状态（0：草稿，1：进行中，2：已完成，3：已归档）',
  `created_by` BIGINT NOT NULL COMMENT '创建人ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`project_id`),
  KEY `idx_team_id` (`team_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_by` (`created_by`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`) ON DELETE CASCADE,
  FOREIGN KEY (`created_by`) REFERENCES `sys_user` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目表';

-- 5. 蓝图表
CREATE TABLE `blueprints` (
  `blueprint_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '蓝图ID',
  `project_id` BIGINT NOT NULL COMMENT '所属项目ID',
  `name` VARCHAR(100) NOT NULL COMMENT '蓝图名称',
  `content` LONGTEXT NOT NULL COMMENT '蓝图内容（JSON格式）',
  `preview_html` LONGTEXT COMMENT '预览HTML',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '蓝图状态（0：草稿，1：已发布，2：已归档）',
  `created_by` BIGINT NOT NULL COMMENT '创建人ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`blueprint_id`),
  KEY `idx_project_id` (`project_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_by` (`created_by`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`) ON DELETE CASCADE,
  FOREIGN KEY (`created_by`) REFERENCES `sys_user` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='蓝图表';

-- 6. 生成任务表
CREATE TABLE `generation_jobs` (
  `job_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `project_id` BIGINT NOT NULL COMMENT '所属项目ID',
  `blueprint_id` BIGINT NOT NULL COMMENT '所属蓝图ID',
  `type` VARCHAR(50) NOT NULL COMMENT '生成类型（form/page/api/code）',
  `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '任务状态（pending/running/success/failed）',
  `prompt` LONGTEXT NOT NULL COMMENT 'AI生成提示',
  `parameters` JSON COMMENT '生成参数（JSON格式）',
  `error_message` TEXT COMMENT '错误信息',
  `created_by` BIGINT NOT NULL COMMENT '创建人ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`job_id`),
  KEY `idx_project_id` (`project_id`),
  KEY `idx_blueprint_id` (`blueprint_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_by` (`created_by`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`) ON DELETE CASCADE,
  FOREIGN KEY (`blueprint_id`) REFERENCES `blueprints` (`blueprint_id`) ON DELETE CASCADE,
  FOREIGN KEY (`created_by`) REFERENCES `sys_user` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生成任务表';

-- 7. 生成成果表
CREATE TABLE `generated_artifacts` (
  `artifact_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '成果ID',
  `job_id` BIGINT NOT NULL COMMENT '所属任务ID',
  `type` VARCHAR(50) NOT NULL COMMENT '成果类型（html/css/javascript/api/code）',
  `name` VARCHAR(255) NOT NULL COMMENT '成果名称',
  `content` LONGTEXT NOT NULL COMMENT '成果内容',
  `file_path` VARCHAR(255) COMMENT '文件路径',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`artifact_id`),
  KEY `idx_job_id` (`job_id`),
  KEY `idx_type` (`type`),
  FOREIGN KEY (`job_id`) REFERENCES `generation_jobs` (`job_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生成成果表';

-- 8. 索引优化示例
-- 为蓝图表的content字段添加全文索引（可选）
ALTER TABLE `blueprints` ADD FULLTEXT INDEX `ft_content` (`content`);

-- 为团队成员表添加复合索引
CREATE INDEX `idx_team_id_role` ON `team_members` (`team_id`, `role`);
