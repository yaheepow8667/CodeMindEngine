# Pinia状态管理设计文档

## 1. 状态管理概述

### 1.1 设计目标
采用Pinia作为前端状态管理方案，统一管理智码引擎的全局状态，包括用户信息、团队管理、项目管理、蓝图管理等核心业务状态，实现状态共享和高效通信。

### 1.2 设计原则
- **模块化**：按业务功能划分状态模块，实现关注点分离
- **单一职责**：每个模块只管理特定领域的状态
- **响应式**：利用Vue 3的响应式系统，确保状态变更能实时反映到视图
- **持久化**：关键状态持久化存储，提升用户体验
- **类型安全**：确保状态类型的一致性和完整性

## 2. 现有Pinia模块分析

### 2.1 核心模块结构

| 模块名 | 主要功能 | 状态管理内容 |
|-------|---------|-------------|
| `user` | 用户认证与信息 | token、用户基本信息、角色、权限 |
| `app` | 应用配置 | 侧边栏状态、设备类型、尺寸设置 |
| `permission` | 权限管理 | 路由权限、按钮权限 |
| `settings` | 系统设置 | 主题、布局、动画等 |
| `tagsView` | 标签页管理 | 打开的标签页、缓存的组件 |
| `dict` | 字典管理 | 系统字典数据 |

### 2.2 模块实现示例

```javascript
// user.js 示例
const useUserStore = defineStore(
  'user',
  {
    state: () => ({
      token: getToken(),
      id: '',
      name: '',
      nickName: '',
      avatar: '',
      roles: [],
      permissions: []
    }),
    actions: {
      // 登录
      login(userInfo) {
        return new Promise((resolve, reject) => {
          login(username, password, code, uuid).then(res => {
            setToken(res.token)
            this.token = res.token
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      // 其他actions...
    }
  })
```

## 3. 新增业务模块设计

### 3.1 团队管理模块（teams）

**状态定义**
```javascript
state: () => ({
  currentTeam: null, // 当前选中团队
  teams: [], // 用户所属团队列表
  teamMembers: [], // 当前团队成员列表
  loading: false, // 加载状态
  pagination: {
    current: 1,
    size: 10,
    total: 0
  }
})
```

**核心操作**
```javascript
actions: {
  // 获取用户团队列表
  getTeams(params) {
    this.loading = true
    return new Promise((resolve, reject) => {
      getTeams(params).then(res => {
        this.teams = res.data
        this.pagination.total = res.total
        resolve(res)
      }).catch(error => {
        reject(error)
      }).finally(() => {
        this.loading = false
      })
    })
  },
  // 设置当前团队
  setCurrentTeam(team) {
    this.currentTeam = team
    localStorage.setItem('currentTeam', JSON.stringify(team))
  },
  // 创建团队
  createTeam(teamInfo) {
    return new Promise((resolve, reject) => {
      createTeam(teamInfo).then(res => {
        this.teams.push(res.data)
        resolve(res)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // 其他团队相关操作...
}
```

### 3.2 项目管理模块（projects）

**状态定义**
```javascript
state: () => ({
  currentProject: null, // 当前选中项目
  projects: [], // 项目列表
  projectStats: {}, // 项目统计信息
  loading: false, // 加载状态
  pagination: {
    current: 1,
    size: 10,
    total: 0
  }
})
```

**核心操作**
```javascript
actions: {
  // 获取项目列表
  getProjects(params) {
    this.loading = true
    return new Promise((resolve, reject) => {
      listProjects(params).then(res => {
        this.projects = res.data
        this.pagination.total = res.total
        resolve(res)
      }).catch(error => {
        reject(error)
      }).finally(() => {
        this.loading = false
      })
    })
  },
  // 设置当前项目
  setCurrentProject(project) {
    this.currentProject = project
    localStorage.setItem('currentProject', JSON.stringify(project))
  },
  // 创建项目
  createProject(projectInfo) {
    return new Promise((resolve, reject) => {
      createProject(projectInfo).then(res => {
        this.projects.push(res.data)
        resolve(res)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // 其他项目相关操作...
}
```

### 3.3 蓝图管理模块（blueprints）

**状态定义**
```javascript
state: () => ({
  currentBlueprint: null, // 当前选中蓝图
  blueprints: [], // 蓝图列表
  blueprintChanges: [], // 蓝图变更记录
  loading: false, // 加载状态
  pagination: {
    current: 1,
    size: 10,
    total: 0
  }
})
```

**核心操作**
```javascript
actions: {
  // 获取蓝图列表
  getBlueprints(projectId, params) {
    this.loading = true
    return new Promise((resolve, reject) => {
      listBlueprints(projectId, params).then(res => {
        this.blueprints = res.data
        this.pagination.total = res.total
        resolve(res)
      }).catch(error => {
        reject(error)
      }).finally(() => {
        this.loading = false
      })
    })
  },
  // 设置当前蓝图
  setCurrentBlueprint(blueprint) {
    this.currentBlueprint = blueprint
    localStorage.setItem('currentBlueprint', JSON.stringify(blueprint))
  },
  // 创建蓝图
  createBlueprint(projectId, blueprintInfo) {
    return new Promise((resolve, reject) => {
      createBlueprint(projectId, blueprintInfo).then(res => {
        this.blueprints.push(res.data)
        resolve(res)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // 解析需求
  parseRequirements(blueprintId, requirements) {
    return new Promise((resolve, reject) => {
      parseRequirements(blueprintId, requirements).then(res => {
        resolve(res)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // 其他蓝图相关操作...
}
```

