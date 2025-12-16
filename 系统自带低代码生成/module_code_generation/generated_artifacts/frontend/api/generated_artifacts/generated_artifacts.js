import request from '@/utils/request'

// 查询生成产物列表
export function listGenerated_artifacts(query) {
  return request({
    url: '/generated_artifacts/generated_artifacts/list',
    method: 'get',
    params: query
  })
}

// 查询生成产物详细
export function getGenerated_artifacts(id) {
  return request({
    url: '/generated_artifacts/generated_artifacts/' + id,
    method: 'get'
  })
}

// 新增生成产物
export function addGenerated_artifacts(data) {
  return request({
    url: '/generated_artifacts/generated_artifacts',
    method: 'post',
    data: data
  })
}

// 修改生成产物
export function updateGenerated_artifacts(data) {
  return request({
    url: '/generated_artifacts/generated_artifacts',
    method: 'put',
    data: data
  })
}

// 删除生成产物
export function delGenerated_artifacts(id) {
  return request({
    url: '/generated_artifacts/generated_artifacts/' + id,
    method: 'delete'
  })
}
