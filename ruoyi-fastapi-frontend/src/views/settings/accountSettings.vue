<template>
  <div class="account-settings-container">
    <!-- 整体布局：左侧导航和右侧内容 -->
    <div class="flex flex-col lg:flex-row gap-6">
      <!-- 左侧导航 -->
      <aside class="lg:w-64 flex-shrink-0 bg-white rounded-lg shadow-card h-fit lg:sticky lg:top-24">
        <div class="p-4 border-b border-border-color">
          <h4 class="text-base font-semibold text-text-primary">设置导航</h4>
        </div>
        <nav class="p-2">
          <router-link to="/settings/accountSettings" class="menu-item active-menu">
            <UserCircle class="mr-3 text-lg" />
            <span>个人设置</span>
          </router-link>
          <router-link to="/settings/workspaceSettings" class="menu-item">
            <Cogs class="mr-3 text-lg" />
            <span>工作空间设置</span>
          </router-link>
          <router-link to="/settings/notificationSettings" class="menu-item">
            <Bell class="mr-3 text-lg" />
            <span>通知偏好</span>
          </router-link>
          <!-- 恢复默认设置链接 -->
          <a href="javascript:void(0);" @click="showNotification('info', '恢复默认设置', '此操作将恢复所有设置项至默认值。')" class="menu-item mt-4 text-danger hover:text-danger/80">
            <Undo class="mr-3 text-lg" />
            <span>恢复默认设置</span>
          </a>
        </nav>
      </aside>
      <!-- 右侧内容区 -->
      <main class="flex-1 space-y-8">
        <!-- 1. 个人信息模块 -->
        <el-card shadow="hover" bordered="false" class="ant-card">
          <template #header>
            <h4 class="text-lg font-medium text-text-primary">个人信息</h4>
          </template>
          <!-- 头像区域 -->
          <div class="flex flex-col md:flex-row items-center md:items-start mb-6 space-y-4 md:space-y-0 md:space-x-6">
            <!-- 头像 -->
            <div class="relative flex-shrink-0">
              <img :src="avatarUrl" alt="用户头像" class="w-32 h-32 rounded-full object-cover border-4 border-white shadow-md">
              <!-- 占位上传控件 -->
              <label for="avatar-upload" class="absolute bottom-0 right-0 bg-white p-2 rounded-full shadow-lg border border-border-color cursor-pointer hover:bg-primary-light transition-colors duration-200">
                <Camera class="text-primary text-xl" />
                <input type="file" id="avatar-upload" accept="image/jpeg, image/png" class="hidden" @change="handleAvatarUpload">
              </label>
            </div>
            <!-- 提示 -->
            <div class="flex flex-col justify-center h-32">
              <p class="text-sm text-text-secondary">支持JPG、PNG格式，大小不超过2MB</p>
            </div>
          </div>
          <!-- 基本信息表单 -->
          <el-form ref="profileFormRef" :model="profileForm" label-position="top" class="profile-form">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
              <!-- 姓名 -->
              <el-form-item label="姓名" prop="name" :rules="[{ required: true, message: '请输入姓名', trigger: 'blur' }]">
                <el-input v-model="profileForm.name" maxlength="20" placeholder="请输入姓名" />
              </el-form-item>
              <!-- 显示名称 -->
              <el-form-item label="显示名称">
                <el-input v-model="profileForm.displayName" placeholder="请输入显示名称" />
                <p class="text-xs text-text-tertiary mt-1">用于在团队中显示的名称</p>
              </el-form-item>
              <!-- 邮箱 -->
              <el-form-item label="邮箱" prop="email" :rules="[{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }]">
                <div class="flex items-center">
                  <el-input v-model="profileForm.email" :readonly="!emailEditMode" class="flex-1 mr-2" />
                  <el-button type="primary" plain @click="emailEditMode = !emailEditMode" :disabled="emailEditMode">修改</el-button>
                </div>
                <div v-if="emailEditMode" class="mt-2 space-y-2">
                  <el-input v-model="newEmail" placeholder="输入新邮箱" />
                  <div class="flex space-x-2">
                    <el-input v-model="verificationCode" placeholder="验证码" class="w-1/2" />
                    <el-button type="primary" plain @click="sendEmailCode" class="w-1/2">发送验证码</el-button>
                  </div>
                  <el-button type="primary" @click="handleEmailUpdate" class="w-full">确认修改</el-button>
                </div>
                <div class="flex items-center mt-1 text-success">
                  <CheckCircle class="mr-1 text-sm" />
                  <span class="text-sm">验证通过</span>
                </div>
              </el-form-item>
              <!-- 职位 -->
              <el-form-item label="职位">
                <el-input v-model="profileForm.position" placeholder="请输入职位" />
              </el-form-item>
            </div>
            <!-- 个人简介 -->
            <el-form-item label="个人简介">
              <el-input v-model="profileForm.bio" type="textarea" rows="3" maxlength="200" placeholder="请输入个人简介" />
              <p class="text-xs text-text-tertiary mt-1 text-right">{{ bioCount }} /200</p>
            </el-form-item>
            <!-- 底部操作 -->
            <div class="flex justify-end items-center pt-4 border-t mt-4">
              <p class="text-xs text-text-tertiary mr-4">上次保存: {{ lastSaved }}</p>
              <el-button type="primary" @click="handleProfileSave"><Save class="mr-1" />保存更改</el-button>
            </div>
          </el-form>
        </el-card>
        <!-- 2. 账户安全模块 -->
        <el-card shadow="hover" bordered="false" class="ant-card">
          <template #header>
            <h4 class="text-lg font-medium text-text-primary">账户安全</h4>
          </template>
          <!-- 安全项列表 -->
          <div id="security-list">
            <!-- 密码安全 -->
            <div class="flex justify-between items-center py-3 border-b last:border-b-0">
              <div class="flex items-center">
                <Lock class="text-xl text-primary mr-4" />
                <div>
                  <p class="font-medium">登录密码</p>
                  <p class="text-xs text-text-secondary">用于保护您的账户安全</p>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <span class="text-xs text-success font-medium">已设置</span>
                <span class="text-xs text-text-tertiary hidden sm:inline">最近修改：2023-10-27</span>
                <el-button type="primary" plain @click="handleSecurityAction('password')">修改</el-button>
              </div>
            </div>
            <!-- 手机绑定 -->
            <div class="flex justify-between items-center py-3 border-b last:border-b-0">
              <div class="flex items-center">
                <Mobile class="text-xl text-info mr-4" />
                <div>
                  <p class="font-medium">绑定手机</p>
                  <p class="text-xs text-text-secondary">用于接收重要通知和找回密码</p>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <span class="text-xs text-text-primary font-medium">138****5678</span>
                <el-button type="primary" plain @click="handleSecurityAction('phone', '更换')">更换</el-button>
                <el-button type="primary" plain text="danger" @click="handleSecurityAction('phone', '解绑')">解绑</el-button>
              </div>
            </div>
            <!-- 邮箱绑定 -->
            <div class="flex justify-between items-center py-3 border-b last:border-b-0">
              <div class="flex items-center">
                <Message class="text-xl text-info mr-4" />
                <div>
                  <p class="font-medium">绑定邮箱</p>
                  <p class="text-xs text-text-secondary">用于接收系统通知和账户活动提醒</p>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <span class="text-xs text-text-primary font-medium">zhang.dev@example.com</span>
                <el-button type="primary" plain @click="handleSecurityAction('email', '更换')">更换</el-button>
              </div>
            </div>
            <!-- 双重认证 (2FA) -->
            <div class="flex justify-between items-center py-3 border-b last:border-b-0">
              <div class="flex items-center">
                <ShieldCheck class="text-xl text-success mr-4" />
                <div>
                  <p class="font-medium">双重认证 (2FA)</p>
                  <p class="text-xs text-text-secondary">增加一层安全保护，推荐开启</p>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <el-switch v-model="twoFASwitch" @change="handle2FASwitch" />
                <el-button type="primary" plain @click="handleSecurityAction('2fa')">管理</el-button>
              </div>
            </div>
          </div>
          <!-- 登录设备管理 -->
          <div class="mt-8 pt-4 border-t">
            <h5 class="text-md font-medium mb-3">最近登录的设备</h5>
            <!-- Table for Login Devices -->
            <div class="overflow-x-auto">
              <el-table :data="loginDevices" border="false" stripe>
                <el-table-column prop="device" label="设备" width="80" />
                <el-table-column prop="deviceType" label="设备类型" width="120" />
                <el-table-column prop="browser" label="浏览器" width="120" />
                <el-table-column prop="ipAddress" label="IP地址" width="180" />
                <el-table-column prop="lastActiveTime" label="最后活跃时间" width="120" />
                <el-table-column label="操作" width="120" fixed="right">
                  <template #default="scope">
                    <el-button type="text" text="danger" size="small" @click="revokeSession(scope.row)">
                      撤销
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <div class="mt-4 flex justify-end">
              <el-button text="danger" @click="confirmClearSessions">
                <SignOut class="mr-1" />
                清除所有其他会话
              </el-button>
            </div>
          </div>
        </el-card>
        <!-- 3. API 令牌管理模块 -->
        <el-card shadow="hover" bordered="false" class="ant-card">
          <template #header>
            <h4 class="text-lg font-medium text-text-primary">API 令牌管理</h4>
          </template>
          <!-- 创建新令牌区域 -->
          <div class="bg-primary-light p-4 rounded-lg mb-6 border border-primary/30">
            <h5 class="font-semibold text-primary mb-3 flex items-center">
              <Key class="mr-2" />
              创建新的访问令牌
            </h5>
            <el-form ref="tokenCreationFormRef" :model="tokenCreationForm" label-position="top" class="token-creation-form">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <!-- 令牌名称 -->
                <el-form-item label="令牌名称" prop="tokenName" :rules="[{ required: true, message: '请输入令牌名称', trigger: 'blur' }]">
                  <el-input v-model="tokenCreationForm.tokenName" placeholder="例如: CI/CD Pipeline Access" />
                </el-form-item>
                <!-- 权限范围 -->
                <el-form-item label="权限范围" prop="tokenScopes" :rules="[{ required: true, message: '请选择权限范围', trigger: 'change' }]">
                  <el-select v-model="tokenCreationForm.tokenScopes" multiple placeholder="请选择权限范围" class="h-24">
                    <el-option label="项目读取" value="read_project" />
                    <el-option label="项目写入" value="write_project" />
                    <el-option label="生成任务" value="generate_task" />
                    <el-option label="管理设置" value="manage_settings" />
                  </el-select>
                  <p class="text-xs text-text-tertiary mt-1">按住 Ctrl/Cmd 键可多选</p>
                </el-form-item>
                <!-- 过期时间 -->
                <el-form-item label="过期时间 (可选)">
                  <el-date-picker v-model="tokenCreationForm.tokenExpiry" type="date" placeholder="选择过期时间" />
                </el-form-item>
              </div>
              <div class="mt-4 flex justify-end">
                <el-button type="primary" @click="handleTokenCreation">
                  <Plus class="mr-1" />
                  生成令牌
                </el-button>
              </div>
            </el-form>
          </div>
          <!-- 令牌列表 -->
          <h5 class="text-md font-medium mb-3">已创建的令牌 (共 {{ tokens.length }} 个)</h5>
          <div class="overflow-x-auto">
            <el-table :data="tokens" border="false" stripe>
              <el-table-column prop="name" label="令牌名称" width="200" />
              <el-table-column prop="scopes" label="权限" width="200" />
              <el-table-column prop="createdAt" label="创建时间" width="150" />
              <el-table-column prop="lastUsed" label="最后使用" width="150" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                    {{ scope.row.status === 'active' ? '活跃' : '过期' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="scope">
                  <el-button type="text" size="small" @click="viewTokenDetail(scope.row)">
                    查看
                  </el-button>
                  <el-button type="text" text="danger" size="small" @click="revokeToken(scope.row)">
                    撤销
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </main>
    </div>
    <!-- 模态框：查看令牌详情 -->
    <el-dialog v-model="tokenDetailVisible" title="令牌详情" width="600px">
      <div class="space-y-3">
        <p><strong>令牌名称: </strong> <span>{{ selectedToken.name }}</span></p>
        <p>
          <strong>令牌值 (仅显示一次): </strong>
          <el-input v-model="selectedToken.value" type="textarea" readonly class="mt-1" />
          <span class="text-xs text-text-tertiary block mt-1">注意：令牌创建后仅显示一次，请妥善保管。</span>
        </p>
        <p><strong>权限范围: </strong> <span>{{ selectedToken.scopes }}</span></p>
        <p><strong>创建时间: </strong> <span>{{ selectedToken.createdAt }}</span></p>
        <p><strong>最后使用: </strong> <span>{{ selectedToken.lastUsed }}</span></p>
      </div>
      <template #footer>
        <div class="flex justify-end">
          <el-button @click="tokenDetailVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  UserCircle,
  Cogs,
  Bell,
  Undo,
  Camera,
  CheckCircle,
  Save,
  Lock,
  Mobile,
  Message,
  ShieldCheck,
  SignOut,
  Key,
  Plus,
  Times
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 头像URL
const avatarUrl = ref('./accountSettings/8cda41a084d5db2f669546a3dd9efe41.png')

// 个人信息表单
const profileForm = reactive({
  name: '张开发',
  displayName: 'Zhang_Dev',
  email: 'zhang.dev@example.com',
  position: '前端架构师',
  bio: '专注于AI驱动的低代码平台前端架构设计与实现。'
})

// 邮箱编辑模式
const emailEditMode = ref(false)
const newEmail = ref('')
const verificationCode = ref('')

// 个人简介字数统计
const bioCount = computed(() => profileForm.bio.length)

// 上次保存时间
const lastSaved = ref('2024-01-15 14:30')

// 双重认证开关
const twoFASwitch = ref(true)

// 登录设备列表
const loginDevices = ref([
  {
    device: '设备1',
    deviceType: 'Windows PC',
    browser: 'Chrome 120',
    ipAddress: '192.168.1.100',
    lastActiveTime: '2024-01-15 14:30'
  },
  {
    device: '设备2',
    deviceType: 'MacBook Pro',
    browser: 'Safari 17',
    ipAddress: '10.0.0.100',
    lastActiveTime: '2024-01-14 10:20'
  },
  {
    device: '设备3',
    deviceType: 'iPhone 15',
    browser: 'Safari 17',
    ipAddress: '172.16.0.100',
    lastActiveTime: '2024-01-13 16:45'
  }
])

// API令牌创建表单
const tokenCreationForm = reactive({
  tokenName: '',
  tokenScopes: [] as string[],
  tokenExpiry: null as Date | null
})

// API令牌列表
const tokens = ref([
  {
    id: '1',
    name: 'CI/CD Pipeline Access',
    scopes: '项目读取, 项目写入, 生成任务',
    createdAt: '2024-01-10 09:00',
    lastUsed: '2024-01-15 10:30',
    status: 'active'
  },
  {
    id: '2',
    name: 'API Testing',
    scopes: '项目读取, 生成任务',
    createdAt: '2024-01-05 14:30',
    lastUsed: '2024-01-12 16:45',
    status: 'active'
  },
  {
    id: '3',
    name: 'Legacy Integration',
    scopes: '项目读取',
    createdAt: '2023-12-20 11:15',
    lastUsed: '2024-01-01 09:30',
    status: 'expired'
  }
])

// 令牌详情模态框
const tokenDetailVisible = ref(false)
const selectedToken = reactive({
  name: '',
  value: '',
  scopes: '',
  createdAt: '',
  lastUsed: ''
})

// 表单引用
const profileFormRef = ref()
const tokenCreationFormRef = ref()

// 处理头像上传
const handleAvatarUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const file = input.files[0]
    // 这里可以添加文件验证逻辑
    if (file.size > 2 * 1024 * 1024) {
      ElMessage.warning('文件大小不能超过2MB')
      return
    }
    // 这里可以添加文件上传逻辑
    ElMessage.success('头像上传成功')
  }
}

