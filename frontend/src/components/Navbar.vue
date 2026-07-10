<script setup lang="ts">
import { RouterLink } from "vue-router";
import logo from "../assets/images/logo.png";


</script>

<template>
  <header class="navbar">
    <div class="container">

      <div class="logo">
      <img :src="logo" alt="اتوگالری">
    
</div>

<nav class="menu">

    <RouterLink to="/">
        خانه
    </RouterLink>

    <RouterLink to="/cars">
        خودروها
    </RouterLink>

    <RouterLink to="/favorites">
        علاقه‌مندی‌ها
    </RouterLink>

</nav>

<div class="auth">

    <RouterLink class="login" to="/login">
        ورود
    </RouterLink>

    <RouterLink class="register" to="/register">
        ثبت نام
    </RouterLink>

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
    gap:15px;
}

.login,
.register{
    text-decoration:none;
    padding:10px 20px;
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

</style>