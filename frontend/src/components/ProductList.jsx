import { useEffect, useState } from "react";
import { fetchProducts, searchProducts } from "../api";
import ProductCard from "./ProductCard";
import ProductDetails from "./ProductDetails";

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    loadProducts();
  }, []);

  async function loadProducts() {
    try {
      const data = await fetchProducts();
      setProducts(data);
    } catch (err) {
      console.error("Failed to load products", err);
    }
  }

  async function handleSearch(e) {
    e.preventDefault();
    try {
      if (!query.trim()) {
        loadProducts();
      } else {
        const data = await searchProducts(query);
        setProducts(data);
      }
    } catch (err) {
      console.error("Search failed", err);
    }
  }

  if (selected) {
    return <ProductDetails product={selected} onBack={() => setSelected(null)} />;
  }

  return (
    <div className="container">
      <h1>Product List</h1>
      <form onSubmit={handleSearch} className="search-bar">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search products..."
        />
        <button type="submit">Search</button>
      </form>

      <div className="grid">
        {products.length > 0 ? (
          products.map((p) => (
            <ProductCard key={p.id} product={p} onSelect={setSelected} />
          ))
        ) : (
          <p>No products found</p>
        )}
      </div>
    </div>
  );
}