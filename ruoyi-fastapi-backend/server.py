from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.env import AppConfig
from config.get_db import init_create_table
from config.get_redis import RedisUtil
from config.get_scheduler import SchedulerUtil
from exceptions.handle import handle_exception
from middlewares.handle import handle_middleware
from module_admin.controller.cache_controller import cacheController
from module_admin.controller.captcha_controller import captchaController
from module_admin.controller.common_controller import commonController
from module_admin.controller.config_controller import configController
from module_admin.controller.dept_controller import deptController
from module_admin.controller.dict_controller import dictController
from module_admin.controller.log_controller import logController
from module_admin.controller.login_controller import loginController
from module_admin.controller.job_controller import jobController
from module_admin.controller.menu_controller import menuController
from module_admin.controller.notice_controller import noticeController
from module_admin.controller.online_controller import onlineController
from module_admin.controller.post_controler import postController
from module_admin.controller.role_controller import roleController
from module_admin.controller.server_controller import serverController
from module_admin.controller.user_controller import userController
from module_generator.controller.gen_controller import genController
# 导入团队协作模块控制器
from module_team_collaboration.team_members.controller.members_controller import membersController
from module_team_collaboration.teams.controller.teams_controller import teamsController
from module_team_collaboration.invitations.controller.invitations_controller import invitationsController
# 导入代码生成模块控制器
from module_code_generation.deployment_configs.controller.deployment_configs_controller import deployment_configsController
from module_code_generation.generated_artifacts.controller.generated_artifacts_controller import generated_artifactsController
from module_code_generation.generation_jobs.controller.generation_jobs_controller import generation_jobsController
# 导入项目蓝图模块控制器
from module_project_blueprint.blueprint_changes.controller.changes_controller import changesController
from module_project_blueprint.blueprints.controller.blueprints_controller import blueprintsController
from module_project_blueprint.projects.controller.projects_controller import projectsController
# 导入系统资源模块控制器
from module_system_resource.api_tokens.controller.api_tokens_controller import api_tokensController
from module_system_resource.resources.controller.resources_controller import resourcesController
from module_system_resource.subscriptions.controller.subscriptions_controller import subscriptionsController
# 导入模板插件模块控制器
from module_template_plugin.plugins.controller.plugins_controller import pluginsController
from module_template_plugin.template_versions.controller.template_versions_controller import template_versionsController
from module_template_plugin.templates.controller.templates_controller import templatesController
from sub_applications.handle import handle_sub_applications
from utils.common_util import worship
from utils.log_util import logger


# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'⏰️ {AppConfig.app_name}开始启动')
    worship()
    await init_create_table()
    app.state.redis = await RedisUtil.create_redis_pool()
    await RedisUtil.init_sys_dict(app.state.redis)
    await RedisUtil.init_sys_config(app.state.redis)
    await SchedulerUtil.init_system_scheduler()
    logger.info(f'🚀 {AppConfig.app_name}启动成功')
    yield
    await RedisUtil.close_redis_pool(app)
    await SchedulerUtil.close_system_scheduler()


# 初始化FastAPI对象
app = FastAPI(
    title=AppConfig.app_name,
    description=f'{AppConfig.app_name}接口文档',
    version=AppConfig.app_version,
    lifespan=lifespan,
)

# 挂载子应用
handle_sub_applications(app)
# 加载中间件处理方法
handle_middleware(app)
# 加载全局异常处理方法
handle_exception(app)


# 加载路由列表
controller_list = [
    {'router': loginController, 'tags': ['登录模块']},
    {'router': captchaController, 'tags': ['验证码模块']},
    {'router': userController, 'tags': ['系统管理-用户管理']},
    {'router': roleController, 'tags': ['系统管理-角色管理']},
    {'router': menuController, 'tags': ['系统管理-菜单管理']},
    {'router': deptController, 'tags': ['系统管理-部门管理']},
    {'router': postController, 'tags': ['系统管理-岗位管理']},
    {'router': dictController, 'tags': ['系统管理-字典管理']},
    {'router': configController, 'tags': ['系统管理-参数管理']},
    {'router': noticeController, 'tags': ['系统管理-通知公告管理']},
    {'router': logController, 'tags': ['系统管理-日志管理']},
    {'router': onlineController, 'tags': ['系统监控-在线用户']},
    {'router': jobController, 'tags': ['系统监控-定时任务']},
    {'router': serverController, 'tags': ['系统监控-菜单管理']},
    {'router': cacheController, 'tags': ['系统监控-缓存监控']},
    {'router': commonController, 'tags': ['通用模块']},
    {'router': genController, 'tags': ['代码生成']},
    # 团队协作模块路由
    {'router': teamsController, 'tags': ['团队协作-团队管理']},
    {'router': membersController, 'tags': ['团队协作-成员管理']},
    {'router': invitationsController, 'tags': ['团队协作-邀请管理']},
    # 代码生成模块路由
    {'router': deployment_configsController, 'tags': ['代码生成-部署配置管理']},
    {'router': generated_artifactsController, 'tags': ['代码生成-生成产物管理']},
    {'router': generation_jobsController, 'tags': ['代码生成-生成任务管理']},
    # 项目蓝图模块路由
    {'router': changesController, 'tags': ['项目蓝图-变更管理']},
    {'router': blueprintsController, 'tags': ['项目蓝图-蓝图管理']},
    {'router': projectsController, 'tags': ['项目蓝图-项目管理']},
    # 系统资源模块路由
    {'router': api_tokensController, 'tags': ['系统资源-API令牌管理']},
    {'router': resourcesController, 'tags': ['系统资源-资源管理']},
    {'router': subscriptionsController, 'tags': ['系统资源-订阅管理']},
    # 模板插件模块路由
    {'router': pluginsController, 'tags': ['模板插件-插件管理']},
    {'router': template_versionsController, 'tags': ['模板插件-模板版本管理']},
    {'router': templatesController, 'tags': ['模板插件-模板管理']},
]

for controller in controller_list:
    app.include_router(router=controller.get('router'), tags=controller.get('tags'))
