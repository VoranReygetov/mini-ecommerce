export default function ProductCard({ product, onSelect }) {
  return (
    <div className="card" onClick={() => onSelect(product)}>
      <img src={product.image} alt={product.name} />
      <div className="card-body">
        <h2>{product.name}</h2>
        <p>{product.category}</p>
        <p>${product.price}</p>
        <p>Stock: {product.stock}</p>
      </div>
    </div>
  );
}