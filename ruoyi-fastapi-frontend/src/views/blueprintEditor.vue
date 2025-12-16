<template>
  <div class="font-inter bg-light text-text-primary p-0 m-0 flex flex-col h-screen">
    <!-- 顶部工具栏 -->
    <header class="bg-toolbar-bg border-b border-border-color shadow-toolbar flex items-center h-12 px-4 z-10">
      <div class="flex items-center space-x-1">
        <el-button type="text" icon="fas fa-save" class="toolbar-btn" title="保存蓝图">
        </el-button>
        <el-button type="text" icon="fas fa-download" class="toolbar-btn" title="导出蓝图">
        </el-button>
        <div class="h-6 border-r border-border-color mx-1">
        </div>
        <el-button type="text" icon="fas fa-undo" class="toolbar-btn" title="撤销">
        </el-button>
        <el-button type="text" icon="fas fa-redo" class="toolbar-btn" title="重做">
        </el-button>
        <div class="h-6 border-r border-border-color mx-1">
        </div>
        <el-button type="text" icon="fas fa-check-circle" class="toolbar-btn" title="验证蓝图">
        </el-button>
      </div>
      <div class="ml-6 flex items-center space-x-1">
        <div class="text-sm text-text-secondary mr-2">视图:</div>
        <el-button 
          :type="activeView === 'flow' ? 'primary' : 'text'" 
          plain 
          size="small" 
          :class="{ 'toolbar-btn-active': activeView === 'flow' }" 
          title="页面流视图"
          @click="switchView('flow')"
        >
          <i class="fas fa-project-diagram mr-1.5"></i>
          <span class="text-xs">页面流</span>
        </el-button>
        <el-button 
          :type="activeView === 'ui' ? 'primary' : 'text'" 
          plain 
          size="small" 
          :class="{ 'toolbar-btn-active': activeView === 'ui' }" 
          title="UI编排视图"
          @click="switchView('ui')"
        >
          <i class="fas fa-th-large mr-1.5"></i>
          <span class="text-xs">UI编排</span>
        </el-button>
        <el-button 
          :type="activeView === 'data' ? 'primary' : 'text'" 
          plain 
          size="small" 
          :class="{ 'toolbar-btn-active': activeView === 'data' }" 
          title="数据模型视图"
          @click="switchView('data')"
        >
          <i class="fas fa-database mr-1.5"></i>
          <span class="text-xs">数据模型</span>
        </el-button>
      </div>
      <div class="ml-auto flex items-center space-x-1">
        <el-button type="text" class="toolbar-btn" title="缩放">
          <i class="fas fa-search-minus mr-1"></i>
          <span class="text-xs">100%</span>
          <i class="fas fa-search-plus ml-1"></i>
        </el-button>
        <el-button type="text" icon="fas fa-th" class="toolbar-btn" title="网格">
        </el-button>
        <el-button type="text" icon="fas fa-align-left" class="toolbar-btn" title="对齐">
        </el-button>
        <div class="h-6 border-r border-border-color mx-1">
        </div>
        <el-button type="primary" size="small">
          <i class="fas fa-magic mr-1.5"></i>生成代码
        </el-button>
        <el-button type="secondary" size="small">
          <i class="fas fa-sliders-h mr-1.5"></i>高级选项
        </el-button>
      </div>
    </header>

    <!-- 主内容区域 -->
    <div class="flex flex-1 overflow-hidden">
      <!-- 左侧组件库 -->
      <aside class="w-64 bg-panel-bg border-r border-border-color flex flex-col h-full">
        <!-- 组件库标签页 -->
        <div class="flex border-b border-border-color">
          <button class="flex-1 py-3 text-sm font-medium text-primary border-b-2 border-primary">组件库</button>
          <button class="flex-1 py-3 text-sm font-medium text-text-tertiary">数据模型</button>
        </div>
        <!-- 组件搜索 -->
        <div class="px-3 py-2">
          <el-input
            placeholder="搜索组件..."
            size="small"
            prefix-icon="fas fa-search"
          />
        </div>
        <!-- 组件分类 -->
        <div class="overflow-y-auto flex-1 scrollbar-thin">
          <!-- 布局组件 -->
          <div class="mt-1">
            <div class="panel-title flex items-center justify-between">
              <span>布局组件</span>
              <i class="fas fa-chevron-down text-xs text-text-tertiary"></i>
            </div>
            <div class="p-2">
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-columns"></i>
                </div>
                <span class="text-sm">基础布局</span>
              </div>
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-th-large"></i>
                </div>
                <span class="text-sm">卡片布局</span>
              </div>
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-layer-group"></i>
                </div>
                <span class="text-sm">分栏布局</span>
              </div>
            </div>
          </div>
          <!-- 数据展示 -->
          <div class="mt-1">
            <div class="panel-title flex items-center justify-between">
              <span>数据展示</span>
              <i class="fas fa-chevron-down text-xs text-text-tertiary"></i>
            </div>
            <div class="p-2">
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-table"></i>
                </div>
                <span class="text-sm">高级表格</span>
              </div>
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-chart-bar"></i>
                </div>
                <span class="text-sm">图表卡片</span>
              </div>
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-list"></i>
                </div>
                <span class="text-sm">数据列表</span>
              </div>
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-user-circle"></i>
                </div>
                <span class="text-sm">详情卡片</span>
              </div>
            </div>
          </div>
          <!-- 表单组件 -->
          <div class="mt-1">
            <div class="panel-title flex items-center justify-between">
              <span>表单组件</span>
              <i class="fas fa-chevron-down text-xs text-text-tertiary"></i>
            </div>
            <div class="p-2">
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-search"></i>
                </div>
                <span class="text-sm">查询表单</span>
              </div>
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-edit"></i>
                </div>
                <span class="text-sm">基础表单</span>
              </div>
              <div class="draggable-item rounded-md p-2 mb-1.5 flex items-center">
                <div class="w-8 h-8 bg-primary-light rounded flex items-center justify-center text-primary mr-2.5">
                  <i class="fas fa-sort-numeric-up"></i>
                </div>
                <span class="text-sm">步骤表单</span>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- 中央画布区域 -->
      <main class="flex-1 bg-canvas-bg overflow-hidden relative flex flex-col">
        <!-- 页面流工具栏 -->
        <div class="bg-white border-b border-border-color px-4 py-2 flex items-center">
          <div class="text-sm text-text-secondary mr-3">页面流视图</div>
          <el-button type="text" size="small" class="text-xs text-primary">
            <i class="fas fa-plus-circle mr-1.5"></i>添加页面
          </el-button>
          <div class="ml-auto flex items-center space-x-3">
            <el-button type="text" size="small" class="text-xs text-text-secondary">
              <i class="fas fa-arrows-alt mr-1.5"></i>自动排列
            </el-button>
            <el-button type="text" size="small" class="text-xs text-text-secondary">
              <i class="fas fa-link mr-1.5"></i>添加连接
            </el-button>
          </div>
        </div>
        <!-- 画布容器 -->
        <div class="flex-1 overflow-auto relative">
          <div class="absolute inset-0 canvas-grid flex items-center justify-center" @click="clearSelection">
            <!-- 画布内容 -->
            <div class="relative w-[1200px] h-[800px]">
              <!-- 页面节点 -->
              <div 
                v-for="(node, index) in pageNodes" 
                :key="node.id"
                class="absolute w-48 bg-white rounded-lg shadow-md p-3 cursor-move"
                :style="{ left: `${node.x}px`, top: `${node.y}px` }"
                :class="{ 
                  'node-selected': node.selected, 
                  'border-2 border-primary': node.selected, 
                  'border border-border-color': !node.selected 
                }"
                @click="toggleNodeSelection(node.id)"
              >
                <div class="flex items-start justify-between mb-2">
                  <div class="flex items-center">
                    <i :class="node.icon + ' text-primary mr-2'"></i>
                    <span class="font-medium text-sm">{{ node.name }}</span>
                  </div>
                  <div class="text-xs text-text-tertiary">{{ node.path }}</div>
                </div>
                <div class="text-xs text-text-tertiary mb-2">{{ node.componentName }}</div>
                <div class="flex justify-end">
                  <div :class="`w-2 h-2 ${getNodeStatusClass(node.status)} rounded-full mr-1.5`"></div>
                  <span class="text-xs text-text-tertiary">{{ getNodeStatusText(node.status) }}</span>
                </div>
                <div v-if="node.id === 'home'" class="absolute -bottom-1.5 -right-1.5 w-4 h-4 bg-primary rounded-full text-white text-xs flex items-center justify-center">1</div>
                <div class="resize-handle"></div>
              </div>
              <!-- 连接线（使用SVG绘制） -->
              <svg class="absolute inset-0 w-full h-full pointer-events-none" xmlns="http://www.w3.org/2000/svg">
                <!-- 首页 -> 用户列表 -->
                <path d="M148,120 C198,120 250,120 250,120 L250,120" stroke="#ccc" stroke-width="1.5" fill="none" marker-end="url(#arrowhead)"></path>
                <!-- 用户列表 -> 用户详情 -->
                <path d="M348,120 C398,120 450,120 450,120 L450,120" stroke="#ccc" stroke-width="1.5" fill="none" marker-end="url(#arrowhead)"></path>
                <!-- 首页 -> 角色管理 -->
                <path d="M148,160 C198,160 250,180 250,180 L250,180" stroke="#ccc" stroke-width="1.5" fill="none" marker-end="url(#arrowhead)"></path>
                <!-- 箭头标记定义 -->
                <defs>
                  <marker id="arrowhead" markerwidth="10" markerheight="7" refx="9" refy="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#ccc"></polygon>
                  </marker>
                </defs>
              </svg>
            </div>
          </div>
        </div>
      </main>

      <!-- 右侧属性面板 -->
      <aside class="w-72 bg-panel-bg border-l border-border-color flex flex-col h-full">
        <!-- 选中状态提示 -->
        <div id="no-selection" class="hidden flex-1 flex items-center justify-center text-text-tertiary text-sm">未选择任何元素</div>
        <!-- 属性面板内容 -->
        <div id="property-panel">
          <!-- 页面信息 -->
          <div class="panel-title">页面属性</div>
          <div class="p-4 space-y-4">
            <div class="property-group">
              <label class="property-label">页面名称</label>
              <el-input v-model="selectedPage.name" size="small" placeholder="输入页面名称" />
            </div>
            <div class="property-group">
              <label class="property-label">路由路径</label>
              <el-input v-model="selectedPage.path" size="small" placeholder="输入路由路径" />
            </div>
            <div class="property-group">
              <label class="property-label">组件名称</label>
              <el-input v-model="selectedPage.componentName" size="small" placeholder="输入组件名称" />
            </div>
            <div class="property-group">
              <label class="property-label">页面图标</label>
              <el-input v-model="selectedPage.icon" size="small" placeholder="输入图标类名" />
            </div>
            <div class="property-group">
              <label class="property-label">页面状态</label>
              <el-select v-model="selectedPage.status" size="small">
                <el-option label="已生成" value="generated" />
                <el-option label="待优化" value="optimizing" />
                <el-option label="未生成" value="not-generated" />
              </el-select>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 选中的页面信息
