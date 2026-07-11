<script setup lang="ts">

import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";

import { RouterView } from "vue-router";

</script>


<template>

  <Navbar />

  <main>

    <RouterView />

  </main>

  <Footer />

</template>


<style>

html,
body{
    margin:0;
    padding:0;
    direction:rtl;
    text-align:right;
    font-family:Tahoma, Arial, sans-serif;
    background:#f5f7fb;
    color:#222;
}


#app{
    min-height:100vh;
}


main{
    min-height:80vh;
}


*{
    box-sizing:border-box;
}


a{
    text-decoration:none;
}

</style>