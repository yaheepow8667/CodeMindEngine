import request from '@/utils/request'

// 查询文件资源列表
export function listResources(query) {
  return request({
    url: '/resources/resources/list',
    method: 'get',
    params: query
  })
}

// 查询文件资源详细
export function getResources(id) {
  return request({
    url: '/resources/resources/' + id,
    method: 'get'
  })
}

// 新增文件资源
export function addResources(data) {
  return request({
    url: '/resources/resources',
    method: 'post',
    data: data
  })
}

// 修改文件资源
export function updateResources(data) {
  return request({
    url: '/resources/resources',
    method: 'put',
    data: data
  })
}

// 删除文件资源
export function delResources(id) {
  return request({
    url: '/resources/resources/' + id,
    method: 'delete'
  })
}
