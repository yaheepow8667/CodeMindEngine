<template>
  <div class="p-4 md:p-6">
    <div class="max-w-7xl mx-auto">
      <!-- 页面标题 -->
      <div class="mb-8">
        <h1 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-text-primary">智能生成向导</h1>
        <p class="text-text-secondary mt-1">通过简单几步，快速生成符合您需求的应用代码</p>
      </div>

      <!-- 步骤导航 -->
      <div class="mb-10">
        <div class="flex flex-wrap md:flex-nowrap justify-between relative">
          <!-- 步骤线 -->
          <div class="absolute top-4 left-4 right-4 h-0.5 bg-neutral-dark z-0">
            <div 
              id="step-progress" 
              class="h-full bg-primary transition-all duration-500"
              :style="{ width: progressWidth }"
            ></div>
          </div>

          <!-- 步骤1 -->
          <div 
            class="step-item relative z-10 flex flex-col items-center w-1/4 md:w-auto"
            @click="goToStep(1)"
          >
            <div class="step-number" :class="{ 'step-active': currentStep === 1 }">
              1
            </div>
            <div class="step-title mt-2 text-center" :class="{ 'step-active': currentStep === 1 }">
              需求输入
            </div>
          </div>

          <!-- 步骤2 -->
          <div 
            class="step-item relative z-10 flex flex-col items-center w-1/4 md:w-auto"
            @click="goToStep(2)"
          >
            <div class="step-number" :class="{ 'step-active': currentStep === 2 }">
              2
            </div>
            <div class="step-title mt-2 text-center" :class="{ 'step-active': currentStep === 2 }">
              技术栈选择
            </div>
          </div>

          <!-- 步骤3 -->
          <div 
            class="step-item relative z-10 flex flex-col items-center w-1/4 md:w-auto"
            @click="goToStep(3)"
          >
            <div class="step-number" :class="{ 'step-active': currentStep === 3 }">
              3
            </div>
            <div class="step-title mt-2 text-center" :class="{ 'step-active': currentStep === 3 }">
              蓝图预览
            </div>
          </div>

          <!-- 步骤4 -->
          <div 
            class="step-item relative z-10 flex flex-col items-center w-1/4 md:w-auto"
            @click="goToStep(4)"
          >
            <div class="step-number" :class="{ 'step-active': currentStep === 4 }">
              4
            </div>
            <div class="step-title mt-2 text-center" :class="{ 'step-active': currentStep === 4 }">
              生成结果
            </div>
          </div>
        </div>
      </div>

      <!-- 步骤内容区域 -->
      <div class="bg-white rounded-lg shadow-card p-6 md:p-8 mb-6 min-h-[calc(100vh-280px)]">
        <!-- 步骤1：需求输入 -->
        <div 
          id="step-1" 
          :class="{
            'animate-fadeIn': currentStep === 1,
            'block': currentStep === 1,
            'hidden': currentStep !== 1
          }"
        >
          <div class="mb-6">
            <h2 class="text-xl font-bold text-text-primary">描述您的应用需求</h2>
            <p class="text-text-secondary mt-1">用自然语言描述您想要创建的应用，越详细越好</p>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- 左侧：需求输入区域 -->
            <div class="lg:col-span-2 space-y-6">
              <div>
                <label class="form-label">需求描述</label>
                <el-input
                  v-model="demandDescription"
                  type="textarea"
                  placeholder="例如：创建一个用户管理系统，包含用户列表（显示姓名、邮箱、状态）、支持增删改查和按状态筛选，并有数据看板展示统计。"
                  :rows="8"
                  resize="y"
                  class="form-control"
                ></el-input>
                <p class="text-xs text-text-tertiary mt-1.5">提示：描述应用功能、页面、数据和交互等关键信息，越详细生成效果越好</p>
              </div>
              <div>
                <label class="form-label">附加输入</label>
                <el-upload
                  drag
                  action=""
                  :auto-upload="false"
                  :file-list="fileList"
                  :on-change="handleFileChange"
                  accept="image/jpg,image/png"
                  class="border border-dashed border-border-color rounded-md p-6 text-center hover:border-primary transition-all duration-300 cursor-pointer"
                >
                  <i class="fas fa-cloud-upload-alt text-3xl text-text-tertiary mb-2"></i>
                  <p class="text-text-secondary">拖拽图片或点击上传需求草图（可选）</p>
                  <p class="text-xs text-text-tertiary mt-1">支持JPG、PNG格式，最大2MB</p>
                </el-upload>
              </div>
              <div class="flex flex-wrap gap-3 pt-2">
                <el-button type="primary" plain @click="loadFromTemplate">
                  <i class="fas fa-file-alt mr-2"></i> 从模板示例载入
                </el-button>
                <el-button type="primary" plain @click="parseFromPRD">
                  <i class="fas fa-file-code mr-2"></i> 从PRD文档解析
                </el-button>
                <el-button type="primary" plain @click="voiceInput">
                  <i class="fas fa-microphone mr-2"></i> 语音输入
                </el-button>
              </div>
            </div>

            <!-- 右侧：需求解析预览 -->
            <div class="lg:col-span-1">
              <div class="card sticky top-4">
                <h3 class="text-lg font-semibold mb-4 flex items-center">
                  <i class="fas fa-lightbulb text-warning mr-2"></i> 需求解析预览
                </h3>
                <div class="space-y-4">
                  <div>
                    <h4 class="text-sm font-medium text-text-secondary mb-2">关键实体</h4>
                    <div class="flex flex-wrap gap-2">
                      <span 
                        v-for="entity in keyEntities" 
                        :key="entity"
                        class="px-2 py-1 bg-primary-light/30 text-primary text-xs rounded-full"
                      >
                        {{ entity }}
                      </span>
                    </div>
                  </div>
                  <div>
                    <h4 class="text-sm font-medium text-text-secondary mb-2">主要功能</h4>
                    <ul class="space-y-1.5">
                      <li 
                        v-for="(feature, index) in mainFeatures" 
                        :key="index"
                        class="flex items-start"
                      >
                        <i class="fas fa-check-circle text-success mt-0.5 mr-2 text-xs"></i>
                        <span class="text-sm">{{ feature }}</span>
                      </li>
                    </ul>
                  </div>
                  <div class="pt-2">
                    <div class="w-full bg-neutral-dark rounded-full h-1.5">
                      <div class="bg-success h-1.5 rounded-full" :style="{ width: '75%' }"></div>
                    </div>
                    <p class="text-xs text-text-tertiary mt-1.5 text-right">解析完成度：75%</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤2：架构与技术栈选择 -->
        <div 
          id="step-2" 
          :class="{
            'animate-fadeIn': currentStep === 2,
            'block': currentStep === 2,
            'hidden': currentStep !== 2
          }"
        >
          <div class="mb-6">
            <h2 class="text-xl font-bold text-text-primary">选择您的技术偏好</h2>
            <p class="text-text-secondary mt-1">选择适合您项目的技术栈组合</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- 左侧：主要技术选择 -->
            <div class="space-y-6">
              <div>
                <label class="form-label">前端框架</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.frontend === 'vue' }"
                    @click="techStack.frontend = 'vue'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.frontend" label="vue" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fab fa-vuejs text-2xl text-green-500 mr-3"></i>
                        <div>
                          <div class="font-medium">Vue 3</div>
                          <div class="text-xs text-text-tertiary">Composition API, SFC</div>
                        </div>
                      </label>
                    </div>
                  </div>
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.frontend === 'react' }"
                    @click="techStack.frontend = 'react'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.frontend" label="react" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fab fa-react text-2xl text-blue-400 mr-3"></i>
                        <div>
                          <div class="font-medium">React</div>
                          <div class="text-xs text-text-tertiary">Hooks, JSX</div>
                        </div>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <label class="form-label">UI组件库</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.uilib === 'antd' }"
                    @click="techStack.uilib = 'antd'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.uilib" label="antd" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fab fa-android text-2xl text-primary mr-3"></i>
                        <div>
                          <div class="font-medium">Ant Design</div>
                          <div class="text-xs text-text-tertiary">企业级UI设计语言</div>
                        </div>
                      </label>
                    </div>
                  </div>
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.uilib === 'element' }"
                    @click="techStack.uilib = 'element'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.uilib" label="element" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fab fa-elementor text-2xl text-purple-500 mr-3"></i>
                        <div>
                          <div class="font-medium">Element UI</div>
                          <div class="text-xs text-text-tertiary">桌面端组件库</div>
                        </div>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <label class="form-label">后端框架</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.backend === 'nest' }"
                    @click="techStack.backend = 'nest'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.backend" label="nest" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fab fa-node-js text-2xl text-red-500 mr-3"></i>
                        <div>
                          <div class="font-medium">NestJS</div>
                          <div class="text-xs text-text-tertiary">Node.js后端框架</div>
                        </div>
                      </label>
                    </div>
                  </div>
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.backend === 'spring' }"
                    @click="techStack.backend = 'spring'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.backend" label="spring" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fab fa-java text-2xl text-orange-500 mr-3"></i>
                        <div>
                          <div class="font-medium">Spring Boot</div>
                          <div class="text-xs text-text-tertiary">Java后端框架</div>
                        </div>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <label class="form-label">数据库</label>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.database === 'mysql' }"
                    @click="techStack.database = 'mysql'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.database" label="mysql" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fas fa-database text-2xl text-blue-600 mr-3"></i>
                        <div class="text-sm font-medium">MySQL</div>
                      </label>
                    </div>
                  </div>
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.database === 'postgres' }"
                    @click="techStack.database = 'postgres'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.database" label="postgres" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fas fa-database text-2xl text-blue-700 mr-3"></i>
                        <div class="text-sm font-medium">PostgreSQL</div>
                      </label>
                    </div>
                  </div>
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    :class="{ 'border-primary bg-primary-light/30': techStack.database === 'mongodb' }"
                    @click="techStack.database = 'mongodb'"
                  >
                    <div class="flex items-center">
                      <el-radio v-model="techStack.database" label="mongodb" class="mr-3 text-primary"></el-radio>
                      <label class="flex items-center cursor-pointer">
                        <i class="fas fa-database text-2xl text-green-600 mr-3"></i>
                        <div class="text-sm font-medium">MongoDB</div>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 右侧：推荐组合和高级配置 -->
            <div class="space-y-6">
              <div class="card">
                <h3 class="text-lg font-semibold mb-4">推荐组合</h3>
                <div class="space-y-4">
                  <div 
                    class="border border-primary-light bg-primary-light/20 rounded-md p-4 cursor-pointer hover:bg-primary-light/40 transition-all duration-300"
                    @click="selectRecommendedStack('vue+antd+nest')"
                  >
                    <div class="flex items-start">
                      <div class="mr-3 mt-1">
                        <i class="fas fa-star text-warning"></i>
                      </div>
                      <div>
                        <div class="font-medium">Vue 3 + Ant Design Vue + NestJS</div>
                        <p class="text-sm text-text-secondary mt-1">全栈TypeScript，开发体验一致，适合企业级应用</p>
                        <div class="flex flex-wrap gap-2 mt-2">
                          <span class="text-xs bg-primary-light text-primary px-2 py-0.5 rounded-full">热门选择</span>
                          <span class="text-xs bg-success/10 text-success px-2 py-0.5 rounded-full">高效开发</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div 
                    class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                    @click="selectRecommendedStack('react+antd+spring')"
                  >
                    <div class="font-medium">React + Ant Design Pro + Spring Boot</div>
                    <p class="text-sm text-text-secondary mt-1">成熟稳定组合，适合大型商业应用</p>
                  </div>
                </div>
              </div>

              <!-- 高级配置 -->
              <div>
                <div 
                  class="flex items-center justify-between cursor-pointer"
                  @click="advancedConfigVisible = !advancedConfigVisible"
                >
                  <h3 class="text-lg font-semibold flex items-center">
                    <i class="fas fa-sliders-h mr-2 text-text-secondary"></i> 高级配置
                  </h3>
                  <i 
                    class="fas fa-chevron-down text-text-tertiary transition-transform duration-300"
                    :class="{ 'transform rotate-180': advancedConfigVisible }"
                  ></i>
                </div>
                <div 
                  class="mt-4 space-y-4"
                  :class="{ 'hidden': !advancedConfigVisible }"
                >
                  <div>
                    <label class="form-label">状态管理</label>
                    <el-select v-model="advancedConfig.stateManagement" class="form-control">
                      <el-option label="Pinia (Vue3推荐)" value="pinia"></el-option>
                      <el-option label="Vuex" value="vuex"></el-option>
                      <el-option label="Redux" value="redux"></el-option>
                      <el-option label="Zustand" value="zustand"></el-option>
                    </el-select>
                  </div>
                  <div>
                    <label class="form-label">API风格</label>
                    <div class="grid grid-cols-2 gap-3">
                      <div 
                        class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                        :class="{ 'border-primary bg-primary-light/30': advancedConfig.apiStyle === 'rest' }"
                        @click="advancedConfig.apiStyle = 'rest'"
                      >
                        <div class="flex items-center">
                          <el-radio v-model="advancedConfig.apiStyle" label="rest" class="mr-3 text-primary"></el-radio>
                          <div class="font-medium">RESTful API</div>
                        </div>
                      </div>
                      <div 
                        class="border border-border-color rounded-md p-4 cursor-pointer hover:border-primary hover:bg-primary-light/30 transition-all duration-300"
                        :class="{ 'border-primary bg-primary-light/30': advancedConfig.apiStyle === 'graphql' }"
                        @click="advancedConfig.apiStyle = 'graphql'"
                      >
                        <div class="flex items-center">
                          <el-radio v-model="advancedConfig.apiStyle" label="graphql" class="mr-3 text-primary"></el-radio>
                          <div class="font-medium">GraphQL</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤3：蓝图预览 -->
        <div 
          id="step-3" 
          :class="{
            'animate-fadeIn': currentStep === 3,
            'block': currentStep === 3,
            'hidden': currentStep !== 3
          }"
        >
          <div class="mb-6">
            <h2 class="text-xl font-bold text-text-primary">蓝图预览</h2>
            <p class="text-text-secondary mt-1">查看根据您的需求生成的应用架构蓝图</p>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- 左侧：架构图 -->
            <div class="lg:col-span-2">
              <div class="card h-full">
                <h3 class="text-lg font-semibold mb-4">系统架构图</h3>
                <div class="bg-neutral-bg rounded-md p-4 h-[400px] flex items-center justify-center">
                  <i class="fas fa-project-diagram text-6xl text-text-tertiary"></i>
                  <p class="text-text-tertiary ml-4">系统架构图预览区域</p>
                </div>
              </div>
            </div>
            <!-- 右侧：架构详情 -->
            <div class="lg:col-span-1">
              <div class="card">
                <h3 class="text-lg font-semibold mb-4">架构详情</h3>
                <div class="space-y-4">
                  <div>
                    <h4 class="text-sm font-medium text-text-secondary mb-2">页面结构</h4>
                    <ul class="space-y-1.5">
                      <li class="flex items-start">
                        <i class="fas fa-file-alt text-primary mt-0.5 mr-2 text-xs"></i>
                        <span class="text-sm">首页 (Dashboard)</span>
                      </li>
                      <li class="flex items-start">
                        <i class="fas fa-file-alt text-primary mt-0.5 mr-2 text-xs"></i>
                        <span class="text-sm">用户列表</span>
                      </li>
                      <li class="flex items-start">
                        <i class="fas fa-file-alt text-primary mt-0.5 mr-2 text-xs"></i>
                        <span class="text-sm">数据统计页</span>
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h4 class="text-sm font-medium text-text-secondary mb-2">数据模型</h4>
                    <div class="flex flex-wrap gap-2">
                      <span class="px-2 py-1 bg-primary-light/30 text-primary text-xs rounded-full">User</span>
                      <span class="px-2 py-1 bg-primary-light/30 text-primary text-xs rounded-full">Role</span>
                      <span class="px-2 py-1 bg-primary-light/30 text-primary text-xs rounded-full">Permission</span>
                    </div>
                  </div>
                  <div>
                    <h4 class="text-sm font-medium text-text-secondary mb-2">核心功能</h4>
                    <ul class="space-y-1.5">
                      <li class="flex items-start">
                        <i class="fas fa-check-circle text-success mt-0.5 mr-2 text-xs"></i>
                        <span class="text-sm">用户认证与授权</span>
                      </li>
                      <li class="flex items-start">
                        <i class="fas fa-check-circle text-success mt-0.5 mr-2 text-xs"></i>
                        <span class="text-sm">数据增删改查</span>
                      </li>
                      <li class="flex items-start">
                        <i class="fas fa-check-circle text-success mt-0.5 mr-2 text-xs"></i>
                        <span class="text-sm">数据统计与分析</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤4：生成结果 -->
        <div 
          id="step-4" 
          :class="{
            'animate-fadeIn': currentStep === 4,
            'block': currentStep === 4,
            'hidden': currentStep !== 4
          }"
        >
          <div class="mb-6">
            <h2 class="text-xl font-bold text-text-primary">生成结果</h2>
            <p class="text-text-secondary mt-1">您的应用代码已生成完成</p>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- 左侧：生成结果概览 -->
            <div class="space-y-6">
              <div class="card">
                <h3 class="text-lg font-semibold mb-4">生成概览</h3>
                <div class="space-y-4">
                  <div class="flex justify-between items-center">
                    <span class="text-text-secondary">生成状态</span>
                    <span class="text-success font-medium">已完成</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-text-secondary">生成文件数</span>
                    <span class="font-medium">24</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-text-secondary">代码行数</span>
                    <span class="font-medium">1,234</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-text-secondary">技术栈</span>
                    <span class="font-medium text-primary">{{ getTechStackSummary() }}</span>
                  </div>
                </div>
              </div>
              <div class="card">
                <h3 class="text-lg font-semibold mb-4">生成的文件</h3>
                <div class="space-y-2 max-h-[300px] overflow-y-auto">
                  <div 
                    v-for="file in generatedFiles" 
                    :key="file.path"
                    class="flex items-center p-2 hover:bg-primary-light/30 rounded-md cursor-pointer"
                  >
                    <i class="fas fa-file-code text-primary mr-3"></i>
                    <span class="text-sm text-text-primary truncate">{{ file.path }}</span>
                  </div>
                </div>
              </div>
            </div>
            <!-- 右侧：操作区域 -->
            <div class="space-y-6">
              <div class="card">
                <h3 class="text-lg font-semibold mb-4">下载代码</h3>
                <div class="space-y-4">
                  <div class="flex items-center p-4 bg-primary-light/20 rounded-md">
                    <i class="fas fa-file-archive text-3xl text-primary mr-4"></i>
                    <div>
                      <div class="font-medium">应用代码包</div>
                      <div class="text-sm text-text-secondary mt-1">zip格式，包含完整代码</div>
                    </div>
                    <el-button type="primary" class="ml-auto">
                      <i class="fas fa-download mr-2"></i> 下载
                    </el-button>
                  </div>
                </div>
              </div>
              <div class="card">
                <h3 class="text-lg font-semibold mb-4">快速部署</h3>
                <div class="space-y-4">
                  <el-button type="primary" class="w-full">
                    <i class="fas fa-rocket mr-2"></i> 一键部署到开发环境
                  </el-button>
                  <el-button type="primary" plain class="w-full">
                    <i class="fas fa-copy mr-2"></i> 复制部署命令
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 步骤导航按钮 -->
      <div class="flex justify-between items-center">
        <el-button 
          v-if="currentStep > 1"
          type="primary" 
          plain 
          @click="prevStep"
          class="btn-secondary"
        >
          <i class="fas fa-chevron-left mr-2"></i> 上一步
        </el-button>
        <div v-else></div>
        
        <el-button 
          v-if="currentStep < 4"
          type="primary"
          @click="nextStep"
          class="btn-primary"
        >
          下一步 <i class="fas fa-chevron-right ml-2"></i>
        </el-button>
        <el-button 
          v-else
          type="primary"
          @click="generateCode"
          class="btn-primary"
        >
          <i class="fas fa-rocket mr-2"></i> 开始生成
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 步骤管理
const currentStep = ref(1)

