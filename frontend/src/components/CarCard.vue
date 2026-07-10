```vue
<script setup lang="ts">

import { RouterLink } from "vue-router";
import axios from "axios";


const props = defineProps({

    id:{
        type:Number,
        required:true
    },

    title:{
        type:String,
        required:true
    },

    year:{
        type:Number,
        required:false
    },

    mileage:{
        type:String,
        required:false
    },

    price:{
        type:[String, Number],
        required:true
    },

    image:{
        type:String,
        required:true
    }

});



function formatPrice(value:any){

    return Number(value).toLocaleString();

}



async function addFavorite(){


    const token = localStorage.getItem("token");


    if(!token){

        alert("لطفاً ابتدا وارد حساب کاربری شوید.");

        return;

    }



    try{


        await axios.get(

            `http://127.0.0.1:8000/favorites/add/${props.id}`,

            {

                headers:{

                    Authorization:`Bearer ${token}`

                }

            }

        );



        alert("❤️ خودرو به علاقه‌مندی‌ها اضافه شد");


    }


    catch(err:any){


        console.error(err);


        if(err.response?.status === 401){

            alert("نشست شما منقضی شده، دوباره وارد شوید.");

        }

        else{

            alert("❌ خطا در افزودن علاقه‌مندی");

        }


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



        <h3>
            {{ title }}
        </h3>



        <div class="info">


            <p v-if="year">
                📅 سال ساخت: {{ year }}
            </p>


            <p v-if="mileage">
                🚗 {{ mileage }}
            </p>


        </div>




        <h2 class="price">

            💰 {{ formatPrice(price) }}

            تومان

        </h2>





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

    border-radius:18px;

    overflow:hidden;

    box-shadow:0 10px 25px rgba(0,0,0,.08);

    transition:.3s;

}



.card:hover{


    transform:translateY(-5px);

    box-shadow:0 15px 35px rgba(0,0,0,.15);


}




img{


    width:100%;

    height:220px;

    object-fit:cover;


}





.content{


    padding:20px;


}





h3{


    margin-bottom:15px;

    font-size:20px;


}





.info p{


    color:#555;

    margin:8px 0;


}





.price{


    color:#16a34a;

    font-size:22px;

    margin:20px 0;


}





.favorite{


    width:100%;

    padding:13px;

    margin-bottom:12px;


    border:none;

    border-radius:12px;


    background:#ef4444;

    color:white;


    font-weight:bold;

    cursor:pointer;


    transition:.25s;


}




.favorite:hover{


    background:#dc2626;


}





.btn{


    display:block;

    width:100%;

    text-align:center;


    padding:13px;


    background:#2563eb;

    color:white;


    text-decoration:none;

    border-radius:12px;


    transition:.25s;


}





.btn:hover{


    background:#1d4ed8;


}


</style>
