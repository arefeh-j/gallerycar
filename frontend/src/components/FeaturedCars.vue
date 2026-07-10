<script setup lang="ts">

const cars = [

{
id:1,
title:"BMW 320i",
price:"۲,۵۰۰,۰۰۰,۰۰۰ تومان",
year:"۱۴۰۲",
image:"https://placehold.co/600x400"
},

{
id:2,
title:"Toyota Corolla",
price:"۱,۹۰۰,۰۰۰,۰۰۰ تومان",
year:"۱۴۰۱",
image:"https://placehold.co/600x400"
},

{
id:3,
title:"Mercedes C200",
price:"۴,۱۰۰,۰۰۰,۰۰۰ تومان",
year:"۱۴۰۳",
image:"https://placehold.co/600x400"
}

]

</script>

<template>

<section class="featured">

<h2>

خودروهای ویژه

</h2>

<div class="cards">

<div
class="card"
v-for="car in cars"
:key="car.id"
>

<img :src="car.image">

<div class="body">

<span class="badge">

ویژه

</span>

<h3>

{{ car.title }}

</h3>

<p>

سال ساخت:
{{ car.year }}

</p>

<h2>

{{ car.price }}

</h2>

<button>

مشاهده آگهی

</button>

</div>

</div>

</div>

</section>

</template>

<style scoped>

.featured{

max-width:1200px;

margin:70px auto;

padding:0 20px;

direction:rtl;

}

.featured h2{

margin-bottom:30px;

font-size:30px;

}

.cards{

display:grid;

grid-template-columns:repeat(3,1fr);

gap:25px;

}

.card{

background:white;

border-radius:18px;

overflow:hidden;

box-shadow:0 10px 25px rgba(0,0,0,.08);

transition:.3s;

}

.card:hover{

transform:translateY(-8px);

}

img{

width:100%;

height:230px;

object-fit:cover;

}

.body{

padding:20px;

}

.badge{

display:inline-block;

background:#f59e0b;

color:white;

padding:5px 12px;

border-radius:20px;

font-size:13px;

margin-bottom:15px;

}

h3{

margin:10px 0;

}

p{

color:#666;

}

h2{

color:#2563eb;

margin-top:15px;

}

button{

width:100%;

margin-top:20px;

padding:12px;

border:none;

border-radius:10px;

background:#2563eb;

color:white;

cursor:pointer;

font-size:15px;

}

button:hover{

background:#1d4ed8;

}

@media(max-width:900px){

.cards{

grid-template-columns:1fr;

}

}

</style>