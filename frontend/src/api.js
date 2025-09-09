import axios from "axios";

const API_URL = "http://localhost:8000/api/products";

// Fetch all products
export async function fetchProducts() {
  const response = await axios.get(API_URL + "/");
  return response.data;
}

// Search products by name
export async function searchProducts(name) {
  try {
    const response = await axios.get(API_URL + "/search", {
      params: { name },
    });
    return response.data;
  } catch (error) {
    return [];
  }
}
