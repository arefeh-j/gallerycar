<template>
  <div class="container">
    <h1>مدیریت خودروها</h1>

    <div v-if="loading" class="loading">در حال بارگذاری...</div>

    <table v-else>
      <thead>
        <tr>
          <th>ID</th>
          <th>برند</th>
          <th>مدل</th>
          <th>قیمت (تومان)</th>
          <th>وضعیت</th>
          <th>عملیات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="car in cars" :key="car.id">
          <td>{{ car.id }}</td>
          <td>{{ car.brand }}</td>
          <td>{{ car.model }}</td>
          <td>{{ car.price.toLocaleString() }}</td>
          <td>
            <span :class="statusClass(car.status)">
              {{ statusText(car.status) }}
            </span>
          </td>
          <td>
            <button 
              v-if="car.status === 'pending'" 
              @click="approveCar(car.id)"
              class="btn approve"
            >
              تأیید
            </button>
            <button 
              v-if="car.status === 'pending' || car.status === 'approved'" 
              @click="rejectCar(car.id)"
              class="btn reject"
            >
              رد
            </button>
            <button 
              @click="deleteCar(car.id)"
              class="btn delete"
            >
              حذف
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

const cars = ref<any[]>([]);
const loading = ref(true);

// توابع کمکی برای نمایش وضعیت
const statusText = (status: string) => {
  const map: Record<string, string> = {
    pending: "در انتظار",
    approved: "تأیید شده",
    rejected: "رد شده"
  };
  return map[status] || status;
};

const statusClass = (status: string) => {
  return {
    "status-pending": status === "pending",
    "status-approved": status === "approved",
    "status-rejected": status === "rejected"
  };
};

// بارگذاری خودروها با هدر Authorization
async function loadCars() {
  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    const response = await axios.get(
      "http://127.0.0.1:8000/cars/api/admin",
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );
    cars.value = response.data;
  } catch (error) {
    console.error(error);
    alert("خطا در دریافت لیست خودروها");
  } finally {
    loading.value = false;
  }
}

// تأیید خودرو
async function approveCar(id: number) {
  try {
    const token = localStorage.getItem("token");
    await axios.post(
      `http://127.0.0.1:8000/cars/api/admin/${id}/approve`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    await loadCars();
    alert("خودرو تأیید شد.");
  } catch (error) {
    console.error(error);
    alert("خطا در تأیید خودرو");
  }
}

// رد خودرو
async function rejectCar(id: number) {
  try {
    const token = localStorage.getItem("token");
    await axios.post(
      `http://127.0.0.1:8000/cars/api/admin/${id}/reject`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    await loadCars();
    alert("خودرو رد شد.");
  } catch (error) {
    console.error(error);
    alert("خطا در رد خودرو");
  }
}

// حذف خودرو
async function deleteCar(id: number) {
  if (!confirm("آیا از حذف این خودرو اطمینان دارید؟")) return;
  try {
    const token = localStorage.getItem("token");
    await axios.delete(
      `http://127.0.0.1:8000/cars/api/admin/${id}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    await loadCars();
    alert("خودرو حذف شد.");
  } catch (error) {
    console.error(error);
    alert("خطا در حذف خودرو");
  }
}

onMounted(loadCars);
</script>

<style scoped>
.container {
  width: 95%;
  margin: 30px auto;
  font-family: Vazir, sans-serif;
  direction: rtl;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #555;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

th {
  background: #f8f9fa;
  font-weight: 700;
  padding: 14px;
  border-bottom: 2px solid #e9ecef;
}

td {
  padding: 12px 14px;
  border-bottom: 1px solid #f1f3f5;
  text-align: center;
}

.btn {
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  margin: 0 4px;
  transition: all 0.2s;
  color: #fff;
}

.btn.approve {
  background: #28a745;
}
.btn.approve:hover {
  background: #218838;
}

.btn.reject {
  background: #ffc107;
  color: #212529;
}
.btn.reject:hover {
  background: #e0a800;
}

.btn.delete {
  background: #dc3545;
}
.btn.delete:hover {
  background: #c82333;
}

.status-pending {
  color: #ff9f00;
  font-weight: 600;
}
.status-approved {
  color: #28a745;
  font-weight: 600;
}
.status-rejected {
  color: #dc3545;
  font-weight: 600;
}
</style>