import axios from "axios";

export async function APICategories() {
    try {
        const response = await axios.get("http://127.0.0.1:8000/api/categories/",)
        return response.data
    } catch (e) {
        return null
    }
}

export async function API_all_items(page) {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/all/items/?page=${page}`,)
        return response.data

    } catch (e) {
        return null
    }
}
export async function API_category_items() {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/items/`,)
        return response.data
    } catch (e) {
        return null
    }
}