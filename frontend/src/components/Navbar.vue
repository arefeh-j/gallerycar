<script setup lang="ts">

import { RouterLink, useRouter, useRoute } from "vue-router";
import { ref, watch, computed } from "vue";
import { useToast } from "vue-toastification";
import logo from "../assets/images/logo.png";

const router = useRouter();
const route = useRoute();
const toast = useToast();

const token = ref<string | null>(null);
const fullName = ref<string | null>(null);
const role = ref<string | null>(null);

const menuOpen = ref(false);

const isLoggedIn = computed(() => !!token.value);
const isAdmin = computed(() => role.value === "admin");

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

function checkUser() {
  token.value = localStorage.getItem("token");
  fullName.value = localStorage.getItem("full_name");
  role.value = localStorage.getItem("role");
}

watch(
  () => route.fullPath,
  () => {
    checkUser();
    menuOpen.value = false;
  },
  {
    immediate: true,
  }
);

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("full_name");
  localStorage.removeItem("role");

  checkUser();

  toast.success("با موفقیت خارج شدید.", {
    timeout: 3000,
  });

  router.push("/login");
}

function goFavorites() {
  if (!token.value) {
    toast.error(
      "برای مشاهده علاقه‌مندی‌ها ابتدا وارد حساب کاربری شوید یا ثبت‌نام کنید.",
      {
        timeout: 3000,
      }
    );

    router.push("/login");
    return;
  }

  router.push("/favorites");
}

</script>

<template>

<header class="navbar">

<div class="container">

<!-- لوگو -->

<div class="logo">

<RouterLink to="/">

<img
:src="logo"
alt="اتوگالری"
/>

</RouterLink>

</div>

<!-- دکمه منوی موبایل -->

<button
class="menu-toggle"
@click="toggleMenu"
>

☰

</button>

<!-- منو -->

<nav
class="menu"
:class="{ open: menuOpen }"
>

<RouterLink to="/">
 خانه
</RouterLink>

<RouterLink to="/cars">
 خودروها
</RouterLink>

<a
href="#"
@click.prevent="goFavorites"
>
 علاقه‌مندی‌ها
</a>

<!-- پنل ادمین -->

<template v-if="isAdmin">

<RouterLink
to="/admin"
class="admin-link"
>
 داشبورد
</RouterLink>

<RouterLink
to="/admin/cars"
class="admin-link"
>
 آگهی‌های من
</RouterLink>

<RouterLink
to="/cars/add"
class="admin-link"
>
 ثبت آگهی
</RouterLink>

<RouterLink
to="/admin/orders"
class="admin-link"
>
 سفارش‌های خرید
</RouterLink>

<RouterLink
to="/admin/brands"
class="admin-link"
>
 برندها
</RouterLink>

</template>

</nav>

<!-- احراز هویت -->

<div class="auth">

<template v-if="isLoggedIn">

<span class="username">

 سلام {{ fullName }}

</span>

<RouterLink
class="profile"
to="/profile"
>

 پروفایل

</RouterLink>

<button
class="logout"
@click="logout"
>

 خروج

</button>

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
    display:block;
}

.menu{
    display:flex;
    flex-direction:row-reverse;
    align-items:center;
    gap:28px;
}

.menu a,
.menu :deep(a){
    text-decoration:none;
    color:#1f2937;
    font-size:16px;
    font-weight:700;
    transition:.25s;
}

.menu a:hover,
.menu :deep(a:hover){
    color:#2563eb;
}

.menu :deep(.router-link-active){
    color:#2563eb;
}

/* لینک‌های ادمین */

.admin-link{
    color:#0f766e !important;
    font-weight:700;
}

.admin-link:hover{
    color:#0d9488 !important;
}

/* احراز هویت */

.auth{
    display:flex;
    align-items:center;
    gap:12px;
}

.username{
    font-weight:bold;
    color:#374151;
    white-space:nowrap;
}

.login,
.register,
.profile{
    text-decoration:none;
    padding:10px 18px;
    border-radius:10px;
    font-size:14px;
    font-weight:600;
    transition:.25s;
}

.login{
    color:#2563eb;
}

.login:hover{
    background:#eff6ff;
}

.register{
    background:#2563eb;
    color:white;
}

.register:hover{
    background:#1d4ed8;
}

.profile{
    background:#10b981;
    color:white;
}

.profile:hover{
    background:#059669;
}

.logout{
    border:none;
    background:#ef4444;
    color:white;
    padding:10px 18px;
    border-radius:10px;
    cursor:pointer;
    font-size:14px;
    font-weight:600;
    transition:.25s;
}

.logout:hover{
    background:#dc2626;
}

.menu-toggle{
    display:none;
    border:none;
    background:none;
    font-size:28px;
    cursor:pointer;
}

/* موبایل */

@media (max-width:768px){

.container{
    flex-wrap:wrap;
}

.menu-toggle{
    display:block;
}

.menu{
    display:none;
    width:100%;
    margin-top:18px;
    flex-direction:column;
    gap:18px;
    padding:15px 0;
}

.menu.open{
    display:flex;
}

.auth{
    width:100%;
    margin-top:18px;
    justify-content:center;
    flex-wrap:wrap;
}

.username{
    width:100%;
    text-align:center;
}

}
</style>