<script setup lang="ts">

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { addFavorite } from "../services/favoriteService";


const route = useRoute();
const router = useRouter();


const car = ref<any>(null);
const loading = ref(true);
const currentImage = ref(0);


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



async function addToFavorites(){

    try{

        await addFavorite(Number(id));

        alert("❤️ خودرو به علاقه‌مندی‌ها اضافه شد");


    }catch(error:any){

        console.log(error);
        alert("❌ خطا در افزودن به علاقه‌مندی");

    }

}



<<<<<<< HEAD

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
=======
function nextImage(){

    if(!car.value?.images?.length)
        return;


    currentImage.value =
        (currentImage.value + 1)
        % car.value.images.length;
>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb

}


<<<<<<< HEAD
function goBack() {
=======

function prevImage(){

    if(!car.value?.images?.length)
        return;


    currentImage.value =
        (currentImage.value - 1 + car.value.images.length)
        % car.value.images.length;

}



function imageUrl(url:string){

    return "http://127.0.0.1:8000" + url;

}



function goBack(){
>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb

    router.back();

}

<<<<<<< HEAD
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
=======

</script>



<template>


<div class="page">


    <div v-if="loading" class="loading">

        در حال بارگذاری...

    </div>



    <div v-else-if="car" class="car-details">



        <!-- Gallery -->

        <div class="gallery">


            <img
                v-if="car.images && car.images.length"
                :src="imageUrl(car.images[currentImage].url)"
                class="main-image"
            />


            <div
                v-else
                class="no-image"
            >
                بدون تصویر
            </div>



            <button
                v-if="car.images.length > 1"
                @click="prevImage"
                class="arrow left"
            >
                ❮
            </button>


            <button
                v-if="car.images.length > 1"
                @click="nextImage"
                class="arrow right"
            >
                ❯
            </button>



        </div>



        <!-- Information -->


        <div class="info">



            <h1>
                {{ car.model }}
            </h1>


            <div class="price">

                💰 {{ car.price }} تومان

            </div>




            <div class="cards">


                <div class="card">
                    🏷 مدل
                    <b>{{ car.model }}</b>
                </div>


                <div class="card">
                    📅 سال
                    <b>{{ car.year }}</b>
                </div>


                <div class="card">
                    🎨 رنگ
                    <b>{{ car.color }}</b>
                </div>


                <div class="card">
                    ⚙ گیربکس
                    <b>{{ car.transmission }}</b>
                </div>


                <div class="card">
                    ⛽ سوخت
                    <b>{{ car.fuel_type }}</b>
                </div>


                <div class="card">
                    🚗 کارکرد
                    <b>{{ car.mileage }}</b>
                </div>


                <div class="card">
                    ✅ وضعیت
                    <b>{{ car.status }}</b>
                </div>


            </div>



            <div class="buttons">


                <button
                    class="favorite"
                    @click="addToFavorites"
                >

                    ❤️ افزودن به علاقه‌مندی

                </button>



                <button class="contact">

                    📞 تماس با فروشنده

                </button>


            </div>



        </div>



        <!-- Description -->


        <div class="description">


            <h2>
                توضیحات خودرو
            </h2>


            <p>
                {{ car.description }}
            </p>


        </div>



    </div>



</div>


</template>



<style scoped>


.page{

    padding:40px 20px;
    background:#f3f4f6;
    min-height:100vh;

}



.loading{

    text-align:center;
    font-size:24px;
    padding:100px;

}




.car-details{

    max-width:1000px;
    margin:auto;

}



/* Gallery */


.gallery{

    position:relative;

    background:white;

    padding:18px;

    border-radius:24px;

    box-shadow:0 15px 35px rgba(0,0,0,.08);

}



.main-image{

    width:100%;

    height:360px;

    object-fit:cover;

    border-radius:18px;

}



.no-image{

    height:360px;

    display:flex;

    justify-content:center;

    align-items:center;

    background:#eee;

    border-radius:18px;

    font-size:22px;

}





.arrow{

    position:absolute;

    top:50%;

    transform:translateY(-50%);

    width:50px;

    height:50px;

    border-radius:50%;

    border:none;

    background:white;

    font-size:25px;

    cursor:pointer;

    box-shadow:0 5px 15px #ccc;

}



.left{

    left:30px;

}



.right{

    right:30px;

}




/* Main Info */


.info{

    margin-top:25px;

    background:white;

    padding:35px;

    border-radius:24px;

    box-shadow:0 15px 35px rgba(0,0,0,.08);

}



.info h1{

    font-size:38px;

    margin-bottom:10px;

    color:#111827;

}





.price{

    font-size:32px;

    font-weight:900;

    color:#16a34a;

    margin:25px 0;

}





.cards{


    display:grid;

    grid-template-columns:repeat(3,1fr);

    gap:18px;

}





.card{

    background:#f9fafb;

    border-radius:18px;

    padding:20px;

    text-align:center;

    font-size:16px;

    transition:.25s;

}



.card:hover{

    transform:translateY(-5px);

    box-shadow:0 10px 20px rgba(0,0,0,.08);
>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb

}



<<<<<<< HEAD
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

=======
.card b{

    display:block;

    margin-top:12px;

    font-size:18px;

}





/* Buttons */


.buttons{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:20px;

    margin-top:30px;

}




.buttons button{

    height:55px;

    border:none;

    border-radius:15px;

    font-size:17px;

    cursor:pointer;

    transition:.25s;

}



.favorite{

    background:#fee2e2;

    color:#dc2626;

}



.favorite:hover{

    background:#fecaca;

}



.contact{

    background:#dbeafe;

    color:#2563eb;

}



.contact:hover{

    background:#bfdbfe;

}





/* Description */


.description{

    margin-top:25px;

    background:white;

    padding:35px;

    border-radius:24px;

    box-shadow:0 15px 35px rgba(0,0,0,.08);

}



.description h2{

    font-size:28px;

    margin-bottom:20px;

}





.description p{

    line-height:2;

    color:#555;

}





@media(max-width:768px){



.page{

    padding:20px 10px;

}



.main-image{

    height:250px;

}



.info{

    padding:20px;

}



.info h1{

    font-size:26px;

}



.cards{

    grid-template-columns:1fr;

}



.buttons{

    grid-template-columns:1fr;

}



}



>>>>>>> e808297a8431d55d36623f6e02228f5715a5d3cb
</style>