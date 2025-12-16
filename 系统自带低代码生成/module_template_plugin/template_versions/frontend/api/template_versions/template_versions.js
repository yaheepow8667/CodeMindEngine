import request from '@/utils/request'

// 查询模板版本列表
export function listTemplate_versions(query) {
  return request({
    url: '/template_versions/template_versions/list',
    method: 'get',
    params: query
  })
}

// 查询模板版本详细
export function getTemplate_versions(id) {
  return request({
    url: '/template_versions/template_versions/' + id,
    method: 'get'
  })
}

// 新增模板版本
export function addTemplate_versions(data) {
  return request({
    url: '/template_versions/template_versions',
    method: 'post',
    data: data
  })
}

// 修改模板版本
export function updateTemplate_versions(data) {
  return request({
    url: '/template_versions/template_versions',
    method: 'put',
    data: data
  })
}

// 删除模板版本
export function delTemplate_versions(id) {
  return request({
    url: '/template_versions/template_versions/' + id,
    method: 'delete'
  })
}
