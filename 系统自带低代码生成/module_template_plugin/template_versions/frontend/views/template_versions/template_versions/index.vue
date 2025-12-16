<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="模板ID" prop="templateId">
        <el-input
          v-model="queryParams.templateId"
          placeholder="请输入模板ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="版本号" prop="version">
        <el-input
          v-model="queryParams.version"
          placeholder="请输入版本号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="是否启用" prop="isActive">
        <el-input
          v-model="queryParams.isActive"
          placeholder="请输入是否启用"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="发布时间" prop="publishedAt">
        <el-date-picker
          v-model="queryParams.publishedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择发布时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="发布者用户ID" prop="publishedByUserId">
        <el-input
          v-model="queryParams.publishedByUserId"
          placeholder="请输入发布者用户ID"
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
          v-hasPermi="['template_versions:template_versions:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['template_versions:template_versions:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['template_versions:template_versions:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['template_versions:template_versions:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="template_versionsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="模板版本ID" align="center" prop="id" />
      <el-table-column label="模板ID" align="center" prop="templateId" />
      <el-table-column label="版本号" align="center" prop="version" />
      <el-table-column label="更新日志" align="center" prop="changelog" />
      <el-table-column label="模板JSON定义" align="center" prop="templateContent" />
      <el-table-column label="示例蓝图" align="center" prop="exampleBlueprint" />
      <el-table-column label="是否启用" align="center" prop="isActive" />
      <el-table-column label="发布时间" align="center" prop="publishedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.publishedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="发布者用户ID" align="center" prop="publishedByUserId" />
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['template_versions:template_versions:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['template_versions:template_versions:remove']">删除</el-button>
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

    <!-- 添加或修改模板版本对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="template_versionsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="模板ID" prop="templateId">
        <el-input v-model="form.templateId" placeholder="请输入模板ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="版本号" prop="version">
        <el-input v-model="form.version" placeholder="请输入版本号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="更新日志" prop="changelog">
        <el-input v-model="form.changelog" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="模板JSON定义" prop="templateContent">
        <editor v-model="form.templateContent" :min-height="192"/>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否启用" prop="isActive">
        <el-input v-model="form.isActive" placeholder="请输入是否启用" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="发布时间" prop="publishedAt">
        <el-date-picker clearable
          v-model="form.publishedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择发布时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="发布者用户ID" prop="publishedByUserId">
        <el-input v-model="form.publishedByUserId" placeholder="请输入发布者用户ID" />
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

<script setup name="Template_versions">
import { listTemplate_versions, getTemplate_versions, delTemplate_versions, addTemplate_versions, updateTemplate_versions } from "@/api/template_versions/template_versions";

const { proxy } = getCurrentInstance();

const template_versionsList = ref([]);
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
    templateId: null,
    version: null,
    changelog: null,
    templateContent: null,
    exampleBlueprint: null,
    isActive: null,
    publishedAt: null,
    publishedByUserId: null,
    createdAt: null,
  },
  rules: {
    templateId: [
      { required: true, message: "模板ID不能为空", trigger: "blur" }
    ],
    version: [
      { required: true, message: "版本号不能为空", trigger: "blur" }
    ],
    templateContent: [
      { required: true, message: "模板JSON定义不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询模板版本列表 */
function getList() {
  loading.value = true;
  listTemplate_versions(queryParams.value).then(response => {
    template_versionsList.value = response.rows;
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
    templateId: null,
    version: null,
    changelog: null,
    templateContent: null,
    exampleBlueprint: null,
    isActive: null,
    publishedAt: null,
    publishedByUserId: null,
    createdAt: null,
  };
  proxy.resetForm("template_versionsRef");
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
  title.value = "添加模板版本";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getTemplate_versions(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改模板版本";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["template_versionsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateTemplate_versions(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addTemplate_versions(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除模板版本编号为"' + _ids + '"的数据项？').then(function() {
    return delTemplate_versions(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('template_versions/template_versions/export', {
    ...queryParams.value
  }, `template_versions_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>