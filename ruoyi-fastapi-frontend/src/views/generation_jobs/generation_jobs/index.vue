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
      <el-form-item label="蓝图ID" prop="blueprintId">
        <el-input
          v-model="queryParams.blueprintId"
          placeholder="请输入蓝图ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="任务状态 (pending, generating, qa, success, failed)" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择任务状态 (pending, generating, qa, success, failed)" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="触发类型 (manual, api, webhook, schedule)" prop="triggerType">
        <el-select v-model="queryParams.triggerType" placeholder="请选择触发类型 (manual, api, webhook, schedule)" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="触发者用户ID" prop="triggeredByUserId">
        <el-input
          v-model="queryParams.triggeredByUserId"
          placeholder="请输入触发者用户ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="开始时间" prop="startedAt">
        <el-date-picker
          v-model="queryParams.startedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择开始时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="完成时间" prop="completedAt">
        <el-date-picker
          v-model="queryParams.completedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择完成时间"
          clearable
          style="width: 240px"
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
          v-hasPermi="['generation_jobs:generation_jobs:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['generation_jobs:generation_jobs:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['generation_jobs:generation_jobs:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['generation_jobs:generation_jobs:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="generation_jobsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="生成任务ID" align="center" prop="id" />
      <el-table-column label="项目ID" align="center" prop="projectId" />
      <el-table-column label="蓝图ID" align="center" prop="blueprintId" />
      <el-table-column label="任务状态 (pending, generating, qa, success, failed)" align="center" prop="status" />
      <el-table-column label="目标技术栈配置" align="center" prop="targetTechStack" />
      <el-table-column label="触发类型 (manual, api, webhook, schedule)" align="center" prop="triggerType" />
      <el-table-column label="触发者用户ID" align="center" prop="triggeredByUserId" />
      <el-table-column label="开始时间" align="center" prop="startedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.startedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="完成时间" align="center" prop="completedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.completedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="错误信息" align="center" prop="errorMessage" />
      <el-table-column label="生成日志" align="center" prop="logs" />
      <el-table-column label="质量检查报告" align="center" prop="qaReport" />
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['generation_jobs:generation_jobs:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['generation_jobs:generation_jobs:remove']">删除</el-button>
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

    <!-- 添加或修改生成任务对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="generation_jobsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="项目ID" prop="projectId">
        <el-input v-model="form.projectId" placeholder="请输入项目ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="蓝图ID" prop="blueprintId">
        <el-input v-model="form.blueprintId" placeholder="请输入蓝图ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="任务状态 (pending, generating, qa, success, failed)" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio label="请选择字典生成" value="" />
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="触发类型 (manual, api, webhook, schedule)" prop="triggerType">
        <el-select v-model="form.triggerType" placeholder="请选择触发类型 (manual, api, webhook, schedule)">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="触发者用户ID" prop="triggeredByUserId">
        <el-input v-model="form.triggeredByUserId" placeholder="请输入触发者用户ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="开始时间" prop="startedAt">
        <el-date-picker clearable
          v-model="form.startedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择开始时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="完成时间" prop="completedAt">
        <el-date-picker clearable
          v-model="form.completedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择完成时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="错误信息" prop="errorMessage">
        <el-input v-model="form.errorMessage" type="textarea" placeholder="请输入内容" />
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

<script setup name="Generation_jobs">
import { listGeneration_jobs, getGeneration_jobs, delGeneration_jobs, addGeneration_jobs, updateGeneration_jobs } from "@/api/generation_jobs/generation_jobs";

const { proxy } = getCurrentInstance();

const generation_jobsList = ref([]);
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
    blueprintId: null,
    status: null,
    targetTechStack: null,
    triggerType: null,
    triggeredByUserId: null,
    startedAt: null,
    completedAt: null,
    errorMessage: null,
    logs: null,
    qaReport: null,
    createdAt: null,
  },
  rules: {
    projectId: [
      { required: true, message: "项目ID不能为空", trigger: "blur" }
    ],
    blueprintId: [
      { required: true, message: "蓝图ID不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询生成任务列表 */
function getList() {
  loading.value = true;
  listGeneration_jobs(queryParams.value).then(response => {
    generation_jobsList.value = response.rows;
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
    blueprintId: null,
    status: null,
    targetTechStack: null,
    triggerType: null,
    triggeredByUserId: null,
    startedAt: null,
    completedAt: null,
    errorMessage: null,
    logs: null,
    qaReport: null,
    createdAt: null,
  };
  proxy.resetForm("generation_jobsRef");
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
  title.value = "添加生成任务";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getGeneration_jobs(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改生成任务";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["generation_jobsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateGeneration_jobs(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addGeneration_jobs(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除生成任务编号为"' + _ids + '"的数据项？').then(function() {
    return delGeneration_jobs(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('generation_jobs/generation_jobs/export', {
    ...queryParams.value
  }, `generation_jobs_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>