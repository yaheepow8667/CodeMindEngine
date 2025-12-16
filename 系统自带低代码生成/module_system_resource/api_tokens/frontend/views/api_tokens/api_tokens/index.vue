<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="用户ID" prop="userId">
        <el-input
          v-model="queryParams.userId"
          placeholder="请输入用户ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="团队ID" prop="teamId">
        <el-input
          v-model="queryParams.teamId"
          placeholder="请输入团队ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="令牌名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入令牌名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="令牌哈希值" prop="tokenHash">
        <el-input
          v-model="queryParams.tokenHash"
          placeholder="请输入令牌哈希值"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="令牌前缀" prop="tokenPrefix">
        <el-input
          v-model="queryParams.tokenPrefix"
          placeholder="请输入令牌前缀"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="过期时间" prop="expiresAt">
        <el-date-picker
          v-model="queryParams.expiresAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择过期时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="最后使用时间" prop="lastUsedAt">
        <el-date-picker
          v-model="queryParams.lastUsedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择最后使用时间"
          clearable
          style="width: 240px"
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
          v-hasPermi="['api_tokens:api_tokens:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['api_tokens:api_tokens:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['api_tokens:api_tokens:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['api_tokens:api_tokens:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="api_tokensList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="访问令牌ID" align="center" prop="id" />
      <el-table-column label="用户ID" align="center" prop="userId" />
      <el-table-column label="团队ID" align="center" prop="teamId" />
      <el-table-column label="令牌名称" align="center" prop="name" />
      <el-table-column label="令牌哈希值" align="center" prop="tokenHash" />
      <el-table-column label="令牌前缀" align="center" prop="tokenPrefix" />
      <el-table-column label="权限范围" align="center" prop="scopes" />
      <el-table-column label="过期时间" align="center" prop="expiresAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.expiresAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="最后使用时间" align="center" prop="lastUsedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.lastUsedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="是否启用" align="center" prop="isActive" />
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['api_tokens:api_tokens:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['api_tokens:api_tokens:remove']">删除</el-button>
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

    <!-- 添加或修改API访问令牌对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="api_tokensRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="用户ID" prop="userId">
        <el-input v-model="form.userId" placeholder="请输入用户ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="团队ID" prop="teamId">
        <el-input v-model="form.teamId" placeholder="请输入团队ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="令牌名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入令牌名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="令牌哈希值" prop="tokenHash">
        <el-input v-model="form.tokenHash" placeholder="请输入令牌哈希值" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="令牌前缀" prop="tokenPrefix">
        <el-input v-model="form.tokenPrefix" placeholder="请输入令牌前缀" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="过期时间" prop="expiresAt">
        <el-date-picker clearable
          v-model="form.expiresAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择过期时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="最后使用时间" prop="lastUsedAt">
        <el-date-picker clearable
          v-model="form.lastUsedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择最后使用时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否启用" prop="isActive">
        <el-input v-model="form.isActive" placeholder="请输入是否启用" />
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

<script setup name="Api_tokens">
import { listApi_tokens, getApi_tokens, delApi_tokens, addApi_tokens, updateApi_tokens } from "@/api/api_tokens/api_tokens";

const { proxy } = getCurrentInstance();

const api_tokensList = ref([]);
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
    userId: null,
    teamId: null,
    name: null,
    tokenHash: null,
    tokenPrefix: null,
    scopes: null,
    expiresAt: null,
    lastUsedAt: null,
    isActive: null,
    createdAt: null,
  },
  rules: {
    userId: [
      { required: true, message: "用户ID不能为空", trigger: "blur" }
    ],
    name: [
      { required: true, message: "令牌名称不能为空", trigger: "blur" }
    ],
    tokenHash: [
      { required: true, message: "令牌哈希值不能为空", trigger: "blur" }
    ],
    tokenPrefix: [
      { required: true, message: "令牌前缀不能为空", trigger: "blur" }
    ],
    scopes: [
      { required: true, message: "权限范围不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询API访问令牌列表 */
function getList() {
  loading.value = true;
  listApi_tokens(queryParams.value).then(response => {
    api_tokensList.value = response.rows;
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
    userId: null,
    teamId: null,
    name: null,
    tokenHash: null,
    tokenPrefix: null,
    scopes: null,
    expiresAt: null,
    lastUsedAt: null,
    isActive: null,
    createdAt: null,
  };
  proxy.resetForm("api_tokensRef");
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
  title.value = "添加API访问令牌";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getApi_tokens(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改API访问令牌";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["api_tokensRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateApi_tokens(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addApi_tokens(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除API访问令牌编号为"' + _ids + '"的数据项？').then(function() {
    return delApi_tokens(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('api_tokens/api_tokens/export', {
    ...queryParams.value
  }, `api_tokens_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>