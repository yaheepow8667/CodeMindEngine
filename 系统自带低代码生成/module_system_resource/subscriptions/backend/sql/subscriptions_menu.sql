-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('订阅与支付', '4', '1', 'subscriptions', 'subscriptions/subscriptions/index', 1, 0, 'C', '0', '0', 'subscriptions:subscriptions:list', '#', 'admin', sysdate(), '', null, '订阅与支付菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('订阅与支付查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'subscriptions:subscriptions:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('订阅与支付新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'subscriptions:subscriptions:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('订阅与支付修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'subscriptions:subscriptions:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('订阅与支付删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'subscriptions:subscriptions:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('订阅与支付导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'subscriptions:subscriptions:export',       '#', 'admin', sysdate(), '', null, '');
