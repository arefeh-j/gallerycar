<script setup lang="ts">
import { RouterLink, useRouter, useRoute } from "vue-router";
import { ref, watch } from "vue";
import logo from "../assets/images/logo.png";

const router = useRouter();
const route = useRoute();

const token = ref<string | null>(null);
const fullName = ref<string | null>(null);

function checkUser() {
  token.value = localStorage.getItem("token");
  fullName.value = localStorage.getItem("full_name");
}

watch(
  () => route.fullPath,
  () => {
    checkUser();
  },
  {
    immediate: true
  }
);

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("full_name");
  localStorage.removeItem("role");

  checkUser();

  router.push("/login");
}
</script>

<template>
  <header class="navbar">
    <div class="container">

      <div class="logo">
        <img :src="logo" alt="اتوگالری">
      </div>

      <nav class="menu">
        <RouterLink to="/">خانه</RouterLink>
        <RouterLink to="/cars">خودروها</RouterLink>
        <RouterLink to="/favorites">علاقه‌مندی‌ها</RouterLink>
      </nav>

      <div class="auth">

        <template v-if="token">

          <span class="username">
            👋 سلام {{ fullName }}
          </span>

          <RouterLink
            class="profile"
            to="/profile"
          >
            ویرایش اطلاعات
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
    background:#fff;
    border-bottom:1px solid #e5e5e5;
    position:sticky;
    top:0;
    z-index:1000;
}

.container{
    max-width:1200px;
    margin:auto;
    padding:18px 25px;
    display:flex;
    flex-direction:row-reverse;
    justify-content:space-between;
    align-items:center;
}

.logo{
    display:flex;
    align-items:center;
}

.logo img{
    width:140px;
    height:auto;
}

.menu{
    display:flex;
    flex-direction:row-reverse;
    gap:35px;
}

.menu a{
    text-decoration:none;
    color:#222;
    font-size:17px;
    font-weight:700;
}

.menu a:hover{
    color:#2563eb;
}

.auth{
    display:flex;
    flex-direction:row-reverse;
    gap:12px;
    align-items:center;
}

.login,
.register,
.profile{
    text-decoration:none;
    padding:10px 18px;
    border-radius:10px;
    font-weight:bold;
}

.login{
    color:#2563eb;
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

.username{
    font-weight:bold;
    color:#222;
}

.logout{
    border:none;
    background:#ef4444;
    color:white;
    padding:10px 18px;
    border-radius:10px;
    cursor:pointer;
    font-weight:bold;
}

.logout:hover{
    background:#dc2626;
}
</style>