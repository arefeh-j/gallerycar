<script setup lang="ts">

import { RouterLink, useRouter, useRoute } from "vue-router";
<<<<<<< HEAD
import { ref, watch, computed } from "vue";
=======
import { ref, watch } from "vue";
import { useToast } from "vue-toastification";

>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb
import logo from "../assets/images/logo.png";


const router = useRouter();
const route = useRoute();
const toast = useToast();


const token = ref<string | null>(null);
const fullName = ref<string | null>(null);
const role = ref<string | null>(null);

const menuOpen = ref(false);



function toggleMenu() {

  menuOpen.value = !menuOpen.value;

}



function checkUser() {

  token.value = localStorage.getItem("token");
  fullName.value = localStorage.getItem("full_name");
<<<<<<< HEAD
  role.value = localStorage.getItem("role");
}

const isAdmin = computed(() => role.value === "admin");
const isLoggedIn = computed(() => !!token.value);
=======

}


>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb

watch(
  () => route.fullPath,
  () => {

    checkUser();

    menuOpen.value = false;

  },
<<<<<<< HEAD
  { immediate: true }
=======
  {
    immediate:true,
  }
>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb
);



function logout(){

  localStorage.removeItem("token");
  localStorage.removeItem("full_name");
  localStorage.removeItem("role");
<<<<<<< HEAD
  checkUser();
=======


  checkUser();


  toast.success(
    "با موفقیت خارج شدید.",
    {
      timeout:3000
    }
  );


>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb
  router.push("/login");

}




function goFavorites(){


  if(!token.value){


    toast.error(
      "برای مشاهده علاقه‌مندی‌ها ابتدا وارد حساب کاربری شوید یا ثبت‌نام کنید.",
      {
        timeout:3000
      }
    );


    router.push("/login");


    return;

  }



  router.push("/favorites");


}



</script>



<template>
<<<<<<< HEAD
  <header class="navbar">
    <div class="container">
      <!-- لوگو -->
      <div class="logo">
        <img :src="logo" alt="اتوگالری" />
      </div>

      <!-- منوی اصلی -->
      <nav class="menu">
        <RouterLink to="/" class="menu-link">خانه</RouterLink>
        <RouterLink to="/cars" class="menu-link">خودروها</RouterLink>

        <template v-if="isAdmin">

  <RouterLink to="/admin" class="menu-link admin">
    داشبورد
  </RouterLink>

  <RouterLink to="/admin/cars" class="menu-link admin">
    آگهی‌های من
  </RouterLink>

  <RouterLink to="/cars/add" class="menu-link add">
    ثبت آگهی
  </RouterLink>

  <RouterLink to="/admin/orders" class="menu-link admin">
    سفارش‌های خرید
  </RouterLink>

  <RouterLink to="/admin/brands" class="menu-link admin">
    برندها
  </RouterLink>

</template>

        <!-- لینک علاقه‌مندی‌ها (فقط برای کاربر عادی) -->
        <RouterLink
          v-if="isLoggedIn && !isAdmin"
          to="/favorites"
          class="menu-link"
        >
          علاقه‌مندی‌ها
        </RouterLink>
      </nav>

      <!-- بخش احراز هویت -->
      <div class="auth">
        <template v-if="isLoggedIn">
          <span class="username">👋 {{ fullName }}</span>
          <RouterLink to="/profile" class="btn-profile">پروفایل</RouterLink>
          <button class="btn-logout" @click="logout">خروج</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn-login">ورود</RouterLink>
          <RouterLink to="/register" class="btn-register">ثبت‌نام</RouterLink>
        </template>
      </div>
    </div>
  </header>
=======

<header class="navbar">


<div class="container">



<!-- Logo -->

<div class="logo">

<RouterLink to="/">

<img
:src="logo"
alt="اتوگالری"
/>

</RouterLink>

</div>





<!-- Mobile Button -->

<button
class="menu-toggle"
@click="toggleMenu"
>

☰

</button>






<!-- Menu -->

<nav
class="menu"
:class="{open:menuOpen}"
>



<RouterLink to="/">

🏠 خانه

</RouterLink>




<RouterLink to="/cars">

🚘 خودروها

</RouterLink>




<RouterLink to="/cars">

⭐ خودروهای ویژه

</RouterLink>




