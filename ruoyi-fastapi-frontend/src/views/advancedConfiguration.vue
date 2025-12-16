<template>
  <div class="p-4 md:p-6">
    <div class="max-w-6xl mx-auto">
      <!-- 页面标题 -->
      <div class="mb-6 animate-fade-in">
        <h1 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-text-primary flex items-center">
          <i class="fas fa-sliders-h mr-3 text-primary"></i>
          高级生成配置与规则引擎
        </h1>
        <p class="text-text-tertiary mt-1 max-w-3xl text-balance">
          自定义代码生成规则和系统行为，满足特定项目需求，提升开发效率与代码质量
        </p>
      </div>
      
      <!-- 配置卡片 -->
      <el-card class="bg-card-bg rounded-lg shadow-card p-5 mb-5 transition-all duration-300 hover:shadow-card-hover">
        <!-- 操作按钮区 -->
        <div class="flex flex-wrap justify-between items-center mb-6 gap-4">
          <div class="text-text-secondary flex items-center">
            <i class="fas fa-info-circle mr-1 text-primary"></i>
            <span>配置将应用于所有新生成的项目和代码</span>
          </div>
          <div class="flex space-x-3">
            <el-button type="info" plain @click="resetConfig">
              <i class="fas fa-undo mr-1"></i>重置默认
            </el-button>
            <el-button type="primary" @click="saveConfig">
              <i class="fas fa-save mr-1"></i>保存配置
            </el-button>
          </div>
        </div>
        
        <!-- 折叠面板区域 -->
        <div class="space-y-5">
          <!-- 代码规范配置 -->
          <div class="border border-border-color rounded-lg overflow-hidden bg-card-bg shadow-sm">
            <div class="collapse-header" @click="toggleCollapse('code-style')" aria-expanded="codeStyleExpanded">
              <div class="flex items-center">
                <i class="fas fa-code text-primary mr-3 text-xl"></i>
                <h2 class="text-lg font-semibold">代码规范配置</h2>
              </div>
              <i class="fas fa-chevron-down text-text-tertiary transition-transform duration-300" :style="{ transform: codeStyleExpanded ? 'rotate(180deg)' : '' }"></i>
            </div>
            <transition name="collapse">
              <div v-show="codeStyleExpanded" class="collapse-content border-t border-border-color" style="max-height: 1000px;">
                <div class="px-0 pb-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="single-quote-switch">使用单引号</label>
                          <el-switch v-model="config.codeStyle.singleQuote" id="single-quote-switch" />
                        </div>
                        <p class="text-text-tertiary text-sm mt-1">生成的代码中使用单引号而非双引号</p>
                      </div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="jsdoc-switch">自动生成JsDoc注释</label>
                          <el-switch v-model="config.codeStyle.jsdoc" id="jsdoc-switch" />
                        </div>
                        <p class="text-text-tertiary text-sm mt-1">为函数、类和组件自动生成文档注释</p>
                      </div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="semicolon-switch">使用分号结尾</label>
                          <el-switch v-model="config.codeStyle.semicolon" id="semicolon-switch" />
                        </div>
                        <p class="text-text-tertiary text-sm mt-1">在语句结尾添加分号</p>
                      </div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="eslint-switch">启用ESLint规则</label>
                          <el-switch v-model="config.codeStyle.eslint" id="eslint-switch" />
                        </div>
                        <p class="text-text-tertiary text-sm mt-1">生成符合ESLint标准的代码</p>
                      </div>
                    </div>
                    <div>
                      <div class="form-item">
                        <label class="form-label" for="indentation-select">缩进空格数</label>
                        <el-select v-model="config.codeStyle.indentation" class="form-control" id="indentation-select" aria-label="选择缩进空格数">
                          <el-option label="2个空格" value="2" />
                          <el-option label="4个空格" value="4" />
                          <el-option label="使用Tab" value="tab" />
                        </el-select>
                      </div>
                      <div class="form-item">
                        <label class="form-label">函数括号风格</label>
                        <div class="grid grid-cols-2 gap-3">
                          <el-radio v-model="config.codeStyle.braceStyle" label="same-line" border>
                            同一行 (K&R风格)
                          </el-radio>
                          <el-radio v-model="config.codeStyle.braceStyle" label="new-line" border>
                            新行 (Allman风格)
                          </el-radio>
                        </div>
                      </div>
                      <div class="form-item">
                        <label class="form-label">命名规范</label>
                        <div class="grid grid-cols-2 gap-3">
                          <el-radio v-model="config.codeStyle.namingConvention" label="camelCase" border>
                            camelCase
                          </el-radio>
                          <el-radio v-model="config.codeStyle.namingConvention" label="snake_case" border>
                            snake_case
                          </el-radio>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>
          
          <!-- 安全规则配置 -->
          <div class="border border-border-color rounded-lg overflow-hidden bg-card-bg shadow-sm">
            <div class="collapse-header" @click="toggleCollapse('security-rules')" aria-expanded="securityRulesExpanded">
              <div class="flex items-center">
                <i class="fas fa-shield-alt text-primary mr-3 text-xl"></i>
                <h2 class="text-lg font-semibold">安全规则配置</h2>
              </div>
              <i class="fas fa-chevron-down text-text-tertiary transition-transform duration-300" :style="{ transform: securityRulesExpanded ? 'rotate(180deg)' : '' }"></i>
            </div>
            <transition name="collapse">
              <div v-show="securityRulesExpanded" class="collapse-content border-t border-border-color">
                <div class="px-0 pb-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="input-validation-switch">自动生成输入验证</label>
                          <el-switch v-model="config.security.inputValidation" id="input-validation-switch" />
                        </div>
                        <p class="text-text-tertiary text-sm mt-1">为所有API接口生成输入验证逻辑</p>
                      </div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="confirm-dialog-switch">敏感操作二次确认</label>
                          <el-switch v-model="config.security.confirmDialog" id="confirm-dialog-switch" />
                        </div>
                        <p class="text-text-tertiary text-sm mt-1">为删除、修改等敏感操作添加确认对话框</p>
                      </div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="xss-protection-switch">XSS防护</label>
                          <el-switch v-model="config.security.xssProtection" id="xss-protection-switch" />
                        </div>
                        <p class="text-text-tertiary text-sm mt-1">自动对用户输入进行XSS过滤</p>
                      </div>
                    </div>
                    <div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="password-encrypt-switch">密码字段加密传输</label>
                          <el-switch v-model="config.security.passwordEncrypt" id="password-encrypt-switch" />
                        </div>
                        <p class="text-text-tertiary text-sm mt-1">密码在传输前进行加密处理</p>
                      </div>
                      <div class="form-item">
                        <label class="form-label" for="log-level-select">敏感操作日志记录</label>
                        <el-select v-model="config.security.logLevel" class="form-control" id="log-level-select" aria-label="选择敏感操作日志记录级别">
                          <el-option label="不记录" value="none" />
                          <el-option label="基本信息" value="basic" />
                          <el-option label="详细记录" value="detailed" />
                        </el-select>
                      </div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="rate-limit-switch">API访问限流</label>
                          <el-switch v-model="config.security.rateLimit" id="rate-limit-switch" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>
          
          <!-- 性能优化配置 -->
          <div class="border border-border-color rounded-lg overflow-hidden bg-card-bg shadow-sm">
            <div class="collapse-header" @click="toggleCollapse('performance')" aria-expanded="performanceExpanded">
              <div class="flex items-center">
                <i class="fas fa-tachometer-alt text-primary mr-3 text-xl"></i>
                <h2 class="text-lg font-semibold">性能优化配置</h2>
              </div>
              <i class="fas fa-chevron-down text-text-tertiary transition-transform duration-300" :style="{ transform: performanceExpanded ? 'rotate(180deg)' : '' }"></i>
            </div>
            <transition name="collapse">
              <div v-show="performanceExpanded" class="collapse-content border-t border-border-color">
                <div class="px-0 pb-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <div class="form-item">
                        <label class="form-label">前端组件懒加载</label>
                        <div class="grid grid-cols-1 gap-3">
                          <el-radio v-model="config.performance.lazyLoad" label="none" border>
                            不启用
                          </el-radio>
                          <el-radio v-model="config.performance.lazyLoad" label="route" border>
                            路由级别懒加载
                          </el-radio>
                          <el-radio v-model="config.performance.lazyLoad" label="component" border>
                            组件级别懒加载
                          </el-radio>
                        </div>
                      </div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="image-optimization-switch">图片优化</label>
                          <el-switch v-model="config.performance.imageOptimization" id="image-optimization-switch" />
                        </div>
                      </div>
                    </div>
                    <div>
                      <div class="form-item">
                        <label class="form-label">表格数据处理策略</label>
                        <div class="form-item">
                          <label class="form-label" for="pagination-threshold">分页阈值</label>
                          <div class="flex items-center">
                            <el-input-number v-model="config.performance.paginationThreshold" class="form-control w-24" id="pagination-threshold" :min="10" :max="1000" aria-label="分页阈值数量" />
                            <span class="mx-2 text-text-tertiary">条数据</span>
                          </div>
                          <p class="text-text-tertiary text-sm mt-1">超过此数量自动启用分页</p>
                        </div>
                        <div class="form-item">
                          <label class="form-label" for="virtual-scroll-threshold">虚拟滚动阈值</label>
                          <div class="flex items-center">
                            <el-input-number v-model="config.performance.virtualScrollThreshold" class="form-control w-24" id="virtual-scroll-threshold" :min="100" :max="2000" aria-label="虚拟滚动阈值数量" />
                            <span class="mx-2 text-text-tertiary">条数据</span>
                          </div>
                          <p class="text-text-tertiary text-sm mt-1">超过此数量自动启用虚拟滚动</p>
                        </div>
                      </div>
                      <div class="form-item">
                        <div class="flex items-center justify-between">
                          <label class="form-label" for="db-index-switch">生成数据库索引建议</label>
                          <el-switch v-model="config.performance.dbIndex" id="db-index-switch" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>
          
          <!-- 自定义模板注入点 -->
          <div class="border border-border-color rounded-lg overflow-hidden bg-card-bg shadow-sm">
            <div class="collapse-header" @click="toggleCollapse('template')" aria-expanded="templateExpanded">
              <div class="flex items-center">
                <i class="fas fa-file-code text-primary mr-3 text-xl"></i>
                <h2 class="text-lg font-semibold">自定义模板注入点</h2>
              </div>
              <i class="fas fa-chevron-down text-text-tertiary transition-transform duration-300" :style="{ transform: templateExpanded ? 'rotate(180deg)' : '' }"></i>
            </div>
            <transition name="collapse">
              <div v-show="templateExpanded" class="collapse-content border-t border-border-color">
                <div class="px-0 pb-4">
                  <p class="text-text-tertiary mb-4">上传自定义模板文件，覆盖平台默认生成的代码结构</p>
                  <div class="space-y-6">
                    <div class="form-item">
                      <label class="form-label" for="service-template-upload">Service层基类模板</label>
                      <div class="upload-area">
                        <i class="fas fa-upload text-2xl text-text-tertiary mb-2"></i>
                        <p class="text-text-tertiary mb-3">拖放文件到此处或点击上传</p>
                        <el-upload
                          action="#"
                          :auto-upload="false"
                          accept=".js,.ts,.vue"
                          :file-list="serviceTemplateFiles"
                          :on-change="handleServiceTemplateChange"
                          class="inline-block"
                        >
                          <el-button type="primary" plain>选择文件</el-button>
                        </el-upload>
                        <p class="text-text-tertiary text-xs mt-2">支持 .js, .ts, .vue 文件，最大 5MB</p>
                      </div>
                    </div>
                    <div class="form-item">
                      <label class="form-label" for="api-template-upload">API响应格式模板</label>
                      <div class="upload-area">
                        <i class="fas fa-upload text-2xl text-text-tertiary mb-2"></i>
                        <p class="text-text-tertiary mb-3">拖放文件到此处或点击上传</p>
                        <el-upload
                          action="#"
                          :auto-upload="false"
                          accept=".js,.ts,.vue"
                          :file-list="apiTemplateFiles"
                          :on-change="handleApiTemplateChange"
                          class="inline-block"
                        >
                          <el-button type="primary" plain>选择文件</el-button>
                        </el-upload>
                        <p class="text-text-tertiary text-xs mt-2">支持 .js, .ts, .vue 文件，最大 5MB</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

