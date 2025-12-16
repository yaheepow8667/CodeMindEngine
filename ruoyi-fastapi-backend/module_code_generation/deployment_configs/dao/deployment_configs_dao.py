from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_code_generation.deployment_configs.entity.do.deployment_configs_do import DeploymentConfigs
from module_code_generation.deployment_configs.entity.vo.deployment_configs_vo import Deployment_configsModel, Deployment_configsPageQueryModel
from utils.page_util import PageUtil


class Deployment_configsDao:
    """
    部署配置模块数据库操作层
    """

    @classmethod
    async def get_deployment_configs_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据部署配置ID获取部署配置详细信息

        :param db: orm对象
        :param id: 部署配置ID
        :return: 部署配置信息对象
        """
        deployment_configs_info = (
            (
                await db.execute(
                    select(DeploymentConfigs)
                    .where(
                        DeploymentConfigs.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return deployment_configs_info

    @classmethod
    async def get_deployment_configs_detail_by_info(cls, db: AsyncSession, deployment_configs: Deployment_configsModel):
        """
        根据部署配置参数获取部署配置信息

        :param db: orm对象
        :param deployment_configs: 部署配置参数对象
        :return: 部署配置信息对象
        """
        deployment_configs_info = (
            (
                await db.execute(
                    select(DeploymentConfigs).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return deployment_configs_info

    @classmethod
    async def get_deployment_configs_list(cls, db: AsyncSession, query_object: Deployment_configsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取部署配置列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 部署配置列表信息对象
        """
        query = (
            select(DeploymentConfigs)
            .where(
                DeploymentConfigs.project_id == query_object.project_id if query_object.project_id else True,
                DeploymentConfigs.name.like(f'%{query_object.name}%') if query_object.name else True,
                DeploymentConfigs.environment == query_object.environment if query_object.environment else True,
                DeploymentConfigs.config == query_object.config if query_object.config else True,
                DeploymentConfigs.is_active == query_object.is_active if query_object.is_active else True,
                DeploymentConfigs.deployed_job_id == query_object.deployed_job_id if query_object.deployed_job_id else True,
                DeploymentConfigs.deployed_at == query_object.deployed_at if query_object.deployed_at else True,
                DeploymentConfigs.deployed_by_user_id == query_object.deployed_by_user_id if query_object.deployed_by_user_id else True,
                DeploymentConfigs.created_at == query_object.created_at if query_object.created_at else True,
                DeploymentConfigs.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(DeploymentConfigs.id)
            .distinct()
        )
        deployment_configs_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return deployment_configs_list

    @classmethod
    async def add_deployment_configs_dao(cls, db: AsyncSession, deployment_configs: Deployment_configsModel):
        """
        新增部署配置数据库操作

        :param db: orm对象
        :param deployment_configs: 部署配置对象
        :return:
        """
        db_deployment_configs = DeploymentConfigs(**deployment_configs.model_dump(exclude={}))
        db.add(db_deployment_configs)
        await db.flush()

        return db_deployment_configs

    @classmethod
    async def edit_deployment_configs_dao(cls, db: AsyncSession, deployment_configs: dict):
        """
        编辑部署配置数据库操作

        :param db: orm对象
        :param deployment_configs: 需要更新的部署配置字典
        :return:
        """
        await db.execute(update(DeploymentConfigs), [deployment_configs])

    @classmethod
    async def delete_deployment_configs_dao(cls, db: AsyncSession, deployment_configs: Deployment_configsModel):
        """
        删除部署配置数据库操作

        :param db: orm对象
        :param deployment_configs: 部署配置对象
        :return:
        """
        await db.execute(delete(DeploymentConfigs).where(DeploymentConfigs.id.in_([deployment_configs.id])))

