from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_code_generation.generated_artifacts.entity.do.generated_artifacts_do import GeneratedArtifacts
from module_code_generation.generated_artifacts.entity.vo.generated_artifacts_vo import Generated_artifactsModel, Generated_artifactsPageQueryModel
from utils.page_util import PageUtil


class Generated_artifactsDao:
    """
    生成产物模块数据库操作层
    """

    @classmethod
    async def get_generated_artifacts_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据产物ID获取生成产物详细信息

        :param db: orm对象
        :param id: 产物ID
        :return: 生成产物信息对象
        """
        generated_artifacts_info = (
            (
                await db.execute(
                    select(GeneratedArtifacts)
                    .where(
                        GeneratedArtifacts.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return generated_artifacts_info

    @classmethod
    async def get_generated_artifacts_detail_by_info(cls, db: AsyncSession, generated_artifacts: Generated_artifactsModel):
        """
        根据生成产物参数获取生成产物信息

        :param db: orm对象
        :param generated_artifacts: 生成产物参数对象
        :return: 生成产物信息对象
        """
        generated_artifacts_info = (
            (
                await db.execute(
                    select(GeneratedArtifacts).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return generated_artifacts_info

    @classmethod
    async def get_generated_artifacts_list(cls, db: AsyncSession, query_object: Generated_artifactsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取生成产物列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 生成产物列表信息对象
        """
        query = (
            select(GeneratedArtifacts)
            .where(
                GeneratedArtifacts.job_id == query_object.job_id if query_object.job_id else True,
                GeneratedArtifacts.artifact_type == query_object.artifact_type if query_object.artifact_type else True,
                GeneratedArtifacts.artifact_name.like(f'%{query_object.artifact_name}%') if query_object.artifact_name else True,
                GeneratedArtifacts.storage_type == query_object.storage_type if query_object.storage_type else True,
                GeneratedArtifacts.storage_path == query_object.storage_path if query_object.storage_path else True,
                GeneratedArtifacts.storage_url == query_object.storage_url if query_object.storage_url else True,
                GeneratedArtifacts.file_size_bytes == query_object.file_size_bytes if query_object.file_size_bytes else True,
                GeneratedArtifacts.mime_type == query_object.mime_type if query_object.mime_type else True,
                GeneratedArtifacts.checksum == query_object.checksum if query_object.checksum else True,
                GeneratedArtifacts.is_compressed == query_object.is_compressed if query_object.is_compressed else True,
                GeneratedArtifacts.created_at == query_object.created_at if query_object.created_at else True,
            )
            .order_by(GeneratedArtifacts.id)
            .distinct()
        )
        generated_artifacts_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return generated_artifacts_list

    @classmethod
    async def add_generated_artifacts_dao(cls, db: AsyncSession, generated_artifacts: Generated_artifactsModel):
        """
        新增生成产物数据库操作

        :param db: orm对象
        :param generated_artifacts: 生成产物对象
        :return:
        """
        db_generated_artifacts = GeneratedArtifacts(**generated_artifacts.model_dump(exclude={}))
        db.add(db_generated_artifacts)
        await db.flush()

        return db_generated_artifacts

    @classmethod
    async def edit_generated_artifacts_dao(cls, db: AsyncSession, generated_artifacts: dict):
        """
        编辑生成产物数据库操作

        :param db: orm对象
        :param generated_artifacts: 需要更新的生成产物字典
        :return:
        """
        await db.execute(update(GeneratedArtifacts), [generated_artifacts])

    @classmethod
    async def delete_generated_artifacts_dao(cls, db: AsyncSession, generated_artifacts: Generated_artifactsModel):
        """
        删除生成产物数据库操作

        :param db: orm对象
        :param generated_artifacts: 生成产物对象
        :return:
        """
        await db.execute(delete(GeneratedArtifacts).where(GeneratedArtifacts.id.in_([generated_artifacts.id])))

