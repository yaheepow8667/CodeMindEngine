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
      <el-form-item label="项目名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入项目名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="项目标识" prop="slug">
        <el-input
          v-model="queryParams.slug"
          placeholder="请输入项目标识"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="项目状态 (active, archived, deleted)" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择项目状态 (active, archived, deleted)" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="是否公开" prop="isPublic">
        <el-input
          v-model="queryParams.isPublic"
          placeholder="请输入是否公开"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="存储配额 (MB)" prop="storageQuotaMb">
        <el-input
          v-model="queryParams.storageQuotaMb"
          placeholder="请输入存储配额 (MB)"
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
          v-hasPermi="['projects:projects:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['projects:projects:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['projects:projects:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['projects:projects:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="projectsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="项目ID" align="center" prop="id" />
      <el-table-column label="团队ID" align="center" prop="teamId" />
      <el-table-column label="项目名称" align="center" prop="name" />
      <el-table-column label="项目标识" align="center" prop="slug" />
      <el-table-column label="项目描述" align="center" prop="description" />
      <el-table-column label="技术栈配置 {"frontend": "vue3", "backend": "nestjs", "ui": "ant-design-vue"}" align="center" prop="techStack" />
      <el-table-column label="项目状态 (active, archived, deleted)" align="center" prop="status" />
      <el-table-column label="是否公开" align="center" prop="isPublic" />
      <el-table-column label="存储配额 (MB)" align="center" prop="storageQuotaMb" />
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
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['projects:projects:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['projects:projects:remove']">删除</el-button>
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

    <!-- 添加或修改项目对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="projectsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="团队ID" prop="teamId">
        <el-input v-model="form.teamId" placeholder="请输入团队ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入项目名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目标识" prop="slug">
        <el-input v-model="form.slug" placeholder="请输入项目标识" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目描述" prop="description">
        <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目状态 (active, archived, deleted)" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio label="请选择字典生成" value="" />
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否公开" prop="isPublic">
        <el-input v-model="form.isPublic" placeholder="请输入是否公开" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="存储配额 (MB)" prop="storageQuotaMb">
        <el-input v-model="form.storageQuotaMb" placeholder="请输入存储配额 (MB)" />
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

<script setup name="Projects">
import { listProjects, getProjects, delProjects, addProjects, updateProjects } from "@/api/projects/projects";

const { proxy } = getCurrentInstance();

const projectsList = ref([]);
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
    name: null,
    slug: null,
    description: null,
    techStack: null,
    status: null,
    isPublic: null,
    storageQuotaMb: null,
    createdByUserId: null,
    createdAt: null,
    updatedAt: null,
  },
  rules: {
    teamId: [
      { required: true, message: "团队ID不能为空", trigger: "blur" }
    ],
    name: [
      { required: true, message: "项目名称不能为空", trigger: "blur" }
    ],
    slug: [
      { required: true, message: "项目标识不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询项目列表 */
function getList() {
  loading.value = true;
  listProjects(queryParams.value).then(response => {
    projectsList.value = response.rows;
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
    name: null,
    slug: null,
    description: null,
    techStack: null,
    status: null,
    isPublic: null,
    storageQuotaMb: null,
    createdByUserId: null,
    createdAt: null,
    updatedAt: null,
  };
  proxy.resetForm("projectsRef");
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
  title.value = "添加项目";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getProjects(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改项目";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["projectsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateProjects(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addProjects(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除项目编号为"' + _ids + '"的数据项？').then(function() {
    return delProjects(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('projects/projects/export', {
    ...queryParams.value
  }, `projects_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>