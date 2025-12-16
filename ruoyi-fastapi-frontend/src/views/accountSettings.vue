<template>
  <div class="min-h-screen bg-light">
    <!-- 顶部标题区域 -->
    <div class="bg-white border-b border-border-color pt-6 pb-4 px-4 md:px-6">
      <h3 class="text-xl font-semibold text-text-primary">设置中心</h3>
      <!-- 面包屑导航 -->
      <nav class="mt-2 text-sm text-text-secondary">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item @click="navigateTo('workbench')">首页</el-breadcrumb-item>
          <el-breadcrumb-item @click="navigateTo('settings')">设置中心</el-breadcrumb-item>
          <el-breadcrumb-item>账户设置</el-breadcrumb-item>
        </el-breadcrumb>
      </nav>
    </div>

    <!-- 内容区域 -->
    <div class="p-4 md:p-6">
      <!-- 整体布局 -->
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- 左侧导航 -->
        <aside class="lg:w-64 flex-shrink-0 bg-white rounded-lg shadow-card h-fit lg:sticky lg:top-24">
          <div class="p-4 border-b border-border-color">
            <h4 class="text-base font-semibold text-text-primary">设置导航</h4>
          </div>
          <nav class="p-2">
            <el-menu :default-active="'accountSettings'" class="menu-item-list">
              <el-menu-item index="accountSettings" @click="navigateTo('accountSettings')">
                <template #title>
                  <i class="fas fa-user-circle mr-3 text-lg"></i>
                  <span>个人设置</span>
                </template>
              </el-menu-item>
              <el-menu-item index="workspaceSettings" @click="navigateTo('workspaceSettings')">
                <template #title>
                  <i class="fas fa-cogs mr-3 text-lg"></i>
                  <span>工作空间设置</span>
                </template>
              </el-menu-item>
              <el-menu-item index="notificationSettings" @click="navigateTo('notificationSettings')">
                <template #title>
                  <i class="fas fa-bell mr-3 text-lg"></i>
                  <span>通知偏好</span>
                </template>
              </el-menu-item>
              <el-menu-item index="reset" @click="showResetConfirm" class="text-danger">
                <template #title>
                  <i class="fas fa-undo mr-3 text-lg"></i>
                  <span>恢复默认设置</span>
                </template>
              </el-menu-item>
            </el-menu>
          </nav>
        </aside>

        <!-- 右侧内容区 -->
        <main class="flex-1 space-y-8">
          <!-- 1. 个人信息模块 -->
          <el-card class="ant-card">
            <template #header>
              <h4 class="text-lg font-medium text-text-primary">个人信息</h4>
            </template>
            
            <!-- 头像区域 -->
            <div class="flex flex-col md:flex-row items-center md:items-start mb-6 space-y-4 md:space-y-0 md:space-x-6">
              <!-- 头像 -->
              <div class="relative flex-shrink-0">
                <el-avatar :size="128" :src="userInfo.avatar" class="border-4 border-white shadow-md">
                  {{ userInfo.name.substring(0, 1) }}
                </el-avatar>
                <!-- 头像上传 -->
                <el-upload
                  class="avatar-uploader"
                  action="#"
                  :show-file-list="false"
                  :before-upload="handleAvatarUpload"
                  accept="image/jpeg, image/png"
                >
                  <div class="absolute bottom-0 right-0 bg-white p-2 rounded-full shadow-lg border border-border-color cursor-pointer hover:bg-primary-light transition-colors duration-200">
                    <i class="fas fa-camera text-primary text-xl"></i>
                  </div>
                </el-upload>
              </div>
              <!-- 提示 -->
              <div class="flex flex-col justify-center h-32">
                <p class="text-sm text-text-secondary">支持JPG、PNG格式，大小不超过2MB</p>
              </div>
            </div>

            <!-- 基本信息表单 -->
            <el-form :model="userInfo" label-position="top" class="profile-form">
              <el-row :gutter="[32, 16]">
                <el-col :xs="24" :md="12">
                  <el-form-item label="姓名" required>
                    <el-input v-model="userInfo.name" placeholder="请输入姓名" maxlength="20" />
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :md="12">
                  <el-form-item label="显示名称">
                    <el-input v-model="userInfo.displayName" placeholder="请输入显示名称" />
                    <div class="text-xs text-text-tertiary mt-1">用于在团队中显示的名称</div>
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :md="12">
                  <el-form-item label="邮箱" required>
                    <div class="flex items-center">
                      <el-input v-model="userInfo.email" readonly class="flex-1 mr-2" />
                      <el-button type="primary" size="small" plain @click="toggleEmailEdit(true)">
                        修改
                      </el-button>
                    </div>
                    <div v-if="showEmailEdit" class="mt-2 space-y-2">
                      <el-input v-model="newEmail" placeholder="输入新邮箱" />
                      <div class="flex space-x-2">
                        <el-input v-model="verificationCode" placeholder="验证码" class="w-1/2" />
                        <el-button type="primary" size="small" plain @click="sendEmailCode" class="w-1/2">
                          发送验证码
                        </el-button>
                      </div>
                      <el-button type="primary" size="small" @click="handleEmailUpdate" class="w-full">
                        确认修改
                      </el-button>
                    </div>
                    <div class="flex items-center mt-1 text-success">
                      <i class="fas fa-check-circle mr-1 text-sm"></i>
                      <span class="text-sm">验证通过</span>
                    </div>
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :md="12">
                  <el-form-item label="职位">
                    <el-input v-model="userInfo.position" placeholder="请输入职位" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <!-- 个人简介 -->
              <el-form-item label="个人简介">
                <el-input
                  v-model="userInfo.bio"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入个人简介"
                  maxlength="200"
                  show-word-limit
                />
              </el-form-item>
              
              <!-- 底部操作 -->
              <el-form-item class="flex justify-end items-center pt-4 border-t mt-4">
                <div class="text-xs text-text-tertiary mr-4">上次保存: 2024-01-15 14:30</div>
                <el-button type="primary" @click="saveProfile">
                  <i class="fas fa-save mr-1"></i> 保存更改
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 2. 账户安全模块 -->
          <el-card class="ant-card">
            <template #header>
              <h4 class="text-lg font-medium text-text-primary">账户安全</h4>
            </template>
            
            <!-- 安全项列表 -->
            <div id="security-list">
              <!-- 密码安全 -->
              <div class="flex justify-between items-center py-3 border-b last:border-b-0">
                <div class="flex items-center">
                  <i class="fas fa-lock text-xl text-primary mr-4"></i>
                  <div>
                    <p class="font-medium">登录密码</p>
                    <p class="text-xs text-text-secondary">用于保护您的账户安全</p>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <span class="text-xs text-success font-medium">已设置</span>
                  <span class="text-xs text-text-tertiary hidden sm:inline">最近修改：2023-10-27</span>
                  <el-button type="primary" size="small" plain @click="handleSecurityAction('password')">
                    修改
                  </el-button>
                </div>
              </div>
              
              <!-- 手机绑定 -->
              <div class="flex justify-between items-center py-3 border-b last:border-b-0">
                <div class="flex items-center">
                  <i class="fas fa-mobile-alt text-xl text-info mr-4"></i>
                  <div>
                    <p class="font-medium">绑定手机</p>
                    <p class="text-xs text-text-secondary">用于接收重要通知和找回密码</p>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <span class="text-xs text-text-primary font-medium">138****5678</span>
                  <el-button type="primary" size="small" plain @click="handleSecurityAction('phone', '更换')">
                    更换
                  </el-button>
                  <el-button type="danger" size="small" plain @click="handleSecurityAction('phone', '解绑')">
                    解绑
                  </el-button>
                </div>
              </div>
              
              <!-- 邮箱绑定 -->
              <div class="flex justify-between items-center py-3 border-b last:border-b-0">
                <div class="flex items-center">
                  <i class="fas fa-envelope text-xl text-info mr-4"></i>
                  <div>
                    <p class="font-medium">绑定邮箱</p>
                    <p class="text-xs text-text-secondary">用于接收系统通知和账户活动提醒</p>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <span class="text-xs text-text-primary font-medium">{{ userInfo.email }}</span>
                  <el-button type="primary" size="small" plain @click="handleSecurityAction('email', '更换')">
                    更换
                  </el-button>
                </div>
              </div>
              
              <!-- 双重认证 (2FA) -->
              <div class="flex justify-between items-center py-3 border-b last:border-b-0">
                <div class="flex items-center">
                  <i class="fas fa-shield-alt text-xl text-success mr-4"></i>
                  <div>
                    <p class="font-medium">双重认证 (2FA)</p>
                    <p class="text-xs text-text-secondary">增加一层安全保护，推荐开启</p>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <el-switch v-model="is2FAEnabled" @change="handle2FASwitch" />
                  <el-button type="primary" size="small" plain @click="handleSecurityAction('2fa')">
                    管理
                  </el-button>
                </div>
              </div>
            </div>
            
            <!-- 登录设备管理 -->
            <div class="mt-8 pt-4 border-t">
              <h5 class="text-md font-medium mb-3">最近登录的设备</h5>
              <el-table :data="loginDevices" stripe style="width: 100%">
                <el-table-column prop="device" label="设备" width="100" />
                <el-table-column prop="deviceType" label="设备类型" width="120" />
                <el-table-column prop="browser" label="浏览器" width="150" />
                <el-table-column prop="ipAddress" label="IP地址" />
                <el-table-column prop="lastActive" label="最后活跃时间" width="180" />
                <el-table-column label="操作" width="100" fixed="right">
                  <template #default="scope">
                    <el-button
                      type="danger"
                      size="small"
                      text
                      @click="handleLogoutDevice(scope.row)"
                    >
                      登出
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              
              <div class="mt-4 flex justify-end">
                <el-button type="danger" text @click="confirmClearSessions">
                  <i class="fas fa-sign-out-alt mr-1"></i> 清除所有其他会话
                </el-button>
              </div>
            </div>
          </el-card>

          <!-- 3. API 令牌管理模块 -->
          <el-card class="ant-card">
            <template #header>
              <h4 class="text-lg font-medium text-text-primary">API 令牌管理</h4>
            </template>
            
            <!-- 创建新令牌区域 -->
            <div class="bg-primary-light p-4 rounded-lg mb-6 border border-primary/30">
              <h5 class="font-semibold text-primary mb-3 flex items-center">
                <i class="fas fa-key mr-2"></i> 创建新的访问令牌
              </h5>
              <el-form :model="tokenForm" label-position="top">
                <el-row :gutter="[16, 16]">
                  <el-col :xs="24" :md="8">
                    <el-form-item label="令牌名称" required>
                      <el-input
                        v-model="tokenForm.name"
                        placeholder="例如: CI/CD Pipeline Access"
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="8">
                    <el-form-item label="权限范围" required>
                      <el-select
                        v-model="tokenForm.scopes"
                        multiple
                        placeholder="请选择权限范围"
                        style="width: 100%"
                        size="large"
                      >
                        <el-option label="项目读取" value="read_project" />
                        <el-option label="项目写入" value="write_project" />
                        <el-option label="生成任务" value="generate_task" />
                        <el-option label="管理设置" value="manage_settings" />
                      </el-select>
                      <div class="text-xs text-text-tertiary mt-1">按住 Ctrl/Cmd 键可多选</div>
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :md="8">
                    <el-form-item label="过期时间 (可选)">
                      <el-date-picker
                        v-model="tokenForm.expiryDate"
                        type="date"
                        placeholder="选择过期时间"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item>
                  <el-button type="primary" @click="createToken">
                    <i class="fas fa-plus mr-1"></i> 生成令牌
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <!-- 令牌列表 -->
            <h5 class="text-md font-medium mb-3">已创建的令牌 (共 {{ tokens.length }} 个)</h5>
            <el-table :data="tokens" stripe style="width: 100%">
              <el-table-column prop="name" label="令牌名称" width="200" />
              <el-table-column prop="scopes" label="权限">
                <template #default="scope">
                  <el-tag
                    v-for="scope in scope.row.scopes"
                    :key="scope"
                    size="small"
                    class="mr-1"
                  >
                    {{ scope }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="createdAt" label="创建时间" width="180" />
              <el-table-column prop="lastUsed" label="最后使用" width="180" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="scope">
                  <el-button
                    type="primary"
                    size="small"
                    text
                    @click="showTokenDetail(scope.row)"
                  >
                    查看
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    text
                    @click="revokeToken(scope.row)"
                  >
                    撤销
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </main>
      </div>
    </div>

    <!-- 令牌详情模态框 -->
    <el-dialog
      v-model="tokenModalVisible"
      title="令牌详情"
      width="50%"
      :close-on-click-modal="false"
    >
      <div class="space-y-3">
        <p><strong>令牌名称:</strong> {{ selectedToken.name }}</p>
        <p><strong>令牌值 (仅显示一次):</strong></p>
        <el-input
          v-model="selectedToken.value"
          type="text"
          readonly
          class="bg-light p-2 rounded text-sm text-danger border border-danger/50"
        />
        <div class="text-xs text-text-tertiary">注意：令牌创建后仅显示一次，请妥善保管。</div>
        <p><strong>权限范围:</strong> {{ selectedToken.scopes.join(', ') }}</p>
        <p><strong>创建时间:</strong> {{ selectedToken.createdAt }}</p>
        <p><strong>最后使用:</strong> {{ selectedToken.lastUsed }}</p>
      </div>
      <template #footer>
        <div class="flex justify-end">
          <el-button @click="tokenModalVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

// 定义数据类型
interface UserInfo {
  name: string
  displayName: string
  email: string
  position: string
  bio: string
  avatar: string
}

interface LoginDevice {
  id: string
  device: string
  deviceType: string
  browser: string
  ipAddress: string
  lastActive: string
}

interface TokenForm {
  name: string
  scopes: string[]
  expiryDate: string
}

interface Token {
  id: string
  name: string
  value: string
  scopes: string[]
  createdAt: string
  lastUsed: string
  status: string
}

// 初始化路由
const router = useRouter()

// 用户信息
const userInfo = reactive<UserInfo>({
  name: '张开发',
  displayName: 'Zhang_Dev',
  email: 'zhang.dev@example.com',
  position: '前端架构师',
  bio: '专注于AI驱动的低代码平台前端架构设计与实现。',
  avatar: './accountSettings/8cda41a084d5db2f669546a3dd9efe41.png'
})

// 邮箱修改相关
const showEmailEdit = ref(false)
const newEmail = ref('')
const verificationCode = ref('')

// 双重认证
const is2FAEnabled = ref(true)

// 登录设备列表
const loginDevices = ref<LoginDevice[]>([
  // 模拟数据
  {
    id: '1',
    device: 'Windows',
    deviceType: 'PC',
    browser: 'Chrome 120',
    ipAddress: '192.168.1.100',
    lastActive: '2024-01-15 14:30'
  },
  {
    id: '2',
    device: 'iPhone',
    deviceType: 'Mobile',
    browser: 'Safari 17',
    ipAddress: '192.168.1.101',
    lastActive: '2024-01-14 20:15'
  }
])

// 令牌管理
const tokenForm = reactive<TokenForm>({
  name: '',
  scopes: [],
  expiryDate: ''
})

const tokens = ref<Token[]>([
  // 模拟数据
  {
    id: '1',
    name: 'CI/CD Pipeline',
    value: 'cm_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    scopes: ['read_project', 'write_project', 'generate_task'],
    createdAt: '2024-01-10 09:00',
    lastUsed: '2024-01-15 10:30',
    status: 'active'
  },
  {
    id: '2',
    name: 'API Testing',
    value: 'cm_sk_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',
    scopes: ['read_project'],
    createdAt: '2024-01-05 14:00',
    lastUsed: '2024-01-12 16:45',
    status: 'active'
  }
])

const tokenModalVisible = ref(false)
const selectedToken = reactive<Token>({
  id: '',
  name: '',
  value: '',
  scopes: [],
  createdAt: '',
  lastUsed: '',
  status: 'active'
})

// 导航方法
const navigateTo = (path: string) => {
  router.push(`/${path}`)
}

// 处理头像上传
const handleAvatarUpload = (file: File) => {
  // 模拟上传逻辑
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('上传头像图片大小不能超过 2MB!')
    return false
  }
  
  // 这里可以添加实际的上传逻辑
  ElMessage.success('头像上传成功')
  return false // 阻止自动上传
}

