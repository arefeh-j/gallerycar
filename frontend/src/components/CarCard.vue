<script setup lang="ts">
import { RouterLink } from "vue-router";
import axios from "axios";

const props = defineProps({
    id: Number,
    title: String,
    year: Number,
    mileage: String,
    price: String,
    image: String
});


async function addFavorite(){

    try{

        const token = localStorage.getItem("token");

        await axios.get(
            `http://127.0.0.1:8000/favorites/add/${props.id}`,
            {
                headers:{
                    Authorization:`Bearer ${token}`
                }
            }
        );


        alert("به علاقه‌مندی‌ها اضافه شد ❤️");


    }catch(err){

        console.error(err);
        alert("خطا در افزودن علاقه‌مندی");

    }

}

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


        <button
            class="favorite"
            @click="addFavorite"
        >
            ❤️ افزودن به علاقه‌مندی
        </button>


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
}


img{
    width:100%;
    height:220px;
    object-fit:cover;
}


.content{
    padding:18px;
}


.favorite{

    width:100%;
    padding:12px;
    margin-bottom:12px;

    border:none;
    border-radius:10px;

    background:#ef4444;
    color:white;

    font-weight:bold;
    cursor:pointer;

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

}

</style>