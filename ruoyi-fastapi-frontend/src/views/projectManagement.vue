<template>
  <div class="p-4 md:p-6">
    <!-- 页面标题和操作区 -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <div>
        <h1 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-text-primary mb-1">项目管理空间</h1>
        <p class="text-text-tertiary">管理和维护您的所有AI生成项目</p>
      </div>
      <div class="mt-4 md:mt-0 flex space-x-3">
        <el-button type="primary" :icon="Plus" class="flex items-center">
          <i class="fas fa-plus mr-2"></i>新建项目
        </el-button>
        <el-button type="default" :icon="Filter" class="flex items-center">
          <i class="fas fa-filter mr-2"></i>筛选
        </el-button>
      </div>
    </div>

    <!-- 项目列表视图和详情视图切换 -->
    <el-card class="bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] mb-6" shadow="hover">
      <el-tabs v-model="activeView" @tab-change="handleViewChange">
        <el-tab-pane label="项目列表" name="list-view">
          <template #label>
            <div class="flex items-center">
              <i class="fas fa-th-large mr-2"></i>
              <span>项目列表</span>
            </div>
          </template>
          <!-- 项目列表视图 -->
          <div class="p-5">
            <!-- 搜索框 -->
            <div class="relative mb-6">
              <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-text-tertiary"></i>
              <el-input
                v-model="searchQuery"
                placeholder="搜索项目名称、描述或技术栈..."
                class="w-full pl-10 pr-4 py-2 rounded-md border border-border-color focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all duration-200"
              />
            </div>
            <!-- 项目卡片网格 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
              <!-- 项目卡片 -->
              <el-card
                v-for="project in projects"
                :key="project.id"
                class="project-card relative bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1 cursor-pointer"
                @click="handleProjectClick(project)"
              >
                <div class="project-actions absolute top-2 right-2 opacity-0 transition-opacity duration-200 flex space-x-1">
                  <el-button
                    type="text"
                    size="small"
                    :icon="Share"
                    title="打开项目"
                    class="w-7 h-7 flex items-center justify-center rounded-full bg-white/80 text-text-secondary hover:bg-primary hover:text-white transition-all duration-200 shadow-sm"
                    @click.stop="handleOpenProject(project)"
                  />
                  <el-button
                    type="text"
                    size="small"
                    :icon="Setting"
                    title="项目设置"
                    class="w-7 h-7 flex items-center justify-center rounded-full bg-white/80 text-text-secondary hover:bg-primary hover:text-white transition-all duration-200 shadow-sm"
                    @click.stop="handleProjectSettings(project)"
                  />
                  <el-dropdown @command="(command) => handleProjectAction(project, command)">
                    <el-button
                      type="text"
                      size="small"
                      :icon="More"
                      title="更多选项"
                      class="w-7 h-7 flex items-center justify-center rounded-full bg-white/80 text-text-secondary hover:bg-primary hover:text-white transition-all duration-200 shadow-sm"
                    />
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="edit">编辑项目</el-dropdown-item>
                        <el-dropdown-item command="delete">删除项目</el-dropdown-item>
                        <el-dropdown-item command="share">分享项目</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
                <img :src="project.imageUrl" :alt="project.name" class="w-full h-40 object-cover">
                <div class="p-4">
                  <h3 class="font-semibold text-lg mb-1 line-clamp-1">{{ project.name }}</h3>
                  <p class="text-text-tertiary text-sm mb-3 line-clamp-2">{{ project.description }}</p>
                  <div class="flex flex-wrap mb-3">
                    <el-tag
                      v-for="tech in project.techStack"
                      :key="tech"
                      type="primary"
                      size="small"
                      class="bg-primary-light/30 text-primary text-xs px-2 py-1 rounded-full mr-1 mb-1"
                    >
                      {{ tech }}
                    </el-tag>
                  </div>
                  <div class="flex justify-between items-center text-xs text-text-tertiary">
                    <span><i class="far fa-clock mr-1"></i>{{ project.createDate }}</span>
                    <el-tag
                      :type="getStatusTagType(project.status)"
                      size="small"
                      class="bg-[var(--status-bg)] text-[var(--status-text)]"
                    >
                      {{ project.status }}
                    </el-tag>
                  </div>
                </div>
              </el-card>
              <!-- 项目卡片 - 新建项目占位符 -->
              <div
                class="border-2 border-dashed border-border-color rounded-lg flex flex-col items-center justify-center h-full p-6 hover:border-primary hover:text-primary transition-all duration-300 cursor-pointer"
                @click="handleCreateNewProject"
              >
                <div class="w-16 h-16 rounded-full bg-primary-light/30 flex items-center justify-center mb-4">
                  <i class="fas fa-plus text-2xl"></i>
                </div>
                <h3 class="font-medium text-lg mb-1">创建新项目</h3>
                <p class="text-text-tertiary text-sm text-center">使用AI生成全新的应用项目</p>
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="项目详情" name="detail-view">
          <template #label>
            <div class="flex items-center">
              <i class="fas fa-chart-line mr-2"></i>
              <span>项目详情</span>
            </div>
          </template>
          <!-- 项目详情视图 -->
          <div class="p-5">
            <!-- 项目头部信息 -->
            <div class="p-5 border-b border-border-color">
              <div class="flex flex-col md:flex-row md:items-center md:justify-between">
                <div>
                  <div class="flex items-center">
                    <h2 class="text-xl font-bold mr-3">用户管理系统</h2>
                    <el-tag type="success" size="small" class="bg-success/10 text-success">已部署</el-tag>
                  </div>
                  <p class="text-text-tertiary mt-1">完整的用户管理解决方案，包含权限控制和数据分析功能</p>
                </div>
                <div class="mt-4 md:mt-0 flex space-x-3">
                  <el-button type="default" :icon="Code" class="flex items-center">
                    <i class="fas fa-code mr-2"></i>生成新版本
                  </el-button>
                  <el-button type="primary" :icon="Share" class="flex items-center">
                    <i class="fas fa-external-link-alt mr-2"></i>打开项目
                  </el-button>
                </div>
              </div>
              <!-- 技术栈标签 -->
              <div class="mt-4 flex flex-wrap">
                <el-tag
                  v-for="tech in detailTechStack"
                  :key="tech"
                  type="primary"
                  size="small"
                  class="bg-primary-light/30 text-primary text-xs px-2 py-1 rounded-full mr-1 mb-1"
                >
                  {{ tech }}
                </el-tag>
              </div>
            </div>
            <!-- 项目详情标签页 -->
            <el-tabs v-model="activeDetailTab">
              <el-tab-pane label="概览" name="overview">
                <!-- 概览标签内容 -->
                <div class="p-5">
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
                    <el-card class="bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] p-5 transition-all duration-300 hover:shadow-lg">
                      <div class="flex items-center justify-between">
                        <div>
                          <p class="text-text-tertiary text-sm">生成次数</p>
                          <h3 class="text-2xl font-bold mt-1">12</h3>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-primary-light/30 flex items-center justify-center text-primary">
                          <i class="fas fa-magic text-xl"></i>
                        </div>
                      </div>
                      <div class="mt-4 text-xs text-success flex items-center">
                        <i class="fas fa-arrow-up mr-1"></i>较上月增长 20%
                      </div>
                    </el-card>
                    <el-card class="bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] p-5 transition-all duration-300 hover:shadow-lg">
                      <div class="flex items-center justify-between">
                        <div>
                          <p class="text-text-tertiary text-sm">代码行数</p>
                          <h3 class="text-2xl font-bold mt-1">15.8k</h3>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-primary-light/30 flex items-center justify-center text-primary">
                          <i class="fas fa-file-code text-xl"></i>
                        </div>
                      </div>
                      <div class="mt-4 text-xs text-success flex items-center">
                        <i class="fas fa-arrow-up mr-1"></i>较上次生成 8.5%
                      </div>
                    </el-card>
                    <el-card class="bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] p-5 transition-all duration-300 hover:shadow-lg">
                      <div class="flex items-center justify-between">
                        <div>
                          <p class="text-text-tertiary text-sm">质量评分</p>
                          <h3 class="text-2xl font-bold mt-1">96 <span class="text-base font-normal text-text-tertiary">/100</span></h3>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-primary-light/30 flex items-center justify-center text-primary">
                          <i class="fas fa-check-circle text-xl"></i>
                        </div>
                      </div>
                      <div class="mt-4 text-xs text-text-tertiary flex items-center">
                        <i class="fas fa-check mr-1"></i>优秀代码质量
                      </div>
                    </el-card>
                  </div>
                  <!-- 项目活动时间线 -->
                  <el-card class="bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] p-5 transition-all duration-300 hover:shadow-lg">
                    <h3 class="text-lg font-semibold mb-4">项目活动</h3>
                    <div class="space-y-5">
                      <div v-for="activity in projectActivities" :key="activity.id" class="flex">
                        <div
                          :class="`flex-shrink-0 w-8 h-8 rounded-full ${getActiviyBgColor(activity.type)} flex items-center justify-center ${getActiviyTextColor(activity.type)}`"
                        >
                          <i :class="getActiviyIcon(activity.type)"></i>
                        </div>
                        <div class="ml-4">
                          <div class="flex items-center">
                            <span class="font-medium">{{ activity.title }}</span>
                            <span class="text-text-tertiary text-sm ml-3">{{ activity.time }}</span>
                          </div>
                          <p class="text-text-secondary mt-1">{{ activity.description }}</p>
                        </div>
                      </div>
                    </div>
                  </el-card>
                </div>
              </el-tab-pane>
              <el-tab-pane label="代码仓库" name="code-repo" />
              <el-tab-pane label="蓝图历史" name="blueprint-history" />
              <el-tab-pane label="环境部署" name="environment" />
              <el-tab-pane label="文档API" name="docs" />
              <el-tab-pane label="成员管理" name="members" />
            </el-tabs>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus,
  Filter,
  Share,
  Setting,
  More,
  Code
} from '@element-plus/icons-vue'

