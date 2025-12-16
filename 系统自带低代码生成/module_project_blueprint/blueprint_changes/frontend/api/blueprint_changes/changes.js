import request from '@/utils/request'

// 查询蓝图变更记录列表
export function listChanges(query) {
  return request({
    url: '/blueprint_changes/changes/list',
    method: 'get',
    params: query
  })
}

// 查询蓝图变更记录详细
export function getChanges(id) {
  return request({
    url: '/blueprint_changes/changes/' + id,
    method: 'get'
  })
}

// 新增蓝图变更记录
export function addChanges(data) {
  return request({
    url: '/blueprint_changes/changes',
    method: 'post',
    data: data
  })
}

// 修改蓝图变更记录
export function updateChanges(data) {
  return request({
    url: '/blueprint_changes/changes',
    method: 'put',
    data: data
  })
}

// 删除蓝图变更记录
export function delChanges(id) {
  return request({
    url: '/blueprint_changes/changes/' + id,
    method: 'delete'
  })
}