interface PageInfo {
  name: string
  path: string
  componentName: string
  icon: string
  status: string
}

// 页面节点数据
interface PageNode {
  id: string
  name: string
  path: string
  componentName: string
  icon: string
  status: string
  x: number
  y: number
  selected: boolean
}

const selectedPage = reactive<PageInfo>({
  name: '首页',
  path: '/',
  componentName: 'Dashboard',
  icon: 'fas fa-home',
  status: 'generated'
})

// 页面节点列表
const pageNodes = ref<PageNode[]>([
  {
    id: 'home',
    name: '首页',
    path: '/',
    componentName: 'Dashboard',
    icon: 'fas fa-home',
    status: 'generated',
    x: 100,
    y: 100,
    selected: true
  },
  {
    id: 'userList',
    name: '用户列表',
    path: '/users',
    componentName: 'UserList',
    icon: 'fas fa-users',
    status: 'generated',
    x: 300,
    y: 80,
    selected: false
  },
  {
    id: 'userDetail',
    name: '用户详情',
    path: '/users/:id',
    componentName: 'UserDetail',
    icon: 'fas fa-user',
    status: 'optimizing',
    x: 500,
    y: 80,
    selected: false
  },
  {
    id: 'roleManagement',
    name: '角色管理',
    path: '/roles',
    componentName: 'RoleManagement',
    icon: 'fas fa-shield-alt',
    status: 'not-generated',
    x: 300,
    y: 220,
    selected: false
  }
])

