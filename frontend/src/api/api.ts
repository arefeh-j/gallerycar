const API_URL = "http://127.0.0.1:8000"

export async function getCars() {
    const response = await fetch(`${API_URL}/cars/api`)

    if (!response.ok) {
        throw new Error("Failed to fetch cars")
    }

    return await response.json()
}