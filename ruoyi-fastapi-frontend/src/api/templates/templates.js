import request from '@/utils/request'

// 查询模板列表
export function listTemplates(query) {
  return request({
    url: '/templates/templates/list',
    method: 'get',
    params: query
  })
}

// 查询模板详细
export function getTemplates(id) {
  return request({
    url: '/templates/templates/' + id,
    method: 'get'
  })
}

// 新增模板
export function addTemplates(data) {
  return request({
    url: '/templates/templates',
    method: 'post',
    data: data
  })
}

// 修改模板
export function updateTemplates(data) {
  return request({
    url: '/templates/templates',
    method: 'put',
    data: data
  })
}

// 删除模板
export function delTemplates(id) {
  return request({
    url: '/templates/templates/' + id,
    method: 'delete'
  })
}
