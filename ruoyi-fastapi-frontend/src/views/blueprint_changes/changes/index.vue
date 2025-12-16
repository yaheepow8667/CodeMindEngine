<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="蓝图ID" prop="blueprintId">
        <el-input
          v-model="queryParams.blueprintId"
          placeholder="请输入蓝图ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="变更类型 (create, update, delete)" prop="changeType">
        <el-select v-model="queryParams.changeType" placeholder="请选择变更类型 (create, update, delete)" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="变更字段路径 如 "dataModels.User.fields"" prop="fieldPath">
        <el-input
          v-model="queryParams.fieldPath"
          placeholder="请输入变更字段路径 如 "dataModels.User.fields""
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="变更者用户ID" prop="changedByUserId">
        <el-input
          v-model="queryParams.changedByUserId"
          placeholder="请输入变更者用户ID"
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
          v-hasPermi="['blueprint_changes:changes:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['blueprint_changes:changes:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['blueprint_changes:changes:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['blueprint_changes:changes:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="changesList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="蓝图变更ID" align="center" prop="id" />
      <el-table-column label="蓝图ID" align="center" prop="blueprintId" />
      <el-table-column label="变更类型 (create, update, delete)" align="center" prop="changeType" />
      <el-table-column label="变更字段路径 如 "dataModels.User.fields"" align="center" prop="fieldPath" />
      <el-table-column label="旧值" align="center" prop="oldValue" />
      <el-table-column label="新值" align="center" prop="newValue" />
      <el-table-column label="变更者用户ID" align="center" prop="changedByUserId" />
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['blueprint_changes:changes:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['blueprint_changes:changes:remove']">删除</el-button>
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

    <!-- 添加或修改蓝图变更记录对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="changesRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="蓝图ID" prop="blueprintId">
        <el-input v-model="form.blueprintId" placeholder="请输入蓝图ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="变更类型 (create, update, delete)" prop="changeType">
        <el-select v-model="form.changeType" placeholder="请选择变更类型 (create, update, delete)">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="变更字段路径 如 "dataModels.User.fields"" prop="fieldPath">
        <el-input v-model="form.fieldPath" placeholder="请输入变更字段路径 如 "dataModels.User.fields"" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="变更者用户ID" prop="changedByUserId">
        <el-input v-model="form.changedByUserId" placeholder="请输入变更者用户ID" />
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

<script setup name="Changes">
import { listChanges, getChanges, delChanges, addChanges, updateChanges } from "@/api/blueprint_changes/changes";

const { proxy } = getCurrentInstance();

const changesList = ref([]);
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
    blueprintId: null,
    changeType: null,
    fieldPath: null,
    oldValue: null,
    newValue: null,
    changedByUserId: null,
    createdAt: null,
  },
  rules: {
    blueprintId: [
      { required: true, message: "蓝图ID不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询蓝图变更记录列表 */
function getList() {
  loading.value = true;
  listChanges(queryParams.value).then(response => {
    changesList.value = response.rows;
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
    blueprintId: null,
    changeType: null,
    fieldPath: null,
    oldValue: null,
    newValue: null,
    changedByUserId: null,
    createdAt: null,
  };
  proxy.resetForm("changesRef");
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
  title.value = "添加蓝图变更记录";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getChanges(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改蓝图变更记录";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["changesRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateChanges(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addChanges(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除蓝图变更记录编号为"' + _ids + '"的数据项？').then(function() {
    return delChanges(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('blueprint_changes/changes/export', {
    ...queryParams.value
  }, `changes_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>