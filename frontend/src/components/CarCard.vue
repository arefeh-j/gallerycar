<script setup lang="ts">
import { RouterLink } from "vue-router";

defineProps({
    id: Number,
    title: String,
    year: Number,
    mileage: String,
    price: String,
    image: String
});
</script>

<template>

<div class="card">

    <img
        :src="image"
        :alt="title"
        loading="lazy"
    />

    <div class="content">

        <h3>{{ title }}</h3>

        <p>سال ساخت: {{ year }}</p>

        <p>{{ mileage }}</p>

        <h2>{{ price }}</h2>

        <RouterLink
            class="btn"
            :to="`/cars/${id}`"
        >
            مشاهده جزئیات
        </RouterLink>

    </div>

</div>

</template>

<style scoped>

.card{
    background:white;
    border-radius:16px;
    overflow:hidden;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    transition:.3s;
}

.card:hover{
    transform:translateY(-8px);
    box-shadow:0 18px 35px rgba(0,0,0,.15);
}

img{
    width:100%;
    height:220px;
    object-fit:cover;
    display:block;
}

.content{
    padding:18px;
}

h3{
    margin:0 0 10px;
    font-size:22px;
    color:#222;
}

p{
    color:#666;
    margin:8px 0;
}

h2{
    color:#2563eb;
    margin-top:15px;
    margin-bottom:20px;
    font-size:26px;
}

.btn{
    display:block;
    width:100%;
    text-align:center;
    padding:13px;
    background:#2563eb;
    color:#fff;
    text-decoration:none;
    border-radius:10px;
    font-size:15px;
    font-weight:bold;
    transition:.25s;
}

.btn:hover{
    background:#1d4ed8;
}

</style>