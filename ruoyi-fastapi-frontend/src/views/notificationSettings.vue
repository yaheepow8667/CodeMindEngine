<template>
  <div class="notification-settings-container min-h-full font-inter bg-light text-text-primary">
    <!-- 顶部标题区域 -->
    <div class="pb-4 mb-6 border-b border-border-color">
      <h3 class="text-2xl font-semibold text-text-primary">设置中心</h3>
      <!-- 面包屑导航 -->
      <div class="text-sm text-text-secondary mt-1">
        <a href="javascript:void(0);" class="hover:text-primary">设置中心</a>
        <span class="mx-1">/</span>
        <span class="text-text-tertiary">通知偏好设置</span>
      </div>
    </div>

    <!-- 通知渠道管理模块 -->
    <el-card class="mb-8" shadow="hover">
      <template #header>
        <div class="ant-card-header">
          通知渠道管理
        </div>
      </template>
      <div id="channel-management" class="space-y-4">
        <!-- 站内通知 -->
        <div class="flex items-center justify-between p-4 border border-border-color rounded-lg hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <i class="fas fa-bell text-xl text-primary mr-4"></i>
            <div>
              <p class="font-medium">站内通知</p>
              <p class="text-sm text-text-secondary">系统内所有重要提醒和动态通知。</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm" :class="{ 'text-success font-medium': inAppChannel.enabled, 'text-text-tertiary': !inAppChannel.enabled }">
              {{ inAppChannel.enabled ? '已开启' : '已关闭' }}
            </span>
            <el-switch
              v-model="inAppChannel.enabled"
              @change="handleChannelChange('inApp', inAppChannel.enabled)"
            />
          </div>
        </div>

        <!-- 邮件通知 -->
        <div class="flex items-center justify-between p-4 border border-border-color rounded-lg hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <i class="fas fa-envelope text-xl text-info mr-4"></i>
            <div>
              <p class="font-medium">邮件通知</p>
              <p class="text-sm text-text-secondary">接收重要安全提醒和项目摘要邮件。当前绑定: <span class="font-mono text-xs bg-light px-1 rounded">user@example.com</span></p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm" :class="{ 'text-success font-medium': emailChannel.enabled, 'text-text-tertiary': !emailChannel.enabled }">
              {{ emailChannel.enabled ? '已开启' : '已关闭' }}
            </span>
            <el-switch
              v-model="emailChannel.enabled"
              @change="handleChannelChange('email', emailChannel.enabled)"
            />
          </div>
        </div>

        <!-- 企业应用通知 -->
        <div class="flex items-center justify-between p-4 border border-border-color rounded-lg hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <i class="fab fa-weixin text-xl text-warning mr-4"></i>
            <div>
              <p class="font-medium">企业应用通知</p>
              <p class="text-sm text-text-secondary">通过企业微信/钉钉接收实时通知。状态: <span :class="{ 'text-danger font-medium': !isCorpConfigured, 'text-success font-medium': isCorpConfigured }">
                {{ isCorpConfigured ? '已连接' : '未配置' }}
              </span></p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <el-button
              type="outline"
              size="small"
              @click="toggleCorpConfig"
            >
              <i class="fas fa-cogs mr-1"></i>{{ isCorpConfigured ? '管理' : '立即配置' }}
            </el-button>
            <el-switch
              v-model="corpChannel.enabled"
              :disabled="!isCorpConfigured"
              @change="handleChannelChange('corp', corpChannel.enabled)"
            />
          </div>
        </div>
      </div>
    </el-card>

    <!-- 通知类型细分模块 -->
    <el-card shadow="hover">
      <template #header>
        <div class="ant-card-header">
          通知类型细分
        </div>
      </template>
      <!-- 快捷操作按钮 -->
      <div class="flex justify-end space-x-3 mb-4">
        <el-button
          type="outline"
          size="small"
          @click="enableAllNotifications"
        >
          <i class="fas fa-check-circle mr-1"></i>全部开启
        </el-button>
        <el-button
          type="outline"
          size="small"
          @click="disableAllNotifications"
        >
          <i class="fas fa-times-circle mr-1"></i>全部关闭
        </el-button>
      </div>
      <!-- 表格容器 -->
      <div class="overflow-x-auto">
        <el-table
          :data="notificationTypes"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column
            prop="name"
            label="通知类型"
            width="25%"
          >
            <template #default="scope">
              <div class="flex items-center">
                <i :class="['fas', scope.row.icon, 'text-base text-text-secondary mr-3 w-4 text-center']"></i>
                <div>
                  <p class="font-medium text-sm">{{ scope.row.name }}</p>
                  <p class="text-xs text-text-tertiary">{{ scope.row.desc }}</p>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            label="站内通知"
            align="center"
          >
            <template #default="scope">
              <el-switch
                v-model="scope.row.inApp"
                :disabled="!inAppChannel.enabled"
                @change="handleNotificationChange(scope.row.id, 'inApp', scope.row.inApp)"
              />
              <span v-if="!inAppChannel.enabled" class="text-text-tertiary text-xs block mt-1">（渠道关闭）</span>
            </template>
          </el-table-column>
          <el-table-column
            label="邮件通知"
            align="center"
          >
            <template #default="scope">
              <el-switch
                v-model="scope.row.email"
                :disabled="!emailChannel.enabled"
                @change="handleNotificationChange(scope.row.id, 'email', scope.row.email)"
              />
              <span v-if="!emailChannel.enabled" class="text-text-tertiary text-xs block mt-1">（渠道关闭）</span>
            </template>
          </el-table-column>
          <el-table-column
            label="企业应用"
            align="center"
          >
            <template #default="scope">
              <el-switch
                v-model="scope.row.corp"
                :disabled="!isCorpConfigured || !emailChannel.enabled"
                @change="handleNotificationChange(scope.row.id, 'corp', scope.row.corp)"
              />
              <span v-if="!isCorpConfigured || !emailChannel.enabled" class="text-text-tertiary text-xs block mt-1">（渠道关闭）</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 恢复默认设置链接 -->
    <div class="mt-6 text-center">
      <a href="javascript:void(0);" @click="restoreDefaultSettings" class="text-sm text-text-secondary hover:text-danger transition-colors duration-200">
        <i class="fas fa-undo-alt mr-1"></i>恢复默认设置
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

