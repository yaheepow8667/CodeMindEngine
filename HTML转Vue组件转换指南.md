# HTML 转 Vue 组件转换指南（ruoyi-fastapi-frontend 适配版）


## 1. 概述

本指南基于 `ruoyi-fastapi-frontend` 项目技术栈与架构规范，详细介绍将 `html/page` 目录下的静态 HTML 页面转换为符合项目风格的 Vue 组件的流程。转换需严格遵循项目现有技术栈（Vue3 + Element Plus + TypeScript + Pinia + SCSS）及代码规范，确保组件无缝集成、风格统一且可维护。


## 2. 转换阶段详解

### 2.1 阶段一：项目分析与准备

**阶段目标**：对齐原 HTML 页面特性与 `ruoyi-fastapi-frontend` 项目规范。

**核心工作**：
1. **原 HTML 页面分析**（聚焦 `html/page` 目录）：
   - 识别模块：从 `templateMarket.html`、`generationWizard.html` 等页面中提取核心模块（如模板卡片、生成进度条、任务列表）。
   - 布局特征：解析 Tailwind CSS 响应式类（如 `grid-cols-1 md:grid-cols-3`）、Flex 布局（`flex justify-between`）的实现逻辑。
   - 样式提取：记录自定义工具类（如 `card-hover`、`text-text-secondary`）及颜色方案（如 `bg-success/10`、`text-primary`）。

2. **目标项目技术栈适配**：
   - 核心框架：Vue3（`setup` 语法糖）、TypeScript 类型约束、Vite 构建工具。
   - UI 组件库：优先使用 Element Plus（`el-*` 组件，如 `el-card`、`el-button`），部分场景兼容 Ant Design Vue（如 `a-progress`）。
   - 状态管理：通过 Pinia 管理全局状态（参考 `src/store/modules/permission.js` 模式）。
   - 样式系统：基于 SCSS 变量（复用项目主题色 `var(--el-color-primary)` 等），禁止直接使用 Tailwind 类。
   - 代码生成工具：利用 `src/utils/generator` 下的 `html.js`（模板生成）、`js.js`（逻辑生成）辅助转换。

**输出成果**：
- HTML 模块与项目组件映射表
- 样式变量替换对照表（如 `bg-primary` → `var(--el-color-primary)`）


### 2.2 阶段二：组件结构规划

**阶段目标**：基于项目目录规范设计组件拆分策略。

**核心工作**：
1. **组件拆分原则**：
   - 遵循项目目录结构：页面级组件放 `src/views`（如 `src/views/tool/build/index.vue`），复用组件放 `src/components`。
   - 粒度参考：参考 `DraggableItem.vue`、`RightPanel.vue` 等现有组件，单个组件代码量控制在 300 行内。
   - 示例拆分：将 `generationWizard.html` 拆分为 `GenerationWizard.vue`（主页面）、`TaskCard.vue`（任务卡片）、`ProgressBar.vue`（进度条）。

2. **数据结构设计**：
   - 类型定义：使用 TypeScript 接口约束数据（如任务卡片定义 `interface Task { id: string; status: 'pending' | 'completed'; ... }`）。
   - 数据传递：父传子用 Props（参考 `DraggableItem` 组件的 props 定义），子传父用 Emit，跨组件用 Pinia。

**输出成果**：
- 组件目录结构示意图（如 `views/generation/Wizard.vue` → `components/TaskCard.vue`）
- TypeScript 接口定义文件（如 `src/types/generation.ts`）


### 2.3 阶段三：模板转换与适配

**阶段目标**：将 HTML 结构转换为 Vue 模板，并适配 Element Plus 组件。

**核心工作**：
1. **HTML 转 Vue 模板**：
   - 动态渲染：使用 `v-for` 渲染列表（参考 `drawingList` 在 `build/index.vue` 中的渲染方式）。
   - 条件渲染：用 `v-if/v-else` 处理状态展示（如任务完成/未完成状态）。
   - 事件绑定：统一使用 `@click` 而非原生 `onclick`，事件处理函数命名遵循 `handleXxx` 规范（如 `handleContinueLearning`）。

