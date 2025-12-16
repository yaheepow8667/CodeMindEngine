from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_system_resource.subscriptions.dao.subscriptions_dao import SubscriptionsDao
from module_system_resource.subscriptions.entity.vo.subscriptions_vo import DeleteSubscriptionsModel, SubscriptionsModel, SubscriptionsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class SubscriptionsService:
    """
    订阅与支付模块服务层
    """

    @classmethod
    async def get_subscriptions_list_services(
        cls, query_db: AsyncSession, query_object: SubscriptionsPageQueryModel, is_page: bool = False
    ):
        """
        获取订阅与支付列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 订阅与支付列表信息对象
        """
        subscriptions_list_result = await SubscriptionsDao.get_subscriptions_list(query_db, query_object, is_page)

        return subscriptions_list_result


    @classmethod
    async def add_subscriptions_services(cls, query_db: AsyncSession, page_object: SubscriptionsModel):
        """
        新增订阅与支付信息service

        :param query_db: orm对象
        :param page_object: 新增订阅与支付对象
        :return: 新增订阅与支付校验结果
        """
        try:
            await SubscriptionsDao.add_subscriptions_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_subscriptions_services(cls, query_db: AsyncSession, page_object: SubscriptionsModel):
        """
        编辑订阅与支付信息service

        :param query_db: orm对象
        :param page_object: 编辑订阅与支付对象
        :return: 编辑订阅与支付校验结果
        """
        edit_subscriptions = page_object.model_dump(exclude_unset=True, exclude={})
        subscriptions_info = await cls.subscriptions_detail_services(query_db, page_object.id)
        if subscriptions_info.id:
            try:
                await SubscriptionsDao.edit_subscriptions_dao(query_db, edit_subscriptions)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='订阅与支付不存在')

    @classmethod
    async def delete_subscriptions_services(cls, query_db: AsyncSession, page_object: DeleteSubscriptionsModel):
        """
        删除订阅与支付信息service

        :param query_db: orm对象
        :param page_object: 删除订阅与支付对象
        :return: 删除订阅与支付校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await SubscriptionsDao.delete_subscriptions_dao(query_db, SubscriptionsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入订阅与支付ID为空')

    @classmethod
    async def subscriptions_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取订阅与支付详细信息service

        :param query_db: orm对象
        :param id: 订阅与支付ID
        :return: 订阅与支付ID对应的信息
        """
        subscriptions = await SubscriptionsDao.get_subscriptions_detail_by_id(query_db, id=id)
        if subscriptions:
            result = SubscriptionsModel(**CamelCaseUtil.transform_result(subscriptions))
        else:
            result = SubscriptionsModel(**dict())

        return result

    @staticmethod
    async def export_subscriptions_list_services(subscriptions_list: List):
        """
        导出订阅与支付信息service

        :param subscriptions_list: 订阅与支付信息列表
        :return: 订阅与支付信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '订阅与支付ID',
            'teamId': '团队ID',
            'plan': '订阅计划',
            'status': '订阅状态',
            'currentPeriodStart': '当前订阅周期开始时间',
            'currentPeriodEnd': '当前订阅周期结束时间',
            'cancelAtPeriodEnd': '是否在周期结束时取消',
            'canceledAt': '取消时间',
            'stripeCustomerId': 'Stripe客户ID',
            'stripeSubscriptionId': 'Stripe订阅ID',
            'createdAt': '创建时间',
            'updatedAt': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(subscriptions_list, mapping_dict)

        return binary_data
