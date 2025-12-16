import request from '@/utils/request'

// 查询蓝图列表
export function listBlueprints(query) {
  return request({
    url: '/blueprints/blueprints/list',
    method: 'get',
    params: query
  })
}

// 查询蓝图详细
export function getBlueprints(id) {
  return request({
    url: '/blueprints/blueprints/' + id,
    method: 'get'
  })
}

// 新增蓝图
export function addBlueprints(data) {
  return request({
    url: '/blueprints/blueprints',
    method: 'post',
    data: data
  })
}

// 修改蓝图
export function updateBlueprints(data) {
  return request({
    url: '/blueprints/blueprints',
    method: 'put',
    data: data
  })
}

// 删除蓝图
export function delBlueprints(id) {
  return request({
    url: '/blueprints/blueprints/' + id,
    method: 'delete'
  })
}
