import axios from "axios";

const API = "http://127.0.0.1:8000";

function authHeader() {

  const token = localStorage.getItem("token");

  return {
    headers: {
      Authorization: token ? `Bearer ${token}` : "",
    },
  };

}

export async function getFavorites() {

  try {

    const response = await axios.get(
      `${API}/favorites/api`,
      authHeader()
    );

    return response.data;

  } catch (err: any) {

    if (err.response?.status === 401) {
      throw new Error("ابتدا وارد حساب کاربری شوید.");
    }

    throw new Error("خطا در دریافت علاقه‌مندی‌ها");

  }

}

export async function addFavorite(carId: number) {

  try {

    const response = await axios.post(
      `${API}/favorites/api/${carId}`,
      {},
      authHeader()
    );

    return response.data;

  } catch (err: any) {

    if (err.response?.status === 401) {
      throw new Error("ابتدا وارد حساب کاربری شوید.");
    }

    if (err.response?.status === 400) {
      throw new Error("این خودرو قبلاً به علاقه‌مندی‌ها اضافه شده است.");
    }

    throw new Error("خطا در افزودن علاقه‌مندی");

  }

}

export async function deleteFavorite(favoriteId: number) {

  try {

    const response = await axios.delete(
      `${API}/favorites/api/${favoriteId}`,
      authHeader()
    );

    return response.data;

  } catch (err: any) {

    if (err.response?.status === 401) {
      throw new Error("ابتدا وارد حساب کاربری شوید.");
    }

    throw new Error("خطا در حذف علاقه‌مندی");

  }

}