// 切换邮箱编辑状态
const toggleEmailEdit = (show: boolean) => {
  showEmailEdit.value = show
  if (!show) {
    newEmail.value = ''
    verificationCode.value = ''
  }
}

// 发送邮箱验证码
const sendEmailCode = () => {
  if (!newEmail.value) {
    ElMessage.warning('请输入新邮箱')
    return
  }
  
  // 模拟发送验证码
  ElMessage.success('验证码已发送到您的新邮箱')
}

// 处理邮箱更新
const handleEmailUpdate = () => {
  if (!newEmail.value || !verificationCode.value) {
    ElMessage.warning('请输入新邮箱和验证码')
    return
  }
  
  // 模拟邮箱更新
  userInfo.email = newEmail.value
  toggleEmailEdit(false)
  ElMessage.success('邮箱更新成功')
}

// 保存个人资料
const saveProfile = () => {
  // 模拟保存
  ElMessage.success('个人信息保存成功')
}

// 处理安全操作
const handleSecurityAction = (type: string, action?: string) => {
  console.log('安全操作:', type, action)
  switch (type) {
    case 'password':
      // 处理密码修改
      ElMessage.info('密码修改功能开发中')
      break
    case 'phone':
      // 处理手机绑定/解绑
      ElMessage.info('手机绑定功能开发中')
      break
    case 'email':
      // 处理邮箱绑定/解绑
      ElMessage.info('邮箱绑定功能开发中')
      break
    case '2fa':
      // 处理双重认证
      ElMessage.info('双重认证管理功能开发中')
      break
  }
}

