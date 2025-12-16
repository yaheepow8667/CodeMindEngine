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
      <el-form-item label="订阅计划" prop="plan">
        <el-input
          v-model="queryParams.plan"
          placeholder="请输入订阅计划"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="订阅状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择订阅状态" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="当前订阅周期开始时间" prop="currentPeriodStart">
        <el-date-picker
          v-model="queryParams.currentPeriodStart"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择当前订阅周期开始时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="当前订阅周期结束时间" prop="currentPeriodEnd">
        <el-date-picker
          v-model="queryParams.currentPeriodEnd"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择当前订阅周期结束时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="是否在周期结束时取消" prop="cancelAtPeriodEnd">
        <el-input
          v-model="queryParams.cancelAtPeriodEnd"
          placeholder="请输入是否在周期结束时取消"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="取消时间" prop="canceledAt">
        <el-date-picker
          v-model="queryParams.canceledAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择取消时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="Stripe客户ID" prop="stripeCustomerId">
        <el-input
          v-model="queryParams.stripeCustomerId"
          placeholder="请输入Stripe客户ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="Stripe订阅ID" prop="stripeSubscriptionId">
        <el-input
          v-model="queryParams.stripeSubscriptionId"
          placeholder="请输入Stripe订阅ID"
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
          v-hasPermi="['subscriptions:subscriptions:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['subscriptions:subscriptions:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['subscriptions:subscriptions:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['subscriptions:subscriptions:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="subscriptionsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="订阅与支付ID" align="center" prop="id" />
      <el-table-column label="团队ID" align="center" prop="teamId" />
      <el-table-column label="订阅计划" align="center" prop="plan" />
      <el-table-column label="订阅状态" align="center" prop="status" />
      <el-table-column label="当前订阅周期开始时间" align="center" prop="currentPeriodStart" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.currentPeriodStart, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="当前订阅周期结束时间" align="center" prop="currentPeriodEnd" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.currentPeriodEnd, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="是否在周期结束时取消" align="center" prop="cancelAtPeriodEnd" />
      <el-table-column label="取消时间" align="center" prop="canceledAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.canceledAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Stripe客户ID" align="center" prop="stripeCustomerId" />
      <el-table-column label="Stripe订阅ID" align="center" prop="stripeSubscriptionId" />
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
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['subscriptions:subscriptions:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['subscriptions:subscriptions:remove']">删除</el-button>
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

    <!-- 添加或修改订阅与支付对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="subscriptionsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="团队ID" prop="teamId">
        <el-input v-model="form.teamId" placeholder="请输入团队ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="订阅计划" prop="plan">
        <el-input v-model="form.plan" placeholder="请输入订阅计划" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="订阅状态" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio label="请选择字典生成" value="" />
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="当前订阅周期开始时间" prop="currentPeriodStart">
        <el-date-picker clearable
          v-model="form.currentPeriodStart"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择当前订阅周期开始时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="当前订阅周期结束时间" prop="currentPeriodEnd">
        <el-date-picker clearable
          v-model="form.currentPeriodEnd"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择当前订阅周期结束时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否在周期结束时取消" prop="cancelAtPeriodEnd">
        <el-input v-model="form.cancelAtPeriodEnd" placeholder="请输入是否在周期结束时取消" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="取消时间" prop="canceledAt">
        <el-date-picker clearable
          v-model="form.canceledAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择取消时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="Stripe客户ID" prop="stripeCustomerId">
        <el-input v-model="form.stripeCustomerId" placeholder="请输入Stripe客户ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="Stripe订阅ID" prop="stripeSubscriptionId">
        <el-input v-model="form.stripeSubscriptionId" placeholder="请输入Stripe订阅ID" />
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

<script setup name="Subscriptions">
import { listSubscriptions, getSubscriptions, delSubscriptions, addSubscriptions, updateSubscriptions } from "@/api/subscriptions/subscriptions";

const { proxy } = getCurrentInstance();

const subscriptionsList = ref([]);
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
    plan: null,
    status: null,
    currentPeriodStart: null,
    currentPeriodEnd: null,
    cancelAtPeriodEnd: null,
    canceledAt: null,
    stripeCustomerId: null,
    stripeSubscriptionId: null,
    createdAt: null,
    updatedAt: null,
  },
  rules: {
    teamId: [
      { required: true, message: "团队ID不能为空", trigger: "blur" }
    ],
    plan: [
      { required: true, message: "订阅计划不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询订阅与支付列表 */
function getList() {
  loading.value = true;
  listSubscriptions(queryParams.value).then(response => {
    subscriptionsList.value = response.rows;
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
    plan: null,
    status: null,
    currentPeriodStart: null,
    currentPeriodEnd: null,
    cancelAtPeriodEnd: null,
    canceledAt: null,
    stripeCustomerId: null,
    stripeSubscriptionId: null,
    createdAt: null,
    updatedAt: null,
  };
  proxy.resetForm("subscriptionsRef");
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
  title.value = "添加订阅与支付";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getSubscriptions(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改订阅与支付";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["subscriptionsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateSubscriptions(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addSubscriptions(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除订阅与支付编号为"' + _ids + '"的数据项？').then(function() {
    return delSubscriptions(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('subscriptions/subscriptions/export', {
    ...queryParams.value
  }, `subscriptions_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>