2. **Element Plus 组件替换**：
   - 卡片：`div.rounded-xl.shadow-md` → `el-card`（设置 `shadow="hover"`、`bordered="false"`）。
   - 按钮：`button.bg-primary` → `el-button`（指定 `type="primary"`、`size="small"`）。
   - 进度条：`div.bg-neutral-dark` → `el-progress`（绑定 `percentage` 属性）。
   - 图标：`i.fas` → Element Plus 内置图标（如 `<Clock />` 替代 `i.fas.fa-clock`，参考 `build/index.vue` 中的图标使用）。

3. **利用生成工具辅助**：
   - 调用 `src/utils/generator/html.js` 中的 `vueTemplate` 函数生成基础模板结构。
   - 表单类组件参考 `buildFormTemplate` 函数逻辑，自动注入 `el-form` 与 `el-form-item` 结构。

**输出成果**：
- 适配后的 Vue 模板文件（含组件库替换记录）


### 2.4 阶段四：样式系统迁移

**阶段目标**：优先重用 Tailwind CSS 样式，确保其在 Vue 组件中正常工作，仅在必要时进行 Tailwind CSS 到 SCSS 的转换。

**核心工作**：
1. **Tailwind CSS 样式重用（优先）**：
   - 直接在 Vue 组件的模板中保留 Tailwind CSS 类名，无需转换。
   - 确保项目已安装 Tailwind CSS 依赖：`npm install tailwindcss postcss autoprefixer`。
   - 确保项目已正确配置 Tailwind CSS：
     - 生成配置文件：`npx tailwindcss init -p`
     - 在 `tailwind.config.js` 中配置内容路径：`content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"]`
     - 在 `src/assets/styles/index.scss` 中导入 Tailwind 指令：
       ```scss
       @tailwind base;
       @tailwind components;
       @tailwind utilities;
       ```

2. **Tailwind 转 SCSS（仅在必要时）**：
   - 对于需要深度定制或与项目 SCSS 系统集成的样式，进行 Tailwind CSS 到 SCSS 的转换。
   - 布局转换：`flex justify-between` → `.parent { display: flex; justify-content: space-between; }`。
   - 响应式转换：`md:grid-cols-3` → `@media (min-width: $screen-md) { grid-template-columns: repeat(3, 1fr); }`（复用项目断点变量）。
   - 颜色替换：`bg-success/10` → `background-color: var(--el-color-success-light-9);`（使用 Element Plus 内置浅色变量）。

3. **样式隔离与复用**：
   - 使用 `<style lang="scss" scoped>` 确保自定义 SCSS 样式的隔离，避免污染全局。
   - 公共样式提取到 `src/styles` 目录（如 `_mixins.scss`），参考项目现有 SCSS 结构。
   - 禁止硬编码颜色值，必须使用主题变量（如 `var(--el-color-primary)`、`var(--el-text-color-secondary)`）。

**输出成果**：
- 配置完成的 Tailwind CSS 环境
- 重用了 Tailwind CSS 样式的 Vue 组件
- （可选）部分转换为 SCSS 的样式文件
- 样式变量映射表


### 2.5 阶段五：交互逻辑与状态管理

**阶段目标**：实现符合项目规范的交互逻辑与状态管理。

**核心工作**：
1. **交互逻辑开发**：
   - 事件处理：参考 `build/index.vue` 中的 `activeFormItem`、`copy` 等函数，使用 `setup` 语法糖定义方法。
   - API 集成：通过项目封装的 Axios 工具调用接口（参考 `@/api/generation` 中的 `parseRequirements` 调用方式）。
   - 弹窗逻辑：使用 `ElDialog` 组件，参考 `dialogWrapper` 函数生成弹窗结构。

2. **状态管理**：
   - 局部状态：用 `ref`/`reactive` 管理组件内部状态（如 `drawingList` 在 `build/index.vue` 中的定义）。
   - 全局状态：通过 Pinia 定义 store（参考 `permission.js` 的模块结构），如学习进度需全局共享时存入 `src/store/modules/learning.js`。

