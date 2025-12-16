-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('团队', '4', '1', 'teams', 'teams/teams/index', 1, 0, 'C', '0', '0', 'teams:teams:list', '#', 'admin', sysdate(), '', null, '团队菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('团队查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'teams:teams:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('团队新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'teams:teams:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('团队修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'teams:teams:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('团队删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'teams:teams:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('团队导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'teams:teams:export',       '#', 'admin', sysdate(), '', null, '');
