<script setup lang="ts">

import { RouterLink, useRouter, useRoute } from "vue-router";
import { ref, watch } from "vue";
import { useToast } from "vue-toastification";

import logo from "../assets/images/logo.png";


const router = useRouter();
const route = useRoute();
const toast = useToast();


const token = ref<string | null>(null);
const fullName = ref<string | null>(null);

const menuOpen = ref(false);



function toggleMenu() {

  menuOpen.value = !menuOpen.value;

}



function checkUser() {

  token.value = localStorage.getItem("token");
  fullName.value = localStorage.getItem("full_name");

}



watch(
  () => route.fullPath,
  () => {

    checkUser();

    menuOpen.value = false;

  },
  {
    immediate:true,
  }
);



function logout(){

  localStorage.removeItem("token");
  localStorage.removeItem("full_name");
  localStorage.removeItem("role");


  checkUser();


  toast.success(
    "با موفقیت خارج شدید.",
    {
      timeout:3000
    }
  );


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