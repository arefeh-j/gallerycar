<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useToast } from "vue-toastification";

const router = useRouter();
const toast = useToast();

const loading = ref(false);

const brands = ref<any[]>([]);

const form = ref({
  brand_id: "",
  model: "",
  year: "",
  price: "",
  mileage: "",
  color: "",
  fuel_type: "",
  transmission: "",
  description: "",
});

const imageFiles = ref<File[]>([]);
const imagePreviews = ref<string[]>([]);

async function loadBrands() {
  try {
    const token = localStorage.getItem("token");

    const res = await axios.get(
      "http://127.0.0.1:8000/brands/api/brands",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    brands.value = res.data;
  } catch (err) {
    console.error(err);
    toast.error("خطا در دریافت برندها");
  }
}

function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement;

  if (!input.files) return;

  const files = Array.from(input.files);

  if (imageFiles.value.length + files.length > 5) {
    toast.warning("حداکثر ۵ تصویر مجاز است.");
    return;
  }

  files.forEach((file) => {
    imageFiles.value.push(file);

    const reader = new FileReader();

    reader.onload = (e) => {
      imagePreviews.value.push(e.target?.result as string);
    };

    reader.readAsDataURL(file);
  });

  input.value = "";
}

function removeImage(index: number) {
  imageFiles.value.splice(index, 1);
  imagePreviews.value.splice(index, 1);
}