3. **类型约束**：
   - 为 Props、事件、API 响应数据添加 TypeScript 类型（如 `defineProps<{ task: Task }>()`）。

**输出成果**：
- 交互逻辑代码（含 TypeScript 类型定义）
- Pinia store 模块（如需全局状态）


### 2.6 阶段六：集成与测试

**阶段目标**：确保组件在项目中正常运行且符合规范。

**核心工作**：
1. **路由集成**：
   - 在 `src/router` 中配置路由，参考权限路由逻辑（`permission.js`），设置 `meta` 信息（如 `title`、`icon`、`roles`）。

2. **测试验证**：
   - 功能测试：验证所有交互（如按钮点击、状态切换）是否正常（参考 `generationWizard.html` 中的流程）。
   - 样式测试：在不同屏幕尺寸下检查响应式布局（复用项目断点 `$screen-sm`、`$screen-md` 等）。
   - 性能测试：避免不必要的重渲染，复杂列表使用 `v-memo` 优化（参考项目现有性能实践）。

3. **代码规范检查**：
   - 命名规范：组件名 PascalCase（如 `TaskCard.vue`），方法名 camelCase（如 `handleSubmit`）。
   - 注释规范：为组件、Props、核心方法添加注释（参考 `html.js` 中的函数注释）。

**输出成果**：
- 路由配置代码
- 测试报告（含功能、样式、性能验证结果）


## 3. 提示词工程（增强版）

### 3.1 项目分析阶段提示词

**HTML 页面分析**：
```
基于 ruoyi-fastapi-frontend 项目，分析 html/page/templateMarket.html：
1. 页面包含哪些可复用模块（如卡片、列表、按钮组）？
2. 哪些 Tailwind 类需要转换为 Element Plus 样式（如 bg-primary → 组件主题色）？
3. 响应式布局（如 md:grid-cols-3）如何映射到项目的 SCSS 媒体查询？
4. 交互元素（如按钮、链接）的行为逻辑是什么？
```

**项目技术栈适配**：
```
针对 ruoyi-fastapi-frontend 项目，回答：
1. Element Plus 组件中，哪类组件可替代 HTML 中的卡片（div.rounded-xl.shadow-md）？
2. 项目中如何引入图标（如替代 i.fas.fa-check）？
3. 状态管理优先用 Pinia 的哪种模式（模块拆分/单一 store）？
4. 表单类组件的标准结构是什么（参考 src/utils/generator/html.js）？
```


### 3.2 模板转换提示词

**Element Plus 组件替换**：
```
将以下 HTML 转换为 ruoyi-fastapi-frontend 风格的 Vue 模板：
1. 用 el-card 替代 div.bg-white.rounded-xl.shadow-md，需设置 shadow 和 bordered 属性。
2. 用 el-button 替代 button.bg-primary，指定 type="primary" 和 size。
3. 用 Element Plus 内置图标（如 CheckCircle）替代 i.fas 图标。
4. 确保结构符合项目模板规范（参考 src/views/tool/build/index.vue）。
```


### 3.3 样式迁移提示词

**Tailwind 转 SCSS**：
```
将以下 Tailwind 样式转换为 ruoyi-fastapi-frontend 的 SCSS：
1. .card-hover { @apply transition-all duration-300 hover:shadow-lg hover:-translate-y-1; }
2. 需使用项目主题变量（如 var(--el-color-primary)），禁止硬编码颜色。
3. 响应式类 md:grid-cols-3 转换为 SCSS 媒体查询（使用项目断点变量）。
4. 确保样式隔离（使用 scoped）且不与现有样式冲突。
```


## 4. 转换示例（基于项目实际代码）

### 4.1 原 HTML 片段（来自 html/page/generationWizard.html）

