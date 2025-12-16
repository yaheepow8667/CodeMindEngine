-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('插件', '4', '1', 'plugins', 'plugins/plugins/index', 1, 0, 'C', '0', '0', 'plugins:plugins:list', '#', 'admin', sysdate(), '', null, '插件菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('插件查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'plugins:plugins:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('插件新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'plugins:plugins:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('插件修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'plugins:plugins:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('插件删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'plugins:plugins:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('插件导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'plugins:plugins:export',       '#', 'admin', sysdate(), '', null, '');
