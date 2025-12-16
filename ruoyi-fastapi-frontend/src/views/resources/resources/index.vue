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
      <el-form-item label="资源名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入资源名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="资源类型 (image, file, json, sql)" prop="resourceType">
        <el-select v-model="queryParams.resourceType" placeholder="请选择资源类型 (image, file, json, sql)" clearable style="width: 240px">
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
      <el-form-item label="上传者用户ID" prop="uploadedByUserId">
        <el-input
          v-model="queryParams.uploadedByUserId"
          placeholder="请输入上传者用户ID"
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
          v-hasPermi="['resources:resources:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['resources:resources:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['resources:resources:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['resources:resources:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="resourcesList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="文件资源ID" align="center" prop="id" />
      <el-table-column label="项目ID" align="center" prop="projectId" />
      <el-table-column label="资源名称" align="center" prop="name" />
      <el-table-column label="资源类型 (image, file, json, sql)" align="center" prop="resourceType" />
      <el-table-column label="存储路径" align="center" prop="storagePath" />
      <el-table-column label="文件大小 (字节)" align="center" prop="fileSizeBytes" />
      <el-table-column label="上传者用户ID" align="center" prop="uploadedByUserId" />
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['resources:resources:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['resources:resources:remove']">删除</el-button>
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

    <!-- 添加或修改文件资源对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="resourcesRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="项目ID" prop="projectId">
        <el-input v-model="form.projectId" placeholder="请输入项目ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="资源名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入资源名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="资源类型 (image, file, json, sql)" prop="resourceType">
        <el-select v-model="form.resourceType" placeholder="请选择资源类型 (image, file, json, sql)">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="存储路径" prop="storagePath">
        <el-input v-model="form.storagePath" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文件大小 (字节)" prop="fileSizeBytes">
        <el-input v-model="form.fileSizeBytes" placeholder="请输入文件大小 (字节)" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="上传者用户ID" prop="uploadedByUserId">
        <el-input v-model="form.uploadedByUserId" placeholder="请输入上传者用户ID" />
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

<script setup name="Resources">
import { listResources, getResources, delResources, addResources, updateResources } from "@/api/resources/resources";

const { proxy } = getCurrentInstance();

const resourcesList = ref([]);
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
    resourceType: null,
    storagePath: null,
    fileSizeBytes: null,
    uploadedByUserId: null,
    createdAt: null,
  },
  rules: {
    projectId: [
      { required: true, message: "项目ID不能为空", trigger: "blur" }
    ],
    name: [
      { required: true, message: "资源名称不能为空", trigger: "blur" }
    ],
    resourceType: [
      { required: true, message: "资源类型 (image, file, json, sql)不能为空", trigger: "change" }
    ],
    storagePath: [
      { required: true, message: "存储路径不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询文件资源列表 */
function getList() {
  loading.value = true;
  listResources(queryParams.value).then(response => {
    resourcesList.value = response.rows;
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
    resourceType: null,
    storagePath: null,
    fileSizeBytes: null,
    uploadedByUserId: null,
    createdAt: null,
  };
  proxy.resetForm("resourcesRef");
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
  title.value = "添加文件资源";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getResources(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改文件资源";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["resourcesRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateResources(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addResources(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除文件资源编号为"' + _ids + '"的数据项？').then(function() {
    return delResources(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('resources/resources/export', {
    ...queryParams.value
  }, `resources_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>