from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Generated_artifactsModel(BaseModel):
    """
    生成产物表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='产物ID')
    job_id: Optional[int] = Field(default=None, description='生成任务ID')
    artifact_type: Optional[str] = Field(default=None, description='产物类型 (source_zip, qa_report, deploy_config, api_docs)')
    artifact_name: Optional[str] = Field(default=None, description='产物名称')
    storage_type: Optional[str] = Field(default=None, description='存储类型 (s3, oss, local)')
    storage_path: Optional[str] = Field(default=None, description='存储路径')
    storage_url: Optional[str] = Field(default=None, description='访问URL')
    file_size_bytes: Optional[int] = Field(default=None, description='文件大小 (字节)')
    mime_type: Optional[str] = Field(default=None, description='文件类型')
    checksum: Optional[str] = Field(default=None, description='校验和')
    is_compressed: Optional[int] = Field(default=None, description='是否压缩')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')

    @NotBlank(field_name='job_id', message='生成任务ID不能为空')
    def get_job_id(self):
        return self.job_id

    @NotBlank(field_name='artifact_type', message='产物类型 (source_zip, qa_report, deploy_config, api_docs)不能为空')
    def get_artifact_type(self):
        return self.artifact_type

    @NotBlank(field_name='artifact_name', message='产物名称不能为空')
    def get_artifact_name(self):
        return self.artifact_name

    @NotBlank(field_name='storage_path', message='存储路径不能为空')
    def get_storage_path(self):
        return self.storage_path


    def validate_fields(self):
        self.get_job_id()
        self.get_artifact_type()
        self.get_artifact_name()
        self.get_storage_path()




class Generated_artifactsQueryModel(Generated_artifactsModel):
    """
    生成产物不分页查询模型
    """
    pass


@as_query
class Generated_artifactsPageQueryModel(Generated_artifactsQueryModel):
    """
    生成产物分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteGenerated_artifactsModel(BaseModel):
    """
    删除生成产物模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的产物ID')