async function submitForm() {
  if (
    !form.value.brand_id ||
    !form.value.model ||
    !form.value.year ||
    !form.value.price
  ) {
    toast.error("لطفاً فیلدهای الزامی را تکمیل کنید.");
    return;
  }

  loading.value = true;

  try {
    const token = localStorage.getItem("token");

    const payload = {
      brand_id: Number(form.value.brand_id),
      model: form.value.model,
      year: Number(form.value.year),
      price: Number(form.value.price),
      mileage: form.value.mileage
        ? Number(form.value.mileage)
        : 0,
      color: form.value.color,
      fuel_type: form.value.fuel_type,
      transmission: form.value.transmission,
      description: form.value.description,
    };

    const car = await axios.post(
      "http://127.0.0.1:8000/cars/api",
      payload,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const carId = car.data.id;

    if (imageFiles.value.length > 0) {
      const fd = new FormData();

      imageFiles.value.forEach((img) => {
        fd.append("images", img);
      });

      await axios.post(
        `http://127.0.0.1:8000/cars/api/${carId}/images`,
        fd,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );
    }

    toast.success("خودرو با موفقیت ثبت شد.", {
      timeout: 3000,
    });

    router.push("/admin/cars");
  } catch (err: any) {
    console.error(err);

    toast.error(
      typeof err.response?.data?.detail === "string"
        ? err.response.data.detail
        : "خطا در ثبت خودرو",
      {
        timeout: 3000,
      }
    );
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadBrands();
});
</script>


<template>

<div class="page">

  <div class="card">

    <h1>ثبت خودرو</h1>

    <p class="subtitle">
      اطلاعات خودرو را وارد کنید.
    </p>

    <form @submit.prevent="submitForm">

      <!-- برند -->
      <div class="form-group">
        <label>برند</label>

        <select
          v-model="form.brand_id"
          required
        >
          <option value="">انتخاب برند</option>

          <option
            v-for="brand in brands"
            :key="brand.id"
            :value="brand.id"
          >
            {{ brand.name }}
          </option>

        </select>
      </div>


      <!-- مدل -->
      <div class="form-group">
        <label>مدل</label>

        <input
          v-model="form.model"
          type="text"
          placeholder="مثلاً BMW 320"
          required
        >
      </div>


      <!-- سال -->
      <div class="form-group">
        <label>سال ساخت</label>

        <input
          v-model="form.year"
          type="number"
          required
        >
      </div>


      <!-- قیمت -->
      <div class="form-group">
        <label>قیمت</label>

        <input
          v-model="form.price"
          type="number"
          required
        >
      </div>


      <!-- کارکرد -->
      <div class="form-group">
        <label>کارکرد</label>

        <input
          v-model="form.mileage"
          type="number"
        >
      </div>


      <!-- رنگ -->
      <div class="form-group">
        <label>رنگ</label>

        <input
          v-model="form.color"
          type="text"
        >
      </div>


      <!-- سوخت -->
      <div class="form-group">

        <label>نوع سوخت</label>

        <select v-model="form.fuel_type">

          <option value="">انتخاب کنید</option>

          <option value="بنزین">
            بنزین
          </option>

          <option value="دیزل">
            دیزل
          </option>

          <option value="برقی">
            برقی
          </option>

          <option value="هیبرید">
            هیبرید
          </option>

          <option value="گاز">
            گاز
          </option>

        </select>

      </div>


      <!-- گیربکس -->
      <div class="form-group">

        <label>گیربکس</label>

        <select v-model="form.transmission">

          <option value="">انتخاب کنید</option>

          <option value="اتومات">
            اتومات
          </option>

          <option value="دنده‌ای">
            دنده‌ای
          </option>

          <option value="CVT">
            CVT
          </option>

        </select>

      </div>


      <!-- توضیحات -->
      <div class="form-group full">

        <label>توضیحات</label>

        <textarea
          rows="5"
          v-model="form.description"
        ></textarea>

      </div>



      <!-- تصاویر -->

      <div class="form-group full">

        <label>
          تصاویر خودرو
        </label>

        <input
          type="file"
          multiple
          accept="image/*"
          @change="handleFileUpload"
        >

        <small>
          حداکثر ۵ تصویر
        </small>


        <div
          class="preview-list"
          v-if="imagePreviews.length"
        >

          <div
            class="preview-item"
            v-for="(img,index) in imagePreviews"
            :key="index"
          >

            <img
              :src="img"
            >

            <button
              type="button"
              class="remove"
              @click="removeImage(index)"
            >

              ✕

            </button>

          </div>

        </div>

      </div>



      <button
        class="submit"
        :disabled="loading"
      >

        {{ loading ? "در حال ثبت..." : "ثبت خودرو" }}

      </button>

    </form>

  </div>

</div>

</template>


<style scoped>

.page{

direction:rtl;

padding:40px 20px;

display:flex;

justify-content:center;

}


.card{

width:100%;
max-width:950px;

background:white;

border-radius:18px;

padding:35px;

box-shadow:0 8px 25px rgba(0,0,0,.08);

}


h1{

text-align:center;

font-size:30px;

margin-bottom:8px;

color:#1f2937;

}


.subtitle{

text-align:center;

color:#6b7280;

margin-bottom:35px;

}


form{

display:grid;

grid-template-columns:1fr 1fr;

gap:22px;

}


.form-group{

display:flex;

flex-direction:column;

}


.full{

grid-column:1/-1;

}


label{

font-size:15px;

font-weight:700;

margin-bottom:8px;

color:#374151;

}


input,
select,
textarea{

padding:13px 15px;

border:1px solid #d1d5db;

border-radius:10px;

font-size:15px;

font-family:inherit;

transition:.25s;

background:#fff;

}


input:focus,
select:focus,
textarea:focus{

outline:none;

border-color:#2563eb;

box-shadow:0 0 0 3px rgba(37,99,235,.15);

}


textarea{

resize:vertical;

min-height:120px;

}


small{

margin-top:8px;

color:#6b7280;

font-size:13px;

}



.preview-list{

display:flex;

flex-wrap:wrap;

gap:14px;

margin-top:18px;

}



.preview-item{

position:relative;

width:120px;

height:120px;

border-radius:12px;

overflow:hidden;

border:1px solid #e5e7eb;

background:#f9fafb;

transition:.25s;

}


.preview-item:hover{

transform:translateY(-3px);

box-shadow:0 6px 18px rgba(0,0,0,.12);

}



.preview-item img{

width:100%;

height:100%;

object-fit:cover;

}



.remove{

position:absolute;

top:6px;

left:6px;

width:28px;

height:28px;

border:none;

border-radius:50%;

background:#ef4444;

color:white;

cursor:pointer;

font-size:16px;

font-weight:bold;

transition:.2s;

}


.remove:hover{

background:#dc2626;

transform:scale(1.08);

}



.submit{

grid-column:1/-1;

margin-top:10px;

padding:15px;

border:none;

border-radius:12px;

background:#2563eb;

color:white;

font-size:17px;

font-weight:700;

cursor:pointer;

transition:.25s;

}


.submit:hover{

background:#1d4ed8;

transform:translateY(-2px);

box-shadow:0 8px 18px rgba(37,99,235,.25);

}


.submit:disabled{

background:#94a3b8;

cursor:not-allowed;

box-shadow:none;

transform:none;

}



@media(max-width:768px){

.card{

padding:22px;

}

form{

grid-template-columns:1fr;

}

.full{

grid-column:auto;

}

.preview-item{

width:100px;

height:100px;

}

}

</style>