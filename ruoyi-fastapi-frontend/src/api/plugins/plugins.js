import request from '@/utils/request'

// 查询插件列表
export function listPlugins(query) {
  return request({
    url: '/plugins/plugins/list',
    method: 'get',
    params: query
  })
}

// 查询插件详细
export function getPlugins(id) {
  return request({
    url: '/plugins/plugins/' + id,
    method: 'get'
  })
}

// 新增插件
export function addPlugins(data) {
  return request({
    url: '/plugins/plugins',
    method: 'post',
    data: data
  })
}

// 修改插件
export function updatePlugins(data) {
  return request({
    url: '/plugins/plugins',
    method: 'put',
    data: data
  })
}

// 删除插件
export function delPlugins(id) {
  return request({
    url: '/plugins/plugins/' + id,
    method: 'delete'
  })
}
