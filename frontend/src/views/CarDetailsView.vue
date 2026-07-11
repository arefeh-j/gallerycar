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

// ===== بارگذاری اطلاعات خودرو =====
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

// ===== افزودن به علاقه‌مندی‌ها =====
async function addToFavorites() {
  try {
    await addFavorite(Number(id));
    alert(" خودرو به علاقه‌مندی‌ها اضافه شد");
  } catch (error: any) {
    console.log(error);
    alert(" خطا در افزودن به علاقه‌مندی");
  }
}

// ===== ثبت درخواست خرید (از نسخه HEAD) =====
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
        car_id: Number(id),
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    alert(" درخواست خرید با موفقیت ثبت شد.");
  } catch (error: any) {
    console.log(error);
    alert(error.response?.data?.detail || "خطا در ثبت درخواست خرید");
  }
}

// ===== گالری تصاویر (از نسخه دوستم) =====
function nextImage() {
  if (!car.value?.images?.length) return;
  currentImage.value = (currentImage.value + 1) % car.value.images.length;
}

function prevImage() {
  if (!car.value?.images?.length) return;
  currentImage.value =
    (currentImage.value - 1 + car.value.images.length) %
    car.value.images.length;
}

function imageUrl(url: string) {
  return "http://127.0.0.1:8000" + url;
}

// ===== بازگشت به صفحه قبل (از نسخه HEAD) =====
function goBack() {
  router.back();
}
</script>

<template>
  <div class="page">
    <!-- دکمه بازگشت (از HEAD) -->
    <div class="back-wrapper">
      <button class="back" @click="goBack">← بازگشت</button>
    </div>

    <div v-if="loading" class="loading">در حال بارگذاری...</div>

    <div v-else-if="car" class="car-details">
      <!-- گالری تصاویر (از نسخه دوستم) -->
      <div class="gallery">
        <img
          v-if="car.images && car.images.length"
          :src="imageUrl(car.images[currentImage].url)"
          class="main-image"
        />
        <div v-else class="no-image">بدون تصویر</div>

        <button
          v-if="car.images && car.images.length > 1"
          @click="prevImage"
          class="arrow left"
        >
          ❮
        </button>
        <button
          v-if="car.images && car.images.length > 1"
          @click="nextImage"
          class="arrow right"
        >
          ❯
        </button>
      </div>

      <!-- اطلاعات اصلی (از نسخه دوستم با حفظ داده‌ها) -->
      <div class="info">
        <h1>{{ car.brand }} {{ car.model }}</h1>

        <div class="price"> {{ Number(car.price).toLocaleString("fa-IR") }} تومان</div>

        <div class="cards">
          <div class="card">
             مدل <b>{{ car.model }}</b>
          </div>
          <div class="card">
             سال <b>{{ car.year }}</b>
          </div>
          <div class="card">
             رنگ <b>{{ car.color }}</b>
          </div>
          <div class="card">
             گیربکس <b>{{ car.transmission }}</b>
          </div>
          <div class="card">
             سوخت <b>{{ car.fuel_type }}</b>
          </div>
          <div class="card">
             کارکرد <b>{{ Number(car.mileage).toLocaleString("fa-IR") }} کیلومتر</b>
          </div>
          <div class="card">
             وضعیت <b>
        {{
          car.status === "approved"
             ? "منتشر شده"
            : car.status === "pending"
            ? "در انتظار"
            : car.status === "sold"
            ? "فروخته شده"

: car.status
        }}
            </b>
          </div>
        </div>

        <!-- دکمه‌های عملیاتی (از هر دو نسخه) -->
        <div class="buttons">
          <button class="favorite" @click="addToFavorites">
             افزودن به علاقه‌مندی
          </button>

          <!-- دکمه خرید از HEAD -->
          <button class="buy" @click="orderCar"> ثبت درخواست خرید</button>

          <!-- دکمه تماس با فروشنده از نسخه دوستم -->
          <button class="contact"> تماس با فروشنده</button>
        </div>
      </div>

      <!-- توضیحات (از نسخه دوستم) -->
      <div class="description">
        <h2>توضیحات خودرو</h2>
        <p>{{ car.description || "توضیحی ثبت نشده است." }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ===== استایل‌های کلی (از نسخه دوستم) ===== /
.page {
  padding: 40px 20px;
  background: #f3f4f6;
  min-height: 100vh;
}

.loading {
  text-align: center;
  font-size: 24px;
  padding: 100px;
}

.car-details {
  max-width: 1000px;
  margin: auto;
}

/ ===== دکمه بازگشت (از HEAD) ===== /
.back-wrapper {
  max-width: 1000px;
  margin: 0 auto 20px auto;
}
.back {
  padding: 10px 20px;
  border: none;
  background: #2563eb;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}
.back:hover {
  background: #1d4ed8;
}

/ ===== گالری (از نسخه دوستم) ===== /
.gallery {
  position: relative;
  background: white;
  padding: 18px;
  border-radius: 24px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
}

.main-image {
  width: 100%;
  height: 360px;
  object-fit: cover;
  border-radius: 18px;
}

.no-image {
  height: 360px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eee;
  border-radius: 18px;
  font-size: 22px;
  color: #888;
}

.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: none;
  background: white;
  font-size: 25px;
  cursor: pointer;
  box-shadow: 0 5px 15px #ccc;
  transition: 0.2s;
}
.arrow:hover {
  background: #f0f0f0;
}
.left {
  left: 30px;
}
.right {
  right: 30px;
}

/ ===== اطلاعات (از نسخه دوستم) ===== /
.info {
  margin-top: 25px;
  background: white;
  padding: 35px;
  border-radius: 24px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
}

.info h1 {
  font-size: 38px;
  margin-bottom: 10px;
  color: #111827;
}

.price {
  font-size: 32px;
  font-weight: 900;
  color: #16a34a;
  margin: 25px 0;
}

.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.card {
  background: #f9fafb;
  border-radius: 18px;
  padding: 20px;
  text-align: center;
  font-size: 16px;
  transition: 0.25s;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
}
.card b {
  display: block;
  margin-top: 12px;
  font-size: 18px;
}

/ ===== دکمه‌ها (ترکیبی) ===== /
.buttons {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
  margin-top: 30px;
}

.buttons button {
  height: 55px;
  border: none;
  border-radius: 15px;
  font-size: 17px;
  cursor: pointer;
  transition: 0.25s;
}

.favorite {
  background: #fee2e2;
  color: #dc2626;
}
.favorite:hover {
  background: #fecaca;
}

.buy {
  background: #dcfce7;
  color: #16a34a;
}
.buy:hover {
  background: #bbf7d0;
}

.contact {
  background: #dbeafe;
  color: #2563eb;
}
.contact:hover {
  background: #bfdbfe;
}

/ ===== توضیحات (از نسخه دوستم) ===== /
.description {
  margin-top: 25px;
  background: white;
  padding: 35px;
  border-radius: 24px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
}

.description h2 {
  font-size: 28px;
  margin-bottom: 20px;
}

.description p {
  line-height: 2;
  color: #555;
}

/ ===== ریسپانسیو ===== */
@media (max-width: 768px) {
  .page {
    padding: 20px 10px;
  }
  .main-image {
    height: 250px;
  }
  .info {
    padding: 20px;
  }
  .info h1 {
    font-size: 26px;
  }
  .cards {
    grid-template-columns: 1fr;
  }
  .buttons {
    grid-template-columns: 1fr;
  }
  .arrow {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
  .left {
    left: 15px;

}
  .right {
    right: 15px;
  }
}
</style>