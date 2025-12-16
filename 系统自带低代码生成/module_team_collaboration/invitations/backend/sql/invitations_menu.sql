-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('邀请', '3', '1', 'invitations', 'invitations/invitations/index', 1, 0, 'C', '0', '0', 'invitations:invitations:list', '#', 'admin', sysdate(), '', null, '邀请菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('邀请查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'invitations:invitations:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('邀请新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'invitations:invitations:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('邀请修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'invitations:invitations:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('邀请删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'invitations:invitations:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('邀请导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'invitations:invitations:export',       '#', 'admin', sysdate(), '', null, '');
