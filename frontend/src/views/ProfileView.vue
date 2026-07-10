<script setup lang="ts">

import { ref, onMounted } from "vue";
import { getProfile } from "../services/profileService";

const user = ref<any>(null);
const loading = ref(true);

onMounted(async()=>{

    try{

        user.value = await getProfile();

    }catch(error){

        console.log(error);

    }finally{

        loading.value=false;

    }

});

</script>

<template>

<div class="page">

<h1>پروفایل کاربر</h1>

<div v-if="loading">

در حال بارگذاری...

</div>

<div v-else-if="user">

<p><strong>نام:</strong> {{ user.full_name }}</p>

<p><strong>ایمیل:</strong> {{ user.email }}</p>

<p><strong>نقش:</strong> {{ user.role }}</p>

</div>

</div>

</template>

<style scoped>

.page{

max-width:800px;
margin:auto;
padding:40px;

}

</style>