// 处理双重认证开关
const handle2FASwitch = (checked: boolean) => {
  is2FAEnabled.value = checked
  ElMessage.success(`双重认证已${checked ? '开启' : '关闭'}`)
}

// 处理登出设备
const handleLogoutDevice = (device: LoginDevice) => {
  ElMessageBox.confirm(`确定要登出设备 ${device.device} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟登出
    ElMessage.success('设备已登出')
  }).catch(() => {
    // 取消操作
  })
}

// 确认清除所有会话
const confirmClearSessions = () => {
  ElMessageBox.confirm('确定要清除所有其他会话吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'danger'
  }).then(() => {
    // 模拟清除
    ElMessage.success('所有其他会话已清除')
  }).catch(() => {
    // 取消操作
  })
}

// 创建令牌
const createToken = () => {
  if (!tokenForm.name || tokenForm.scopes.length === 0) {
    ElMessage.warning('请填写令牌名称和选择权限范围')
    return
  }
  
  // 模拟创建令牌
  const newToken: Token = {
    id: Date.now().toString(),
    name: tokenForm.name,
    value: `cm_sk_${Math.random().toString(36).substring(2, 34)}`,
    scopes: [...tokenForm.scopes],
    createdAt: new Date().toLocaleString(),
    lastUsed: '从未使用',
    status: 'active'
  }
  
  tokens.value.push(newToken)
  Object.assign(selectedToken, newToken)
  tokenModalVisible.value = true
  
  // 重置表单
  tokenForm.name = ''
  tokenForm.scopes = []
  tokenForm.expiryDate = ''
}

// 显示令牌详情
const showTokenDetail = (token: Token) => {
  Object.assign(selectedToken, token)
  tokenModalVisible.value = true
}

// 撤销令牌
const revokeToken = (token: Token) => {
  ElMessageBox.confirm(`确定要撤销令牌 ${token.name} 吗？`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'danger'
  }).then(() => {
    // 模拟撤销
    token.status = 'revoked'
    ElMessage.success('令牌已撤销')
  }).catch(() => {
    // 取消操作
  })
}

// 生命周期钩子
onMounted(() => {
  // 可以在这里加载用户信息和其他数据
})
</script>

<style scoped lang="scss">
/* 这里可以添加需要的组件级样式 */
.ant-card {
  @apply bg-white rounded-lg shadow-card p-5 mb-5 transition-all duration-300 hover:shadow-lg;
}

.form-label {
  @apply text-sm font-medium text-text-primary mb-1 block;
}

.menu-item-list {
  border: none;
  width: 100%;
}

.menu-item {
  @apply flex items-center px-4 py-2 rounded-md transition-all duration-200 text-sm cursor-pointer;
  
  &:hover {
    @apply bg-primary-light text-primary;
  }
  
  &.active-menu {
    @apply bg-primary/10 text-primary border-r-2 border-primary;
  }
}
</style>