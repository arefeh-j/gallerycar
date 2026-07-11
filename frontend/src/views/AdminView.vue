<template>
  <div class="dashboard">

    <h1>داشبورد مدیریت</h1>

    <div v-if="loading" class="loading">
      در حال دریافت اطلاعات...
    </div>

    <div v-else class="cards">

      <div class="card blue">
        <h2>{{ stats.cars }}</h2>
        <p>کل خودروها</p>
      </div>

      <div class="card green">
        <h2>{{ stats.orders }}</h2>
        <p>سفارش‌ها</p>
      </div>

      <div class="card orange">
        <h2>{{ stats.users }}</h2>
        <p>کاربران</p>
      </div>

      <div class="card purple">
        <h2>{{ stats.brands }}</h2>
        <p>برندها</p>
      </div>

    </div>

    <div class="actions">

      <RouterLink
        to="/admin/cars"
        class="btn"
      >
        مدیریت آگهی‌ها
      </RouterLink>

      <RouterLink
        to="/admin/orders"
        class="btn"
      >
        سفارش‌های خرید
      </RouterLink>

      <RouterLink
        to="/admin/brands"
        class="btn"
      >
        مدیریت برندها
      </RouterLink>

      <RouterLink
        to="/cars/add"
        class="btn primary"
      >
        ثبت آگهی جدید
      </RouterLink>

    </div>

  </div>
</template>

<script setup lang="ts">

import {ref,onMounted} from "vue";
import axios from "axios";

const loading = ref(true);

const stats = ref({
    cars:0,
    users:0,
    brands:0,
    orders:0
});

async function loadDashboard(){

    try{

        const token = localStorage.getItem("token");

        const res = await axios.get(
            "http://127.0.0.1:8000/admin/api/dashboard",
            {
                headers:{
                    Authorization:`Bearer ${token}`
                }
            }
        );

        stats.value = res.data;

    }catch(err){

        console.log(err);

        alert("خطا در دریافت اطلاعات داشبورد");

    }finally{

        loading.value=false;

    }

}

onMounted(loadDashboard);

</script>

<style scoped>

.dashboard{

max-width:1200px;
margin:auto;
padding:40px;
direction:rtl;

}

h1{

text-align:center;
margin-bottom:35px;

}

.loading{

text-align:center;
padding:50px;

}

.cards{

display:grid;
grid-template-columns:repeat(4,1fr);
gap:25px;
margin-bottom:40px;

}

.card{

padding:30px;
border-radius:18px;
color:white;
text-align:center;
box-shadow:0 10px 25px rgba(0,0,0,.08);

}

.card h2{

font-size:42px;
margin-bottom:10px;

}

.card p{

font-size:18px;

}

.blue{

background:#2563eb;

}

.green{

background:#10b981;

}

.orange{

background:#f59e0b;

}

.purple{

background:#8b5cf6;

}

.actions{

display:grid;
grid-template-columns:repeat(2,1fr);
gap:20px;

}

.btn{

background:white;
padding:18px;
border-radius:14px;
text-decoration:none;
text-align:center;
font-size:17px;
color:#333;
box-shadow:0 5px 15px rgba(0,0,0,.08);

}

.primary{

background:#2563eb;
color:white;

}

@media(max-width:900px){

.cards{

grid-template-columns:repeat(2,1fr);

}

.actions{

grid-template-columns:1fr;

}

}

</style>