// 通知渠道接口
export interface NotificationChannel {
  enabled: boolean
}

// 通知类型接口
export interface NotificationType {
  id: number
  name: string
  icon: string
  desc: string
  inApp: boolean
  email: boolean
  corp: boolean
}

// 通知渠道状态
const inAppChannel = reactive<NotificationChannel>({ enabled: true })
const emailChannel = reactive<NotificationChannel>({ enabled: true })
const corpChannel = reactive<NotificationChannel>({ enabled: false })

// 企业应用配置状态
const isCorpConfigured = ref(false)

// 通知类型数据
const notificationTypes = ref<NotificationType[]>([
  {
    id: 1,
    name: '项目通知',
    icon: 'fa-folder-open',
    desc: '项目创建、更新、代码合并等',
    inApp: true,
    email: true,
    corp: true
  },
  {
    id: 2,
    name: '团队协作',
    icon: 'fa-users',
    desc: '成员邀请、权限变更',
    inApp: true,
    email: false,
    corp: true
  },
  {
    id: 3,
    name: '系统公告',
    icon: 'fa-bullhorn',
    desc: '平台维护、新功能发布',
    inApp: true,
    email: true,
    corp: false
  },
  {
    id: 4,
    name: '生成任务状态',
    icon: 'fa-magic',
    desc: '生成任务开始、完成、失败',
    inApp: true,
    email: true,
    corp: true
  },
  {
    id: 5,
    name: '营销资讯',
    icon: 'fa-newspaper',
    desc: '产品更新、活动推广',
    inApp: false,
    email: true,
    corp: false
  }
])

