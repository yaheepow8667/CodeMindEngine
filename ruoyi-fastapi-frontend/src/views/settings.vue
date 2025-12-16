<template>
  <div class="min-h-screen bg-light">
    <!-- 顶部标题区域 -->
    <div class="bg-white border-b border-border-color pt-6 pb-4 px-4 md:px-6">
      <h3 class="text-xl font-semibold text-text-primary">设置中心</h3>
      <!-- 面包屑导航 -->
      <nav class="mt-2 text-sm text-text-secondary">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item @click="navigateTo('workbench')">首页</el-breadcrumb-item>
          <el-breadcrumb-item>设置中心</el-breadcrumb-item>
        </el-breadcrumb>
      </nav>
    </div>

    <!-- 内容区域 -->
    <div class="p-4 md:p-6">
      <!-- 整体布局 -->
      <div class="flex flex-col md:flex-row gap-6">
        <!-- 左侧导航菜单 -->
        <div class="w-full md:w-64 flex-shrink-0">
          <el-card class="sticky top-4" shadow="hover">
            <div class="px-4 py-4 border-b border-border-color">
              <h2 class="text-lg font-semibold">设置中心</h2>
            </div>
            <nav class="py-2">
              <el-menu :default-active="activeTab" @select="handleMenuSelect" class="menu-item-list">
                <el-menu-item index="accountSettings" @click="navigateTo('settings/accountSettings')">
                  <template #title>
                    <i class="fas fa-user mr-3 text-lg"></i>
                    <span>账户设置</span>
                  </template>
                </el-menu-item>
                <el-menu-item index="workspaceSettings" @click="navigateTo('settings/workspaceSettings')">
                  <template #title>
                    <i class="fas fa-desktop mr-3 text-lg"></i>
                    <span>工作空间设置</span>
                  </template>
                </el-menu-item>
                <el-menu-item index="notificationSettings" @click="navigateTo('settings/notificationSettings')">
                  <template #title>
                    <i class="fas fa-bell mr-3 text-lg"></i>
                    <span>通知偏好设置</span>
                  </template>
                </el-menu-item>
                <el-menu-item index="team">
                  <template #title>
                    <i class="fas fa-users mr-3 text-lg"></i>
                    <span>团队管理</span>
                  </template>
                </el-menu-item>
                <el-menu-item index="system">
                  <template #title>
                    <i class="fas fa-cogs mr-3 text-lg"></i>
                    <span>系统配置</span>
                  </template>
                </el-menu-item>
                <el-menu-item index="about">
                  <template #title>
                    <i class="fas fa-info-circle mr-3 text-lg"></i>
                    <span>关于</span>
                  </template>
                </el-menu-item>
              </el-menu>
            </nav>
          </el-card>
        </div>
        
        <!-- 右侧主内容区 -->
        <div class="flex-1">
          <!-- 账户设置 -->
          <div class="setting-content" id="account">
            <el-card shadow="hover">
              <h3 class="text-xl font-semibold mb-6">账户设置</h3>
              <!-- 个人信息 -->
              <div class="mb-8">
                <h4 class="text-lg font-medium mb-4">个人信息</h4>
                <div class="flex flex-col md:flex-row gap-6">
                  <!-- 头像上传 -->
                  <div class="w-full md:w-32 flex flex-col items-center">
                    <div class="relative mb-3">
                      <img src="/src/assets/images/user-avatar.png" alt="用户头像" class="w-24 h-24 rounded-full object-cover border-2 border-border-color">
                      <div class="absolute bottom-0 right-0 bg-primary rounded-full p-1 cursor-pointer hover:bg-primary-dark transition-colors duration-200">
                        <i class="fas fa-camera text-white text-sm"></i>
                      </div>
                    </div>
                    <p class="text-sm text-text-tertiary text-center">点击更换头像</p>
                    <p class="text-xs text-text-tertiary text-center mt-1">支持 JPG, PNG 格式，最大 2MB</p>
                  </div>
                  <!-- 个人信息表单 -->
                  <div class="flex-1">
                    <el-form :model="userInfo" label-position="top" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <el-form-item label="姓名" class="form-label">
                        <el-input v-model="userInfo.name" placeholder="请输入姓名"></el-input>
                      </el-form-item>
                      <el-form-item label="显示名称" class="form-label">
                        <el-input v-model="userInfo.displayName" placeholder="请输入显示名称"></el-input>
                      </el-form-item>
                      <el-form-item label="邮箱" class="form-label">
                        <div class="relative">
                          <el-input v-model="userInfo.email" placeholder="请输入邮箱" readonly></el-input>
                          <span class="absolute right-3 top-1/2 transform -translate-y-1/2 text-success text-xs">已验证</span>
                        </div>
                      </el-form-item>
                      <el-form-item label="职位" class="form-label">
                        <el-input v-model="userInfo.position" placeholder="请输入职位"></el-input>
                      </el-form-item>
                      <el-form-item label="个人简介" class="form-label md:col-span-2">
                        <el-input v-model="userInfo.bio" type="textarea" :rows="4" placeholder="请输入个人简介"></el-input>
                      </el-form-item>
                    </el-form>
                    <div class="mt-6 flex justify-end">
                      <el-button type="primary" class="btn btn-primary">保存更改</el-button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 账户安全 -->
              <div class="mb-8">
                <h4 class="text-lg font-medium mb-4">账户安全</h4>
                <div class="space-y-4">
                  <div class="flex items-center justify-between p-4 border border-border-color rounded-lg">
                    <div>
                      <h5 class="font-medium">登录密码</h5>
                      <p class="text-sm text-text-tertiary">已设置，最后修改于 2023-10-15</p>
                    </div>
                    <el-button type="info" plain>修改</el-button>
                  </div>
                  <div class="flex items-center justify-between p-4 border border-border-color rounded-lg">
                    <div>
                      <h5 class="font-medium">绑定手机</h5>
                      <p class="text-sm text-text-tertiary">已绑定: 138****5678</p>
                    </div>
                    <div class="flex gap-2">
                      <el-button type="info" plain>更换</el-button>
                      <el-button type="info" plain>解绑</el-button>
                    </div>
                  </div>
                  <div class="flex items-center justify-between p-4 border border-border-color rounded-lg">
                    <div>
                      <h5 class="font-medium">绑定邮箱</h5>
                      <p class="text-sm text-text-tertiary">已绑定: zhang***@example.com</p>
                    </div>
                    <div class="flex gap-2">
                      <el-button type="info" plain>更换</el-button>
                      <el-button type="info" plain>解绑</el-button>
                    </div>
                  </div>
                  <div class="flex items-center justify-between p-4 border border-border-color rounded-lg">
                    <div>
                      <h5 class="font-medium">双重认证（2FA）</h5>
                      <p class="text-sm text-text-tertiary">未开启</p>
                    </div>
                    <el-button type="primary">立即开启</el-button>
                  </div>
                </div>
              </div>
              
              <!-- 登录设备管理 -->
              <div>
                <div class="flex items-center justify-between mb-4">
                  <h4 class="text-lg font-medium">登录设备管理</h4>
                  <a href="#" class="text-primary text-sm hover:underline">查看全部</a>
                </div>
                <div class="overflow-x-auto">
                  <el-table :data="loginDevices" stripe style="width: 100%">
                    <el-table-column prop="deviceType" label="设备类型">
                      <template #default="scope">
                        <div class="flex items-center">
                          <i :class="['fas', scope.row.icon, 'mr-2 text-text-tertiary']"></i>
                          <span>{{ scope.row.deviceType }}</span>
                        </div>
                      </template>
                    </el-table-column>
                    <el-table-column prop="browser" label="浏览器"></el-table-column>
                    <el-table-column prop="ipAddress" label="IP地址"></el-table-column>
                    <el-table-column prop="lastActivity" label="最后活动时间" width="150"></el-table-column>
                    <el-table-column prop="action" label="操作" width="100">
                      <template #default>
                        <a href="#" class="text-text-tertiary hover:text-danger">注销</a>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </el-card>
            
            <!-- API访问令牌 -->
            <el-card class="mt-5" shadow="hover">
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg font-medium">API访问令牌</h3>
                <el-button type="primary">创建新令牌</el-button>
              </div>
              <div class="overflow-x-auto">
                <el-table :data="apiTokens" stripe style="width: 100%">
                  <el-table-column prop="name" label="令牌名称"></el-table-column>
                  <el-table-column prop="permissions" label="权限"></el-table-column>
                  <el-table-column prop="createdAt" label="创建时间"></el-table-column>
                  <el-table-column prop="lastUsed" label="最后使用"></el-table-column>
                  <el-table-column prop="status" label="状态">
                    <template #default="scope">
                      <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="actions" label="操作" width="200">
                    <template #default>
                      <div class="flex space-x-3">
                        <a href="#" class="text-text-tertiary hover:text-primary">复制</a>
                        <a href="#" class="text-text-tertiary hover:text-primary">详情</a>
                        <a href="#" class="text-text-tertiary hover:text-danger">撤销</a>
                      </div>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const router = useRouter();
