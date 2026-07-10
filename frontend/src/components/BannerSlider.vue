<script setup lang="ts">
import { ref } from "vue";

const slides = [

{
title:"خرید خودرو با بهترین قیمت",
subtitle:"جدیدترین خودروهای صفر و کارکرده",
image:"https://placehold.co/1400x450"
},

{
title:"فروش خودروی شما در کمترین زمان",
subtitle:"آگهی خود را رایگان ثبت کنید",
image:"https://placehold.co/1400x450"
},

{
title:"مقایسه قیمت خودرو",
subtitle:"قیمت روز خودروها را مشاهده کنید",
image:"https://placehold.co/1400x450"
}

];

const current = ref(0);

setInterval(()=>{

current.value++;

if(current.value>=slides.length){

current.value=0;

}

},4000);

</script>

<template>

<section
class="slider"
:style="{
backgroundImage:`url(${slides[current].image})`
}"
>

<div class="overlay">

<h1>

{{ slides[current].title }}

</h1>

<p>

{{ slides[current].subtitle }}

</p>

</div>

</section>

</template>

<style scoped>

.slider{

height:420px;

background-size:cover;

background-position:center;

display:flex;

align-items:center;

justify-content:center;

position:relative;

}

.overlay{

background:rgba(0,0,0,.45);

width:100%;

height:100%;

display:flex;

flex-direction:column;

justify-content:center;

align-items:center;

color:white;

text-align:center;

}

h1{

font-size:46px;

margin-bottom:20px;

}

p{

font-size:22px;

}

</style>