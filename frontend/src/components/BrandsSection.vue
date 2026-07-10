<script setup lang="ts">

const brands = [

{
    name:"BMW",
    logo:"https://logo.clearbit.com/bmw.com"
},

{
    name:"Mercedes",
    logo:"https://logo.clearbit.com/mercedes-benz.com"
},

{
    name:"Toyota",
    logo:"https://logo.clearbit.com/toyota.com"
},

{
    name:"Hyundai",
    logo:"https://logo.clearbit.com/hyundai.com"
},

{
    name:"Kia",
    logo:"https://logo.clearbit.com/kia.com"
},

{
    name:"Peugeot",
    logo:"https://logo.clearbit.com/peugeot.com"
}

];

</script>

<template>

<section class="brands">

<h2>

برندهای محبوب

</h2>

<div class="grid">

<div
class="brand-card"
v-for="brand in brands"
:key="brand.name"
>

<img
:src="brand.logo"
:alt="brand.name"
/>

<h3>

{{ brand.name }}

</h3>

</div>

</div>

</section>

</template>

<style scoped>

.brands{

max-width:1200px;

margin:70px auto;

padding:0 20px;

direction:rtl;

}

.brands h2{

margin-bottom:25px;

font-size:30px;

}

.grid{

display:grid;

grid-template-columns:repeat(auto-fit,minmax(150px,1fr));

gap:20px;

}

.brand-card{

background:white;

padding:25px;

border-radius:16px;

text-align:center;

box-shadow:0 5px 15px rgba(0,0,0,.08);

transition:.3s;

cursor:pointer;

}

.brand-card:hover{

transform:translateY(-8px);

}

.brand-card img{

width:70px;

height:70px;

object-fit:contain;

margin-bottom:15px;

}

.brand-card h3{

margin:0;

font-size:18px;

}

</style>