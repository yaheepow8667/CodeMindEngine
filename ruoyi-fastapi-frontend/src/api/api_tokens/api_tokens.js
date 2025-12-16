import request from '@/utils/request'

// 查询API访问令牌列表
export function listApi_tokens(query) {
  return request({
    url: '/api_tokens/api_tokens/list',
    method: 'get',
    params: query
  })
}

// 查询API访问令牌详细
export function getApi_tokens(id) {
  return request({
    url: '/api_tokens/api_tokens/' + id,
    method: 'get'
  })
}

// 新增API访问令牌
export function addApi_tokens(data) {
  return request({
    url: '/api_tokens/api_tokens',
    method: 'post',
    data: data
  })
}

// 修改API访问令牌
export function updateApi_tokens(data) {
  return request({
    url: '/api_tokens/api_tokens',
    method: 'put',
    data: data
  })
}

// 删除API访问令牌
export function delApi_tokens(id) {
  return request({
    url: '/api_tokens/api_tokens/' + id,
    method: 'delete'
  })
}