interface CodeStyleConfig {
  singleQuote: boolean
  jsdoc: boolean
  semicolon: boolean
  eslint: boolean
  indentation: string
  braceStyle: string
  namingConvention: string
}

interface SecurityConfig {
  inputValidation: boolean
  confirmDialog: boolean
  xssProtection: boolean
  passwordEncrypt: boolean
  logLevel: string
  rateLimit: boolean
}

interface PerformanceConfig {
  lazyLoad: string
  imageOptimization: boolean
  paginationThreshold: number
  virtualScrollThreshold: number
  dbIndex: boolean
}

interface Config {
  codeStyle: CodeStyleConfig
  security: SecurityConfig
  performance: PerformanceConfig
}

// 折叠面板状态
const codeStyleExpanded = ref(true)
const securityRulesExpanded = ref(false)
const performanceExpanded = ref(false)
const templateExpanded = ref(false)

// 配置数据
const config = reactive<Config>({
  codeStyle: {
    singleQuote: true,
    jsdoc: true,
    semicolon: false,
    eslint: true,
    indentation: '4',
    braceStyle: 'same-line',
    namingConvention: 'camelCase'
  },
  security: {
    inputValidation: true,
    confirmDialog: true,
    xssProtection: true,
    passwordEncrypt: true,
    logLevel: 'detailed',
    rateLimit: false
  },
  performance: {
    lazyLoad: 'route',
    imageOptimization: true,
    paginationThreshold: 100,
    virtualScrollThreshold: 500,
    dbIndex: true
  }
})

