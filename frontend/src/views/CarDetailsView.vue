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


function goBack() {

    router.back();

}

</script>