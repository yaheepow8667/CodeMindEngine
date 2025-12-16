<template>
  <div class="p-4 md:p-6">
    <!-- 页面标题区域 -->
    <div class="mb-6">
      <h3 class="text-2xl font-semibold text-text-primary">工作空间设置</h3>
      <div class="border-b border-border-color mt-2"></div>
      <!-- 面包屑导航 -->
      <el-breadcrumb class="text-sm text-text-secondary mt-2">
        <el-breadcrumb-item :to="{ path: '/settings' }">设置中心</el-breadcrumb-item>
        <el-breadcrumb-item>工作空间设置</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 工作空间设置内容容器 -->
    <div id="workspace-settings-container">
      <!-- 1. 编辑器偏好配置 -->
      <el-card class="ant-card mb-6" shadow="hover">
        <template #header>
          <div class="module-title">编辑器偏好配置</div>
        </template>

        <!-- 编辑器主题选择 -->
        <div class="mb-6 p-4 border border-border-color rounded-lg">
          <h4 class="text-base font-medium mb-3">界面外观</h4>
          <div class="flex space-x-4">
            <!-- 浅色主题 -->
            <div 
              @click="toggleTheme('light')" 
              :class="['flex-1 p-4 border-2 rounded-lg cursor-pointer transition-all duration-200', 
                currentTheme === 'light' ? 'border-primary bg-primary-light/50 shadow-sm' : 'border-border-color hover:border-primary bg-gray-50']"
            >
              <div class="flex justify-center mb-2">
                <i class="fas fa-sun text-2xl text-warning"></i>
              </div>
              <p class="text-center text-sm font-medium">浅色主题</p>
              <p class="text-center text-xs text-text-tertiary mt-1">默认亮色界面</p>
            </div>

            <!-- 深色主题 -->
            <div 
              @click="toggleTheme('dark')" 
              :class="['flex-1 p-4 border-2 rounded-lg cursor-pointer transition-all duration-200', 
                currentTheme === 'dark' ? 'border-primary bg-primary-light/50 shadow-sm' : 'border-border-color hover:border-primary bg-gray-50']"
            >
              <div class="flex justify-center mb-2">
                <i class="fas fa-moon text-2xl text-text-secondary"></i>
              </div>
              <p class="text-center text-sm font-medium">深色主题</p>
              <p class="text-center text-xs text-text-tertiary mt-1">适合夜间工作</p>
            </div>
          </div>
        </div>

        <!-- 代码编辑器设置 -->
        <div class="space-y-4">
          <h4 class="text-base font-medium mb-3">代码编辑器</h4>

          <!-- 字体大小 -->
          <div class="flex items-center space-x-4">
            <label class="w-32 text-sm text-text-secondary">字体大小:</label>
            <div class="flex-1">
              <el-slider 
                v-model="fontSize" 
                :min="12" 
                :max="24" 
                @change="handleFontSizeChange"
              ></el-slider>
            </div>
            <span class="w-10 text-sm text-right text-primary font-medium">{{ fontSize }}px</span>
          </div>

          <!-- 主题预设 -->
          <div class="flex items-center space-x-4">
            <label class="w-32 text-sm text-text-secondary">主题预设:</label>
            <el-select 
              v-model="editorTheme" 
              class="flex-1" 
              placeholder="请选择主题预设"
            >
              <el-option label="VSCode Dark+" value="vs-dark"></el-option>
              <el-option label="VSCode Light+" value="vs-light"></el-option>
              <el-option label="Monokai" value="monokai"></el-option>
              <el-option label="Solarized Dark" value="solarized-dark"></el-option>
            </el-select>
          </div>

          <!-- 自动保存 -->
          <div class="flex items-center space-x-4">
            <label class="w-32 text-sm text-text-secondary">自动保存:</label>
            <div class="flex-1 flex items-center space-x-4">
              <el-switch v-model="isAutoSaveOn" @change="handleAutoSaveChange"></el-switch>
              <span class="text-sm text-text-secondary">
                {{ isAutoSaveOn ? '开启 (间隔: ' + autoSaveInterval + ' 秒)' : '关闭' }}
              </span>
              <el-input-number 
                v-model="autoSaveInterval" 
                :min="1" 
                :max="60" 
                :disabled="!isAutoSaveOn"
                class="w-20"
              ></el-input-number>
            </div>
          </div>

          <!-- 格式化偏好 -->
          <div class="flex items-center space-x-4">
            <label class="w-32 text-sm text-text-secondary">代码格式化:</label>
            <div class="flex-1 space-x-4">
              <el-radio-group v-model="formatter">
                <el-radio label="prettier">Prettier</el-radio>
                <el-radio label="eslint">ESLint</el-radio>
              </el-radio-group>
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-border-color flex justify-between items-center">
          <el-button type="primary" @click="savePreferences">保存更改</el-button>
          <span id="last-save-time" class="text-xs text-text-tertiary">上次保存: {{ lastSaveTime }}</span>
        </div>
      </el-card>

      <!-- 2. 生成默认项配置 -->
      <el-card class="ant-card mb-6" shadow="hover">
        <template #header>
          <div class="module-title">生成默认项配置</div>
        </template>

        <!-- 默认技术栈 -->
        <div class="mb-6">
          <h4 class="text-base font-medium mb-3">新建项目默认技术栈</h4>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <!-- Vue 3 + TypeScript -->
            <div 
              @click="selectTechStack('vue-ts')" 
              :class="['p-4 border-2 rounded-lg cursor-pointer transition-all duration-200', 
                selectedTechStack === 'vue-ts' ? 'border-primary bg-primary-light/50 shadow-sm' : 'border-border-color hover:border-primary']"
            >
              <div class="flex justify-between items-center mb-2">
                <i class="fas fa-code text-2xl text-primary"></i>
                <i v-if="selectedTechStack === 'vue-ts'" class="fas fa-check-circle text-lg text-primary"></i>
              </div>
              <p class="text-base font-semibold">Vue 3 + TypeScript</p>
              <p class="text-xs text-text-secondary">Vite, Pinia</p>
            </div>

            <!-- React + TypeScript -->
            <div 
              @click="selectTechStack('react-ts')" 
              :class="['p-4 border-2 rounded-lg cursor-pointer transition-all duration-200', 
                selectedTechStack === 'react-ts' ? 'border-primary bg-primary-light/50 shadow-sm' : 'border-border-color hover:border-primary']"
            >
              <div class="flex justify-between items-center mb-2">
                <i class="fas fa-code text-2xl text-info"></i>
                <i v-if="selectedTechStack === 'react-ts'" class="fas fa-check-circle text-lg text-primary"></i>
              </div>
              <p class="text-base font-semibold">React + TypeScript</p>
              <p class="text-xs text-text-secondary">CRA/Vite, Redux</p>
            </div>

            <!-- Node.js + Express -->
            <div 
              @click="selectTechStack('node-express')" 
              :class="['p-4 border-2 rounded-lg cursor-pointer transition-all duration-200', 
                selectedTechStack === 'node-express' ? 'border-primary bg-primary-light/50 shadow-sm' : 'border-border-color hover:border-primary']"
            >
              <div class="flex justify-between items-center mb-2">
                <i class="fas fa-server text-2xl text-success"></i>
                <i v-if="selectedTechStack === 'node-express'" class="fas fa-check-circle text-lg text-primary"></i>
              </div>
              <p class="text-base font-semibold">Node.js + Express</p>
              <p class="text-xs text-text-secondary">REST API</p>
            </div>

            <!-- Spring Boot -->
            <div 
              @click="selectTechStack('spring-boot')" 
              :class="['p-4 border-2 rounded-lg cursor-pointer transition-all duration-200', 
                selectedTechStack === 'spring-boot' ? 'border-primary bg-primary-light/50 shadow-sm' : 'border-border-color hover:border-primary']"
            >
              <div class="flex justify-between items-center mb-2">
                <i class="fas fa-leaf text-2xl text-success"></i>
                <i v-if="selectedTechStack === 'spring-boot'" class="fas fa-check-circle text-lg text-primary"></i>
              </div>
              <p class="text-base font-semibold">Spring Boot</p>
              <p class="text-xs text-text-secondary">Java Backend</p>
            </div>
          </div>
        </div>

        <!-- 代码规范模板 -->
        <div>
          <h4 class="text-base font-medium mb-3">代码规范模板</h4>
          <div class="flex items-center space-x-4">
            <label class="w-32 text-sm text-text-secondary">选择模板:</label>
            <el-select v-model="codeStyle" class="flex-1" placeholder="请选择代码规范模板">
              <el-option label="Airbnb (推荐)" value="airbnb"></el-option>
              <el-option label="Standard" value="standard"></el-option>
              <el-option label="Google" value="google"></el-option>
              <el-option label="自定义" value="custom"></el-option>
            </el-select>
            <el-button type="text" class="text-sm text-primary hover:text-primary-dark whitespace-nowrap">查看规范详情</el-button>
          </div>
        </div>
      </el-card>

      <!-- 3. 集成与存储配置 -->
      <el-card class="ant-card mb-6" shadow="hover">
        <template #header>
          <div class="module-title">集成与存储配置</div>
        </template>

        <!-- Git仓库集成 -->
        <div class="mb-6 p-4 border border-border-color rounded-lg">
          <h4 class="text-base font-medium mb-3">代码仓库自动同步</h4>
          <div class="flex flex-wrap gap-3 mb-4">
            <span class="text-sm text-text-secondary mr-2">已连接提供商:</span>
            <el-tag type="success" effect="light" class="text-xs">
              <i class="fas fa-check-circle mr-1 text-xs"></i>GitHub
            </el-tag>
            <el-tag type="warning" effect="light" class="text-xs">
              <i class="fas fa-exclamation-circle mr-1 text-xs"></i>GitLab (待授权)
            </el-tag>
          </div>
          <el-button type="default" @click="connectGit">
            <i class="fas fa-link mr-2"></i>连接新仓库
          </el-button>
        </div>

        <!-- 文件存储设置 -->
        <div>
          <h4 class="text-base font-medium mb-3">生成文件处理方式</h4>
          <div class="space-y-3">
            <el-radio-group v-model="storageOption">
              <el-radio label="local" class="p-3 border border-border-color rounded-lg hover:bg-primary-light/30 transition-colors cursor-pointer block">
                <div class="flex items-center">
                  <i class="fas fa-download ml-3 mr-2 text-lg text-info"></i>
                  <div>
                    <span class="text-sm font-medium">自动下载到本地</span>
                    <span class="text-xs text-text-tertiary ml-2">(默认行为)</span>
                  </div>
                </div>
              </el-radio>

              <el-radio label="git" class="p-3 border border-border-color rounded-lg hover:bg-primary-light/30 transition-colors cursor-pointer block">
                <div class="flex items-center">
                  <i class="fab fa-git-alt ml-3 mr-2 text-lg text-primary"></i>
                  <div>
                    <span class="text-sm font-medium">自动推送到Git仓库</span>
                    <span class="text-xs text-text-tertiary ml-2">(需要已配置仓库)</span>
                  </div>
                </div>
              </el-radio>

              <el-radio label="cloud" class="p-3 border border-border-color rounded-lg hover:bg-primary-light/30 transition-colors cursor-pointer block">
                <div class="flex items-center">
                  <i class="fas fa-cloud ml-3 mr-2 text-lg text-secondary"></i>
                  <div>
                    <span class="text-sm font-medium">保存到云端工作区</span>
                    <span class="text-xs text-text-tertiary ml-2">(项目空间内持久化)</span>
                  </div>
                </div>
              </el-radio>
            </el-radio-group>
          </div>
        </div>
      </el-card>

      <!-- 恢复默认按钮 -->
      <div class="mt-8 pt-4 border-t border-border-color flex justify-end">
        <el-button type="danger" text @click="resetToDefaults">
          <i class="fas fa-undo-alt mr-1"></i>恢复默认设置
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';

