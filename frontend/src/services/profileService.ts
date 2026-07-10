import axios from "axios";

const API = "http://127.0.0.1:8000";

export async function getProfile() {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        `${API}/users/api/me`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    return response.data;
}