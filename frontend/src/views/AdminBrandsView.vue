<template>
  <div class="container">
    <h1>مدیریت برندها</h1>

    <!-- فرم افزودن برند -->
    <div class="add-form">
      <input v-model="newBrand" placeholder="نام برند جدید" />
      <button @click="addBrand" class="btn-add">افزودن</button>
    </div>

    <!-- لیست برندها -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>نام برند</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="brand in brands" :key="brand.id">
          <td>{{ brand.id }}</td>
          <td>
            <input v-if="editingId === brand.id" v-model="editName" />
            <span v-else>{{ brand.name }}</span>
          </td>
          <td>
            <template v-if="editingId === brand.id">
              <button @click="saveEdit(brand.id)" class="btn-save">ذخیره</button>
              <button @click="cancelEdit" class="btn-cancel">انصراف</button>
            </template>
            <template v-else>
              <button @click="startEdit(brand)" class="btn-edit">ویرایش</button>
              <button @click="deleteBrand(brand.id)" class="btn-delete">حذف</button>
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

const brands = ref<any[]>([]);
const newBrand = ref("");
const editingId = ref<number | null>(null);
const editName = ref("");

// ===== بارگذاری برندها =====
async function loadBrands() {
  try {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://127.0.0.1:8000/brands/api/brands", {
      headers: { Authorization: `Bearer ${token}` }
    });
    brands.value = res.data;
  } catch (err: any) {
    console.error(err);
    alert("خطا در دریافت برندها: " + (err.response?.data?.detail || err.message));
  }
}

// ===== افزودن برند =====
async function addBrand() {
  if (!newBrand.value.trim()) {
    alert("لطفاً نام برند را وارد کنید.");
    return;
  }
  try {
    const token = localStorage.getItem("token");
    await axios.post(
      "http://127.0.0.1:8000/brands/api/brands",
      { name: newBrand.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    newBrand.value = "";
    await loadBrands();
    alert("برند با موفقیت اضافه شد.");
  } catch (err: any) {
    console.error(err);
    alert("خطا در افزودن برند: " + (err.response?.data?.detail || err.message));
  }
}

// ===== شروع ویرایش =====
function startEdit(brand: any) {
  editingId.value = brand.id;
  editName.value = brand.name;
}

// ===== ذخیره ویرایش =====
async function saveEdit(id: number) {
  if (!editName.value.trim()) {
    alert("لطفاً نام برند را وارد کنید.");
    return;
  }
  try {
    const token = localStorage.getItem("token");
    await axios.put(
      `http://127.0.0.1:8000/brands/api/brands/${id}`,
      { name: editName.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    editingId.value = null;
    await loadBrands();
    alert("برند با موفقیت ویرایش شد.");
  } catch (err: any) {
    console.error(err);
    alert("خطا در ویرایش برند: " + (err.response?.data?.detail || err.message));
  }
}

// ===== لغو ویرایش =====
function cancelEdit() {
  editingId.value = null;
  editName.value = "";
}

// ===== حذف برند =====
async function deleteBrand(id: number) {
  if (!confirm("آیا از حذف این برند اطمینان دارید؟")) return;
  try {
    const token = localStorage.getItem("token");
    await axios.delete(`http://127.0.0.1:8000/brands/api/brands/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    await loadBrands();
    alert("برند با موفقیت حذف شد.");
  } catch (err: any) {
    console.error(err);
    alert("خطا در حذف برند: " + (err.response?.data?.detail || err.message));
  }
}

onMounted(loadBrands);
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 30px auto;
  direction: rtl;
  font-family: Vazir, sans-serif;
}
h1 {
  text-align: center;
  margin-bottom: 30px;
}
.add-form {
  display: flex;
  gap: 12px;
  margin-bottom: 30px;
}
.add-form input {
  flex: 1;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
}
.btn-add {
  background: #2563eb;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
}
table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
th {
  background: #f8fafc;
  padding: 12px;
  border-bottom: 2px solid #e2e8f0;
}
td {
  padding: 12px;
  border-bottom: 1px solid #f1f5f9;
  text-align: center;
}
td input {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
.btn-edit,
.btn-delete,
.btn-save,
.btn-cancel {
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  margin: 0 4px;
}
.btn-edit {
  background: #f59e0b;
  color: #fff;
}
.btn-delete {
  background: #ef4444;
  color: #fff;
}
.btn-save {
  background: #10b981;
  color: #fff;
}
.btn-cancel {
  background: #6b7280;
  color: #fff;
}
</style>