// 是否显示属性面板
const showPropertyPanel = ref(true)

// 当前激活的视图
const activeView = ref('flow')

// 切换节点选择状态
const toggleNodeSelection = (nodeId: string) => {
  // 移除所有节点的选中状态
  pageNodes.value.forEach(node => {
    node.selected = false
  })
  
  // 选中当前节点
  const selectedNode = pageNodes.value.find(node => node.id === nodeId)
  if (selectedNode) {
    selectedNode.selected = true
    // 更新属性面板数据
    Object.assign(selectedPage, {
      name: selectedNode.name,
      path: selectedNode.path,
      componentName: selectedNode.componentName,
      icon: selectedNode.icon,
      status: selectedNode.status
    })
    showPropertyPanel.value = true
  }
}

// 取消所有节点选择
const clearSelection = () => {
  pageNodes.value.forEach(node => {
    node.selected = false
  })
  showPropertyPanel.value = false
}

// 切换视图
const switchView = (view: string) => {
  activeView.value = view
}

// 获取节点状态对应的类名
const getNodeStatusClass = (status: string) => {
  switch (status) {
    case 'generated':
      return 'bg-success'
    case 'optimizing':
      return 'bg-warning'
    case 'not-generated':
      return 'bg-danger'
    default:
      return 'bg-gray-400'
  }
}