// 发送验证码
const sendEmailCode = () => {
  ElMessage.success('验证码已发送')
}

// 处理邮箱更新
const handleEmailUpdate = () => {
  // 这里可以添加邮箱更新逻辑
  profileForm.email = newEmail.value
  emailEditMode.value = false
  newEmail.value = ''
  verificationCode.value = ''
  ElMessage.success('邮箱更新成功')
}

// 处理个人信息保存
const handleProfileSave = () => {
  // 这里可以添加表单验证和保存逻辑
  lastSaved.value = new Date().toLocaleString()
  ElMessage.success('个人信息保存成功')
}

// 处理安全操作
const handleSecurityAction = (action: string, subAction?: string) => {
  // 这里可以添加不同安全操作的处理逻辑
  ElMessage.info(`${action} ${subAction || '操作'}`)
}

// 处理双重认证开关
const handle2FASwitch = (value: boolean) => {
  // 这里可以添加双重认证开关的处理逻辑
  ElMessage.info(`双重认证已${value ? '开启' : '关闭'}`)
}

// 撤销会话
const revokeSession = (row: any) => {
  ElMessageBox.confirm('确定要撤销此会话吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里可以添加会话撤销逻辑
    ElMessage.success('会话已撤销')
  }).catch(() => {
    // 取消操作
  })
}

