import request from '@/utils/request'

// 查询订阅与支付列表
export function listSubscriptions(query) {
  return request({
    url: '/subscriptions/subscriptions/list',
    method: 'get',
    params: query
  })
}

// 查询订阅与支付详细
export function getSubscriptions(id) {
  return request({
    url: '/subscriptions/subscriptions/' + id,
    method: 'get'
  })
}

// 新增订阅与支付
export function addSubscriptions(data) {
  return request({
    url: '/subscriptions/subscriptions',
    method: 'post',
    data: data
  })
}

// 修改订阅与支付
export function updateSubscriptions(data) {
  return request({
    url: '/subscriptions/subscriptions',
    method: 'put',
    data: data
  })
}

// 删除订阅与支付
export function delSubscriptions(id) {
  return request({
    url: '/subscriptions/subscriptions/' + id,
    method: 'delete'
  })
}
