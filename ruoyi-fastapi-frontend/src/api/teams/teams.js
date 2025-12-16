import request from '@/utils/request'

// 查询团队列表
export function listTeams(query) {
  return request({
    url: '/teams/teams/list',
    method: 'get',
    params: query
  })
}

// 查询团队详细
export function getTeams(id) {
  return request({
    url: '/teams/teams/' + id,
    method: 'get'
  })
}

// 新增团队
export function addTeams(data) {
  return request({
    url: '/teams/teams',
    method: 'post',
    data: data
  })
}

// 修改团队
export function updateTeams(data) {
  return request({
    url: '/teams/teams',
    method: 'put',
    data: data
  })
}

// 删除团队
export function delTeams(id) {
  return request({
    url: '/teams/teams/' + id,
    method: 'delete'
  })
}
