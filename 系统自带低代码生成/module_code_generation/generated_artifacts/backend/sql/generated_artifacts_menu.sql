-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成产物', '4', '1', 'generated_artifacts', 'generated_artifacts/generated_artifacts/index', 1, 0, 'C', '0', '0', 'generated_artifacts:generated_artifacts:list', '#', 'admin', sysdate(), '', null, '生成产物菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成产物查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'generated_artifacts:generated_artifacts:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成产物新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'generated_artifacts:generated_artifacts:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成产物修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'generated_artifacts:generated_artifacts:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成产物删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'generated_artifacts:generated_artifacts:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('生成产物导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'generated_artifacts:generated_artifacts:export',       '#', 'admin', sysdate(), '', null, '');
