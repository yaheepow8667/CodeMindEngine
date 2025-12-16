<template>
  <div class="notification-settings-container min-h-full">
    <!-- 顶部标题区域 -->
    <div class="pb-4 mb-6 border-b border-border-color">
      <h3 class="text-2xl font-semibold text-text-primary">设置中心</h3>
      <!-- 面包屑导航 -->
      <div class="text-sm text-text-secondary mt-1">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/settings' }">设置中心</el-breadcrumb-item>
          <el-breadcrumb-item>通知偏好设置</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>

    <!-- 通知渠道管理模块 -->
    <el-card class="mb-8" shadow="hover">
      <template #header>
        <div class="ant-card-header">通知渠道管理</div>
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
            <span :class="['text-sm font-medium', inAppEnabled ? 'text-success' : 'text-text-tertiary']">
              {{ inAppEnabled ? '已开启' : '已关闭' }}
            </span>
            <el-switch v-model="inAppEnabled" @change="handleInAppChange" />
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
            <span :class="['text-sm font-medium', emailEnabled ? 'text-success' : 'text-text-tertiary']">
              {{ emailEnabled ? '已开启' : '已关闭' }}
            </span>
            <el-switch v-model="emailEnabled" @change="handleEmailChange" />
          </div>
        </div>

        <!-- 企业应用通知 (模拟钉钉/企业微信) -->
        <div class="flex items-center justify-between p-4 border border-border-color rounded-lg hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <i class="fab fa-weixin text-xl text-warning mr-4"></i>
            <div>
              <p class="font-medium">企业应用通知</p>
              <p class="text-sm text-text-secondary">通过企业微信/钉钉接收实时通知。状态: <span :class="['font-medium', corpConfigured ? 'text-success' : 'text-danger']">{{ corpConfigured ? '已连接' : '未配置' }}</span></p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <el-button type="primary" plain @click="handleCorpConfig">
              <i class="fas fa-cogs mr-1"></i>{{ corpConfigured ? '管理' : '立即配置' }}
            </el-button>
            <el-switch v-model="corpEnabled" :disabled="!corpConfigured" />
          </div>
        </div>
      </div>
    </el-card>

    <!-- 通知类型细分模块 -->
    <el-card shadow="hover">
      <template #header>
        <div class="ant-card-header">通知类型细分</div>
      </template>

      <!-- 快捷操作按钮 -->
      <div class="flex justify-end space-x-3 mb-4">
        <el-button type="primary" plain @click="enableAll">
          <i class="fas fa-check-circle mr-1"></i>全部开启
        </el-button>
        <el-button type="primary" plain @click="disableAll">
          <i class="fas fa-times-circle mr-1"></i>全部关闭
        </el-button>
      </div>

      <!-- 表格容器 -->
      <div class="overflow-x-auto">
        <el-table :data="notificationTypes" style="width: 100%" border>
          <el-table-column prop="name" label="通知类型" width="25%">
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

          <el-table-column label="站内通知" align="center">
            <template #default="scope">
              <el-switch
                v-model="scope.row.inApp"
                :disabled="!inAppEnabled"
                @change="handleTypeSwitchChange(scope.row, 'inApp')"
              />
            </template>
          </el-table-column>

          <el-table-column label="邮件通知" align="center">
            <template #default="scope">
              <el-switch
                v-model="scope.row.email"
                :disabled="!emailEnabled"
                @change="handleTypeSwitchChange(scope.row, 'email')"
              />
            </template>
          </el-table-column>

          <el-table-column label="企业应用" align="center">
            <template #default="scope">
              <el-switch
                v-model="scope.row.corp"
                :disabled="!corpConfigured || !emailEnabled"
                @change="handleTypeSwitchChange(scope.row, 'corp')"
              />
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 恢复默认设置链接 -->
    <div class="mt-6 text-center">
      <a href="javascript:void(0);" id="btn-restore-default" class="text-sm text-text-secondary hover:text-danger transition-colors duration-200" @click="restoreDefault">
        <i class="fas fa-undo-alt mr-1"></i>恢复默认设置
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

// 定义通知类型接口
interface NotificationType {
  id: number
  name: string
  icon: string
  desc: string
  inApp: boolean
  email: boolean
  corp: boolean
}

// 通知渠道状态
const inAppEnabled = ref(true)
const emailEnabled = ref(true)
const corpEnabled = ref(false)
const corpConfigured = ref(false)

// 通知类型数据
const notificationTypes = reactive<NotificationType[]>([
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

// 站内通知开关变化
const handleInAppChange = () => {
  // 更新所有通知类型的站内通知状态
  notificationTypes.forEach(type => {
    type.inApp = inAppEnabled.value
  })
  ElMessage.success(`站内通知渠道已${inAppEnabled.value ? '开启' : '关闭'}`)
}

// 邮件通知开关变化
const handleEmailChange = () => {
  // 更新所有通知类型的邮件通知状态
  notificationTypes.forEach(type => {
    type.email = emailEnabled.value
  })
  ElMessage.success(`邮件通知渠道已${emailEnabled.value ? '开启' : '关闭'}`)
}

// 企业应用配置
const handleCorpConfig = () => {
  corpConfigured.value = !corpConfigured.value
  if (corpConfigured.value) {
    ElMessage.info('已模拟连接企业应用，请前往管理页面进行实际配置。')
  } else {
    ElMessage.info('已模拟断开企业应用连接。')
    corpEnabled.value = false
  }
}

// 通知类型开关变化
const handleTypeSwitchChange = (type: NotificationType, channel: keyof NotificationType) => {
  ElMessage.success(`${type.name}的${channel}通知已${type[channel] ? '开启' : '关闭'}`)
}

// 全部开启
const enableAll = () => {
  notificationTypes.forEach(type => {
    if (inAppEnabled.value) type.inApp = true
    if (emailEnabled.value) type.email = true
    if (corpConfigured.value && emailEnabled.value) type.corp = true
  })
  ElMessage.success('所有可用的通知类型已全部开启。')
}

// 全部关闭
const disableAll = () => {
  notificationTypes.forEach(type => {
    if (inAppEnabled.value) type.inApp = false
    if (emailEnabled.value) type.email = false
    if (corpConfigured.value && emailEnabled.value) type.corp = false
  })
  ElMessage.success('所有可用的通知类型已全部关闭。')
}

// 恢复默认设置
const restoreDefault = () => {
  // 重置渠道状态
  inAppEnabled.value = true
  emailEnabled.value = true
  corpEnabled.value = false
  corpConfigured.value = false

  // 重置通知类型
  notificationTypes.forEach(type => {
    type.inApp = true
    type.email = true
    type.corp = false
  })

  ElMessage.success('已恢复默认设置。')
}
</script>

<style scoped>
/* 全局样式继承自公共页面 */
.notification-settings-container {
  padding: 1rem;
}

@media (min-width: 768px) {
  .notification-settings-container {
    padding: 1.5rem;
  }
}

/* 样式微调 */
.ant-card-header {
  @apply text-lg font-semibold border-b border-border-color pb-3 mb-3;
}
</style>