// 定义数据类型
interface Project {
  id: number
  name: string
  description: string
  imageUrl: string
  techStack: string[]
  createDate: string
  status: string
}

interface Activity {
  id: number
  type: 'deploy' | 'code' | 'edit' | 'create'
  title: string
  time: string
  description: string
}

// 初始化路由
const router = useRouter()

// 响应式数据
const activeView = ref('list-view')
const activeDetailTab = ref('overview')
const searchQuery = ref('')

// 项目数据
const projects: Project[] = [
  {
    id: 1,
    name: '用户管理系统',
    description: '完整的用户管理解决方案，包含权限控制和数据分析功能',
    imageUrl: '/projectManagement/0f8d61df5c7b5450e65d5f067c391d2a.png',
    techStack: ['Vue3', 'Ant Design Vue', 'NestJS'],
    createDate: '2023-11-15',
    status: '已部署'
  },
  {
    id: 2,
    name: '电商管理平台',
    description: '商品管理、订单处理和客户分析的一体化电商解决方案',
    imageUrl: '/projectManagement/b00c5e3bd796d6927740e195b862b5db.png',
    techStack: ['React', 'Ant Design Pro', 'Node.js'],
    createDate: '2023-11-10',
    status: '开发中'
  },
  {
    id: 3,
    name: '数据分析仪表盘',
    description: '多维度数据可视化分析工具，支持自定义报表生成',
    imageUrl: '/projectManagement/d0749de2275fdbd9af68a185ef725fa8.png',
    techStack: ['React', 'ECharts', 'Express'],
    createDate: '2023-11-05',
    status: '已部署'
  },
  {
    id: 4,
    name: '任务管理系统',
    description: '基于看板的团队协作工具，支持任务分配和进度跟踪',
    imageUrl: '/projectManagement/83a70c23df7ce2fc97cd973c12a4acfb.png',
    techStack: ['Vue3', 'Element Plus', 'NestJS'],
    createDate: '2023-10-28',
    status: '需优化'
  }
]

