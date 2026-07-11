<template>
  <div class="add-car-container">
    <h1>ویرایش خودرو</h1>
    <p class="subtitle">اطلاعات خودرو را ویرایش کنید.</p>

    <form @submit.prevent="submitForm" class="car-form" v-if="car">
      <!-- ردیف اول: برند و مدل -->
      <div class="form-row">
        <div class="form-group">
          <label>برند <span class="required">*</span></label>
          <select v-model="form.brand_id" required>
            <option value="">انتخاب برند</option>
            <option v-for="brand in brands" :key="brand.id" :value="brand.id">
              {{ brand.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>مدل <span class="required">*</span></label>
          <input type="text" v-model="form.model" placeholder="مثلاً 320i" required />
        </div>
      </div>

      <!-- ردیف دوم: سال و قیمت -->
      <div class="form-row">
        <div class="form-group">
          <label>سال ساخت <span class="required">*</span></label>
          <input type="number" v-model="form.year" placeholder="مثلاً 1402" required />
        </div>

        <div class="form-group">
          <label>قیمت (تومان) <span class="required">*</span></label>
          <input type="number" v-model="form.price" placeholder="مثلاً ۲۵۰۰۰۰۰۰۰۰" required />
        </div>
      </div>

      <!-- ردیف سوم: کارکرد و رنگ -->
      <div class="form-row">
        <div class="form-group">
          <label>کارکرد (کیلومتر)</label>
          <input type="number" v-model="form.mileage" placeholder="مثلاً ۴۵۰۰۰" />
        </div>

        <div class="form-group">
          <label>رنگ</label>
          <input type="text" v-model="form.color" placeholder="مثلاً مشکی" />
        </div>
      </div>

      <!-- ردیف چهارم: سوخت و گیربکس -->
      <div class="form-row">
        <div class="form-group">
          <label>نوع سوخت</label>
          <select v-model="form.fuel_type">
            <option value="">انتخاب کنید</option>
            <option value="بنزین">بنزین</option>
            <option value="دیزل">دیزل</option>
            <option value="گازسوز">گازسوز</option>
            <option value="برقی">برقی</option>
            <option value="هیبرید">هیبرید</option>
          </select>
        </div>

        <div class="form-group">
          <label>گیربکس</label>
          <select v-model="form.transmission">
            <option value="">انتخاب کنید</option>
            <option value="دنده‌ای">دنده‌ای</option>
            <option value="اتوماتیک">اتوماتیک</option>
            <option value="CVT">CVT</option>
          </select>
        </div>
      </div>

      <!-- توضیحات -->
      <div class="form-group full-width">
        <label>توضیحات</label>
        <textarea v-model="form.description" rows="5" placeholder="توضیحات کامل خودرو را وارد کنید..."></textarea>
      </div>

      <!-- آپلود تصاویر جدید -->
      <div class="form-group full-width">
        <label>افزودن عکس جدید</label>
        <input type="file" multiple accept="image/*" @change="handleFileUpload" />
        <small class="hint">حداکثر ۵ تصویر با فرمت‌های JPG، PNG یا WebP</small>
        <div v-if="imagePreviews.length" class="image-previews">
          <div v-for="(img, idx) in imagePreviews" :key="idx" class="preview-item">
            <img :src="img" alt="پیش‌نمایش" />
            <button type="button" @click="removeImage(idx)" class="remove-image">×</button>
          </div>
        </div>
      </div>

      <!-- دکمه ویرایش -->
      <button type="submit" class="submit-btn" :disabled="loading">
        {{ loading ? 'در حال ویرایش...' : 'ویرایش خودرو' }}
      </button>
    </form>

    <div v-else-if="loading" class="loading">در حال بارگذاری...</div>
    <div v-else class="error">خودروی مورد نظر یافت نشد.</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

const router = useRouter();
const route = useRoute();
const carId = route.params.id as string;

const loading = ref(false);
const car = ref<any>(null);

// لیست برندها
const brands = ref<any[]>([]);

// فرم
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

// تصاویر جدید
const imageFiles = ref<File[]>([]);
const imagePreviews = ref<string[]>([]);

// ===== بارگذاری برندها =====
async function loadBrands() {
  try {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://127.0.0.1:8000/brands/api/brands", {
      headers: { Authorization: `Bearer ${token}` }
    });
    brands.value = res.data;
  } catch (err) {
    console.error("خطا در دریافت برندها:", err);
  }
}

