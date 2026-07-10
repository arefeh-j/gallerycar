<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();

const id = route.params.id;
</script>

<template>

<div class="container">

    <div class="gallery">

        <img
            src="https://placehold.co/900x500"
            alt=""
        >

    </div>

    <div class="info">

        <h1>BMW 320i</h1>

        <h2>۲,۵۰۰,۰۰۰,۰۰۰ تومان</h2>

        <div class="specs">

            <div class="item">
                <span>برند</span>
                <strong>BMW</strong>
            </div>

            <div class="item">
                <span>سال ساخت</span>
                <strong>۱۴۰۲</strong>
            </div>

            <div class="item">
                <span>کارکرد</span>
                <strong>۳۵ هزار کیلومتر</strong>
            </div>

            <div class="item">
                <span>رنگ</span>
                <strong>سفید</strong>
            </div>

        </div>

        <button class="favorite">
            افزودن به علاقه‌مندی‌ها
        </button>

    </div>

</div>

<div class="description">

    <h2>توضیحات خودرو</h2>

    <p>

این خودرو از نظر فنی سالم بوده و تمام سرویس‌های دوره‌ای آن انجام شده است.
بدون رنگ و تصادف، آماده انتقال سند.

    </p>

</div>

</template>

<style scoped>

.container{

max-width:1200px;

margin:40px auto;

display:grid;

grid-template-columns:2fr 1fr;

gap:30px;

direction:rtl;

}

.gallery img{

width:100%;

border-radius:15px;

}

.info{

background:white;

padding:25px;

border-radius:15px;

box-shadow:0 8px 20px rgba(0,0,0,.08);

}

.info h1{

margin-top:0;

}

.info h2{

color:#2563eb;

}

.specs{

margin-top:25px;

display:grid;

grid-template-columns:repeat(2,1fr);

gap:15px;

}

.item{

background:#f5f5f5;

padding:15px;

border-radius:10px;

}

.item span{

display:block;

color:#666;

margin-bottom:8px;

}

.favorite{

margin-top:25px;

width:100%;

padding:14px;

background:#2563eb;

border:none;

color:white;

border-radius:10px;

cursor:pointer;

}

.description{

max-width:1200px;

margin:auto;

margin-bottom:60px;

background:white;

padding:25px;

border-radius:15px;

direction:rtl;

box-shadow:0 8px 20px rgba(0,0,0,.08);

}

</style>