```html
<div class="bg-white rounded-xl shadow-md p-6 card-hover">
  <div class="flex justify-between items-center mb-4">
    <span class="text-sm font-medium text-text-secondary">代码行数</span>
    <span class="font-medium">约 5,280 行</span>
  </div>
  <div>
    <div class="flex justify-between mb-1">
      <span class="text-sm text-text-secondary">代码质量评分</span>
      <span class="font-medium text-success">92/100</span>
    </div>
    <div class="w-full bg-neutral-dark rounded-full h-2">
      <div class="bg-success h-2 rounded-full" style="width: 92%"></div>
    </div>
  </div>
</div>
```

### 4.2 转换后的 Vue 组件

```vue
<template>
  <el-card class="quality-card" shadow="hover" bordered="false">
    <div class="quality-card__row">
      <span class="quality-card__label">代码行数</span>
      <span class="quality-card__value">约 5,280 行</span>
    </div>
    
    <div class="quality-card__score">
      <div class="quality-card__score-row">
        <span class="quality-card__label">代码质量评分</span>
        <span class="quality-card__value quality-card__value--success">92/100</span>
      </div>
      <el-progress 
        :percentage="92" 
        stroke-width="6" 
        stroke-color="var(--el-color-success)"
        background-color="var(--el-bg-color-secondary)"
      />
    </div>
  </el-card>
</template>

<script setup lang="ts">
// 类型定义（符合项目TypeScript规范）
interface QualityData {
  lineCount: string
  score: number
}

// Props定义（使用TypeScript约束）
const props = defineProps<{
  data: QualityData
}>()
</script>

<style lang="scss" scoped>
.quality-card {
  border-radius: 8px;
  transition: all 0.3s ease; // 复用原card-hover动画
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  }
  
  &__row, &__score-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  
  &__label {
    font-size: 14px;
    color: var(--el-text-color-secondary); // 项目主题变量
  }
  
  &__value {
    font-weight: 500;
    
    &--success {
      color: var(--el-color-success); // 复用Element Plus成功色
    }
  }
  
  &__score {
    margin-top: 16px;
  }
}
</style>
```


## 5. 项目特有注意事项

1. **代码生成工具适配**：转换后的组件需兼容 `src/utils/generator` 工具，模板结构应符合 `html.js` 中的生成逻辑（如表单需包含 `el-form`、`el-form-item` 嵌套）。
   
2. **权限路由集成**：页面级组件需在路由配置中添加权限元信息（参考 `permission.js`），如 `meta: { roles: ['admin'] }`。

3. **状态管理规范**：全局状态需遵循项目 Pinia 模块结构（如 `state`、`getters`、`actions` 拆分），避免直接操作原始数据。

4. **样式变量复用**：必须使用 Element Plus 内置变量（如 `var(--el-color-primary)`）和项目自定义变量（如 `$screen-md`），禁止新增全局样式。


## 6. 常见问题与解决方案（项目适配版）

| 问题 | 解决方案 |
|------|----------|
| Element Plus 组件样式与原 HTML 不一致 | 调整组件 `size`、`shadow` 等属性，通过 SCSS 补充样式（如 `::v-deep .el-card__body { padding: 16px; }`） |
| 响应式布局在项目中失效 | 复用项目 `src/styles/mixin.scss` 中的断点混入（如 `@include respond-to(md) { ... }`） |
| 与代码生成器冲突 | 确保组件模板结构符合 `html.js` 中的解析规则（如表单绑定 `:model` 与 `ref` 命名一致） |
| Pinia 状态更新不及时 | 遵循响应式规范，使用 `storeToRefs` 解构状态，通过 `actions` 更新数据 |


## 7. 总结

本指南基于 `ruoyi-fastapi-frontend` 项目实际技术栈与规范，强调组件与项目生态的兼容性。通过六个阶段的系统转换，确保 HTML 页面转换后的 Vue 组件符合项目风格、性能要求及可维护性标准。转换过程中应优先复用项目现有工具（如代码生成器、样式变量），严格遵循目录结构与命名规范，最终实现组件的无缝集成。

**文档版本**：1.0  
**适用项目**：ruoyi-fastapi-frontend  
**适配范围**：html/page 目录下静态页面转换