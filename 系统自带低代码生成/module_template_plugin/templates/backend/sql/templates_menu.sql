-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板', '4', '1', 'templates', 'templates/templates/index', 1, 0, 'C', '0', '0', 'templates:templates:list', '#', 'admin', sysdate(), '', null, '模板菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'templates:templates:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'templates:templates:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'templates:templates:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'templates:templates:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'templates:templates:export',       '#', 'admin', sysdate(), '', null, '');
