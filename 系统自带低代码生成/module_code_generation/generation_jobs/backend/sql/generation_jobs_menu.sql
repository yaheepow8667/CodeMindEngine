-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成任务', '4', '1', 'generation_jobs', 'generation_jobs/generation_jobs/index', 1, 0, 'C', '0', '0', 'generation_jobs:generation_jobs:list', '#', 'admin', sysdate(), '', null, '生成任务菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成任务查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'generation_jobs:generation_jobs:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成任务新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'generation_jobs:generation_jobs:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成任务修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'generation_jobs:generation_jobs:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成任务删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'generation_jobs:generation_jobs:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成任务导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'generation_jobs:generation_jobs:export',       '#', 'admin', sysdate(), '', null, '');
