<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="团队ID" prop="teamId">
        <el-input
          v-model="queryParams.teamId"
          placeholder="请输入团队ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="邀请邮箱" prop="email">
        <el-input
          v-model="queryParams.email"
          placeholder="请输入邀请邮箱"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="邀请令牌" prop="token">
        <el-input
          v-model="queryParams.token"
          placeholder="请输入邀请令牌"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="邀请角色" prop="role">
        <el-input
          v-model="queryParams.role"
          placeholder="请输入邀请角色"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="邀请者用户ID" prop="invitedByUserId">
        <el-input
          v-model="queryParams.invitedByUserId"
          placeholder="请输入邀请者用户ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="邀请过期时间" prop="expiresAt">
        <el-date-picker
          v-model="queryParams.expiresAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择邀请过期时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="接受时间" prop="acceptedAt">
        <el-date-picker
          v-model="queryParams.acceptedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择接受时间"
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
          v-hasPermi="['invitations:invitations:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['invitations:invitations:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['invitations:invitations:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['invitations:invitations:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="invitationsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="" align="center" prop="id" />
      <el-table-column label="团队ID" align="center" prop="teamId" />
      <el-table-column label="邀请邮箱" align="center" prop="email" />
      <el-table-column label="邀请令牌" align="center" prop="token" />
      <el-table-column label="邀请角色" align="center" prop="role" />
      <el-table-column label="邀请者用户ID" align="center" prop="invitedByUserId" />
      <el-table-column label="邀请过期时间" align="center" prop="expiresAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.expiresAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="接受时间" align="center" prop="acceptedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.acceptedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['invitations:invitations:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['invitations:invitations:remove']">删除</el-button>
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

    <!-- 添加或修改邀请对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="invitationsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="团队ID" prop="teamId">
        <el-input v-model="form.teamId" placeholder="请输入团队ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邀请邮箱" prop="email">
        <el-input v-model="form.email" placeholder="请输入邀请邮箱" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邀请令牌" prop="token">
        <el-input v-model="form.token" placeholder="请输入邀请令牌" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邀请角色" prop="role">
        <el-input v-model="form.role" placeholder="请输入邀请角色" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邀请者用户ID" prop="invitedByUserId">
        <el-input v-model="form.invitedByUserId" placeholder="请输入邀请者用户ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邀请过期时间" prop="expiresAt">
        <el-date-picker clearable
          v-model="form.expiresAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择邀请过期时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="接受时间" prop="acceptedAt">
        <el-date-picker clearable
          v-model="form.acceptedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择接受时间">
        </el-date-picker>
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

<script setup name="Invitations">
import { listInvitations, getInvitations, delInvitations, addInvitations, updateInvitations } from "@/api/invitations/invitations";

const { proxy } = getCurrentInstance();

const invitationsList = ref([]);
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
    teamId: null,
    email: null,
    token: null,
    role: null,
    invitedByUserId: null,
    expiresAt: null,
    acceptedAt: null,
    createdAt: null,
  },
  rules: {
    teamId: [
      { required: true, message: "团队ID不能为空", trigger: "blur" }
    ],
    email: [
      { required: true, message: "邀请邮箱不能为空", trigger: "blur" }
    ],
    token: [
      { required: true, message: "邀请令牌不能为空", trigger: "blur" }
    ],
    expiresAt: [
      { required: true, message: "邀请过期时间不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询邀请列表 */
function getList() {
  loading.value = true;
  listInvitations(queryParams.value).then(response => {
    invitationsList.value = response.rows;
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
    teamId: null,
    email: null,
    token: null,
    role: null,
    invitedByUserId: null,
    expiresAt: null,
    acceptedAt: null,
    createdAt: null,
  };
  proxy.resetForm("invitationsRef");
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
  title.value = "添加邀请";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getInvitations(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改邀请";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["invitationsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateInvitations(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addInvitations(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除邀请编号为"' + _ids + '"的数据项？').then(function() {
    return delInvitations(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('invitations/invitations/export', {
    ...queryParams.value
  }, `invitations_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>