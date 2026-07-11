<script setup lang="ts">
import { RouterLink, useRouter, useRoute } from "vue-router";
import { ref, watch, computed } from "vue";
import logo from "../assets/images/logo.png";

const router = useRouter();
const route = useRoute();

const token = ref<string | null>(null);
const fullName = ref<string | null>(null);
const role = ref<string | null>(null);

function checkUser() {
  token.value = localStorage.getItem("token");
  fullName.value = localStorage.getItem("full_name");
  role.value = localStorage.getItem("role");
}

const isAdmin = computed(() => role.value === "admin");
const isLoggedIn = computed(() => !!token.value);

watch(
  () => route.fullPath,
  () => {
    checkUser();
  },
  { immediate: true }
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
</template>

<style scoped>
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
}
</style>