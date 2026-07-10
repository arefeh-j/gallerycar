<template>

<section class="stats">

<div class="box">

<h2>۲۵۰۰+</h2>

<p>خودروی فعال</p>

</div>

<div class="box">

<h2>۸۵+</h2>

<p>برند خودرو</p>

</div>

<div class="box">

<h2>۴۵۰۰+</h2>

<p>کاربر</p>

</div>

<div class="box">

<h2>۱۲۰۰+</h2>

<p>علاقه‌مندی</p>

</div>

</section>

</template>

<style scoped>

.stats{

max-width:1200px;

margin:80px auto;

display:grid;

grid-template-columns:repeat(4,1fr);

gap:25px;

padding:0 20px;

direction:rtl;

}

.box{

background:white;

padding:35px;

border-radius:18px;

text-align:center;

box-shadow:0 10px 25px rgba(0,0,0,.08);

transition:.3s;

}

.box:hover{

transform:translateY(-8px);

}

.box h2{

margin:0;

font-size:38px;

color:#2563eb;

}

.box p{

margin-top:15px;

font-size:18px;

color:#666;

}

@media(max-width:900px){

.stats{

grid-template-columns:repeat(2,1fr);

}

}

</style>