const activeTab = ref('accountSettings');

// 用户信息
interface UserInfo {
  name: string;
  displayName: string;
  email: string;
  position: string;
  bio: string;
}

const userInfo = reactive<UserInfo>({
  name: '张开发',
  displayName: 'dev_zhang',
  email: 'zhang@example.com',
  position: '高级工程师',
  bio: '热爱编程的前端工程师，专注于低代码平台开发与应用。'
});

// 登录设备
interface LoginDevice {
  deviceType: string;
  browser: string;
  ipAddress: string;
  lastActivity: string;
  icon: string;
}

const loginDevices = reactive<LoginDevice[]>([
  {
    deviceType: 'Windows PC',
    browser: 'Chrome 114.0.5735.199',
    ipAddress: '192.168.1.100',
    lastActivity: '今天 10:23',
    icon: 'fa-laptop'
  },
  {
    deviceType: 'iPhone',
    browser: 'Safari Mobile',
    ipAddress: '10.0.0.5',
    lastActivity: '昨天 18:45',
    icon: 'fa-mobile-alt'
  }
]);

// API令牌
interface ApiToken {
  name: string;
  permissions: string;
  createdAt: string;
  lastUsed: string;
  status: string;
}

const apiTokens = reactive<ApiToken[]>([
  {
    name: '项目管理API',
    permissions: '项目读、项目写',
    createdAt: '2023-09-20',
    lastUsed: '今天 09:15',
    status: '活跃'
  },
  {
    name: 'CI/CD集成',
    permissions: '生成任务触发',
    createdAt: '2023-08-15',
    lastUsed: '3天前',
    status: '活跃'
  },
  {
    name: '数据分析',
    permissions: '项目读',
    createdAt: '2023-07-05',
    lastUsed: '从未使用',
    status: '即将过期'
  }
]);

