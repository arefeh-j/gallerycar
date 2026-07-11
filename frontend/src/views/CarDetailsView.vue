<script setup lang="ts">

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { addFavorite } from "../services/favoriteService";

const route = useRoute();
const router = useRouter();

const car = ref<any>(null);
const loading = ref(true);

const id = route.params.id;

onMounted(async () => {

    try {

        const response = await axios.get(
            `http://127.0.0.1:8000/cars/api/${id}`
        );

        car.value = response.data;

    } catch (error) {

        console.log(error);

    } finally {

        loading.value = false;

    }

});


async function addToFavorites() {

    try {

        await addFavorite(Number(id));

        alert("✅ خودرو به علاقه‌مندی‌ها اضافه شد");

    } catch (error: any) {

        console.log(error);
        console.log(error.response);
        console.log(error.response?.status);
        console.log(error.response?.data);

        alert("❌ خطا در افزودن به علاقه‌مندی‌ها");

    }

}




async function orderCar() {

    try {

        const token = localStorage.getItem("token");

        if (!token) {

            alert("ابتدا وارد حساب کاربری شوید.");

            router.push("/login");

            return;

        }

        await axios.post(
            "http://127.0.0.1:8000/orders/api",
            {
                car_id: Number(id)
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        alert("✅ درخواست خرید با موفقیت ثبت شد.");

    } catch (error: any) {

        console.log(error);

        alert(
            error.response?.data?.detail ||
            "خطا در ثبت درخواست خرید"
        );

    }

}


function goBack() {

    router.back();

}

</script>
<template>

<div v-if="loading" class="loading">

در حال دریافت اطلاعات خودرو...

</div>

<div v-else-if="car" class="container">

    <button class="back" @click="goBack">
        ← بازگشت
    </button>

    <div class="card">

        <div class="image-section">

            <img
                v-if="car.images && car.images.length"
                :src="car.images[0].url"
                alt="car"
            />

            <img
                v-else
                src="https://placehold.co/700x450?text=No+Image"
            />

        </div>

        <div class="info">

            <h1>
                {{ car.brand }}
                {{ car.model }}
            </h1>

            <h2>
                {{ Number(car.price).toLocaleString("fa-IR") }}
                تومان
            </h2>

            <div class="grid">

                <div class="item">
                    <span>سال ساخت</span>
                    <strong>{{ car.year }}</strong>
                </div>

                <div class="item">
                    <span>کارکرد</span>
                    <strong>
                        {{ Number(car.mileage).toLocaleString("fa-IR") }}
                        کیلومتر
                    </strong>
                </div>

                <div class="item">
                    <span>رنگ</span>
                    <strong>{{ car.color }}</strong>
                </div>

                <div class="item">
                    <span>گیربکس</span>
                    <strong>{{ car.transmission }}</strong>
                </div>

                <div class="item">
                    <span>سوخت</span>
                    <strong>{{ car.fuel_type }}</strong>
                </div>

                <div class="item">
                    <span>وضعیت</span>
                    <strong>{{ car.status }}</strong>
                </div>

            </div>

            <div class="description">

                <h3>توضیحات</h3>

                <p>

                    {{ car.description || "توضیحی ثبت نشده است." }}

                </p>

            </div>

            <button
                class="favorite"
                @click="addToFavorites"
            >

                ❤️ افزودن به علاقه‌مندی

            </button>

            <button
    class="buy"
    @click="orderCar"
>

🛒 ثبت درخواست خرید

</button>



        </div>

    </div>

</div>

</template>

<style scoped>

.container{
max-width:1200px;
margin:auto;
padding:40px 20px;
direction:rtl;
}

.loading{
padding:80px;
text-align:center;
font-size:22px;
}

.back{
margin-bottom:20px;
padding:10px 20px;
border:none;
background:#2563eb;
color:white;
border-radius:8px;
cursor:pointer;
}

.card{
display:grid;
grid-template-columns:1.1fr 1fr;
gap:40px;
background:white;
border-radius:20px;
padding:30px;
box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.image-section img{
width:100%;
height:450px;
object-fit:cover;
border-radius:16px;
}

.info h1{
margin:0;
font-size:34px;
}

.info h2{
color:#2563eb;
margin:20px 0;
font-size:30px;
}

.grid{
display:grid;
grid-template-columns:repeat(2,1fr);
gap:15px;
margin:25px 0;
}

.item{
background:#f5f7fb;
padding:15px;
border-radius:12px;
display:flex;
justify-content:space-between;
}

.description{
margin-top:25px;
line-height:2;
}

.favorite{
width:100%;
margin-top:30px;
padding:16px;
background:#ef4444;
color:white;
border:none;
border-radius:12px;
font-size:17px;
cursor:pointer;
transition:.3s;
}

.favorite:hover{
background:#dc2626;
}

@media(max-width:900px){

.card{

grid-template-columns:1fr;

}

.image-section img{

height:300px;

}

}



.buy{

width:100%;

margin-top:15px;

padding:16px;

background:#16a34a;

color:white;

border:none;

border-radius:12px;

font-size:17px;

cursor:pointer;

transition:.3s;

}

.buy:hover{

background:#15803d;

}

</style>