// 文件上传
const serviceTemplateFiles = ref([])
const apiTemplateFiles = ref([])

// 切换折叠面板
const toggleCollapse = (collapseType: string) => {
  switch (collapseType) {
    case 'code-style':
      codeStyleExpanded.value = !codeStyleExpanded.value
      break
    case 'security-rules':
      securityRulesExpanded.value = !securityRulesExpanded.value
      break
    case 'performance':
      performanceExpanded.value = !performanceExpanded.value
      break
    case 'template':
      templateExpanded.value = !templateExpanded.value
      break
  }
}

// 保存配置
const saveConfig = () => {
  console.log('保存配置:', config)
  // 这里可以添加保存配置的API调用
}

// 重置配置
const resetConfig = () => {
  // 重置到默认配置
  Object.assign(config, {
    codeStyle: {
      singleQuote: true,
      jsdoc: true,
      semicolon: false,
      eslint: true,
      indentation: '4',
      braceStyle: 'same-line',
      namingConvention: 'camelCase'
    },
    security: {
      inputValidation: true,
      confirmDialog: true,
      xssProtection: true,
      passwordEncrypt: true,
      logLevel: 'detailed',
      rateLimit: false
    },
    performance: {
      lazyLoad: 'route',
      imageOptimization: true,
      paginationThreshold: 100,
      virtualScrollThreshold: 500,
      dbIndex: true
    }
  })
}

// 处理Service模板文件变化
const handleServiceTemplateChange = (file: any) => {
  serviceTemplateFiles.value = [file]
}

// 处理API模板文件变化
const handleApiTemplateChange = (file: any) => {
  apiTemplateFiles.value = [file]
}
</script>

<style scoped>
.collapse-enter-active,
.collapse-leave-active {
  transition: all 0.3s ease;
}

.collapse-enter-from,
.collapse-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
</style>
