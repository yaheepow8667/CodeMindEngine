<template>
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
    <el-card class="mb-8" shadow="hover">
      <!-- 操作按钮区 -->
      <div class="flex flex-wrap justify-between items-center mb-6 gap-4">
        <div class="text-text-secondary flex items-center">
          <i class="fas fa-info-circle mr-1 text-primary"></i>
          <span>配置将应用于所有新生成的项目和代码</span>
        </div>
        <div class="flex space-x-3">
          <el-button type="primary" plain @click="resetConfig">
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
        <el-collapse v-model="activeNames">
          <el-collapse-item name="1">
            <template #title>
              <div class="flex items-center">
                <i class="fas fa-code text-primary mr-3 text-xl"></i>
                <h2 class="text-lg font-semibold">代码规范配置</h2>
              </div>
            </template>
            <div class="px-0 pb-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="single-quote-switch">使用单引号</label>
                      <el-switch v-model="codeStyleConfig.singleQuote" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">生成的代码中使用单引号而非双引号</p>
                  </div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="jsdoc-switch">自动生成JsDoc注释</label>
                      <el-switch v-model="codeStyleConfig.jsdoc" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">为函数、类和组件自动生成文档注释</p>
                  </div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="semicolon-switch">使用分号结尾</label>
                      <el-switch v-model="codeStyleConfig.semicolon" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">在语句结尾添加分号</p>
                  </div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="eslint-switch">启用ESLint规则</label>
                      <el-switch v-model="codeStyleConfig.eslint" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">生成符合ESLint标准的代码</p>
                  </div>
                </div>
                <div>
                  <div class="form-item">
                    <label class="form-label" for="indentation-select">缩进空格数</label>
                    <el-select v-model="codeStyleConfig.indentation" class="form-control">
                      <el-option label="2个空格" value="2" />
                      <el-option label="4个空格" value="4" />
                      <el-option label="使用Tab" value="tab" />
                    </el-select>
                  </div>
                  <div class="form-item">
                    <label class="form-label">函数括号风格</label>
                    <div class="grid grid-cols-2 gap-3">
                      <el-radio v-model="codeStyleConfig.braceStyle" label="same-line" class="radio-option">同一行 (K&amp;R风格)</el-radio>
                      <el-radio v-model="codeStyleConfig.braceStyle" label="new-line" class="radio-option">新行 (Allman风格)</el-radio>
                    </div>
                  </div>
                  <div class="form-item">
                    <label class="form-label">命名规范</label>
                    <div class="grid grid-cols-2 gap-3">
                      <el-radio v-model="codeStyleConfig.namingConvention" label="camelCase" class="radio-option">camelCase</el-radio>
                      <el-radio v-model="codeStyleConfig.namingConvention" label="snake_case" class="radio-option">snake_case</el-radio>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-collapse-item>
          
          <!-- 安全规则配置 -->
          <el-collapse-item name="2">
            <template #title>
              <div class="flex items-center">
                <i class="fas fa-shield-alt text-primary mr-3 text-xl"></i>
                <h2 class="text-lg font-semibold">安全规则配置</h2>
              </div>
            </template>
            <div class="px-0 pb-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="input-validation-switch">自动生成输入验证</label>
                      <el-switch v-model="securityConfig.inputValidation" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">为所有API接口生成输入验证逻辑</p>
                  </div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="confirm-dialog-switch">敏感操作二次确认</label>
                      <el-switch v-model="securityConfig.confirmDialog" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">为删除、修改等敏感操作添加确认对话框</p>
                  </div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="xss-protection-switch">XSS防护</label>
                      <el-switch v-model="securityConfig.xssProtection" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">自动对用户输入进行XSS过滤</p>
                  </div>
                </div>
                <div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="password-encrypt-switch">密码字段加密传输</label>
                      <el-switch v-model="securityConfig.passwordEncrypt" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">密码在传输前进行加密处理</p>
                  </div>
                  <div class="form-item">
                    <label class="form-label" for="log-level-select">敏感操作日志记录</label>
                    <el-select v-model="securityConfig.logLevel" class="form-control">
                      <el-option label="不记录" value="none" />
                      <el-option label="基本信息" value="basic" />
                      <el-option label="详细记录" value="detailed" />
                    </el-select>
                  </div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="rate-limit-switch">API访问限流</label>
                      <el-switch v-model="securityConfig.rateLimit" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">启用API请求频率限制</p>
                  </div>
                </div>
              </div>
            </div>
          </el-collapse-item>
          
          <!-- 性能优化配置 -->
          <el-collapse-item name="3">
            <template #title>
              <div class="flex items-center">
                <i class="fas fa-tachometer-alt text-primary mr-3 text-xl"></i>
                <h2 class="text-lg font-semibold">性能优化配置</h2>
              </div>
            </template>
            <div class="px-0 pb-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <div class="form-item">
                    <label class="form-label">前端组件懒加载</label>
                    <div class="grid grid-cols-1 gap-3">
                      <el-radio v-model="performanceConfig.lazyLoad" label="none" class="radio-option">不启用</el-radio>
                      <el-radio v-model="performanceConfig.lazyLoad" label="route" class="radio-option">路由级别懒加载</el-radio>
                      <el-radio v-model="performanceConfig.lazyLoad" label="component" class="radio-option">组件级别懒加载</el-radio>
                    </div>
                  </div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="image-optimization-switch">图片优化</label>
                      <el-switch v-model="performanceConfig.imageOptimization" />
                    </div>
                    <p class="text-text-tertiary text-sm mt-1">自动生成响应式图片</p>
                  </div>
                </div>
                <div>
                  <div class="form-item">
                    <label class="form-label">表格数据处理策略</label>
                    <div class="form-item">
                      <label class="form-label" for="pagination-threshold">分页阈值</label>
                      <div class="flex items-center">
                        <el-input-number v-model="performanceConfig.paginationThreshold" :min="10" :max="1000" class="w-24" />
                        <span class="mx-2 text-text-tertiary">条数据</span>
                      </div>
                      <p class="text-text-tertiary text-sm mt-1">超过此数量自动启用分页</p>
                    </div>
                    <div class="form-item">
                      <label class="form-label" for="virtual-scroll-threshold">虚拟滚动阈值</label>
                      <div class="flex items-center">
                        <el-input-number v-model="performanceConfig.virtualScrollThreshold" :min="100" :max="2000" class="w-24" />
                        <span class="mx-2 text-text-tertiary">条数据</span>
                      </div>
                      <p class="text-text-tertiary text-sm mt-1">超过此数量自动启用虚拟滚动</p>
                    </div>
                  </div>
                  <div class="form-item">
                    <div class="flex items-center justify-between">
                      <label class="form-label" for="db-index-switch">生成数据库索引建议</label>
                      <el-switch v-model="performanceConfig.dbIndex" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-collapse-item>
          
          <!-- 自定义模板注入点 -->
          <el-collapse-item name="4">
            <template #title>
              <div class="flex items-center">
                <i class="fas fa-file-code text-primary mr-3 text-xl"></i>
                <h2 class="text-lg font-semibold">自定义模板注入点</h2>
              </div>
            </template>
            <div class="px-0 pb-4">
              <p class="text-text-tertiary mb-4">上传自定义模板文件，覆盖平台默认生成的代码结构</p>
              <div class="space-y-6">
                <div class="form-item">
                  <label class="form-label" for="service-template-upload">Service层基类模板</label>
                  <el-upload
                    class="upload-area"
                    action="#"
                    :auto-upload="false"
                    :limit="1"
                    accept=".js,.ts,.vue"
                  >
                    <i class="fas fa-upload text-2xl text-text-tertiary mb-2"></i>
                    <p class="text-text-tertiary mb-3">拖放文件到此处或点击上传</p>
                    <el-button type="primary" plain>选择文件</el-button>
                  </el-upload>
                </div>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

