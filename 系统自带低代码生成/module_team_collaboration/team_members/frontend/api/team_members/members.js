import request from '@/utils/request'

// 查询团队成员列表
export function listMembers(query) {
  return request({
    url: '/team_members/members/list',
    method: 'get',
    params: query
  })
}

// 查询团队成员详细
export function getMembers(id) {
  return request({
    url: '/team_members/members/' + id,
    method: 'get'
  })
}

// 新增团队成员
export function addMembers(data) {
  return request({
    url: '/team_members/members',
    method: 'post',
    data: data
  })
}

// 修改团队成员
export function updateMembers(data) {
  return request({
    url: '/team_members/members',
    method: 'put',
    data: data
  })
}

// 删除团队成员
export function delMembers(id) {
  return request({
    url: '/team_members/members/' + id,
    method: 'delete'
  })
}
