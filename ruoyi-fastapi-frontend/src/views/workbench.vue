<template>
  <div class="p-4 md:p-6">
    <!-- 欢迎区 -->
    <div class="mb-6">
      <h1 class="text-[clamp(1.5rem,3vw,2.5rem)] font-bold text-text-primary mb-2">欢迎回来，张开发</h1>
      <p class="text-text-secondary">今天是 <span id="current-date">{{ currentDate }}</span>，这是您的工作台概览</p>
    </div>

    <!-- 数据卡片区域 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
      <el-card
        v-for="card in dataCards"
        :key="card.title"
        class="bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] p-5 mb-5 transition-all duration-300 hover:shadow-lg"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-text-tertiary text-sm mb-1">{{ card.title }}</p>
            <h3 class="text-2xl font-bold">{{ card.value }}</h3>
          </div>
          <div
            :class="`w-12 h-12 rounded-full ${card.bgColor} flex items-center justify-center ${card.textColor}`"
          >
            <i :class="`fas ${card.icon} text-xl`"></i>
          </div>
        </div>
        <div v-if="card.change" class="mt-4 flex items-center" :class="card.changeColor">
          <i :class="`fas ${card.change.includes('下降') ? 'fa-arrow-down' : 'fa-arrow-up'} mr-1`"></i>
          <span>{{ card.change }}</span>
        </div>
        <div v-else-if="card.total" class="mt-4 flex items-center text-text-tertiary text-sm">
          <span>{{ card.total }}</span>
        </div>
      </el-card>
    </div>

    <!-- 快速开始卡片 -->
    <el-card
      class="bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] p-5 mb-5 transition-all duration-300 hover:shadow-lg mb-6"
    >
      <div class="flex flex-col md:flex-row items-center justify-between">
        <div class="mb-4 md:mb-0 md:mr-6 text-center md:text-left">
          <h2 class="text-xl font-bold mb-2">开始您的智能开发之旅</h2>
          <p class="text-text-secondary max-w-md text-balance">用自然语言描述，生成完整应用。AI将自动理解您的需求并生成高质量代码。</p>
        </div>
        <el-button
          type="primary"
          size="large"
          :icon="'Plus'"
          @click="navigateToGenerationWizard"
          class="px-8 py-6 text-lg"
        >
          开始生成
        </el-button>
      </div>
    </el-card>

    <!-- 最近项目列表 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2">
        <el-card
          class="bg-white rounded-lg shadow-[0_2px_8px_rgba(0,0,0,0.09)] p-5 mb-5 transition-all duration-300 hover:shadow-lg"
        >
          <div class="flex items-center justify-between mb-5">
            <h2 class="text-lg font-bold">最近项目</h2>
            <el-link type="primary" @click="navigateToProjectManagement" class="flex items-center">
              查看全部 <i class="fas fa-angle-right ml-1"></i>
            </el-link>
          </div>
          <el-table
            :data="recentProjects"
            stripe
            style="width: 100%"
            @row-click="handleRowClick"
          >
            <el-table-column prop="name" label="项目名称" min-width="180">
              <template #default="scope">
                <div class="flex items-center">
                  <div
                    :class="`w-8 h-8 rounded ${scope.row.iconBg} flex items-center justify-center ${scope.row.iconColor} mr-3`"
                  >
                    <i :class="`fas ${scope.row.icon}`"></i>
                  </div>
                  <span>{{ scope.row.name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="lastModified" label="最后修改" min-width="120" />
            <el-table-column prop="techStack" label="技术栈" min-width="150">
              <template #default="scope">
                <div class="flex flex-wrap gap-1">
                  <el-tag
                    v-for="tech in scope.row.techStack"
                    :key="tech.name"
                    :type="tech.type"
                    size="small"
                    class="text-xs"
                  >
                    {{ tech.name }}
                  </el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="100">
              <template #default="scope">
                <el-tag :type="scope.row.statusType" size="small" class="text-xs">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" min-width="100" fixed="right">
              <template #default="scope">
                <el-button
                  type="text"
                  size="small"
                  :icon="'Edit'"
                  @click.stop="handleEditProject(scope.row)"
                >
                </el-button>
                <el-dropdown @command="handleDropdownCommand(scope.row)">
                  <el-button type="text" size="small" :icon="'More'">
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="copy">复制项目</el-dropdown-item>
                      <el-dropdown-item command="export">导出代码</el-dropdown-item>
                      <el-dropdown-item command="delete" type="danger">删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 定义数据类型
interface DataCard {
  title: string
  value: string | number
  icon: string
  bgColor: string
  textColor: string
  change?: string
  changeColor?: string
  total?: string
}

interface TechStack {
  name: string
  type: string
}

interface RecentProject {
  id: number
  name: string
  lastModified: string
  techStack: TechStack[]
  status: string
  statusType: string
  icon: string
  iconBg: string
  iconColor: string
}

// 初始化路由
const router = useRouter()

// 当前日期
const currentDate = ref('')

// 数据卡片数据
const dataCards: DataCard[] = [
  {
    title: '我的项目数',
    value: 12,
    icon: 'fa-folder-open',
    bgColor: 'bg-primary-light',
    textColor: 'text-primary',
    change: '2 个项目 (本月新增)',
    changeColor: 'text-success text-sm'
  },
  {
    title: '今日生成次数',
    value: 5,
    icon: 'fa-magic',
    bgColor: 'bg-secondary/10',
    textColor: 'text-secondary',
    total: '本月累计: 32 次'
  },
  {
    title: '团队活跃度',
    value: '87%',
    icon: 'fa-users',
    bgColor: 'bg-success/10',
    textColor: 'text-success',
    change: '较上周提升 12%',
    changeColor: 'text-success text-sm'
  },
  {
    title: '代码质量评分',
    value: 92,
    icon: 'fa-code',
    bgColor: 'bg-warning/10',
    textColor: 'text-warning',
    change: '较上次下降 3 分',
    changeColor: 'text-danger text-sm'
  }
]

// 最近项目数据
const recentProjects: RecentProject[] = [
  {
    id: 1,
    name: '电商管理系统',
    lastModified: '今天 14:30',
    techStack: [
      { name: 'Vue3', type: 'primary' },
      { name: 'NestJS', type: 'info' }
    ],
    status: '生成成功',
    statusType: 'success',
    icon: 'fa-shopping-cart',
    iconBg: 'bg-primary/10',
    iconColor: 'text-primary'
  },
  {
    id: 2,
    name: '用户管理系统',
    lastModified: '昨天 09:15',
    techStack: [
      { name: 'React', type: 'primary' },
      { name: 'Spring Boot', type: 'info' }
    ],
    status: '需审查',
    statusType: 'warning',
    icon: 'fa-user',
    iconBg: 'bg-secondary/10',
    iconColor: 'text-secondary'
  },
  {
    id: 3,
    name: '数据分析平台',
    lastModified: '2023-06-18 16:45',
    techStack: [
      { name: 'React', type: 'primary' },
      { name: 'Node.js', type: 'danger' }
    ],
    status: '开发中',
    statusType: 'primary',
    icon: 'fa-chart-line',
    iconBg: 'bg-warning/10',
    iconColor: 'text-warning'
  },
  {
    id: 4,
    name: '任务管理系统',
    lastModified: '2023-06-15 10:20',
    techStack: [
      { name: 'Vue3', type: 'primary' },
      { name: 'NestJS', type: 'info' }
    ],
    status: '已部署',
    statusType: 'info',
    icon: 'fa-tasks',
    iconBg: 'bg-danger/10',
    iconColor: 'text-danger'
  }
]

// 设置当前日期
const setCurrentDate = () => {
  const now = new Date()
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  }
  currentDate.value = now.toLocaleDateString('zh-CN', options)
}

// 导航到生成向导
const navigateToGenerationWizard = () => {
  router.push('/generationWizard')
}

// 导航到项目管理
const navigateToProjectManagement = () => {
  router.push('/project/projectManagement')
}

// 处理行点击
const handleRowClick = (project: RecentProject) => {
  console.log('点击项目:', project)
  // 可以跳转到项目详情页
}

// 处理编辑项目
const handleEditProject = (project: RecentProject) => {
  console.log('编辑项目:', project)
  // 可以跳转到项目编辑页
}

// 处理下拉菜单命令
const handleDropdownCommand = (project: RecentProject, command: string) => {
  console.log('下拉菜单命令:', command, '项目:', project)
  switch (command) {
    case 'copy':
      // 处理复制项目
      break
    case 'export':
      // 处理导出代码
      break
    case 'delete':
      // 处理删除项目
      break
  }
}

// 生命周期钩子
onMounted(() => {
  setCurrentDate()
})
</script>

<style scoped lang="scss">
/* 这里可以添加需要的组件级样式 */
</style>