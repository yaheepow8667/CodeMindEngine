<template>
  <div id="template-market" class="min-h-full">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-text-primary">模板市场</h1>
      <p class="text-text-tertiary mt-1">探索高质量的应用模板，加速您的开发流程</p>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="p-6 mb-8 bg-white rounded-lg shadow-card transition-all duration-300 hover:shadow-lg">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- 搜索框 -->
        <div class="relative flex-1">
          <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-text-tertiary"></i>
          <el-input 
            v-model="searchQuery" 
            placeholder="搜索模板、技术栈或分类..." 
            class="search-input pl-10"
          ></el-input>
        </div>
        <!-- 筛选选项 -->
        <div class="flex flex-wrap gap-3">
          <!-- 分类筛选 -->
          <el-dropdown>
            <el-button type="primary" plain class="btn btn-outline flex items-center">
              <i class="fas fa-th-large mr-2"></i>
              <span>分类</span>
              <i class="fas fa-chevron-down ml-2 text-xs"></i>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-for="category in categories" :key="category.value" @click="selectCategory(category)">
                  {{ category.label }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <!-- 技术栈筛选 -->
          <el-dropdown>
            <el-button type="primary" plain class="btn btn-outline flex items-center">
              <i class="fas fa-code mr-2"></i>
              <span>技术栈</span>
              <i class="fas fa-chevron-down ml-2 text-xs"></i>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-for="tech in techStacks" :key="tech.value" @click="selectTechStack(tech)">
                  {{ tech.label }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <!-- 排序 -->
          <el-dropdown>
            <el-button type="primary" plain class="btn btn-outline flex items-center">
              <i class="fas fa-sort mr-2"></i>
              <span>排序</span>
              <i class="fas fa-chevron-down ml-2 text-xs"></i>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-for="sort in sortOptions" :key="sort.value" @click="selectSort(sort)">
                  {{ sort.label }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      <!-- 活跃标签 -->
      <div class="mt-4 flex flex-wrap gap-2">
        <span class="text-text-tertiary text-sm flex items-center">已选：</span>
        <el-tag 
          v-for="tag in activeTags" 
          :key="tag.key" 
          type="primary" 
          closable 
          @close="removeTag(tag.key)"
          class="tag tag-primary"
        >
          {{ tag.label }}
        </el-tag>
        <el-button 
          v-if="activeTags.length > 0" 
          type="text" 
          class="text-sm text-text-tertiary hover:text-primary ml-2"
          @click="clearAllTags"
        >
          清除全部
        </el-button>
      </div>
    </el-card>
    
    <!-- 模板市场首页 -->
    <div id="market-home" class="block">
      <!-- 推荐模板横幅 -->
      <div class="relative rounded-xl overflow-hidden mb-8">
        <img src="./templateMarket/5d3d843c36cb8d02b1984dd15e370f40.png" alt="推荐模板" class="w-full h-48 md:h-64 object-cover">
        <div class="absolute inset-0 bg-gradient-to-r from-primary/80 to-primary/40 flex items-center">
          <div class="p-6 md:p-10 text-white max-w-xl">
            <h2 class="text-2xl md:text-3xl font-bold mb-2">企业级管理后台模板</h2>
            <p class="mb-4 opacity-90">集成用户管理、权限控制、数据看板等核心功能，快速搭建企业级应用</p>
            <div class="flex gap-3">
              <el-button type="primary" class="btn btn-primary">立即使用</el-button>
              <el-button class="bg-white/20 hover:bg-white/30 text-white border border-white/30">查看详情</el-button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 分类标题 -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold">热门模板</h2>
        <el-button type="text" class="text-primary hover:text-primary-dark flex items-center">
          查看全部
          <i class="fas fa-angle-right ml-1"></i>
        </el-button>
      </div>
      
      <!-- 模板卡片网格 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <el-card 
          v-for="template in templates" 
          :key="template.id"
          class="overflow-hidden template-card-hover cursor-pointer bg-white rounded-lg shadow-card transition-all duration-300 hover:shadow-lg"
          shadow="hover"
        >
          <div class="relative">
            <el-image 
              :src="template.image" 
              :alt="template.title" 
              class="w-full h-48 object-cover rounded-t-lg"
              fit="cover"
            ></el-image>
            <span 
              v-if="template.tag" 
              :class="getTagClass(template.tag)"
              class="absolute top-3 right-3"
            >
              {{ template.tag }}
            </span>
          </div>
          <div class="p-4">
            <div class="flex justify-between items-start mb-2">
              <h3 class="font-semibold text-lg">{{ template.title }}</h3>
              <div class="star-rating flex">
                <i 
                  v-for="i in 5" 
                  :key="i"
                  :class="[i <= template.rating ? 'fas fa-star star' : (i - 0.5 <= template.rating ? 'fas fa-star-half-alt star' : 'far fa-star star-empty')]"
                ></i>
                <span class="text-xs text-text-tertiary ml-1">{{ template.rating }}</span>
              </div>
            </div>
            <p class="text-text-secondary text-sm mb-3 line-clamp-2">{{ template.description }}</p>
            <div class="flex flex-wrap gap-2 mb-4">
              <el-tag 
                v-for="tech in template.techStack" 
                :key="tech"
                class="tag tag-secondary"
                size="small"
              >
                {{ tech }}
              </el-tag>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-xs text-text-tertiary">
                <i class="fas fa-download mr-1"></i>
                {{ formatDownloadCount(template.downloads) }} 下载
              </span>
              <el-button type="primary" size="small" class="btn btn-primary text-sm py-1.5">
                使用模板
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

// TypeScript接口定义
interface Template {
  id: number;
  title: string;
  description: string;
  image: string;
  rating: number;
  techStack: string[];
  downloads: number;
  tag?: string;
}

interface Category {
  value: string;
  label: string;
}

interface TechStack {
  value: string;
  label: string;
}

interface SortOption {
  value: string;
  label: string;
}

interface ActiveTag {
  key: string;
  label: string;
}

// 响应式状态
const searchQuery = ref('');
const activeTab = ref('market-home');
const activeTags = ref<ActiveTag[]>([
  { key: 'category:management', label: '管理后台' },
  { key: 'tech:vue3', label: 'Vue3' }
]);

// 筛选数据
const categories = reactive<Category[]>([
  { value: 'all', label: '全部分类' },
  { value: 'management', label: '管理后台' },
  { value: 'ecommerce', label: '电商系统' },
  { value: 'content', label: '内容管理' },
  { value: 'analytics', label: '数据分析' },
  { value: 'iot', label: '物联网' }
]);

const techStacks = reactive<TechStack[]>([
  { value: 'all', label: '全部技术栈' },
  { value: 'vue3', label: 'Vue3' },
  { value: 'react', label: 'React' },
  { value: 'angular', label: 'Angular' },
  { value: 'antd', label: 'Ant Design' },
  { value: 'element', label: 'Element UI' }
]);

const sortOptions = reactive<SortOption[]>([
  { value: 'recommend', label: '推荐' },
  { value: 'latest', label: '最新发布' },
  { value: 'popular', label: '使用次数' },
  { value: 'rating', label: '评分最高' }
]);

// 模板数据
const templates = reactive<Template[]>([
  {
    id: 1,
    title: '用户管理系统',
    description: '完整的用户管理解决方案，包含用户列表、权限配置、角色管理等功能模块',
    image: './templateMarket/213421eba6cf2f4d9666d9cd057c0045.png',
    rating: 4.5,
    techStack: ['Vue3', 'Ant Design Vue', '管理后台'],
    downloads: 2400,
    tag: '热门'
  },
  {
    id: 2,
    title: '电商管理平台',
    description: '集成商品管理、订单处理、库存监控和销售分析的完整电商解决方案',
    image: './templateMarket/70a65402ea82a45eb2e82a9c043cd19f.png',
    rating: 4.0,
    techStack: ['React', 'Ant Design Pro', '电商系统'],
    downloads: 1800,
    tag: '新上线'
  },
  {
    id: 3,
    title: '数据分析仪表盘',
    description: '多维度数据可视化，支持实时监控、趋势分析和自定义报表生成',
    image: './templateMarket/ce93f84e872e7a979456749fabde3ab6.png',
    rating: 5.0,
    techStack: ['React', 'ECharts', '数据分析'],
    downloads: 3100
  },
  {
    id: 4,
    title: '内容管理系统',
    description: '文章发布、媒体管理、栏目配置一体化内容管理解决方案',
    image: './templateMarket/24176fcf40583916046fe8dadac7907d.png',
    rating: 4.2,
    techStack: ['Vue3', 'Element Plus', '内容管理'],
    downloads: 1900
  },
  {
    id: 5,
    title: '物联网监控平台',
    description: '实时监控物联网设备状态，数据采集与分析，异常报警处理',
    image: './templateMarket/ea5f6ae0fe164c28bf47f716b613e936.png',
    rating: 3.7,
    techStack: ['React', 'WebSocket', '物联网'],
    downloads: 1500,
    tag: '精品'
  },
  {
    id: 6,
    title: '项目管理工具',
    description: '任务管理、进度跟踪、团队协作一体化项目管理解决方案',
    image: './templateMarket/6abe524f5db00e7ff482c3e9c3e293c3.png',
    rating: 4.1,
    techStack: ['Vue3', 'Ant Design Vue', '团队协作'],
    downloads: 2200
  },
  {
    id: 7,
    title: '客户关系管理',
    description: '客户信息管理、跟进记录、销售漏斗分析，提升客户转化率',
    image: './templateMarket/f4de54cbe6f6461a2f3e7ec9e15231df.png',
    rating: 4.6,
    techStack: ['React', 'Ant Design Pro', '客户管理'],
    downloads: 2700
  },
  {
    id: 8,
    title: '财务管理系统',
    description: '财务报表、预算管理、收支分析一体化财务管理解决方案',
    image: './templateMarket/1234567890abcdef.png',
    rating: 4.3,
    techStack: ['Vue3', 'Element Plus', '财务管理'],
    downloads: 1800
  }
]);

// 辅助函数
const getTagClass = (tag: string) => {
  switch (tag) {
    case '热门':
      return 'tag tag-primary';
    case '新上线':
      return 'tag bg-success/10 text-success';
    case '精品':
      return 'tag bg-warning/10 text-warning';
    default:
      return 'tag tag-secondary';
  }
};

const formatDownloadCount = (count: number) => {
  if (count >= 1000) {
    return (count / 1000).toFixed(1) + 'k';
  }
  return count.toString();
};

const selectCategory = (category: Category) => {
  console.log('Selected category:', category);
  // 实现分类筛选逻辑
};

const selectTechStack = (tech: TechStack) => {
  console.log('Selected tech stack:', tech);
  // 实现技术栈筛选逻辑
};

const selectSort = (sort: SortOption) => {
  console.log('Selected sort:', sort);
  // 实现排序逻辑
};

const removeTag = (key: string) => {
  activeTags.value = activeTags.value.filter(tag => tag.key !== key);
};

const clearAllTags = () => {
  activeTags.value = [];
};
</script>

<style scoped lang="scss">
// 保留并使用Tailwind CSS类
.template-card-hover {
  @apply transform hover:-translate-y-1 transition-all duration-300;
}

.star-rating .star {
  @apply text-warning;
}

.star-rating .star-empty {
  @apply text-gray-300;
}

// 导入全局样式
@import '../../assets/styles/index.scss';
</style>