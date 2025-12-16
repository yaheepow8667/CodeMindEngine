-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图变更记录', '4', '1', 'changes', 'blueprint_changes/changes/index', 1, 0, 'C', '0', '0', 'blueprint_changes:changes:list', '#', 'admin', sysdate(), '', null, '蓝图变更记录菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图变更记录查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'blueprint_changes:changes:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图变更记录新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'blueprint_changes:changes:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图变更记录修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'blueprint_changes:changes:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图变更记录删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'blueprint_changes:changes:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('蓝图变更记录导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'blueprint_changes:changes:export',       '#', 'admin', sysdate(), '', null, '');