// 详情页技术栈
const detailTechStack = ['Vue3', 'Ant Design Vue', 'NestJS', 'MySQL', 'JWT认证']

// 项目活动数据
const projectActivities: Activity[] = [
  {
    id: 1,
    type: 'deploy',
    title: '部署到生产环境',
    time: '今天 14:30',
    description: '版本 v1.2.0 已成功部署到生产环境'
  },
  {
    id: 2,
    type: 'code',
    title: '代码生成完成',
    time: '昨天 09:15',
    description: '根据最新蓝图生成了前端和后端代码'
  },
  {
    id: 3,
    type: 'edit',
    title: '更新项目蓝图',
    time: '2023-11-14',
    description: '修改了用户数据模型，添加了新的角色字段'
  },
  {
    id: 4,
    type: 'create',
    title: '项目创建',
    time: '2023-11-01',
    description: '通过AI生成创建了新项目'
  }
]

// 处理视图切换
const handleViewChange = () => {
  // 可以添加视图切换时的逻辑
}

// 获取状态标签类型
const getStatusTagType = (status: string): string => {
  switch (status) {
    case '已部署':
      return 'success'
    case '开发中':
      return 'warning'
    case '需优化':
      return 'danger'
    default:
      return 'info'
  }
}

// 处理项目点击
const handleProjectClick = (project: Project) => {
  // 点击项目卡片，显示项目详情
  console.log('点击项目:', project)
}