<a
href="#"
@click.prevent="goFavorites"
>

❤️ علاقه‌مندی‌ها

</a>



</nav>







<!-- Auth -->

<div class="auth">



<template v-if="token">



<span class="username">

👋 سلام {{ fullName }}

</span>




<RouterLink
class="profile"
to="/profile"
>

👤 پروفایل

</RouterLink>




<button
class="logout"
@click="logout"
>

🚪 خروج

</button>



>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb
</template>






<template v-else>



<RouterLink
class="login"
to="/login"
>

ورود

</RouterLink>



<RouterLink
class="register"
to="/register"
>

ثبت نام

</RouterLink>



</template>




</div>




</div>


</header>


</template>





<style scoped>
<<<<<<< HEAD
/* ---- reset & base ---- */
.navbar {
  background: #ffffff;
  border-bottom: 1px solid #e9ecef;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  direction: rtl;
}

/* ---- لوگو ---- */
.logo img {
  height: 200px;
  width: auto;
  display: block;
}

/* ---- منو ---- */
.menu {
  display: flex;
  align-items: center;
  gap: 28px;
}

.menu-link {
  text-decoration: none;
  color: #334155;
  font-size: 16px;
  font-weight: 500;
  padding: 6px 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.menu-link:hover {
  color: #1e293b;
  border-bottom-color: #2563eb;
}

.menu-link.router-link-active {
  color: #2563eb;
  border-bottom-color: #2563eb;
}

/* لینک‌های ادمین – فقط یک رنگ ملایم متفاوت */
.menu-link.admin {
  color: #1e40af;
}

.menu-link.admin:hover {
  color: #1e3a8a;
  border-bottom-color: #3b82f6;
}

.menu-link.add {
  color: #16a34a;
}

.menu-link.add:hover {
  color: #15803d;
  border-bottom-color: #22c55e;
}

/* ---- بخش احراز هویت ---- */
.auth {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  font-weight: 500;
  color: #1e293b;
  font-size: 15px;
}

/* دکمه‌ها */
.btn-profile,
.btn-logout,
.btn-login,
.btn-register {
  text-decoration: none;
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.btn-profile {
  background: #f1f5f9;
  color: #1e293b;
}

.btn-profile:hover {
  background: #e2e8f0;
}

.btn-logout {
  background: #fef2f2;
  color: #dc2626;
}

.btn-logout:hover {
  background: #fee2e2;
}

.btn-login {
  background: transparent;
  color: #2563eb;
}

.btn-login:hover {
  background: #eff6ff;
}

.btn-register {
  background: #2563eb;
  color: #ffffff;
}

.btn-register:hover {
  background: #1d4ed8;
=======

/* CSS قبلی خودت بدون تغییر باقی بماند */

.navbar{
    background:#ffffff;
    border-bottom:1px solid #e5e7eb;
    position:sticky;
    top:0;
    z-index:1000;
    box-shadow:0 2px 10px rgba(0,0,0,.05);
}

.container{
    max-width:1200px;
    margin:auto;
    padding:16px 24px;
    display:flex;
    flex-direction:row-reverse;
    justify-content:space-between;
    align-items:center;
}

.logo img{
    width:135px;
}

.menu{
    display:flex;
    flex-direction:row-reverse;
    gap:30px;
    align-items:center;
}

.menu a{
    text-decoration:none;
    color:#1f2937;
    font-size:16px;
    font-weight:700;
    cursor:pointer;
}


.menu a:hover{
    color:#2563eb;
}


.auth{
    display:flex;
    align-items:center;
    gap:12px;
}


.username{
    font-weight:bold;
}


.login,
.register,
.profile{

text-decoration:none;
padding:10px 18px;
border-radius:10px;

}



.login{
color:#2563eb;
}


.register{

background:#2563eb;
color:white;

}


.profile{

background:#10b981;
color:white;

}


.logout{

border:none;
background:#ef4444;
color:white;
padding:10px 18px;
border-radius:10px;
cursor:pointer;

}



.menu-toggle{

display:none;

>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb
}



@media(max-width:768px){


.menu-toggle{

display:block;

}


.menu{

display:none;
width:100%;
flex-direction:column;

}


.menu.open{

display:flex;

}


.auth{

flex-wrap:wrap;
justify-content:center;

}


}

</style>