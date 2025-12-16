<template>
  <div class="help-center-container p-4 md:p-6">
    <!-- 顶部导航 -->
    <div class="help-nav">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange" class="help-tabs">
        <el-tab-pane label="帮助首页" name="home">
          <!-- 搜索框 -->
          <div class="help-search">
            <i class="fas fa-search text-xl"> </i>
            <el-input v-model="searchQuery" placeholder="请问您遇到什么问题？" />
          </div>
          <!-- 快速入门指南 -->
          <div class="mb-8">
            <h2 class="text-xl font-semibold mb-5 text-text-primary"> 快速入门指南 </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
              <div 
                v-for="(step, index) in quickStartSteps" 
                :key="index" 
                class="step-card"
                @click="handleStepClick(index)"
              >
                <div class="step-number">
                  {{ index + 1 }}
                </div>
                <div class="step-content">
                  <div class="step-title">
                    {{ step.title }}
                  </div>
                  <div class="step-desc">
                    {{ step.description }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- 常见问题分类 -->
          <div class="mb-8">
            <h2 class="text-xl font-semibold mb-5 text-text-primary"> 常见问题分类 </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              <div 
                v-for="(category, index) in faqCategories" 
                :key="index" 
                class="help-card"
                @click="handleCategoryClick(category)"
              >
                <div class="help-card-title flex items-center">
                  <i :class="category.icon" class="text-primary mr-2"> </i> {{ category.title }}
                </div>
                <div class="help-card-content">
                  {{ category.description }}
                </div>
              </div>
            </div>
          </div>
          <!-- 热门问题 -->
          <div>
            <h2 class="text-xl font-semibold mb-5 text-text-primary"> 热门问题 </h2>
            <el-collapse accordion>
              <el-collapse-item 
                v-for="(faq, index) in hotFaqs" 
                :key="index" 
                :title="faq.question"
                class="faq-item"
              >
                <div class="faq-answer">
                  {{ faq.answer }}
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-tab-pane>

        <!-- 文档页 -->
        <el-tab-pane label="文档" name="docs">
          <div class="flex flex-col md:flex-row gap-6">
            <!-- 文档目录 -->
            <div class="md:w-1/4 lg:w-1/5">
              <div class="help-card sticky top-4">
                <div class="help-card-title">
                  文档目录
                </div>
                <el-tree
                  :data="documentTree"
                  node-key="id"
                  default-expanded-keys="[3]"
                  default-checked-keys="[3]"
                  highlight-current
                  @node-click="handleDocumentClick"
                  class="text-sm"
                />
              </div>
            </div>
            <!-- 文档内容 -->
            <div class="md:w-3/4 lg:w-4/5">
              <div class="help-card">
                <div class="help-card-title text-xl">
                  {{ currentDocument.title }}
                </div>
                <div class="help-card-content">
                  <h3 class="text-lg font-semibold mt-6 mb-3"> {{ currentDocument.subtitle }} </h3>
                  <p class="mb-4"> {{ currentDocument.intro }} </p>
                  <h3 class="text-lg font-semibold mt-6 mb-3"> 基本工作流程 </h3>
                  <ol class="list-decimal pl-5 mb-4 space-y-2">
                    <li v-for="(step, index) in currentDocument.workflow" :key="index">
                      {{ step }}
                    </li>
                  </ol>
                  <h3 class="text-lg font-semibold mt-6 mb-3"> 创建您的第一个项目 </h3>
                  <p class="mb-4"> {{ currentDocument.firstProjectIntro }} </p>
                  <ol class="list-decimal pl-5 mb-4 space-y-4">
                    <li v-for="(step, index) in currentDocument.firstProjectSteps" :key="index">
                      <p class="font-medium">{{ step.title }}</p>
                      <p class="text-sm text-text-secondary mt-1">{{ step.description }}</p>
                    </li>
                  </ol>
                  <div class="bg-primary-light/30 p-4 rounded-lg mt-6">
                    <div class="font-medium flex items-center mb-2">
                      <i class="fas fa-lightbulb text-primary mr-2"> </i> 小贴士
                    </div>
                    <p class="text-sm text-text-secondary"> {{ currentDocument.tip }} </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 教程页 -->
        <el-tab-pane label="教程" name="tutorials">
          <!-- 筛选栏 -->
          <div class="help-card mb-6">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div class="flex flex-wrap gap-3">
                <el-select v-model="techStackFilter" placeholder="所有技术栈">
                  <el-option label="所有技术栈" value="all" />
                  <el-option label="React" value="react" />
                  <el-option label="Vue" value="vue" />
                  <el-option label="Angular" value="angular" />
                  <el-option label="Node.js" value="nodejs" />
                  <el-option label="Python" value="python" />
                </el-select>
                <el-select v-model="difficultyFilter" placeholder="所有难度">
                  <el-option label="所有难度" value="all" />
                  <el-option label="入门" value="beginner" />
                  <el-option label="中级" value="intermediate" />
                  <el-option label="高级" value="advanced" />
                </el-select>
                <el-select v-model="functionFilter" placeholder="所有功能">
                  <el-option label="所有功能" value="all" />
                  <el-option label="UI生成" value="ui" />
                  <el-option label="API生成" value="api" />
                  <el-option label="数据库设计" value="database" />
                  <el-option label="部署流程" value="deployment" />
                </el-select>
              </div>
              <div class="flex gap-2">
                <el-button :type="viewMode === 'grid' ? 'primary' : 'default'" size="small" @click="viewMode = 'grid'">
                  <i class="fas fa-th-large mr-1"> </i> 网格视图
                </el-button>
                <el-button :type="viewMode === 'list' ? 'primary' : 'default'" size="small" @click="viewMode = 'list'">
                  <i class="fas fa-list mr-1"> </i> 列表视图
                </el-button>
              </div>
            </div>
          </div>
          <!-- 教程列表 -->
          <div :class="viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5' : 'space-y-5'">
            <div 
              v-for="(tutorial, index) in filteredTutorials" 
              :key="index" 
              :class="viewMode === 'grid' ? 'tutorial-card' : 'flex help-card'"
              @click="handleTutorialClick(tutorial)"
            >
              <img v-if="viewMode === 'grid'" :src="tutorial.image" :alt="tutorial.title" class="tutorial-image">
              <img v-else :src="tutorial.image" :alt="tutorial.title" class="w-32 h-32 object-cover mr-4">
              <div class="tutorial-content" :class="viewMode === 'list' ? 'flex-1' : ''">
                <div class="tutorial-title">
                  {{ tutorial.title }}
                </div>
                <p class="text-sm text-text-secondary line-clamp-2"> {{ tutorial.description }} </p>
                <div class="tutorial-meta">
                  <span> <i class="fas fa-clock"> </i> {{ tutorial.duration }} </span>
                  <span> <i class="fas fa-signal"> </i> {{ tutorial.difficulty }} </span>
                  <span> <i class="fas fa-code"> </i> {{ tutorial.techStack }} </span>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 社区页 -->
        <el-tab-pane label="社区" name="community">
          <div class="flex flex-col lg:flex-row gap-6">
            <!-- 左侧内容 -->
            <div class="lg:w-2/3">
              <!-- 动态信息流 -->
              <div class="help-card mb-6">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-semibold text-text-primary"> 社区动态 </h3>
                  <el-button type="primary" size="small" @click="publishPost"> 发布新帖 </el-button>
                </div>
                <div class="space-y-5">
                  <div 
                    v-for="(post, index) in communityPosts" 
                    :key="index" 
                    class="community-post"
                    @click="handlePostClick(post)"
                  >
                    <div class="post-header">
                      <img :src="post.avatar" :alt="post.author" class="post-avatar">
                      <span class="post-author"> {{ post.author }} </span>
                      <span class="post-time"> {{ post.time }} </span>
                    </div>
                    <div class="post-title">
                      {{ post.title }}
                    </div>
                    <div class="post-content">
                      {{ post.content }}
                    </div>
                    <div class="post-meta">
                      <span> <i class="fas fa-comment"> </i> {{ post.comments }} </span>
                      <span> <i class="fas fa-thumbs-up"> </i> {{ post.likes }} </span>
                      <span> <i class="fas fa-eye"> </i> {{ post.views }} </span>
                    </div>
                  </div>
                </div>
                <div class="text-center mt-6">
                  <el-button type="default" @click="loadMorePosts"> 加载更多 </el-button>
                </div>
              </div>
              <!-- 分类讨论区 -->
              <div class="help-card">
                <h3 class="text-lg font-semibold text-text-primary mb-4"> 分类讨论区 </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div 
                    v-for="(forum, index) in forums" 
                    :key="index" 
                    class="border border-border-color rounded-lg p-4 hover:border-primary/50 hover:shadow-md transition-all duration-300 cursor-pointer"
                    @click="handleForumClick(forum)"
                  >
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-full bg-primary-light flex items-center justify-center text-primary mr-3">
                        <i :class="forum.icon"> </i>
                      </div>
                      <div>
                        <div class="font-medium text-text-primary">
                          {{ forum.name }}
                        </div>
                        <div class="text-sm text-text-tertiary">
                          {{ forum.description }}
                        </div>
                      </div>
                      <div class="ml-auto text-right">
                        <div class="font-semibold text-text-primary">
                          {{ forum.topics }}
                        </div>
                        <div class="text-xs text-text-tertiary">
                          主题
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 右侧边栏 -->
            <div class="lg:w-1/3">
              <!-- 贡献者榜单 -->
              <div class="help-card mb-6 sticky top-4">
                <h3 class="text-lg font-semibold text-text-primary mb-4"> 社区贡献者 </h3>
                <div class="space-y-4">
                  <div 
                    v-for="(contributor, index) in contributors" 
                    :key="index" 
                    class="flex items-center"
                    @click="handleContributorClick(contributor)"
                  >
                    <img :src="contributor.avatar" :alt="contributor.name" class="w-10 h-10 rounded-full object-cover mr-3">
                    <div class="flex-1">
                      <div class="font-medium text-text-primary">
                        {{ contributor.name }}
                      </div>
                      <div class="text-xs text-text-tertiary">
                        模板贡献：{{ contributor.templates }}个
                      </div>
                    </div>
                    <div :class="index === 0 ? 'text-primary' : 'text-text-secondary'" class="font-bold">
                      {{ index + 1 }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 在线客服页 -->
        <el-tab-pane label="在线客服" name="support">
          <div class="max-w-2xl mx-auto">
            <div class="help-card text-center mb-8">
              <div class="text-5xl text-primary mb-4">
                <i class="fas fa-comments"> </i>
              </div>
              <h2 class="text-2xl font-semibold mb-2 text-text-primary"> 在线客服支持 </h2>
              <p class="text-text-secondary mb-6"> 我们的客服团队随时为您提供帮助，解答您在使用过程中遇到的问题 </p>
              <div class="flex flex-col sm:flex-row justify-center gap-3">
                <el-button type="primary" @click="startChat"> <i class="fas fa-headphones-alt mr-2"> </i> 开始对话 </el-button>
                <el-button type="default" @click="submitTicket"> <i class="fas fa-file-alt mr-2"> </i> 提交工单 </el-button>
              </div>
            </div>
            <div class="help-card mb-8">
              <h3 class="text-lg font-semibold mb-4 text-text-primary"> 常见问题 </h3>
              <el-collapse accordion>
                <el-collapse-item 
                  v-for="(faq, index) in supportFaqs" 
                  :key="index" 
                  :title="faq.question"
                  class="faq-item"
                >
                  <div class="faq-answer">
                    {{ faq.answer }}
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
            <div class="help-card">
              <h3 class="text-lg font-semibold mb-4 text-text-primary"> 联系我们 </h3>
              <div class="space-y-4">
                <div class="flex items-start">
                  <div class="w-10 h-10 rounded-full bg-primary-light flex items-center justify-center text-primary mr-4 flex-shrink-0">
                    <i class="fas fa-envelope"> </i>
                  </div>
                  <div>
                    <div class="font-medium text-text-primary">
                      电子邮件
                    </div>
                    <p class="text-text-secondary"> support@zhimayinqing.com </p>
                    <p class="text-sm text-text-tertiary mt-1"> 我们通常会在1个工作日内回复您的邮件 </p>
                  </div>
                </div>
                <div class="flex items-start">
                  <div class="w-10 h-10 rounded-full bg-primary-light flex items-center justify-center text-primary mr-4 flex-shrink-0">
                    <i class="fas fa-phone"> </i>
                  </div>
                  <div>
                    <div class="font-medium text-text-primary">
                      电话支持
                    </div>
                    <p class="text-text-secondary"> 400-123-4567 </p>
                    <p class="text-sm text-text-tertiary mt-1"> 工作时间：周一至周五 9:00-18:00 </p>
                  </div>
                </div>
                <div class="flex items-start">
                  <div class="w-10 h-10 rounded-full bg-primary-light flex items-center justify-center text-primary mr-4 flex-shrink-0">
                    <i class="fas fa-map-marker-alt"> </i>
                  </div>
                  <div>
                    <div class="font-medium text-text-primary">
                      公司地址
                    </div>
                    <p class="text-text-secondary"> 北京市海淀区中关村科技园区8号楼15层 </p>
                    <p class="text-sm text-text-tertiary mt-1"> 邮编：100080 </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 客服按钮 -->
    <div class="support-button" id="support-button" @click="toggleSupportModal">
      <i class="fas fa-headphones-alt"> </i>
    </div>
    <!-- 客服弹窗 -->
    <div 
      class="support-modal" 
      id="support-modal"
      :class="{ 'show': showSupportModal }"
    >
      <div class="modal-header">
        <span> 在线客服 </span>
        <i class="fas fa-times cursor-pointer" @click="closeSupportModal"> </i>
      </div>
      <div class="modal-body">
        <p class="text-sm text-text-secondary mb-4"> 您好！有什么可以帮助您的吗？ </p>
        <div class="space-y-2 mb-4">
          <div 
            v-for="(question, index) in quickQuestions" 
            :key="index" 
            class="quick-question"
            @click="askQuestion(question)"
          >
            {{ question }}
          </div>
        </div>
        <div class="text-xs text-text-tertiary text-center">
          <p> 客服工作时间：周一至周五 9:00-18:00 </p>
          <p class="mt-1"> 非工作时间您可以留言，我们会尽快回复 </p>
        </div>
      </div>
      <div class="modal-footer relative">
        <el-input 
          v-model="supportMessage" 
          placeholder="输入您想咨询的问题..."
          @keyup.enter="sendMessage"
        />
        <button class="text-primary" @click="sendMessage"> <i class="fas fa-paper-plane"> </i> </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { ElMessage } from 'element-plus';

// 状态管理
const activeTab = ref('home');
const searchQuery = ref('');
const showSupportModal = ref(false);
const supportMessage = ref('');

// 筛选状态
const techStackFilter = ref('all');
const difficultyFilter = ref('all');
const functionFilter = ref('all');
const viewMode = ref('grid');

// 快速入门指南数据
const quickStartSteps = reactive([
  { title: '注册与登录', description: '创建账户并登录智码引擎平台，开始您的低代码开发之旅。' },
  { title: '描述您的应用', description: '使用自然语言描述您想要创建的应用功能和需求。' },
  { title: '调整与生成', description: '根据需求调整技术栈和配置，一键生成完整项目代码。' },
  { title: '运行与部署', description: '本地运行项目进行测试，满意后一键部署到您的服务器。' }
]);

// 常见问题分类数据
const faqCategories = reactive([
  { title: '账户与计费', description: '关于账户注册、登录、会员套餐、支付方式等相关问题。', icon: 'fas fa-user-circle' },
  { title: '生成过程问题', description: '应用描述、技术栈选择、代码生成过程中遇到的常见问题。', icon: 'fas fa-cogs' },
  { title: '项目管理', description: '项目创建、保存、导出、版本控制等项目管理相关问题。', icon: 'fas fa-folder-open' },
  { title: '团队协作', description: '团队创建、成员邀请、权限管理等协作相关问题。', icon: 'fas fa-users' },
  { title: '部署与运维', description: '项目部署、服务器配置、域名绑定等运维相关问题。', icon: 'fas fa-cloud-upload-alt' },
  { title: '其他问题', description: '不属于以上分类的其他问题，欢迎联系我们的客服团队。', icon: 'fas fa-life-ring' }
]);

// 热门问题数据
const hotFaqs = reactive([
  { question: '智码引擎支持哪些技术栈？', answer: '智码引擎支持多种主流技术栈，包括前端框架如React、Vue、Angular，后端语言如Node.js、Python、Java、Go，数据库如MySQL、PostgreSQL、MongoDB等。您可以根据项目需求自由选择和组合这些技术。' },
  { question: '生成的代码可以导出吗？', answer: '是的，智码引擎生成的所有代码都可以完整导出到本地，包括源代码文件、配置文件和数据库脚本。您也可以直接将代码推送到GitHub、GitLab等代码仓库。' },
  { question: '如何邀请团队成员协作？', answer: '在项目详情页面，点击"团队协作"按钮，输入成员邮箱并设置相应权限，即可邀请团队成员共同参与项目开发。被邀请者将收到邮件通知，接受邀请后即可加入项目。' },
  { question: '免费版和付费版有什么区别？', answer: '免费版用户每月可生成3个项目，支持基础功能和部分技术栈。付费版根据套餐不同，提供更多的生成次数、高级技术栈支持、优先客服、团队协作等功能。详细对比请查看我们的 pricing 页面。' },
  { question: '生成的代码有版权吗？', answer: '您使用智码引擎生成的所有代码的版权归您所有，您可以将其用于任何商业或非商业项目，无需支付额外的版权费用。' }
]);

// 文档树数据
const documentTree = reactive([
  { id: 1, label: '产品介绍' },
  { id: 2, label: '核心概念' },
  { id: 3, label: '用户指南', children: [
    { id: 31, label: '注册与登录' },
    { id: 32, label: '创建项目' },
    { id: 33, label: '生成代码' },
    { id: 34, label: '项目管理' },
    { id: 35, label: '团队协作' }
  ]},
  { id: 4, label: 'API参考' },
  { id: 5, label: '最佳实践' },
  { id: 6, label: '故障排除' }
]);

// 当前文档内容
const currentDocument = reactive({
  title: '用户指南',
  subtitle: '欢迎使用智码引擎',
  intro: '智码引擎是一款AI驱动的低代码开发平台，旨在帮助开发者快速构建高质量的应用程序。通过自然语言描述需求，智码引擎可以自动生成完整的项目代码，大大提高开发效率。',
  workflow: [
    '使用自然语言描述您的应用需求',
    '选择合适的技术栈和配置',
    '生成项目代码',
    '下载或部署生成的代码',
    '根据需要进行二次开发'
  ],
  firstProjectIntro: '登录智码引擎后，您可以通过以下步骤创建您的第一个项目：',
  firstProjectSteps: [
    { title: '点击首页的"创建项目"按钮', description: '在智码引擎首页，您会看到醒目的"创建项目"按钮，点击进入项目创建流程。' },
    { title: '输入项目信息', description: '填写项目名称、描述，并选择项目类型（Web应用、移动应用等）。' },
    { title: '描述您的应用需求', description: '在需求描述框中，使用自然语言详细描述您的应用功能和特性。越详细的描述将获得越精准的代码生成结果。' },
    { title: '选择技术栈', description: '根据您的需求选择合适的前端框架、后端语言和数据库。系统也会根据您的需求描述推荐合适的技术组合。' },
    { title: '生成代码', description: '点击"生成代码"按钮，智码引擎将开始分析您的需求并生成相应的代码。这个过程通常需要几秒钟到几分钟不等，取决于项目复杂度。' }
  ],
  tip: '为了获得最佳的代码生成效果，建议您的需求描述包含以下几个方面：应用的主要功能、目标用户、核心业务流程、所需的数据模型和特殊要求等。'
});

// 教程数据
const tutorials = reactive([
  { title: 'React入门到精通：构建现代Web应用', description: '学习如何使用React框架构建现代化的Web应用，从基础概念到高级特性的全面讲解。', duration: '2小时30分', difficulty: '中级', techStack: 'React', image: './helpCenter/6afcc5febc0deb65f8f9de2e833ddc54.png' },
  { title: 'Vue3实战：组件化开发与状态管理', description: '掌握Vue3的Composition API和组件化开发思想，学习Pinia状态管理的最佳实践。', duration: '3小时15分', difficulty: '中级', techStack: 'Vue', image: './helpCenter/6b808e4adf9271d5b1d0e8105ba72fc1.png' },
  { title: '数据库设计最佳实践：从概念到实现', description: '学习如何设计高效、可扩展的数据库结构，包括实体关系设计、索引优化和查询性能提升。', duration: '1小时45分', difficulty: '中级', techStack: 'SQL', image: './helpCenter/38cefd98e94328791f8e5fa474c02a29.png' },
  { title: 'RESTful API设计与实现：Node.js全栈开发', description: '使用Node.js和Express构建符合REST规范的API服务，包括认证授权、数据验证和错误处理。', duration: '2小时45分', difficulty: '高级', techStack: 'Node.js', image: './helpCenter/40ec887077891f65100e4ed56a127ced.png' },
  { title: '现代应用部署流程：CI/CD与云服务', description: '学习如何搭建自动化部署流程，使用GitHub Actions实现CI/CD，并部署到AWS、Azure或阿里云。', duration: '2小时10分', difficulty: '中级', techStack: 'DevOps', image: './helpCenter/de9b178ae389a964f763401916b7a350.png' },
  { title: '智码引擎高级技巧：AI代码生成优化', description: '掌握如何编写更有效的需求描述，优化AI生成代码的质量，以及自定义生成规则的高级技巧。', duration: '1小时40分', difficulty: '入门', techStack: 'AI生成', image: './helpCenter/271e2fa0072a019e69aba92d96043bca.png' }
]);

// 过滤后的教程数据
const filteredTutorials = computed(() => {
  return tutorials.filter(tutorial => {
    const matchesTechStack = techStackFilter.value === 'all' || tutorial.techStack.toLowerCase().includes(techStackFilter.value.toLowerCase());
    const matchesDifficulty = difficultyFilter.value === 'all' || tutorial.difficulty.toLowerCase().includes(difficultyFilter.value.toLowerCase());
    return matchesTechStack && matchesDifficulty;
  });
});

// 社区帖子数据
const communityPosts = reactive([
  { id: 1, author: '智码引擎官方', time: '2小时前', title: '智码引擎v2.3.0版本发布公告', content: '我们很高兴地宣布智码引擎v2.3.0版本正式发布！本次更新带来了多项重要改进，包括AI代码生成质量提升、新的前端组件库支持、以及团队协作功能增强...', comments: 42, likes: 156, views: 892, avatar: './helpCenter/239f3c73de1e25e3529fd8128eae7986.png' },
  { id: 2, author: '李开发', time: '昨天 14:30', title: '分享一个我用智码引擎生成的电商管理系统', content: '大家好，分享一下我最近使用智码引擎生成的电商管理系统，包含商品管理、订单处理、会员管理等功能。生成效率非常高，代码质量也很不错，稍微修改一下就可以直接使用了...', comments: 36, likes: 98, views: 654, avatar: './helpCenter/b3806b4761c7a4339fbd89021c83acc8.png' },
  { id: 3, author: '王设计', time: '3天前', title: '【模板分享】响应式后台管理系统UI模板', content: '为大家分享一个我制作的响应式后台管理系统UI模板，支持多种布局模式和主题切换，已经发布到模板市场，欢迎大家使用并提出宝贵意见...', comments: 28, likes: 124, views: 782, avatar: './helpCenter/bb1fd1b1cdeeb03cf6e3315a10910d5e.png' }
]);

// 分类讨论区数据
const forums = reactive([
  { name: '创意交流区', description: '分享您的项目创意和想法', topics: 128, icon: 'fas fa-lightbulb' },
  { name: '问题求助区', description: '遇到问题？在这里寻求帮助', topics: 356, icon: 'fas fa-question-circle' },
  { name: '模板分享区', description: '分享您创建的项目模板', topics: 89, icon: 'fas fa-th-large' },
  { name: '功能建议区', description: '为智码引擎提供功能建议', topics: 215, icon: 'fas fa-comment-dots' }
]);

// 社区贡献者数据
const contributors = reactive([
  { name: '张工程师', templates: 24, avatar: './helpCenter/f7e519757cdb3d98c2ef1d3d84756df7.png' },
  { name: '刘开发', templates: 18, avatar: './helpCenter/d2d61724c051c370d0dbc675cf39b40d.png' },
  { name: '赵架构', templates: 15, avatar: './helpCenter/ef878cc3d488d4c9b84011f0bb73de64.png' },
  { name: '陈全栈', templates: 12, avatar: './helpCenter/5683af720dba053d7a36c132b9699deb.png' },
  { name: '杨后端', templates: 10, avatar: './helpCenter/b60d8eaf0a5c33a524d3ae9e7887b86f.png' }
]);

// 客服支持常见问题
const supportFaqs = reactive([
  { question: '客服工作时间是什么时候？', answer: '我们的客服团队工作时间为周一至周五，上午9:00至下午6:00（北京时间）。周末和节假日我们会有值班人员处理紧急问题，但响应时间可能会有所延迟。' },
  { question: '如何获取技术支持？', answer: '您可以通过以下方式获取技术支持：1) 在线客服聊天；2) 提交支持工单；3) 在社区论坛发帖提问；4) 发送邮件至support@zhimayinqing.com。付费用户将获得优先支持服务。' },
  { question: '如何报告bug或提出功能建议？', answer: '您可以通过在线客服、支持工单或社区论坛报告bug。对于功能建议，我们建议您在社区的"功能建议区"发帖，这样其他用户也可以参与讨论和投票。我们会定期查看这些建议并纳入产品规划。' },
  { question: '是否提供一对一的培训服务？', answer: '是的，我们为企业用户提供定制化的一对一培训服务。您可以联系我们的销售团队了解详细的培训方案和定价。此外，我们也会定期举办线上 webinar 和培训课程，所有用户都可以免费参加。' }
]);

// 快速问题数据
const quickQuestions = reactive([
  '如何生成React项目？',
  '会员套餐有什么区别？',
  '如何导出项目代码？',
  '团队协作功能使用方法'
]);

// 事件处理函数
const handleTabChange = (tab: string) => {
  activeTab.value = tab;
};

const handleStepClick = (index: number) => {
  ElMessage.info(`点击了第${index + 1}步：${quickStartSteps[index].title}`);
};

const handleCategoryClick = (category: any) => {
  ElMessage.info(`点击了分类：${category.title}`);
};

const handleDocumentClick = (node: any) => {
  ElMessage.info(`点击了文档：${node.label}`);
};

const handleTutorialClick = (tutorial: any) => {
  ElMessage.info(`点击了教程：${tutorial.title}`);
};

const handlePostClick = (post: any) => {
  ElMessage.info(`点击了帖子：${post.title}`);
};

const handleForumClick = (forum: any) => {
  ElMessage.info(`点击了讨论区：${forum.name}`);
};

const handleContributorClick = (contributor: any) => {
  ElMessage.info(`点击了贡献者：${contributor.name}`);
};

const publishPost = () => {
  ElMessage.info('发布新帖功能开发中...');
};

const loadMorePosts = () => {
  ElMessage.info('加载更多帖子功能开发中...');
};

const startChat = () => {
  ElMessage.info('开始对话功能开发中...');
};

const submitTicket = () => {
  ElMessage.info('提交工单功能开发中...');
};

const toggleSupportModal = () => {
  showSupportModal.value = !showSupportModal.value;
};

const closeSupportModal = () => {
  showSupportModal.value = false;
};

const askQuestion = (question: string) => {
  ElMessage.info(`提问：${question}`);
};

const sendMessage = () => {
  if (supportMessage.value.trim()) {
    ElMessage.success('消息已发送，我们会尽快回复您！');
    supportMessage.value = '';
    closeSupportModal();
  } else {
    ElMessage.warning('请输入您的问题');
  }
};
</script>

<style scoped lang="scss">
// 保留所有Tailwind CSS样式，不进行转换
.help-tabs {
  :deep(.el-tabs__nav-wrap::after) {
    display: none;
  }
  
  :deep(.el-tabs__item) {
    @apply help-nav-item;
  }
  
  :deep(.el-tabs__item.is-active) {
    @apply nav-item-active;
  }
}
</style>
