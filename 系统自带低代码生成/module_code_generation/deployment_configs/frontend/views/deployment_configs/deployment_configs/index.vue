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
      <el-form-item label="配置名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入配置名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="部署环境 (development, staging, production)" prop="environment">
        <el-input
          v-model="queryParams.environment"
          placeholder="请输入部署环境 (development, staging, production)"
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
      <el-form-item label="已部署的任务ID" prop="deployedJobId">
        <el-input
          v-model="queryParams.deployedJobId"
          placeholder="请输入已部署的任务ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="部署时间" prop="deployedAt">
        <el-date-picker
          v-model="queryParams.deployedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择部署时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="部署者用户ID" prop="deployedByUserId">
        <el-input
          v-model="queryParams.deployedByUserId"
          placeholder="请输入部署者用户ID"
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
          v-hasPermi="['deployment_configs:deployment_configs:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['deployment_configs:deployment_configs:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['deployment_configs:deployment_configs:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['deployment_configs:deployment_configs:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="deployment_configsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="部署配置ID" align="center" prop="id" />
      <el-table-column label="项目ID" align="center" prop="projectId" />
      <el-table-column label="配置名称" align="center" prop="name" />
      <el-table-column label="部署环境 (development, staging, production)" align="center" prop="environment" />
      <el-table-column label="部署配置内容" align="center" prop="config" />
      <el-table-column label="是否启用" align="center" prop="isActive" />
      <el-table-column label="已部署的任务ID" align="center" prop="deployedJobId" />
      <el-table-column label="部署时间" align="center" prop="deployedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.deployedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="部署者用户ID" align="center" prop="deployedByUserId" />
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
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['deployment_configs:deployment_configs:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['deployment_configs:deployment_configs:remove']">删除</el-button>
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

    <!-- 添加或修改部署配置对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="deployment_configsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="项目ID" prop="projectId">
        <el-input v-model="form.projectId" placeholder="请输入项目ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="配置名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入配置名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="部署环境 (development, staging, production)" prop="environment">
        <el-input v-model="form.environment" placeholder="请输入部署环境 (development, staging, production)" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否启用" prop="isActive">
        <el-input v-model="form.isActive" placeholder="请输入是否启用" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="已部署的任务ID" prop="deployedJobId">
        <el-input v-model="form.deployedJobId" placeholder="请输入已部署的任务ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="部署时间" prop="deployedAt">
        <el-date-picker clearable
          v-model="form.deployedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择部署时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="部署者用户ID" prop="deployedByUserId">
        <el-input v-model="form.deployedByUserId" placeholder="请输入部署者用户ID" />
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

<script setup name="Deployment_configs">
import { listDeployment_configs, getDeployment_configs, delDeployment_configs, addDeployment_configs, updateDeployment_configs } from "@/api/deployment_configs/deployment_configs";

const { proxy } = getCurrentInstance();

const deployment_configsList = ref([]);
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
    environment: null,
    config: null,
    isActive: null,
    deployedJobId: null,
    deployedAt: null,
    deployedByUserId: null,
    createdAt: null,
    updatedAt: null,
  },
  rules: {
    projectId: [
      { required: true, message: "项目ID不能为空", trigger: "blur" }
    ],
    name: [
      { required: true, message: "配置名称不能为空", trigger: "blur" }
    ],
    environment: [
      { required: true, message: "部署环境 (development, staging, production)不能为空", trigger: "blur" }
    ],
    config: [
      { required: true, message: "部署配置内容不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询部署配置列表 */
function getList() {
  loading.value = true;
  listDeployment_configs(queryParams.value).then(response => {
    deployment_configsList.value = response.rows;
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
    environment: null,
    config: null,
    isActive: null,
    deployedJobId: null,
    deployedAt: null,
    deployedByUserId: null,
    createdAt: null,
    updatedAt: null,
  };
  proxy.resetForm("deployment_configsRef");
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
  title.value = "添加部署配置";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getDeployment_configs(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改部署配置";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["deployment_configsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateDeployment_configs(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addDeployment_configs(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除部署配置编号为"' + _ids + '"的数据项？').then(function() {
    return delDeployment_configs(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('deployment_configs/deployment_configs/export', {
    ...queryParams.value
  }, `deployment_configs_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>