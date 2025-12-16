import request from '@/utils/request'

// 查询部署配置列表
export function listDeployment_configs(query) {
  return request({
    url: '/deployment_configs/deployment_configs/list',
    method: 'get',
    params: query
  })
}

// 查询部署配置详细
export function getDeployment_configs(id) {
  return request({
    url: '/deployment_configs/deployment_configs/' + id,
    method: 'get'
  })
}

// 新增部署配置
export function addDeployment_configs(data) {
  return request({
    url: '/deployment_configs/deployment_configs',
    method: 'post',
    data: data
  })
}

// 修改部署配置
export function updateDeployment_configs(data) {
  return request({
    url: '/deployment_configs/deployment_configs',
    method: 'put',
    data: data
  })
}

// 删除部署配置
export function delDeployment_configs(id) {
  return request({
    url: '/deployment_configs/deployment_configs/' + id,
    method: 'delete'
  })
}
