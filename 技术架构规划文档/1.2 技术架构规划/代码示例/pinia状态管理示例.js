// Pinia状态管理示例

// 1. 用户管理模块 (user.js)
import { defineStore } from 'pinia'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { login, getInfo, logout } from '@/api/user'

export const useUserStore = defineStore(
  'user',
  {
    state: () => ({
      token: getToken(),
      id: '',
      name: '',
      displayName: '',
      avatar: '',
      avatarUrl: '',
      roles: [],
      permissions: []
    }),
    getters: {
      isLoggedIn: (state) => !!state.token,
      hasPermission: (state) => (permission) => {
        return state.permissions.includes(permission)
      }
    },
    actions: {
      async login(userInfo) {
        const { username, password } = userInfo
        const response = await login({
          username: username.trim(),
          password: password
        })
        const { token } = response.data
        this.token = token
        setToken(token)
      },

      async getInfo() {
        const response = await getInfo()
        const { id, username, display_name, avatar_url, roles, permissions } = response.data
        this.id = id
        this.name = username
        this.displayName = display_name
        this.avatar = avatar_url
        this.avatarUrl = avatar_url
        this.roles = roles
        this.permissions = permissions
      },

      async logout() {
        await logout()
        this.resetState()
      },

      resetState() {
        this.token = ''
        this.id = ''
        this.name = ''
        this.displayName = ''
        this.avatar = ''
        this.avatarUrl = ''
        this.roles = []
        this.permissions = []
        removeToken()
      }
    }
  })

// 2. 团队管理模块 (team.js)
import { defineStore } from 'pinia'
import { getTeams, getTeamById, createTeam, updateTeam, deleteTeam, setCurrentTeam } from '@/api/team'

export const useTeamStore = defineStore(
  'team',
  {
    state: () => ({
      currentTeam: null,
      teams: [],
      teamMembers: [],
      loading: false,
      error: null
    }),
    getters: {
      currentTeamName: (state) => state.currentTeam?.name || '',
      teamList: (state) => state.teams
    },
    actions: {
      async fetchTeams() {
        this.loading = true
        try {
          const response = await getTeams()
          this.teams = response.data
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      async fetchTeamById(teamId) {
        this.loading = true
        try {
          const response = await getTeamById(teamId)
          return response.data
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      async createNewTeam(teamData) {
        this.loading = true
        try {
          const response = await createTeam(teamData)
          this.teams.push(response.data)
          return response.data
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      async updateExistingTeam(teamId, teamData) {
        this.loading = true
        try {
          const response = await updateTeam(teamId, teamData)
          const index = this.teams.findIndex(team => team.id === teamId)
          if (index !== -1) {
            this.teams[index] = response.data
          }
          if (this.currentTeam?.id === teamId) {
            this.currentTeam = response.data
            localStorage.setItem('currentTeam', JSON.stringify(response.data))
          }
          return response.data
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      async deleteExistingTeam(teamId) {
        this.loading = true
        try {
          await deleteTeam(teamId)
          this.teams = this.teams.filter(team => team.id !== teamId)
          if (this.currentTeam?.id === teamId) {
            this.currentTeam = null
            localStorage.removeItem('currentTeam')
          }
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      setCurrentTeam(team) {
        this.currentTeam = team
        localStorage.setItem('currentTeam', JSON.stringify(team))
      },

      loadCurrentTeam() {
        const savedTeam = localStorage.getItem('currentTeam')
        if (savedTeam) {
          this.currentTeam = JSON.parse(savedTeam)
        }
      },

      clearCurrentTeam() {
        this.currentTeam = null
        localStorage.removeItem('currentTeam')
      }
    }
  })

// 3. 项目管理模块 (project.js)
import { defineStore } from 'pinia'
import { getProjects, createProject, updateProject, deleteProject, setCurrentProject } from '@/api/project'

export const useProjectStore = defineStore(
  'project',
  {
    state: () => ({
      currentProject: null,
      projects: [],
      loading: false,
      error: null
    }),
    getters: {
      currentProjectName: (state) => state.currentProject?.name || '',
      projectsByTeam: (state) => (teamId) => {
        return state.projects.filter(project => project.team_id === teamId)
      }
    },
    actions: {
      async fetchProjects(teamId) {
        this.loading = true
        try {
          const response = await getProjects(teamId)
          this.projects = response.data
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      async createNewProject(projectData) {
        this.loading = true
        try {
          const response = await createProject(projectData)
          this.projects.push(response.data)
          return response.data
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      async updateExistingProject(projectId, projectData) {
        this.loading = true
        try {
          const response = await updateProject(projectId, projectData)
          const index = this.projects.findIndex(project => project.id === projectId)
          if (index !== -1) {
            this.projects[index] = response.data
          }
          if (this.currentProject?.id === projectId) {
            this.currentProject = response.data
            localStorage.setItem('currentProject', JSON.stringify(response.data))
          }
          return response.data
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      async deleteExistingProject(projectId) {
        this.loading = true
        try {
          await deleteProject(projectId)
          this.projects = this.projects.filter(project => project.id !== projectId)
          if (this.currentProject?.id === projectId) {
            this.currentProject = null
            localStorage.removeItem('currentProject')
          }
        } catch (error) {
          this.error = error.message
        } finally {
          this.loading = false
        }
      },

      setCurrentProject(project) {
        this.currentProject = project
        localStorage.setItem('currentProject', JSON.stringify(project))
      },

      loadCurrentProject() {
        const savedProject = localStorage.getItem('currentProject')
        if (savedProject) {
          this.currentProject = JSON.parse(savedProject)
        }
      },

      clearCurrentProject() {
        this.currentProject = null
        localStorage.removeItem('currentProject')
      }
    }
  })
