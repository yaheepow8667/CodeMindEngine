-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图', '4', '1', 'blueprints', 'blueprints/blueprints/index', 1, 0, 'C', '0', '0', 'blueprints:blueprints:list', '#', 'admin', sysdate(), '', null, '蓝图菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'blueprints:blueprints:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'blueprints:blueprints:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'blueprints:blueprints:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'blueprints:blueprints:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'blueprints:blueprints:export',       '#', 'admin', sysdate(), '', null, '');
