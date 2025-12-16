from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_system_resource.api_tokens.entity.do.api_tokens_do import ApiTokens
from module_system_resource.api_tokens.entity.vo.api_tokens_vo import Api_tokensModel, Api_tokensPageQueryModel
from utils.page_util import PageUtil


class Api_tokensDao:
    """
    API访问令牌模块数据库操作层
    """

    @classmethod
    async def get_api_tokens_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据访问令牌ID获取API访问令牌详细信息

        :param db: orm对象
        :param id: 访问令牌ID
        :return: API访问令牌信息对象
        """
        api_tokens_info = (
            (
                await db.execute(
                    select(ApiTokens)
                    .where(
                        ApiTokens.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_tokens_info

    @classmethod
    async def get_api_tokens_detail_by_info(cls, db: AsyncSession, api_tokens: Api_tokensModel):
        """
        根据API访问令牌参数获取API访问令牌信息

        :param db: orm对象
        :param api_tokens: API访问令牌参数对象
        :return: API访问令牌信息对象
        """
        api_tokens_info = (
            (
                await db.execute(
                    select(ApiTokens).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_tokens_info

    @classmethod
    async def get_api_tokens_list(cls, db: AsyncSession, query_object: Api_tokensPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取API访问令牌列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: API访问令牌列表信息对象
        """
        query = (
            select(ApiTokens)
            .where(
                ApiTokens.user_id == query_object.user_id if query_object.user_id else True,
                ApiTokens.team_id == query_object.team_id if query_object.team_id else True,
                ApiTokens.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiTokens.token_hash == query_object.token_hash if query_object.token_hash else True,
                ApiTokens.token_prefix == query_object.token_prefix if query_object.token_prefix else True,
                ApiTokens.scopes == query_object.scopes if query_object.scopes else True,
                ApiTokens.expires_at == query_object.expires_at if query_object.expires_at else True,
                ApiTokens.last_used_at == query_object.last_used_at if query_object.last_used_at else True,
                ApiTokens.is_active == query_object.is_active if query_object.is_active else True,
                ApiTokens.created_at == query_object.created_at if query_object.created_at else True,
            )
            .order_by(ApiTokens.id)
            .distinct()
        )
        api_tokens_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return api_tokens_list

    @classmethod
    async def add_api_tokens_dao(cls, db: AsyncSession, api_tokens: Api_tokensModel):
        """
        新增API访问令牌数据库操作

        :param db: orm对象
        :param api_tokens: API访问令牌对象
        :return:
        """
        db_api_tokens = ApiTokens(**api_tokens.model_dump(exclude={}))
        db.add(db_api_tokens)
        await db.flush()

        return db_api_tokens

    @classmethod
    async def edit_api_tokens_dao(cls, db: AsyncSession, api_tokens: dict):
        """
        编辑API访问令牌数据库操作

        :param db: orm对象
        :param api_tokens: 需要更新的API访问令牌字典
        :return:
        """
        await db.execute(update(ApiTokens), [api_tokens])

    @classmethod
    async def delete_api_tokens_dao(cls, db: AsyncSession, api_tokens: Api_tokensModel):
        """
        删除API访问令牌数据库操作

        :param db: orm对象
        :param api_tokens: API访问令牌对象
        :return:
        """
        await db.execute(delete(ApiTokens).where(ApiTokens.id.in_([api_tokens.id])))

