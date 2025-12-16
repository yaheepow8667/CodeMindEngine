import request from '@/utils/request'

// 查询生成任务列表
export function listGeneration_jobs(query) {
  return request({
    url: '/generation_jobs/generation_jobs/list',
    method: 'get',
    params: query
  })
}

// 查询生成任务详细
export function getGeneration_jobs(id) {
  return request({
    url: '/generation_jobs/generation_jobs/' + id,
    method: 'get'
  })
}

// 新增生成任务
export function addGeneration_jobs(data) {
  return request({
    url: '/generation_jobs/generation_jobs',
    method: 'post',
    data: data
  })
}

// 修改生成任务
export function updateGeneration_jobs(data) {
  return request({
    url: '/generation_jobs/generation_jobs',
    method: 'put',
    data: data
  })
}

// 删除生成任务
export function delGeneration_jobs(id) {
  return request({
    url: '/generation_jobs/generation_jobs/' + id,
    method: 'delete'
  })
}
