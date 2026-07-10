<template>
<section class="hero">

    <div class="overlay">

        <div class="content">

            <h1>
                خرید و فروش خودرو با اطمینان
            </h1>

            <p>
                هزاران آگهی خودرو را جستجو کنید، قیمت‌ها را مقایسه کنید و بهترین انتخاب را داشته باشید.
            </p>

            <div class="buttons">

                <button class="primary">
                    مشاهده خودروها
                </button>

                <button class="secondary">
                    ثبت آگهی
                </button>

            </div>

        </div>

    </div>

</section>
</template>

<style scoped>

.hero{

height:500px;

background-image:url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1600");

background-size:cover;

background-position:center;

display:flex;

align-items:center;

justify-content:center;

}

.overlay{

width:100%;
height:100%;
background:rgba(0,0,0,.55);

display:flex;

align-items:center;

justify-content:center;

}

.content{

text-align:center;

color:white;

max-width:800px;

padding:20px;

}

.content h1{

font-size:48px;

margin-bottom:20px;

}

.content p{

font-size:20px;

line-height:2;

margin-bottom:35px;

}

.buttons{

display:flex;

justify-content:center;

gap:20px;

}

button{

padding:15px 35px;

border:none;

border-radius:10px;

font-size:17px;

cursor:pointer;

transition:.3s;

}

.primary{

background:#2563eb;

color:white;

}

.primary:hover{

background:#1d4ed8;

}

.secondary{

background:white;

color:#222;

}

.secondary:hover{

background:#ececec;

}

@media(max-width:768px){

.content h1{

font-size:34px;

}

.content p{

font-size:17px;

}

.buttons{

flex-direction:column;

}

}

</style>