// 主题相关
const currentTheme = ref('light');

// 编辑器设置
const fontSize = ref(16);
const editorTheme = ref('vs-dark');
const isAutoSaveOn = ref(true);
const autoSaveInterval = ref(5);
const formatter = ref('prettier');
const lastSaveTime = ref('');

// 技术栈选择
const selectedTechStack = ref('vue-ts');
const codeStyle = ref('airbnb');

// 存储选项
const storageOption = ref('local');

// 主题切换
const toggleTheme = (theme: string) => {
  currentTheme.value = theme;
  // 这里可以添加实际的主题切换逻辑
};

// 字体大小变化处理
const handleFontSizeChange = () => {
  // 这里可以添加实际的字体大小变化逻辑
};

// 自动保存开关处理
const handleAutoSaveChange = () => {
  if (isAutoSaveOn.value) {
    ElMessage.success('自动保存已开启');
  } else {
    ElMessage.warning('自动保存已关闭');
  }
};

// 技术栈选择
const selectTechStack = (stack: string) => {
  selectedTechStack.value = stack;
};

// 保存偏好设置
const savePreferences = () => {
  // 这里可以添加实际的保存逻辑
  lastSaveTime.value = new Date().toLocaleString();
  ElMessage.success('偏好设置已保存');
};

// 连接Git仓库
const connectGit = () => {
  // 这里可以添加实际的连接逻辑
  ElMessage.info('连接新仓库功能开发中');
};

// 恢复默认设置
const resetToDefaults = () => {
  // 恢复默认设置
  currentTheme.value = 'light';
  fontSize.value = 16;
  editorTheme.value = 'vs-dark';
  isAutoSaveOn.value = true;
  autoSaveInterval.value = 5;
  formatter.value = 'prettier';
  selectedTechStack.value = 'vue-ts';
  codeStyle.value = 'airbnb';
  storageOption.value = 'local';
  
  ElMessage.success('已恢复默认设置');
};

// 页面初始化
onMounted(() => {
  // 更新上次保存时间
  lastSaveTime.value = new Date().toLocaleString();
});
</script>

<style scoped lang="scss">
.module-title {
  @apply text-lg font-semibold text-text-primary mb-4 border-b border-border-color pb-2;
}
</style>