// ===== بارگذاری اطلاعات خودرو =====
async function loadCar() {
  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    const res = await axios.get(`http://127.0.0.1:8000/cars/api/${carId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    car.value = res.data;

    // پر کردن فرم با داده‌های موجود
    form.value = {
      brand_id: car.value.brand_id,
      model: car.value.model,
      year: car.value.year,
      price: car.value.price,
      mileage: car.value.mileage || "",
      color: car.value.color || "",
      fuel_type: car.value.fuel_type || "",
      transmission: car.value.transmission || "",
      description: car.value.description || "",
    };
  } catch (err: any) {
    console.error(err);
    alert("خطا در دریافت اطلاعات خودرو: " + (err.response?.data?.detail || err.message));
  } finally {
    loading.value = false;
  }
}

// ===== مدیریت آپلود تصاویر =====
function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement;
  if (!input.files) return;

  const files = Array.from(input.files);
  if (imageFiles.value.length + files.length > 5) {
    alert("حداکثر ۵ تصویر مجاز است.");
    return;
  }

  files.forEach(file => {
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

// ===== ارسال ویرایش =====
async function submitForm() {
  if (!form.value.brand_id || !form.value.model || !form.value.year || !form.value.price) {
    alert("لطفاً فیلدهای الزامی را پر کنید.");
    return;
  }

  loading.value = true;

  try {
    const token = localStorage.getItem("token");

    // ۱. ویرایش خودرو
    const carPayload = {
      brand_id: parseInt(form.value.brand_id),
      model: form.value.model,
      year: parseInt(form.value.year),
      price: parseFloat(form.value.price),
      mileage: form.value.mileage ? parseInt(form.value.mileage) : 0,
      color: form.value.color || "",
      fuel_type: form.value.fuel_type || "",
      transmission: form.value.transmission || "",
      description: form.value.description || "",
    };

    await axios.put(
      `http://127.0.0.1:8000/cars/api/${carId}`,
      carPayload,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    // ۲. آپلود تصاویر جدید (در صورت وجود)
    if (imageFiles.value.length > 0) {
      const formData = new FormData();
      imageFiles.value.forEach(file => {
        formData.append("images", file);
      });

      await axios.post(
        `http://127.0.0.1:8000/cars/api/${carId}/images`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );
    }

    alert("خودرو با موفقیت ویرایش شد.");
    router.push("/admin/cars");
  } catch (err: any) {
    console.error(err);
    alert("خطا در ویرایش خودرو: " + (err.response?.data?.detail || err.message));
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadBrands();
  loadCar();
});
</script>

<style scoped>
.add-car-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
  direction: rtl;
  font-family: Vazir, sans-serif;
}

h1 {
  text-align: center;
  color: #1e293b;
  margin-bottom: 6px;
}

.subtitle {
  text-align: center;
  color: #64748b;
  margin-bottom: 32px;
}

.car-form {
  background: #ffffff;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

label {
  font-weight: 600;
  color: #334155;
  margin-bottom: 6px;
  font-size: 14px;
}

.required {
  color: #ef4444;
}

input,
select,
textarea {
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  transition: border-color 0.2s;
  background: #fafbfc;
  font-family: inherit;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.hint {
  margin-top: 4px;
  font-size: 12px;
  color: #94a3b8;
}

.image-previews {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
}

.preview-item {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #ef4444;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.submit-btn {
  width: 100%;
  padding: 14px;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 8px;
}

.submit-btn:hover {
  background: #1d4ed8;
}

.submit-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  color: #64748b;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>