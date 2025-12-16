from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_team_collaboration.teams.dao.teams_dao import TeamsDao
from module_team_collaboration.teams.entity.vo.teams_vo import DeleteTeamsModel, TeamsModel, TeamsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class TeamsService:
    """
    团队模块服务层
    """

    @classmethod
    async def get_teams_list_services(
        cls, query_db: AsyncSession, query_object: TeamsPageQueryModel, is_page: bool = False
    ):
        """
        获取团队列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 团队列表信息对象
        """
        teams_list_result = await TeamsDao.get_teams_list(query_db, query_object, is_page)

        return teams_list_result


    @classmethod
    async def add_teams_services(cls, query_db: AsyncSession, page_object: TeamsModel):
        """
        新增团队信息service

        :param query_db: orm对象
        :param page_object: 新增团队对象
        :return: 新增团队校验结果
        """
        try:
            await TeamsDao.add_teams_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_teams_services(cls, query_db: AsyncSession, page_object: TeamsModel):
        """
        编辑团队信息service

        :param query_db: orm对象
        :param page_object: 编辑团队对象
        :return: 编辑团队校验结果
        """
        edit_teams = page_object.model_dump(exclude_unset=True, exclude={})
        teams_info = await cls.teams_detail_services(query_db, page_object.id)
        if teams_info.id:
            try:
                await TeamsDao.edit_teams_dao(query_db, edit_teams)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='团队不存在')

    @classmethod
    async def delete_teams_services(cls, query_db: AsyncSession, page_object: DeleteTeamsModel):
        """
        删除团队信息service

        :param query_db: orm对象
        :param page_object: 删除团队对象
        :return: 删除团队校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await TeamsDao.delete_teams_dao(query_db, TeamsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入为空')

    @classmethod
    async def teams_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取团队详细信息service

        :param query_db: orm对象
        :param id: 
        :return: 对应的信息
        """
        teams = await TeamsDao.get_teams_detail_by_id(query_db, id=id)
        if teams:
            result = TeamsModel(**CamelCaseUtil.transform_result(teams))
        else:
            result = TeamsModel(**dict())

        return result

    @staticmethod
    async def export_teams_list_services(teams_list: List):
        """
        导出团队信息service

        :param teams_list: 团队信息列表
        :return: 团队信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '',
            'name': '团队名称',
            'slug': '团队URL标识',
            'description': '团队描述',
            'logoUrl': '团队logo',
            'subscriptionPlan': '订阅计划 (free, team, enterprise)',
            'subscriptionStatus': '订阅状态 (active, canceled, past_due)',
            'subscriptionEndsAt': '订阅到期时间',
            'createdByUserId': '创建者用户ID',
            'createdAt': '创建时间',
            'updatedAt': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(teams_list, mapping_dict)

        return binary_data
