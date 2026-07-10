import axios from "axios";

const API = "http://127.0.0.1:8000";

function authHeader() {
    const token = localStorage.getItem("token");

    return {
        headers: {
            Authorization: `Bearer ${token}`
        }
    };
}

export async function getProfile() {

    const response = await axios.get(
        `${API}/users/api/me`,
        authHeader()
    );

    return response.data;
}

export async function updateProfile(data: any) {

    const response = await axios.put(
        `${API}/users/api/me`,
        data,
        authHeader()
    );

    return response.data;
}