// 确认清除所有其他会话
const confirmClearSessions = () => {
  ElMessageBox.confirm('确定要清除所有其他会话吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里可以添加清除所有会话的逻辑
    ElMessage.success('所有其他会话已清除')
  }).catch(() => {
    // 取消操作
  })
}

// 处理令牌创建
const handleTokenCreation = () => {
  // 这里可以添加表单验证和令牌创建逻辑
  const newToken = {
    id: (tokens.value.length + 1).toString(),
    name: tokenCreationForm.tokenName,
    scopes: tokenCreationForm.tokenScopes.join(', '),
    createdAt: new Date().toLocaleString(),
    lastUsed: '从未使用',
    status: 'active'
  }
  tokens.value.unshift(newToken)
  // 显示令牌详情
  selectedToken.name = newToken.name
  selectedToken.value = 'cm_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  selectedToken.scopes = newToken.scopes
  selectedToken.createdAt = newToken.createdAt
  selectedToken.lastUsed = newToken.lastUsed
  tokenDetailVisible.value = true
  // 重置表单
  tokenCreationForm.tokenName = ''
  tokenCreationForm.tokenScopes = []
  tokenCreationForm.tokenExpiry = null
  ElMessage.success('令牌创建成功')
}

// 查看令牌详情
const viewTokenDetail = (token: any) => {
  selectedToken.name = token.name
  selectedToken.value = 'cm_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  selectedToken.scopes = token.scopes
  selectedToken.createdAt = token.createdAt
  selectedToken.lastUsed = token.lastUsed
  tokenDetailVisible.value = true
}