// 获取节点状态对应的文本
const getNodeStatusText = (status: string) => {
  switch (status) {
    case 'generated':
      return '已生成'
    case 'optimizing':
      return '待优化'
    case 'not-generated':
      return '未生成'
    default:
      return '未知'
  }
}

// 组件挂载后初始化事件监听
onMounted(() => {
  // 这里可以添加更多初始化逻辑
})
</script>

<style scoped lang="scss">
/* 保持Tailwind CSS样式不变，仅添加必要的组件样式调整 */
.scrollbar-thin {
  scrollbar-width: thin;
  &::-webkit-scrollbar {
    width: 4px;
    height: 4px;
  }
  &::-webkit-scrollbar-thumb {
    background-color: rgba(156, 163, 175, 0.5);
    border-radius: 2px;
  }
}

.canvas-grid {
  background-size: 20px 20px;
  background-image: 
    linear-gradient(to right, rgba(232, 232, 232, 0.3) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(232, 232, 232, 0.3) 1px, transparent 1px);
}

.resize-handle {
  @apply absolute w-3 h-3 bg-primary rounded-full -bottom-1.5 -right-1.5 cursor-se-resize border-2 border-white shadow-sm;
}

.node-selected {
  @apply ring-2 ring-primary ring-offset-2;
}

.draggable-item {
  @apply cursor-move transition-all duration-200 hover:bg-primary-light/30;
}

.toolbar-btn {
  @apply p-2 rounded hover:bg-gray-200 transition-colors duration-200 flex items-center justify-center;
}

.toolbar-btn-active {
  @apply bg-primary-light text-primary;
}

.panel-title {
  @apply font-medium text-text-primary text-sm px-4 py-3 border-b border-border-color;
}

.property-group {
  @apply mb-4;
}

.property-label {
  @apply text-xs text-text-tertiary mb-1.5 block;
}
</style>