### 3.4 生成任务管理模块（generation）

**状态定义**
```javascript
state: () => ({
  currentJob: null, // 当前生成任务
  generationJobs: [], // 生成任务列表
  jobLogs: [], // 任务日志
  loading: false, // 加载状态
  pagination: {
    current: 1,
    size: 10,
    total: 0
  }
})
```

**核心操作**
```javascript
actions: {
  // 获取生成任务列表
  getGenerationJobs(params) {
    this.loading = true
    return new Promise((resolve, reject) => {
      listGenerationJobs(params).then(res => {
        this.generationJobs = res.data
        this.pagination.total = res.total
        resolve(res)
      }).catch(error => {
        reject(error)
      }).finally(() => {
        this.loading = false
      })
    })
  },
  // 创建生成任务
  createGenerationJob(jobInfo) {
    return new Promise((resolve, reject) => {
      createGenerationJob(jobInfo).then(res => {
        this.generationJobs.push(res.data)
        this.currentJob = res.data
        resolve(res)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // 获取任务日志
  getJobLogs(jobId) {
    return new Promise((resolve, reject) => {
      getJobLogs(jobId).then(res => {
        this.jobLogs = res.data
        resolve(res)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // 其他生成任务相关操作...
}
```

## 4. 状态持久化策略

### 4.1 持久化方案

| 状态类型 | 持久化方式 | 适用场景 |
|---------|-----------|---------|
| 认证信息 | Cookie + localstorage | token、用户基本信息 |
| 应用配置 | Cookie | 侧边栏状态、主题设置 |
| 业务状态 | localStorage | 当前团队、当前项目、当前蓝图 |
| 临时状态 | 内存 | 加载状态、表单数据 |

### 4.2 持久化实现

```javascript
// 读取持久化状态示例
const useTeamsStore = defineStore(
  'teams',
  {
    state: () => ({
      currentTeam: localStorage.getItem('currentTeam') ? JSON.parse(localStorage.getItem('currentTeam')) : null,
      // 其他状态...
    }),
    actions: {
      // 设置当前团队并持久化
      setCurrentTeam(team) {
        this.currentTeam = team
        localStorage.setItem('currentTeam', JSON.stringify(team))
      },
      // 清除持久化状态
      clearCurrentTeam() {
        this.currentTeam = null
        localStorage.removeItem('currentTeam')
      }
    }
  })
```

## 5. 模块间通信

### 5.1 通信方式

#### 1. 直接访问其他模块

```javascript
// 在team模块中访问user模块
import useUserStore from './user'

const useTeamsStore = defineStore(
  'teams',
  {
    actions: {
      createTeam(teamInfo) {
        const userStore = useUserStore()
        console.log('当前用户:', userStore.name)
        // 其他操作...
      }
    }
  })
```

#### 2. 事件总线

```javascript
// 创建事件总线
import mitt from 'mitt'
const emitter = mitt()

export default emitter

// 发送事件
emitter.emit('team-changed', newTeam)

// 接收事件
emitter.on('team-changed', (newTeam) => {
  console.log('团队变更:', newTeam)
})
```

#### 3. 路由参数

通过路由参数传递关键信息，实现组件间的通信和状态同步。

## 6. 最佳实践

### 6.1 状态管理规范

1. **状态定义**：
   - 初始状态应明确类型
   - 避免使用null作为初始值，优先使用空对象或数组
   - 状态名应清晰表达其含义

2. **Actions实现**：
   - 异步操作必须返回Promise
   - 错误处理应统一规范
   - 复杂操作应拆分为多个小函数

3. **性能优化**：
   - 避免不必要的状态更新
   - 大型列表使用分页加载
   - 合理使用计算属性缓存计算结果

### 6.2 代码示例

```javascript
// 完整的Pinia模块示例
import { defineStore } from 'pinia'
import { listProjects, createProject, updateProject, deleteProject } from '@/api/projects'

const useProjectsStore = defineStore(
  'projects',
  {
    state: () => ({
      projects: [],
      currentProject: localStorage.getItem('currentProject') ? JSON.parse(localStorage.getItem('currentProject')) : null,
      loading: false,
      pagination: {
        current: 1,
        size: 10,
        total: 0
      }
    }),
    
    getters: {
      activeProjects: (state) => state.projects.filter(project => project.status === 'active'),
      projectCount: (state) => state.projects.length
    },
    
    actions: {
      // 获取项目列表
      async fetchProjects(params) {
        try {
          this.loading = true
          const res = await listProjects(params)
          this.projects = res.data
          this.pagination.total = res.total
          return res
        } catch (error) {
          console.error('获取项目列表失败:', error)
          throw error
        } finally {
          this.loading = false
        }
      },
      
      // 创建项目
      async addProject(projectInfo) {
        try {
          const res = await createProject(projectInfo)
          this.projects.push(res.data)
          return res
        } catch (error) {
          console.error('创建项目失败:', error)
          throw error
        }
      },
      
      // 设置当前项目
      setCurrentProject(project) {
        this.currentProject = project
        localStorage.setItem('currentProject', JSON.stringify(project))
      },
      
      // 清除状态
      clearState() {
        this.projects = []
        this.currentProject = null
        this.pagination = {
          current: 1,
          size: 10,
          total: 0
        }
        localStorage.removeItem('currentProject')
      }
    }
  })

export default useProjectsStore
```

## 7. 依赖与安装

### 7.1 安装Pinia

```bash
npm install pinia
```

### 7.2 配置Pinia

```javascript
// main.js
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
```
