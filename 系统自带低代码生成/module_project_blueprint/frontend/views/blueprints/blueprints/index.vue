<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="项目ID" prop="projectId">
        <el-input
          v-model="queryParams.projectId"
          placeholder="请输入项目ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="蓝图名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入蓝图名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="版本标签" prop="versionTag">
        <el-input
          v-model="queryParams.versionTag"
          placeholder="请输入版本标签"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="独立文档存储中的文档ID" prop="specDocumentId">
        <el-input
          v-model="queryParams.specDocumentId"
          placeholder="请输入独立文档存储中的文档ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="是否为草稿" prop="isDraft">
        <el-input
          v-model="queryParams.isDraft"
          placeholder="请输入是否为草稿"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="父蓝图ID" prop="parentBlueprintId">
        <el-input
          v-model="queryParams.parentBlueprintId"
          placeholder="请输入父蓝图ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="创建者用户ID" prop="createdByUserId">
        <el-input
          v-model="queryParams.createdByUserId"
          placeholder="请输入创建者用户ID"
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
      <el-form-item label="更新时间" prop="updatedAt">
        <el-date-picker
          v-model="queryParams.updatedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择更新时间"
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
          v-hasPermi="['blueprints:blueprints:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['blueprints:blueprints:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['blueprints:blueprints:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['blueprints:blueprints:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="blueprintsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="蓝图ID" align="center" prop="id" />
      <el-table-column label="项目ID" align="center" prop="projectId" />
      <el-table-column label="蓝图名称" align="center" prop="name" />
      <el-table-column label="蓝图描述" align="center" prop="description" />
      <el-table-column label="版本标签" align="center" prop="versionTag" />
      <el-table-column label="独立文档存储中的文档ID" align="center" prop="specDocumentId" />
      <el-table-column label="蓝图摘要信息" align="center" prop="specSummary" />
      <el-table-column label="是否为草稿" align="center" prop="isDraft" />
      <el-table-column label="父蓝图ID" align="center" prop="parentBlueprintId" />
      <el-table-column label="创建者用户ID" align="center" prop="createdByUserId" />
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="更新时间" align="center" prop="updatedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.updatedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['blueprints:blueprints:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['blueprints:blueprints:remove']">删除</el-button>
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

    <!-- 添加或修改蓝图对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="blueprintsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="项目ID" prop="projectId">
        <el-input v-model="form.projectId" placeholder="请输入项目ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="蓝图名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入蓝图名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="蓝图描述" prop="description">
        <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="版本标签" prop="versionTag">
        <el-input v-model="form.versionTag" placeholder="请输入版本标签" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="独立文档存储中的文档ID" prop="specDocumentId">
        <el-input v-model="form.specDocumentId" placeholder="请输入独立文档存储中的文档ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否为草稿" prop="isDraft">
        <el-input v-model="form.isDraft" placeholder="请输入是否为草稿" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="父蓝图ID" prop="parentBlueprintId">
        <el-input v-model="form.parentBlueprintId" placeholder="请输入父蓝图ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="创建者用户ID" prop="createdByUserId">
        <el-input v-model="form.createdByUserId" placeholder="请输入创建者用户ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="创建时间" prop="createdAt">
        <el-date-picker clearable
          v-model="form.createdAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择创建时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="更新时间" prop="updatedAt">
        <el-date-picker clearable
          v-model="form.updatedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择更新时间">
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

<script setup name="Blueprints">
import { listBlueprints, getBlueprints, delBlueprints, addBlueprints, updateBlueprints } from "@/api/blueprints/blueprints";

const { proxy } = getCurrentInstance();

const blueprintsList = ref([]);
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
    projectId: null,
    name: null,
    description: null,
    versionTag: null,
    specDocumentId: null,
    specSummary: null,
    isDraft: null,
    parentBlueprintId: null,
    createdByUserId: null,
    createdAt: null,
    updatedAt: null,
  },
  rules: {
    projectId: [
      { required: true, message: "项目ID不能为空", trigger: "blur" }
    ],
    name: [
      { required: true, message: "蓝图名称不能为空", trigger: "blur" }
    ],
    versionTag: [
      { required: true, message: "版本标签不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询蓝图列表 */
function getList() {
  loading.value = true;
  listBlueprints(queryParams.value).then(response => {
    blueprintsList.value = response.rows;
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
    projectId: null,
    name: null,
    description: null,
    versionTag: null,
    specDocumentId: null,
    specSummary: null,
    isDraft: null,
    parentBlueprintId: null,
    createdByUserId: null,
    createdAt: null,
    updatedAt: null,
  };
  proxy.resetForm("blueprintsRef");
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
  title.value = "添加蓝图";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getBlueprints(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改蓝图";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["blueprintsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateBlueprints(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addBlueprints(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除蓝图编号为"' + _ids + '"的数据项？').then(function() {
    return delBlueprints(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('blueprints/blueprints/export', {
    ...queryParams.value
  }, `blueprints_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>