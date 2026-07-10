<script setup lang="ts">

import { ref,onMounted } from "vue";
import { getFavorites, deleteFavorite } from "../services/favoriteService";


const favorites = ref<any[]>([]);

const loading = ref(true);



async function loadFavorites(){

    try{

        const data = await getFavorites();

        favorites.value = data;

    }
    catch(error){

        console.log(error);

    }
    finally{

        loading.value=false;

    }

}



async function removeFavorite(id:number){

    await deleteFavorite(id);

    loadFavorites();

}



onMounted(loadFavorites);


</script>



<template>

<div class="page">

<h1>
علاقه‌مندی‌ها
</h1>


<div v-if="loading">

در حال بارگذاری...

</div>



<div v-else-if="favorites.length===0">

هنوز خودرویی اضافه نکرده‌اید.

</div>



<div v-else class="grid">


<div
class="card"
v-for="item in favorites"
:key="item.id"
>


<h2>
    {{ item.car.model }}
</h2>

<p>
    سال: {{ item.car.year }}
</p>

<p>
    قیمت: {{ item.car.price }} $
</p>


<p>
سال:
{{item.car.year}}
</p>


<p>
قیمت:
{{item.car.price}}
</p>



<button
@click="removeFavorite(item.id)"
>

حذف از علاقه‌مندی‌ها

</button>


</div>


</div>


</div>

</template>



<style scoped>


.page{

max-width:1200px;
margin:auto;
padding:40px;
direction:rtl;

}


.grid{

display:grid;
grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
gap:20px;

}



.card{

background:white;
padding:20px;
border-radius:15px;
box-shadow:0 5px 20px #ddd;

}


button{

background:red;
color:white;
border:none;
padding:10px;
border-radius:8px;
cursor:pointer;

}


</style>