// 折叠面板激活项
const activeNames = ref(['1'])

// 代码规范配置
interface CodeStyleConfig {
  singleQuote: boolean
  jsdoc: boolean
  semicolon: boolean
  eslint: boolean
  indentation: string
  braceStyle: string
  namingConvention: string
}

const codeStyleConfig = reactive<CodeStyleConfig>({
  singleQuote: true,
  jsdoc: true,
  semicolon: false,
  eslint: true,
  indentation: '4',
  braceStyle: 'same-line',
  namingConvention: 'camelCase'
})

// 安全规则配置
interface SecurityConfig {
  inputValidation: boolean
  confirmDialog: boolean
  xssProtection: boolean
  passwordEncrypt: boolean
  logLevel: string
  rateLimit: boolean
}

const securityConfig = reactive<SecurityConfig>({
  inputValidation: true,
  confirmDialog: true,
  xssProtection: true,
  passwordEncrypt: true,
  logLevel: 'detailed',
  rateLimit: false
})

// 性能优化配置
interface PerformanceConfig {
  lazyLoad: string
  imageOptimization: boolean
  paginationThreshold: number
  virtualScrollThreshold: number
  dbIndex: boolean
}

const performanceConfig = reactive<PerformanceConfig>({
  lazyLoad: 'route',
  imageOptimization: true,
  paginationThreshold: 100,
  virtualScrollThreshold: 500,
  dbIndex: true
})

// 保存配置
const saveConfig = () => {
  // 模拟保存配置
  ElMessage.success('配置保存成功')
}

// 重置配置
const resetConfig = () => {
  // 重置所有配置为默认值
  Object.assign(codeStyleConfig, {
    singleQuote: true,
    jsdoc: true,
    semicolon: false,
    eslint: true,
    indentation: '4',
    braceStyle: 'same-line',
    namingConvention: 'camelCase'
  })
  
  Object.assign(securityConfig, {
    inputValidation: true,
    confirmDialog: true,
    xssProtection: true,
    passwordEncrypt: true,
    logLevel: 'detailed',
    rateLimit: false
  })
  
  Object.assign(performanceConfig, {
    lazyLoad: 'route',
    imageOptimization: true,
    paginationThreshold: 100,
    virtualScrollThreshold: 500,
    dbIndex: true
  })
  
  ElMessage.success('配置已重置为默认值')
}
</script>

<style scoped lang="scss">
/* 保持Tailwind CSS样式不变，仅添加必要的组件样式调整 */
.radio-option {
  @apply flex items-center p-3 border border-border-color rounded-md cursor-pointer hover:bg-hover-bg transition-all duration-200;
}

.upload-area {
  @apply border-2 border-dashed border-border-color rounded-md p-6 text-center hover:border-primary transition-colors duration-200;
}
</style>