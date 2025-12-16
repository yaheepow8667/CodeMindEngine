from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_code_generation.generation_jobs.entity.do.generation_jobs_do import GenerationJobs
from module_code_generation.generation_jobs.entity.vo.generation_jobs_vo import Generation_jobsModel, Generation_jobsPageQueryModel
from utils.page_util import PageUtil


class Generation_jobsDao:
    """
    生成任务模块数据库操作层
    """

    @classmethod
    async def get_generation_jobs_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据生成任务ID获取生成任务详细信息

        :param db: orm对象
        :param id: 生成任务ID
        :return: 生成任务信息对象
        """
        generation_jobs_info = (
            (
                await db.execute(
                    select(GenerationJobs)
                    .where(
                        GenerationJobs.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return generation_jobs_info

    @classmethod
    async def get_generation_jobs_detail_by_info(cls, db: AsyncSession, generation_jobs: Generation_jobsModel):
        """
        根据生成任务参数获取生成任务信息

        :param db: orm对象
        :param generation_jobs: 生成任务参数对象
        :return: 生成任务信息对象
        """
        generation_jobs_info = (
            (
                await db.execute(
                    select(GenerationJobs).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return generation_jobs_info

    @classmethod
    async def get_generation_jobs_list(cls, db: AsyncSession, query_object: Generation_jobsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取生成任务列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 生成任务列表信息对象
        """
        query = (
            select(GenerationJobs)
            .where(
                GenerationJobs.project_id == query_object.project_id if query_object.project_id else True,
                GenerationJobs.blueprint_id == query_object.blueprint_id if query_object.blueprint_id else True,
                GenerationJobs.status == query_object.status if query_object.status else True,
                GenerationJobs.target_tech_stack == query_object.target_tech_stack if query_object.target_tech_stack else True,
                GenerationJobs.trigger_type == query_object.trigger_type if query_object.trigger_type else True,
                GenerationJobs.triggered_by_user_id == query_object.triggered_by_user_id if query_object.triggered_by_user_id else True,
                GenerationJobs.started_at == query_object.started_at if query_object.started_at else True,
                GenerationJobs.completed_at == query_object.completed_at if query_object.completed_at else True,
                GenerationJobs.error_message == query_object.error_message if query_object.error_message else True,
                GenerationJobs.logs == query_object.logs if query_object.logs else True,
                GenerationJobs.qa_report == query_object.qa_report if query_object.qa_report else True,
                GenerationJobs.created_at == query_object.created_at if query_object.created_at else True,
            )
            .order_by(GenerationJobs.id)
            .distinct()
        )
        generation_jobs_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return generation_jobs_list

    @classmethod
    async def add_generation_jobs_dao(cls, db: AsyncSession, generation_jobs: Generation_jobsModel):
        """
        新增生成任务数据库操作

        :param db: orm对象
        :param generation_jobs: 生成任务对象
        :return:
        """
        db_generation_jobs = GenerationJobs(**generation_jobs.model_dump(exclude={}))
        db.add(db_generation_jobs)
        await db.flush()

        return db_generation_jobs

    @classmethod
    async def edit_generation_jobs_dao(cls, db: AsyncSession, generation_jobs: dict):
        """
        编辑生成任务数据库操作

        :param db: orm对象
        :param generation_jobs: 需要更新的生成任务字典
        :return:
        """
        await db.execute(update(GenerationJobs), [generation_jobs])

    @classmethod
    async def delete_generation_jobs_dao(cls, db: AsyncSession, generation_jobs: Generation_jobsModel):
        """
        删除生成任务数据库操作

        :param db: orm对象
        :param generation_jobs: 生成任务对象
        :return:
        """
        await db.execute(delete(GenerationJobs).where(GenerationJobs.id.in_([generation_jobs.id])))