const progressWidth = computed(() => {
  const progressMap = {
    1: '0%',
    2: '33.33%',
    3: '66.66%',
    4: '100%'
  }
  return progressMap[currentStep.value as keyof typeof progressMap]
})

const nextStep = () => {
  if (currentStep.value < 4) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const goToStep = (step: number) => {
  if (step >= 1 && step <= 4) {
    currentStep.value = step
  }
}

// 步骤1：需求输入
const demandDescription = ref('')
const fileList = ref<any[]>([])
const keyEntities = ref(['用户(User)', '数据看板(Dashboard)'])
const mainFeatures = ref([
  '用户列表展示（姓名、邮箱、状态）',
  '用户增删改查操作',
  '状态筛选功能',
  '数据统计看板'
])

const handleFileChange = (file: any) => {
  // 处理文件上传逻辑
  ElMessage.info('文件已选择：' + file.name)
}

const loadFromTemplate = () => {
  ElMessage.info('从模板示例载入')
}

const parseFromPRD = () => {
  ElMessage.info('从PRD文档解析')
}

const voiceInput = () => {
  ElMessage.info('语音输入功能')
}

// 步骤2：技术栈选择
interface TechStack {
  frontend: string
  uilib: string
  backend: string
  database: string
}

const techStack = reactive<TechStack>({
  frontend: 'vue',
  uilib: 'antd',
  backend: 'nest',
  database: 'mysql'
})

interface AdvancedConfig {
  stateManagement: string
  apiStyle: string
}

const advancedConfig = reactive<AdvancedConfig>({
  stateManagement: 'pinia',
  apiStyle: 'rest'
})

const advancedConfigVisible = ref(false)

const selectRecommendedStack = (stack: string) => {
  switch (stack) {
    case 'vue+antd+nest':
      techStack.frontend = 'vue'
      techStack.uilib = 'antd'
      techStack.backend = 'nest'
      techStack.database = 'mysql'
      break
    case 'react+antd+spring':
      techStack.frontend = 'react'
      techStack.uilib = 'antd'
      techStack.backend = 'spring'
      techStack.database = 'mysql'
      break
  }
}

// 步骤4：生成结果
const generatedFiles = ref([
  { path: 'src/main.ts' },
  { path: 'src/App.vue' },
  { path: 'src/components/Header.vue' },
  { path: 'src/components/Sidebar.vue' },
  { path: 'src/views/Dashboard.vue' },
  { path: 'src/views/UserList.vue' },
  { path: 'src/router/index.ts' },
  { path: 'src/store/index.ts' }
])

const getTechStackSummary = () => {
  const frontendMap: Record<string, string> = {
    vue: 'Vue 3',
    react: 'React'
  }
  const uilibMap: Record<string, string> = {
    antd: 'Ant Design',
    element: 'Element UI'
  }
  const backendMap: Record<string, string> = {
    nest: 'NestJS',
    spring: 'Spring Boot'
  }
  const databaseMap: Record<string, string> = {
    mysql: 'MySQL',
    postgres: 'PostgreSQL',
    mongodb: 'MongoDB'
  }

  return `${frontendMap[techStack.frontend]} + ${uilibMap[techStack.uilib]} + ${backendMap[techStack.backend]} + ${databaseMap[techStack.database]}`
}

const generateCode = () => {
  ElMessage.success('代码生成完成！')
}
</script>

<style scoped>
/* 保留原有Tailwind工具类定义 */
.step-active {
  @apply text-primary border-primary;
}

.step-line-active {
  @apply bg-primary;
}

.form-focus {
  @apply border-primary ring-1 ring-primary/30;
}
</style>