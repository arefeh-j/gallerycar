<script setup lang="ts">

import { useToast } from "vue-toastification";


const toast = useToast();



function testAddCar(){

  toast.success(
    "خودرو با موفقیت ثبت شد.",
    {
      timeout:3000
    }
  );

}


</script>



<template>

<div class="page">


<h1>
ثبت خودرو
</h1>


<button
@click="testAddCar"
>

تست ثبت خودرو

</button>


</div>

</template>



<style scoped>

.page{

padding:40px;
direction:rtl;

}


button{

background:#2563eb;

color:white;

border:none;

padding:12px 25px;

border-radius:8px;

cursor:pointer;

font-size:16px;

}

</style>