// 获取状态类型
function getStatusType(status: string): string {
  switch (status) {
    case '活跃':
      return 'success';
    case '即将过期':
      return 'warning';
    default:
      return 'info';
  }
}

// 导航到指定页面
function navigateTo(routeName: string): void {
  router.push({
    path: `/${routeName}`
  });
}

// 处理菜单选择
function handleMenuSelect(key: string): void {
  activeTab.value = key;
  if (key === 'accountSettings' || key === 'workspaceSettings' || key === 'notificationSettings') {
    navigateTo(`settings/${key}`);
  } else {
    // 其他菜单可以添加相应的处理逻辑
    ElMessage.info(`即将跳转到${key}页面`);
  }
}
</script>

<style scoped lang="scss">
@use "@/assets/styles/variables.module.scss" as vars;

// 导航菜单样式
.menu-item-list {
  border-right: none;
  
  .el-menu-item {
    @apply flex items-center px-4 py-3 text-text-secondary hover:bg-primary-light/50 hover:text-primary transition-all duration-300 cursor-pointer;
    
    i {
      @apply mr-3 text-lg;
    }
    
    &.is-active {
      @apply bg-primary-light text-primary border-l-4 border-primary;
    }
  }
}

// 表单标签样式
.form-label {
  @apply block text-sm font-medium text-text-secondary mb-1;
}

// 自定义颜色变量
:deep(.text-text-primary) {
  color: vars.$text-primary;
}

:deep(.text-text-secondary) {
  color: vars.$text-secondary;
}

:deep(.text-text-tertiary) {
  color: vars.$text-tertiary;
}

:deep(.border-border-color) {
  border-color: vars.$border-color;
}
</style>