// 撤销令牌
const revokeToken = (token: any) => {
  ElMessageBox.confirm('确定要撤销此令牌吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里可以添加令牌撤销逻辑
    token.status = 'revoked'
    ElMessage.success('令牌已撤销')
  }).catch(() => {
    // 取消操作
  })
}

// 关闭模态框
const closeModal = (modalId: string) => {
  // 这里可以添加模态框关闭逻辑
}

// 显示通知
const showNotification = (type: string, title: string, message: string) => {
  ElMessage({
    type: type as any,
    message: message,
    title: title
  })
}
</script>

<style lang="scss" scoped>
.account-settings-container {
  .menu-item {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    border-radius: 4px;
    color: var(--el-text-color-secondary);
    transition: all 0.3s ease;
    cursor: pointer;
    margin-bottom: 4px;
    
    &:hover {
      background-color: var(--el-color-primary-light-9);
      color: var(--el-color-primary);
    }
    
    &.active-menu {
      background-color: var(--el-color-primary-light-9);
      color: var(--el-color-primary);
      font-weight: 500;
    }
  }
  
  .ant-card {
    border-radius: 8px;
    
    :deep(.el-card__header) {
      padding: 16px;
      border-bottom: 1px solid var(--el-border-color);
    }
    
    :deep(.el-card__body) {
      padding: 16px;
    }
  }
  
  .profile-form {
    :deep(.el-form-item) {
      margin-bottom: 16px;
    }
  }
  
  .token-creation-form {
    :deep(.el-form-item) {
      margin-bottom: 16px;
    }
  }
  
  .bg-primary-light {
    background-color: var(--el-color-primary-light-9);
  }
  
  .border-primary-30 {
    border-color: rgba(22, 119, 255, 0.3);
  }
  
  .text-primary {
    color: var(--el-color-primary);
  }
  
  .text-text-primary {
    color: var(--el-text-color-primary);
  }
  
  .text-text-secondary {
    color: var(--el-text-color-secondary);
  }
  
  .text-text-tertiary {
    color: var(--el-text-color-placeholder);
  }
  
  .border-border-color {
    border-color: var(--el-border-color);
  }
  
  .shadow-card {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.09);
  }
}
</style>