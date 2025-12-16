<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="生成任务ID" prop="jobId">
        <el-input
          v-model="queryParams.jobId"
          placeholder="请输入生成任务ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="产物类型 (source_zip, qa_report, deploy_config, api_docs)" prop="artifactType">
        <el-select v-model="queryParams.artifactType" placeholder="请选择产物类型 (source_zip, qa_report, deploy_config, api_docs)" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="产物名称" prop="artifactName">
        <el-input
          v-model="queryParams.artifactName"
          placeholder="请输入产物名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="存储类型 (s3, oss, local)" prop="storageType">
        <el-select v-model="queryParams.storageType" placeholder="请选择存储类型 (s3, oss, local)" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="文件大小 (字节)" prop="fileSizeBytes">
        <el-input
          v-model="queryParams.fileSizeBytes"
          placeholder="请输入文件大小 (字节)"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="文件类型" prop="mimeType">
        <el-select v-model="queryParams.mimeType" placeholder="请选择文件类型" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="校验和" prop="checksum">
        <el-input
          v-model="queryParams.checksum"
          placeholder="请输入校验和"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="是否压缩" prop="isCompressed">
        <el-input
          v-model="queryParams.isCompressed"
          placeholder="请输入是否压缩"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="创建时间" prop="createdAt">
        <el-date-picker
          v-model="queryParams.createdAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择创建时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['generated_artifacts:generated_artifacts:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['generated_artifacts:generated_artifacts:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['generated_artifacts:generated_artifacts:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['generated_artifacts:generated_artifacts:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="generated_artifactsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="产物ID" align="center" prop="id" />
      <el-table-column label="生成任务ID" align="center" prop="jobId" />
      <el-table-column label="产物类型 (source_zip, qa_report, deploy_config, api_docs)" align="center" prop="artifactType" />
      <el-table-column label="产物名称" align="center" prop="artifactName" />
      <el-table-column label="存储类型 (s3, oss, local)" align="center" prop="storageType" />
      <el-table-column label="存储路径" align="center" prop="storagePath" />
      <el-table-column label="访问URL" align="center" prop="storageUrl" />
      <el-table-column label="文件大小 (字节)" align="center" prop="fileSizeBytes" />
      <el-table-column label="文件类型" align="center" prop="mimeType" />
      <el-table-column label="校验和" align="center" prop="checksum" />
      <el-table-column label="是否压缩" align="center" prop="isCompressed" />
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['generated_artifacts:generated_artifacts:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['generated_artifacts:generated_artifacts:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改生成产物对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="generated_artifactsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="生成任务ID" prop="jobId">
        <el-input v-model="form.jobId" placeholder="请输入生成任务ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="产物类型 (source_zip, qa_report, deploy_config, api_docs)" prop="artifactType">
        <el-select v-model="form.artifactType" placeholder="请选择产物类型 (source_zip, qa_report, deploy_config, api_docs)">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="产物名称" prop="artifactName">
        <el-input v-model="form.artifactName" placeholder="请输入产物名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="存储类型 (s3, oss, local)" prop="storageType">
        <el-select v-model="form.storageType" placeholder="请选择存储类型 (s3, oss, local)">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="存储路径" prop="storagePath">
        <el-input v-model="form.storagePath" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="访问URL" prop="storageUrl">
        <el-input v-model="form.storageUrl" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文件大小 (字节)" prop="fileSizeBytes">
        <el-input v-model="form.fileSizeBytes" placeholder="请输入文件大小 (字节)" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文件类型" prop="mimeType">
        <el-select v-model="form.mimeType" placeholder="请选择文件类型">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="校验和" prop="checksum">
        <el-input v-model="form.checksum" placeholder="请输入校验和" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否压缩" prop="isCompressed">
        <el-input v-model="form.isCompressed" placeholder="请输入是否压缩" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="创建时间" prop="createdAt">
        <el-date-picker clearable
          v-model="form.createdAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择创建时间">
        </el-date-picker>
      </el-form-item>

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Generated_artifacts">
import { listGenerated_artifacts, getGenerated_artifacts, delGenerated_artifacts, addGenerated_artifacts, updateGenerated_artifacts } from "@/api/generated_artifacts/generated_artifacts";

const { proxy } = getCurrentInstance();

const generated_artifactsList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    jobId: null,
    artifactType: null,
    artifactName: null,
    storageType: null,
    storagePath: null,
    storageUrl: null,
    fileSizeBytes: null,
    mimeType: null,
    checksum: null,
    isCompressed: null,
    createdAt: null,
  },
  rules: {
    jobId: [
      { required: true, message: "生成任务ID不能为空", trigger: "blur" }
    ],
    artifactType: [
      { required: true, message: "产物类型 (source_zip, qa_report, deploy_config, api_docs)不能为空", trigger: "change" }
    ],
    artifactName: [
      { required: true, message: "产物名称不能为空", trigger: "blur" }
    ],
    storagePath: [
      { required: true, message: "存储路径不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询生成产物列表 */
function getList() {
  loading.value = true;
  listGenerated_artifacts(queryParams.value).then(response => {
    generated_artifactsList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    id: null,
    jobId: null,
    artifactType: null,
    artifactName: null,
    storageType: null,
    storagePath: null,
    storageUrl: null,
    fileSizeBytes: null,
    mimeType: null,
    checksum: null,
    isCompressed: null,
    createdAt: null,
  };
  proxy.resetForm("generated_artifactsRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 多选框选中数据  */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加生成产物";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getGenerated_artifacts(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改生成产物";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["generated_artifactsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateGenerated_artifacts(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addGenerated_artifacts(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _ids = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除生成产物编号为"' + _ids + '"的数据项？').then(function() {
    return delGenerated_artifacts(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('generated_artifacts/generated_artifacts/export', {
    ...queryParams.value
  }, `generated_artifacts_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>