// 处理渠道开关变化
const handleChannelChange = (channel: string, enabled: boolean) => {
  // 更新对应渠道状态
  switch (channel) {
    case 'inApp':
      inAppChannel.enabled = enabled
      // 影响表格中站内通知列的状态
      notificationTypes.value.forEach(type => {
        type.inApp = enabled
      })
      ElMessage.success(`站内通知渠道已${enabled ? '开启' : '关闭'}`)
      break
    case 'email':
      emailChannel.enabled = enabled
      // 影响表格中邮件通知列的状态
      notificationTypes.value.forEach(type => {
        type.email = enabled
      })
      ElMessage.success(`邮件通知渠道已${enabled ? '开启' : '关闭'}`)
      break
    case 'corp':
      corpChannel.enabled = enabled
      ElMessage.success(`企业应用通知渠道已${enabled ? '开启' : '关闭'}`)
      break
  }
}

// 处理通知类型开关变化
const handleNotificationChange = (id: number, channel: string, enabled: boolean) => {
  const typeIndex = notificationTypes.value.findIndex(type => type.id === id)
  if (typeIndex !== -1) {
    notificationTypes.value[typeIndex][channel as keyof NotificationType] = enabled
    
    // 模拟API调用
    setTimeout(() => {
      const type = notificationTypes.value[typeIndex]
      ElMessage.success(`${type.name}的${channel === 'inApp' ? '站内通知' : channel === 'email' ? '邮件通知' : '企业应用'}已${enabled ? '开启' : '关闭'}`)
    }, 300)
  }
}

// 切换企业应用配置状态
const toggleCorpConfig = () => {
  isCorpConfigured.value = !isCorpConfigured.value
  if (isCorpConfigured.value) {
    ElMessage.info('已模拟连接企业应用，请前往管理页面进行实际配置。')
  } else {
    ElMessage.info('已模拟断开企业应用连接。')
  }
}

// 全部开启通知
const enableAllNotifications = () => {
  notificationTypes.value.forEach(type => {
    if (inAppChannel.enabled) type.inApp = true
    if (emailChannel.enabled) type.email = true
    if (isCorpConfigured.value && emailChannel.enabled) type.corp = true
  })
  ElMessage.success('所有可用的通知类型已全部开启。')
}

// 全部关闭通知
const disableAllNotifications = () => {
  notificationTypes.value.forEach(type => {
    type.inApp = false
    type.email = false
    type.corp = false
  })
  ElMessage.success('所有通知类型已全部关闭。')
}

// 恢复默认设置
const restoreDefaultSettings = () => {
  // 重置渠道状态
  inAppChannel.enabled = true
  emailChannel.enabled = true
  corpChannel.enabled = false
  isCorpConfigured.value = false
  
  // 重置通知类型状态
  notificationTypes.value = [
    {
      id: 1,
      name: '项目通知',
      icon: 'fa-folder-open',
      desc: '项目创建、更新、代码合并等',
      inApp: true,
      email: true,
      corp: true
    },
    {
      id: 2,
      name: '团队协作',
      icon: 'fa-users',
      desc: '成员邀请、权限变更',
      inApp: true,
      email: false,
      corp: true
    },
    {
      id: 3,
      name: '系统公告',
      icon: 'fa-bullhorn',
      desc: '平台维护、新功能发布',
      inApp: true,
      email: true,
      corp: false
    },
    {
      id: 4,
      name: '生成任务状态',
      icon: 'fa-magic',
      desc: '生成任务开始、完成、失败',
      inApp: true,
      email: true,
      corp: true
    },
    {
      id: 5,
      name: '营销资讯',
      icon: 'fa-newspaper',
      desc: '产品更新、活动推广',
      inApp: false,
      email: true,
      corp: false
    }
  ]
  
  ElMessage.success('已恢复默认设置。')
}
</script>

<style scoped lang="scss">
.notification-settings-container {
  padding: 1rem;
  @media (min-width: 768px) {
    padding: 1.5rem;
  }
}

/* 自定义滚动条隐藏 */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
  &::-webkit-scrollbar {
    display: none;
  }
}
</style>