// 处理打开项目
const handleOpenProject = (project: Project) => {
  console.log('打开项目:', project)
}

// 处理项目设置
const handleProjectSettings = (project: Project) => {
  console.log('项目设置:', project)
}

// 处理项目操作
const handleProjectAction = (project: Project, command: string) => {
  console.log('项目操作:', command, '项目:', project)
  switch (command) {
    case 'edit':
      // 处理编辑项目
      break
    case 'delete':
      // 处理删除项目
      break
    case 'share':
      // 处理分享项目
      break
  }
}

// 处理创建新项目
const handleCreateNewProject = () => {
  // 跳转到生成向导
  router.push('/generationWizard')
}

// 获取活动背景颜色
const getActiviyBgColor = (type: string): string => {
  switch (type) {
    case 'deploy':
      return 'bg-success/10'
    case 'code':
      return 'bg-primary/10'
    case 'edit':
      return 'bg-warning/10'
    case 'create':
      return 'bg-info/10'
    default:
      return 'bg-primary/10'
  }
}

// 获取活动文本颜色
const getActiviyTextColor = (type: string): string => {
  switch (type) {
    case 'deploy':
      return 'text-success'
    case 'code':
      return 'text-primary'
    case 'edit':
      return 'text-warning'
    case 'create':
      return 'text-info'
    default:
      return 'text-primary'
  }
}

// 获取活动图标
const getActiviyIcon = (type: string): string => {
  switch (type) {
    case 'deploy':
      return 'fas fa-cloud-upload-alt'
    case 'code':
      return 'fas fa-code'
    case 'edit':
      return 'fas fa-edit'
    case 'create':
      return 'fas fa-plus-circle'
    default:
      return 'fas fa-info-circle'
  }
}
</script>

<style scoped lang="scss">
.project-card:hover .project-actions {
  opacity: 1;
}

// 自定义状态标签颜色
:deep(.el-tag) {
  --status-bg: transparent;
  --status-text: currentColor;
  
  &.el-tag--success {
    --status-bg: #52c41a20;
    --status-text: #52c41a;
  }
  
  &.el-tag--warning {
    --status-bg: #faad1420;
    --status-text: #faad14;
  }
  
  &.el-tag--danger {
    --status-bg: #ff4d4f20;
    --status-text: #ff4d4f;
  }
  
  &.el-tag--info {
    --status-bg: #1890ff20;
    --status-text: #1890ff;
  }
}
</style>