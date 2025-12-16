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
      <el-form-item label="用户ID" prop="userId">
        <el-input
          v-model="queryParams.userId"
          placeholder="请输入用户ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="成员角色 (owner, admin, member, viewer)" prop="role">
        <el-input
          v-model="queryParams.role"
          placeholder="请输入成员角色 (owner, admin, member, viewer)"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="加入时间" prop="joinedAt">
        <el-date-picker
          v-model="queryParams.joinedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择加入时间"
          clearable
          style="width: 240px"
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
      <el-form-item label="邀请时间" prop="invitedAt">
        <el-date-picker
          v-model="queryParams.invitedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择邀请时间"
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
          v-hasPermi="['team_members:members:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['team_members:members:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['team_members:members:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['team_members:members:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="membersList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="" align="center" prop="id" />
      <el-table-column label="团队ID" align="center" prop="teamId" />
      <el-table-column label="用户ID" align="center" prop="userId" />
      <el-table-column label="成员角色 (owner, admin, member, viewer)" align="center" prop="role" />
      <el-table-column label="加入时间" align="center" prop="joinedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.joinedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="邀请者用户ID" align="center" prop="invitedByUserId" />
      <el-table-column label="邀请时间" align="center" prop="invitedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.invitedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['team_members:members:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['team_members:members:remove']">删除</el-button>
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

    <!-- 添加或修改团队成员对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="membersRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="团队ID" prop="teamId">
        <el-input v-model="form.teamId" placeholder="请输入团队ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="用户ID" prop="userId">
        <el-input v-model="form.userId" placeholder="请输入用户ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="成员角色 (owner, admin, member, viewer)" prop="role">
        <el-input v-model="form.role" placeholder="请输入成员角色 (owner, admin, member, viewer)" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="加入时间" prop="joinedAt">
        <el-date-picker clearable
          v-model="form.joinedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择加入时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邀请者用户ID" prop="invitedByUserId">
        <el-input v-model="form.invitedByUserId" placeholder="请输入邀请者用户ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="邀请时间" prop="invitedAt">
        <el-date-picker clearable
          v-model="form.invitedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择邀请时间">
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

<script setup name="Members">
import { listMembers, getMembers, delMembers, addMembers, updateMembers } from "@/api/team_members/members";

const { proxy } = getCurrentInstance();

const membersList = ref([]);
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
    userId: null,
    role: null,
    joinedAt: null,
    invitedByUserId: null,
    invitedAt: null,
    createdAt: null,
  },
  rules: {
    teamId: [
      { required: true, message: "团队ID不能为空", trigger: "blur" }
    ],
    userId: [
      { required: true, message: "用户ID不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询团队成员列表 */
function getList() {
  loading.value = true;
  listMembers(queryParams.value).then(response => {
    membersList.value = response.rows;
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
    userId: null,
    role: null,
    joinedAt: null,
    invitedByUserId: null,
    invitedAt: null,
    createdAt: null,
  };
  proxy.resetForm("membersRef");
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
  title.value = "添加团队成员";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getMembers(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改团队成员";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["membersRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateMembers(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addMembers(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除团队成员编号为"' + _ids + '"的数据项？').then(function() {
    return delMembers(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('team_members/members/export', {
    ...queryParams.value
  }, `members_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>