<template>
  <div class="max-w-7xl mx-auto">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-text-primary">团队协作空间</h1>
      <p class="text-text-tertiary mt-1">管理团队成员、项目和权限</p>
    </div>
    
    <!-- 主标签页导航 -->
    <el-tabs v-model="activeTab" class="mb-6">
      <el-tab-pane label="团队首页" name="team-home">
        <!-- 团队信息卡片 -->
        <el-card class="mb-6 bg-white rounded-lg shadow-card p-5 transition-all duration-300 hover:shadow-lg">
          <div class="flex flex-col md:flex-row md:items-center justify-between">
            <div class="flex items-center mb-4 md:mb-0">
              <div class="w-16 h-16 rounded-full bg-primary-light flex items-center justify-center mr-4">
                <i class="fas fa-users text-primary text-2xl"></i>
              </div>
              <div>
                <h2 class="text-xl font-bold">前端开发精英团队</h2>
                <p class="text-text-tertiary">创建于 2023-05-15 · 5 名成员</p>
              </div>
            </div>
            <div class="flex space-x-3">
              <el-button class="btn btn-outline">
                <i class="fas fa-user-plus mr-2"></i>邀请成员
              </el-button>
              <el-button type="primary" class="btn btn-primary">
                <i class="fas fa-cog mr-2"></i>团队设置
              </el-button>
            </div>
          </div>
          <div class="mt-5 pt-5 border-t border-border-color">
            <h3 class="text-lg font-semibold mb-3">团队描述</h3>
            <p class="text-text-secondary">专注于企业级前端应用开发的精英团队，致力于打造高质量、高性能的用户界面和交互体验。我们使用现代化的前端技术栈，包括React、Vue和Angular等主流框架，为客户提供卓越的Web应用解决方案。</p>
          </div>
        </el-card>
        
        <!-- 团队成员列表 -->
        <el-card class="mb-6 bg-white rounded-lg shadow-card p-5 transition-all duration-300 hover:shadow-lg">
          <div class="flex justify-between items-center mb-5">
            <h2 class="text-lg font-semibold">团队成员</h2>
            <el-button type="primary" plain class="btn btn-outline btn-sm">
              <i class="fas fa-user-plus mr-1"></i>添加成员
            </el-button>
          </div>
          <div class="overflow-x-auto">
            <el-table :data="teamMembers" class="ant-table">
              <el-table-column prop="name" label="成员" width="200">
                <template #default="scope">
                  <div class="flex items-center">
                    <el-avatar :src="scope.row.avatar" class="w-10 h-10 rounded-full mr-3 object-cover"></el-avatar>
                    <div>
                      <div class="font-medium">{{ scope.row.name }}</div>
                      <div class="text-sm text-text-tertiary">{{ scope.row.email }}</div>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="role" label="角色" width="120">
                <template #default="scope">
                  <span :class="getRoleBadgeClass(scope.row.role)">{{ scope.row.role }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="joinDate" label="加入时间" width="140"></el-table-column>
              <el-table-column prop="lastActive" label="最近活跃" width="140"></el-table-column>
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="scope">
                  <div class="flex space-x-2">
                    <el-button type="text" class="text-text-secondary hover:text-primary" title="编辑成员">
                      <i class="fas fa-edit"></i>
                    </el-button>
                    <el-button 
                      type="text" 
                      class="text-text-secondary hover:text-danger" 
                      :disabled="scope.row.role === '管理员'" 
                      title="移除成员"
                    >
                      <i class="fas fa-trash-alt"></i>
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
        
        <!-- 团队项目集 -->
        <el-card class="bg-white rounded-lg shadow-card p-5 transition-all duration-300 hover:shadow-lg">
          <div class="flex justify-between items-center mb-5">
            <h2 class="text-lg font-semibold">团队项目</h2>
            <el-button type="primary" class="btn btn-primary">
              <i class="fas fa-plus mr-2"></i>新建项目
            </el-button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            <el-card 
              v-for="(project, index) in teamProjects" 
              :key="index"
              class="bg-white rounded-lg shadow-card p-4 border border-border-color hover:shadow-lg transition-all duration-300"
              shadow="hover"
            >
              <div class="flex justify-between items-start mb-3">
                <h3 class="font-semibold">{{ project.name }}</h3>
                <el-dropdown>
                  <el-button type="text" class="text-text-tertiary hover:text-primary">
                    <i class="fas fa-ellipsis-v"></i>
                  </el-button>
                </el-dropdown>
              </div>
              <div class="flex flex-wrap gap-2 mb-4">
                <span 
                  v-for="(tech, techIndex) in [...project.techStack, project.status]" 
                  :key="techIndex"
                  :class="getTechBadgeClass(tech)"
                >
                  {{ tech }}
                </span>
              </div>
              <p class="text-sm text-text-tertiary mb-4 line-clamp-2">{{ project.description }}</p>
              <div class="flex justify-between items-center pt-3 border-t border-border-color">
                <div class="text-sm text-text-tertiary">
                  <i class="fas fa-clock mr-1"></i>更新于 {{ project.updateDate }}
                </div>
                <el-button type="text" class="text-primary hover:text-primary-dark text-sm font-medium">
                  查看详情 <i class="fas fa-chevron-right ml-1 text-xs"></i>
                </el-button>
              </div>
            </el-card>
            <!-- 创建新项目卡片 -->
            <el-card 
              class="bg-white rounded-lg shadow-card p-4 border border-border-color hover:shadow-lg transition-all duration-300 flex items-center justify-center h-48 border-dashed cursor-pointer hover:border-primary hover:text-primary"
              shadow="hover"
            >
              <div class="text-center">
                <i class="fas fa-plus-circle text-3xl mb-2"></i>
                <div class="font-medium">创建新项目</div>
              </div>
            </el-card>
          </div>
        </el-card>
      </el-tab-pane>
      
      <!-- 团队设置标签页 -->
      <el-tab-pane label="团队设置" name="team-settings">
        <!-- 设置子标签页导航 -->
        <el-tabs v-model="currentSubtab" class="mb-6 border-b border-border-color">
          <el-tab-pane label="成员与权限" name="member-permissions">
            <el-card class="bg-white rounded-lg shadow-card p-5 transition-all duration-300 hover:shadow-lg">
              <h2 class="text-lg font-semibold mb-5">成员权限管理</h2>
              <p class="text-text-secondary mb-6">配置团队成员对各个项目的访问权限，精细化管理团队资源和数据安全。</p>
              <div class="overflow-x-auto">
                <table class="ant-table">
                  <thead>
                    <tr>
                      <th class="w-48">成员</th>
                      <th v-for="project in permissionProjects" :key="project.id" :class="project.name">{{ project.name }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(member, index) in permissionMembers" :key="index">
                      <td class="flex items-center">
                        <el-avatar :src="member.avatar" class="w-10 h-10 rounded-full mr-3 object-cover"></el-avatar>
                        <div>
                          <div class="font-medium">{{ member.name }}</div>
                          <div class="text-sm text-text-tertiary">{{ member.role }}</div>
                        </div>
                      </td>
                      <td v-for="project in permissionProjects" :key="project.id">
                        <div 
                          v-for="permission in member.permissions" 
                          :key="permission.id"
                          :class="['permission-cell', { 'permission-cell-active': permission.active }]"
                        >
                          {{ permission.name }}
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </el-card>
          </el-tab-pane>
          
          <el-tab-pane label="团队信息" name="team-info">
            <el-card class="bg-white rounded-lg shadow-card p-5 transition-all duration-300 hover:shadow-lg">
              <h2 class="text-lg font-semibold mb-5">团队信息</h2>
              <el-form label-position="top" :model="teamInfo">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="团队名称" class="form-label">
                      <el-input v-model="teamInfo.name" class="form-control"></el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="团队ID" class="form-label">
                      <el-input v-model="teamInfo.id" disabled class="form-control"></el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="创建时间" class="form-label">
                      <el-input v-model="teamInfo.createdAt" disabled class="form-control"></el-input>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item label="团队描述" class="form-label">
                  <el-input v-model="teamInfo.description" type="textarea" rows="4" class="form-control"></el-input>
                </el-form-item>
                <div class="flex justify-end mt-4">
                  <el-button type="primary" class="btn btn-primary mr-2">保存修改</el-button>
                  <el-button class="btn btn-outline">取消</el-button>
                </div>
              </el-form>
            </el-card>
          </el-tab-pane>
          
          <el-tab-pane label="安全设置" name="security-settings">
            <el-card class="bg-white rounded-lg shadow-card p-5 transition-all duration-300 hover:shadow-lg">
              <h2 class="text-lg font-semibold mb-5">安全设置</h2>
              <el-form label-position="top" :model="securitySettings">
                <el-form-item label="密码策略" class="form-label">
                  <div class="space-y-3">
                    <el-checkbox v-model="securitySettings.passwordPolicy.requireUppercase">要求大写字母</el-checkbox>
                    <el-checkbox v-model="securitySettings.passwordPolicy.requireLowercase">要求小写字母</el-checkbox>
                    <el-checkbox v-model="securitySettings.passwordPolicy.requireNumber">要求数字</el-checkbox>
                    <el-checkbox v-model="securitySettings.passwordPolicy.requireSpecialChar">要求特殊字符</el-checkbox>
                    <el-slider v-model="securitySettings.passwordPolicy.minLength" :min="6" :max="20" show-input></el-slider>
                  </div>
                </el-form-item>
                <el-form-item label="会话管理" class="form-label">
                  <el-switch v-model="securitySettings.sessionManagement.autoLogout"></el-switch>
                  <span class="ml-2">自动登出（{{ securitySettings.sessionManagement.timeout }}分钟）</span>
                </el-form-item>
                <div class="flex justify-end mt-4">
                  <el-button type="primary" class="btn btn-primary mr-2">保存设置</el-button>
                  <el-button class="btn btn-outline">重置</el-button>
                </div>
              </el-form>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

// TypeScript接口定义
interface TeamMember {
  name: string;
  email: string;
  avatar: string;
  role: string;
  joinDate: string;
  lastActive: string;
}

interface TeamProject {
  name: string;
  techStack: string[];
  status: string;
  description: string;
  updateDate: string;
}

interface Permission {
  id: number;
  name: string;
  active: boolean;
}

interface PermissionMember {
  name: string;
  avatar: string;
  role: string;
  permissions: Permission[];
}

interface PermissionProject {
  id: number;
  name: string;
}

interface TeamInfo {
  name: string;
  id: string;
  createdAt: string;
  description: string;
}

interface SecuritySettings {
  passwordPolicy: {
    requireUppercase: boolean;
    requireLowercase: boolean;
    requireNumber: boolean;
    requireSpecialChar: boolean;
    minLength: number;
  };
  sessionManagement: {
    autoLogout: boolean;
    timeout: number;
  };
}

// 响应式状态
const activeTab = ref('team-home');
const currentSubtab = ref('member-permissions');

// 团队成员数据
const teamMembers = reactive<TeamMember[]>([
  {
    name: '张开发',
    email: 'zhang@example.com',
    avatar: './teamCollaboration/7e2bbbd0c77d50fb9748b5819f4215af.png',
    role: '管理员',
    joinDate: '2023-05-15',
    lastActive: '今天 14:30'
  },
  {
    name: '李架构',
    email: 'li@example.com',
    avatar: './teamCollaboration/3ed675b7a93073049b13613988e20a8b.png',
    role: '高级开发者',
    joinDate: '2023-06-02',
    lastActive: '昨天 09:15'
  },
  {
    name: '王前端',
    email: 'wang@example.com',
    avatar: './teamCollaboration/75ca9e0303cc796eea6725e9967347e8.png',
    role: '高级开发者',
    joinDate: '2023-06-10',
    lastActive: '今天 10:45'
  },
  {
    name: '赵设计',
    email: 'zhao@example.com',
    avatar: './teamCollaboration/242e0d41b3dfc9bccfc4e2914722543a.png',
    role: '开发者',
    joinDate: '2023-07-05',
    lastActive: '昨天 16:20'
  },
  {
    name: '陈测试',
    email: 'chen@example.com',
    avatar: './teamCollaboration/0d20b09370a130f1edbe373bdf8e9d66.png',
    role: '观察者',
    joinDate: '2023-08-12',
    lastActive: '3天前'
  }
]);

// 团队项目数据
const teamProjects = reactive<TeamProject[]>([
  {
    name: '企业资源管理系统',
    techStack: ['React', 'Ant Design Pro'],
    status: '进行中',
    description: '企业级资源管理平台，包含人力资源、财务、项目管理等核心模块，为企业提供全方位的资源监控和管理解决方案。',
    updateDate: '2023-09-15'
  },
  {
    name: '客户关系管理系统',
    techStack: ['Vue 3', 'Element Plus'],
    status: '进行中',
    description: '全面的客户关系管理解决方案，帮助企业有效管理客户信息、跟进销售机会、提升客户满意度和忠诚度。',
    updateDate: '2023-09-10'
  },
  {
    name: '数据分析仪表盘',
    techStack: ['Vue 3', 'ECharts', 'TypeScript'],
    status: '已完成',
    description: '高性能数据可视化仪表盘，支持多种图表类型和数据筛选，为决策者提供直观的数据洞察和分析工具。',
    updateDate: '2023-08-20'
  },
  {
    name: '智能办公平台',
    techStack: ['React', 'Material UI'],
    status: '暂停中',
    description: '集成协作、文档、任务管理的一站式办公平台，提升团队协作效率和工作体验。',
    updateDate: '2023-07-30'
  },
  {
    name: '电商管理后台',
    techStack: ['Vue 3', 'Vant'],
    status: '进行中',
    description: '全功能电商管理系统，包含商品管理、订单处理、会员管理、营销活动等核心功能模块。',
    updateDate: '2023-09-12'
  }
]);

// 权限管理数据
const permissionMembers = reactive<PermissionMember[]>([
  {
    name: '张开发',
    avatar: './teamCollaboration/7e2bbbd0c77d50fb9748b5819f4215af.png',
    role: '管理员',
    permissions: [
      { id: 1, name: '查看', active: true },
      { id: 2, name: '编辑', active: true },
      { id: 3, name: '删除', active: true },
      { id: 4, name: '管理', active: true }
    ]
  },
  {
    name: '李架构',
    avatar: './teamCollaboration/3ed675b7a93073049b13613988e20a8b.png',
    role: '高级开发者',
    permissions: [
      { id: 1, name: '查看', active: true },
      { id: 2, name: '编辑', active: true },
      { id: 3, name: '删除', active: true },
      { id: 4, name: '管理', active: false }
    ]
  },
  {
    name: '王前端',
    avatar: './teamCollaboration/75ca9e0303cc796eea6725e9967347e8.png',
    role: '高级开发者',
    permissions: [
      { id: 1, name: '查看', active: true },
      { id: 2, name: '编辑', active: true },
      { id: 3, name: '删除', active: false },
      { id: 4, name: '管理', active: false }
    ]
  }
]);

const permissionProjects = reactive<PermissionProject[]>([
  { id: 1, name: '企业资源管理系统' },
  { id: 2, name: '客户关系管理系统' },
  { id: 3, name: '数据分析仪表盘' }
]);

// 团队信息
const teamInfo = reactive<TeamInfo>({
  name: '前端开发精英团队',
  id: 'team-2023-0515',
  createdAt: '2023-05-15',
  description: '专注于企业级前端应用开发的精英团队，致力于打造高质量、高性能的用户界面和交互体验。'
});

// 安全设置
const securitySettings = reactive<SecuritySettings>({
  passwordPolicy: {
    requireUppercase: true,
    requireLowercase: true,
    requireNumber: true,
    requireSpecialChar: false,
    minLength: 8
  },
  sessionManagement: {
    autoLogout: true,
    timeout: 30
  }
});

// 辅助函数
const getRoleBadgeClass = (role: string) => {
  const baseClass = 'badge';
  switch (role) {
    case '管理员':
      return `${baseClass} badge-primary`;
    case '高级开发者':
      return `${baseClass} badge-success`;
    case '开发者':
      return `${baseClass} badge-warning`;
    case '观察者':
      return `${baseClass} badge-danger`;
    default:
      return `${baseClass} badge-primary`;
  }
};

const getTechBadgeClass = (tech: string) => {
  const baseClass = 'badge';
  if (tech === '进行中') return `${baseClass} badge-success`;
  if (tech === '已完成') return `${baseClass} badge-primary`;
  if (tech === '暂停中') return `${baseClass} badge-warning`;
  return `${baseClass} badge-primary`;
};
</script>

<style scoped lang="scss">
// 保留并使用Tailwind CSS类
/* 自定义工具类 */
.permission-cell {
  @apply py-2 px-3 rounded border border-border-color cursor-pointer hover:bg-primary-light/30 transition-all-300;
}

.permission-cell-active {
  @apply bg-primary-light text-primary border-primary;
}

// 导入全局样式
@import '../../assets/styles/index.scss';
</style>