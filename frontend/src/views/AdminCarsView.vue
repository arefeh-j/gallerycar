<template>
  <div class="admin-cars-container">
    <div class="header">
      <h1>آگهی‌های من</h1>
      <RouterLink to="/cars/add" class="btn-add">
        + ثبت آگهی جدید
      </RouterLink>
    </div>

    <div v-if="loading" class="loading">در حال بارگذاری...</div>

    <table v-else class="cars-table">
      <thead>
        <tr>
          <th>عکس</th>
          <th>برند</th>
          <th>مدل</th>
          <th>قیمت (تومان)</th>
          <th>وضعیت</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="car in cars" :key="car.id">
          <td>
            <img :src="car.image || '/default-car.jpg'" alt="عکس خودرو" class="car-thumb" />
          </td>
          <td>{{ car.brand }}</td>
          <td>{{ car.model }}</td>
          <td>{{ car.price.toLocaleString() }}</td>
          <td>
            <span class="status-badge" :class="car.status === 'approved' ? 'status-approved' : 'status-pending'">
              {{ car.status === 'approved' ? 'منتشر شده' : 'در انتظار' }}
            </span>
          </td>
          <td>


  <RouterLink
    :to="`/cars/${car.id}`"
    class="btn-view"
  >
    👁 مشاهده
  </RouterLink>

  <RouterLink
    :to="`/cars/edit/${car.id}`"
    class="btn-edit"
  >
    ✏️ ویرایش
  </RouterLink>

  <button
    @click="deleteCar(car.id)"
    class="btn-delete"
  >
    🗑 حذف
  </button>
</td>



        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const cars = ref<any[]>([]);
const loading = ref(true);

async function loadMyCars() {
  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://127.0.0.1:8000/cars/api/my", {
      headers: { Authorization: `Bearer ${token}` }
    });
    cars.value = res.data;
  } catch (err: any) {
    console.error(err);
    alert("خطا در دریافت آگهی‌ها: " + (err.response?.data?.detail || err.message));
  } finally {
    loading.value = false;
  }
}

async function deleteCar(id: number) {
  if (!confirm("آیا از حذف این آگهی اطمینان دارید؟")) return;
  try {
    const token = localStorage.getItem("token");
    await axios.delete(`http://127.0.0.1:8000/cars/api/admin/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    await loadMyCars();
    alert("آگهی با موفقیت حذف شد.");
  } catch (err: any) {
    console.error(err);
    alert("خطا در حذف آگهی: " + (err.response?.data?.detail || err.message));
  }
}

onMounted(loadMyCars);
</script>

<style scoped>
.admin-cars-container {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
  direction: rtl;
  font-family: Vazir, sans-serif;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}
.header h1 {
  margin: 0;
  color: #1e293b;
}
.btn-add {
  background: #2563eb;
  color: #fff;
  padding: 10px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}
.btn-add:hover {
  background: #1d4ed8;
}
.loading {
  text-align: center;
  padding: 40px;
  color: #64748b;
}
.cars-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}
.cars-table th {
  background: #f8fafc;
  padding: 14px;
  text-align: center;
  border-bottom: 2px solid #e2e8f0;
  font-weight: 700;
  color: #334155;
}
.cars-table td {
  padding: 12px 14px;
  text-align: center;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}
.car-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}
.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}
.status-approved {
  background: #dcfce7;
  color: #16a34a;
}
.status-pending {
  background: #fef3c7;
  color: #d97706;
}
.btn-edit, .btn-delete {
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  margin: 0 4px;
  transition: background 0.2s;
}
.btn-edit {
  background: #f59e0b;
  color: #fff;
}
.btn-edit:hover {
  background: #d97706;
}
.btn-delete {
  background: #ef4444;
  color: #fff;
}
.btn-delete:hover {
  background: #dc2626;
}
.empty-state {
  padding: 40px;
  color: #64748b;
  font-size: 16px;
}
.empty-state a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
}
.empty-state a:hover {
  text-decoration: underline;
}


.btn-view{
  background:#2563eb;
  color:white;
  padding:6px 14px;
  border-radius:6px;
  text-decoration:none;
  margin:0 4px;
  display:inline-block;
}

.btn-view:hover{
  background:#1d4ed8;
}
</style>