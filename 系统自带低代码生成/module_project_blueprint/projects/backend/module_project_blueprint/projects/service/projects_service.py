from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_project_blueprint.projects.dao.projects_dao import ProjectsDao
from module_project_blueprint.projects.entity.vo.projects_vo import DeleteProjectsModel, ProjectsModel, ProjectsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ProjectsService:
    """
    项目模块服务层
    """

    @classmethod
    async def get_projects_list_services(
        cls, query_db: AsyncSession, query_object: ProjectsPageQueryModel, is_page: bool = False
    ):
        """
        获取项目列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目列表信息对象
        """
        projects_list_result = await ProjectsDao.get_projects_list(query_db, query_object, is_page)

        return projects_list_result


    @classmethod
    async def add_projects_services(cls, query_db: AsyncSession, page_object: ProjectsModel):
        """
        新增项目信息service

        :param query_db: orm对象
        :param page_object: 新增项目对象
        :return: 新增项目校验结果
        """
        try:
            await ProjectsDao.add_projects_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_projects_services(cls, query_db: AsyncSession, page_object: ProjectsModel):
        """
        编辑项目信息service

        :param query_db: orm对象
        :param page_object: 编辑项目对象
        :return: 编辑项目校验结果
        """
        edit_projects = page_object.model_dump(exclude_unset=True, exclude={})
        projects_info = await cls.projects_detail_services(query_db, page_object.id)
        if projects_info.id:
            try:
                await ProjectsDao.edit_projects_dao(query_db, edit_projects)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='项目不存在')

    @classmethod
    async def delete_projects_services(cls, query_db: AsyncSession, page_object: DeleteProjectsModel):
        """
        删除项目信息service

        :param query_db: orm对象
        :param page_object: 删除项目对象
        :return: 删除项目校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await ProjectsDao.delete_projects_dao(query_db, ProjectsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入项目ID为空')

    @classmethod
    async def projects_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取项目详细信息service

        :param query_db: orm对象
        :param id: 项目ID
        :return: 项目ID对应的信息
        """
        projects = await ProjectsDao.get_projects_detail_by_id(query_db, id=id)
        if projects:
            result = ProjectsModel(**CamelCaseUtil.transform_result(projects))
        else:
            result = ProjectsModel(**dict())

        return result

    @staticmethod
    async def export_projects_list_services(projects_list: List):
        """
        导出项目信息service

        :param projects_list: 项目信息列表
        :return: 项目信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '项目ID',
            'teamId': '团队ID',
            'name': '项目名称',
            'slug': '项目标识',
            'description': '项目描述',
            'techStack': '技术栈配置 {"frontend": "vue3", "backend": "nestjs", "ui": "ant-design-vue"}',
            'status': '项目状态 (active, archived, deleted)',
            'isPublic': '是否公开',
            'storageQuotaMb': '存储配额 (MB)',
            'createdByUserId': '创建者用户ID',
            'createdAt': '创建时间',
            'updatedAt': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(projects_list, mapping_dict)

        return binary_data
