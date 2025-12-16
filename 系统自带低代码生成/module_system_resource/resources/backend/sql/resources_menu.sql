-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文件资源', '4', '1', 'resources', 'resources/resources/index', 1, 0, 'C', '0', '0', 'resources:resources:list', '#', 'admin', sysdate(), '', null, '文件资源菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文件资源查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'resources:resources:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文件资源新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'resources:resources:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文件资源修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'resources:resources:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文件资源删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'resources:resources:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文件资源导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'resources:resources:export',       '#', 'admin', sysdate(), '', null, '');
