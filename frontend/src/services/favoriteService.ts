import axios from "axios";

const API = "http://127.0.0.1:8000";

function authHeader() {
  return {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  };
}

export async function getFavorites() {
  const response = await axios.get(
    `${API}/favorites/api`,
    authHeader()
  );

  return response.data;
}

export async function addFavorite(carId: number) {
  const response = await axios.post(
    `${API}/favorites/api/${carId}`,
    {},
    authHeader()
  );

  return response.data;
}

export async function deleteFavorite(favoriteId: number) {
  const response = await axios.delete(
    `${API}/favorites/api/${favoriteId}`,
    authHeader()
  );

  return response.data;
}