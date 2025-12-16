<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="模板名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入模板名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="模板标识" prop="slug">
        <el-input
          v-model="queryParams.slug"
          placeholder="请输入模板标识"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="模板分类 (ui_component, api_layer, project_scaffold, workflow)" prop="category">
        <el-input
          v-model="queryParams.category"
          placeholder="请输入模板分类 (ui_component, api_layer, project_scaffold, workflow)"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="目标框架 (vue3, react, nestjs, spring_boot)" prop="targetFramework">
        <el-input
          v-model="queryParams.targetFramework"
          placeholder="请输入目标框架 (vue3, react, nestjs, spring_boot)"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="复杂度 (basic, intermediate, advanced)" prop="complexityLevel">
        <el-input
          v-model="queryParams.complexityLevel"
          placeholder="请输入复杂度 (basic, intermediate, advanced)"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="是否官方模板" prop="isOfficial">
        <el-input
          v-model="queryParams.isOfficial"
          placeholder="请输入是否官方模板"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
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
      <el-form-item label="作者用户ID" prop="authorUserId">
        <el-input
          v-model="queryParams.authorUserId"
          placeholder="请输入作者用户ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="下载次数" prop="downloadCount">
        <el-input
          v-model="queryParams.downloadCount"
          placeholder="请输入下载次数"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="评分" prop="rating">
        <el-input
          v-model="queryParams.rating"
          placeholder="请输入评分"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="版本" prop="version">
        <el-input
          v-model="queryParams.version"
          placeholder="请输入版本"
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
          v-hasPermi="['templates:templates:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['templates:templates:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['templates:templates:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['templates:templates:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="templatesList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="模板ID" align="center" prop="id" />
      <el-table-column label="模板名称" align="center" prop="name" />
      <el-table-column label="模板标识" align="center" prop="slug" />
      <el-table-column label="模板描述" align="center" prop="description" />
      <el-table-column label="模板分类 (ui_component, api_layer, project_scaffold, workflow)" align="center" prop="category" />
      <el-table-column label="目标框架 (vue3, react, nestjs, spring_boot)" align="center" prop="targetFramework" />
      <el-table-column label="复杂度 (basic, intermediate, advanced)" align="center" prop="complexityLevel" />
      <el-table-column label="是否官方模板" align="center" prop="isOfficial" />
      <el-table-column label="是否公开" align="center" prop="isPublic" />
      <el-table-column label="作者用户ID" align="center" prop="authorUserId" />
      <el-table-column label="下载次数" align="center" prop="downloadCount" />
      <el-table-column label="评分" align="center" prop="rating" />
      <el-table-column label="版本" align="center" prop="version" />
      <el-table-column label="标签数组" align="center" prop="tags" />
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
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['templates:templates:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['templates:templates:remove']">删除</el-button>
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

    <!-- 添加或修改模板对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="templatesRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="模板名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入模板名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="模板标识" prop="slug">
        <el-input v-model="form.slug" placeholder="请输入模板标识" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="模板描述" prop="description">
        <el-input v-model="form.description" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="模板分类 (ui_component, api_layer, project_scaffold, workflow)" prop="category">
        <el-input v-model="form.category" placeholder="请输入模板分类 (ui_component, api_layer, project_scaffold, workflow)" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="目标框架 (vue3, react, nestjs, spring_boot)" prop="targetFramework">
        <el-input v-model="form.targetFramework" placeholder="请输入目标框架 (vue3, react, nestjs, spring_boot)" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="复杂度 (basic, intermediate, advanced)" prop="complexityLevel">
        <el-input v-model="form.complexityLevel" placeholder="请输入复杂度 (basic, intermediate, advanced)" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否官方模板" prop="isOfficial">
        <el-input v-model="form.isOfficial" placeholder="请输入是否官方模板" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否公开" prop="isPublic">
        <el-input v-model="form.isPublic" placeholder="请输入是否公开" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="作者用户ID" prop="authorUserId">
        <el-input v-model="form.authorUserId" placeholder="请输入作者用户ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="下载次数" prop="downloadCount">
        <el-input v-model="form.downloadCount" placeholder="请输入下载次数" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="评分" prop="rating">
        <el-input v-model="form.rating" placeholder="请输入评分" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="版本" prop="version">
        <el-input v-model="form.version" placeholder="请输入版本" />
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

<script setup name="Templates">
import { listTemplates, getTemplates, delTemplates, addTemplates, updateTemplates } from "@/api/templates/templates";

const { proxy } = getCurrentInstance();

const templatesList = ref([]);
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
    name: null,
    slug: null,
    description: null,
    category: null,
    targetFramework: null,
    complexityLevel: null,
    isOfficial: null,
    isPublic: null,
    authorUserId: null,
    downloadCount: null,
    rating: null,
    version: null,
    tags: null,
    createdAt: null,
    updatedAt: null,
  },
  rules: {
    name: [
      { required: true, message: "模板名称不能为空", trigger: "blur" }
    ],
    slug: [
      { required: true, message: "模板标识不能为空", trigger: "blur" }
    ],
    category: [
      { required: true, message: "模板分类 (ui_component, api_layer, project_scaffold, workflow)不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询模板列表 */
function getList() {
  loading.value = true;
  listTemplates(queryParams.value).then(response => {
    templatesList.value = response.rows;
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
    name: null,
    slug: null,
    description: null,
    category: null,
    targetFramework: null,
    complexityLevel: null,
    isOfficial: null,
    isPublic: null,
    authorUserId: null,
    downloadCount: null,
    rating: null,
    version: null,
    tags: null,
    createdAt: null,
    updatedAt: null,
  };
  proxy.resetForm("templatesRef");
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
  title.value = "添加模板";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getTemplates(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改模板";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["templatesRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateTemplates(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addTemplates(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除模板编号为"' + _ids + '"的数据项？').then(function() {
    return delTemplates(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('templates/templates/export', {
    ...queryParams.value
  }, `templates_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>