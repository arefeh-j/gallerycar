import api from "../api/api";


// گرفتن لیست علاقه مندی ها
export async function getFavorites(){

    const response = await api.get("/favorites/landing");

    return response.data;

}


// حذف علاقه مندی
export async function deleteFavorite(id:number){

    const response = await api.get(
        `/favorites/delete/${id}`
    );

    return response.data;

}