import request from '@/utils/request'

// 查询项目列表
export function listProjects(query) {
  return request({
    url: '/projects/projects/list',
    method: 'get',
    params: query
  })
}

// 查询项目详细
export function getProjects(id) {
  return request({
    url: '/projects/projects/' + id,
    method: 'get'
  })
}

// 新增项目
export function addProjects(data) {
  return request({
    url: '/projects/projects',
    method: 'post',
    data: data
  })
}

// 修改项目
export function updateProjects(data) {
  return request({
    url: '/projects/projects',
    method: 'put',
    data: data
  })
}

// 删除项目
export function delProjects(id) {
  return request({
    url: '/projects/projects/' + id,
    method: 'delete'
  })
}
