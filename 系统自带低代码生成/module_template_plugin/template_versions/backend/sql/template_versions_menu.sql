-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板版本', '4', '1', 'template_versions', 'template_versions/template_versions/index', 1, 0, 'C', '0', '0', 'template_versions:template_versions:list', '#', 'admin', sysdate(), '', null, '模板版本菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板版本查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'template_versions:template_versions:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板版本新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'template_versions:template_versions:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板版本修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'template_versions:template_versions:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板版本删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'template_versions:template_versions:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('模板版本导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'template_versions:template_versions:export',       '#', 'admin', sysdate(), '', null, '');
