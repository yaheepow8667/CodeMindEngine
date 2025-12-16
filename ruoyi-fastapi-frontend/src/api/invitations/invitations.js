import request from '@/utils/request'

// 查询邀请列表
export function listInvitations(query) {
  return request({
    url: '/invitations/invitations/list',
    method: 'get',
    params: query
  })
}

// 查询邀请详细
export function getInvitations(id) {
  return request({
    url: '/invitations/invitations/' + id,
    method: 'get'
  })
}

// 新增邀请
export function addInvitations(data) {
  return request({
    url: '/invitations/invitations',
    method: 'post',
    data: data
  })
}

// 修改邀请
export function updateInvitations(data) {
  return request({
    url: '/invitations/invitations',
    method: 'put',
    data: data
  })
}

// 删除邀请
export function delInvitations(id) {
  return request({
    url: '/invitations/invitations/' + id,
    method: 'delete'
  })
}
