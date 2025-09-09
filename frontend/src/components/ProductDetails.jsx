export default function ProductDetails({ product, onBack }) {
  if (!product) return null;

  return (
    <div className="container">
        <a className="back-link" onClick={onBack}>
          &larr; Back to Products
        </a>
      <div className="product-details">
        <img src={product.image} alt={product.name} />
        <h2>{product.name}</h2>
        <p><strong>Category:</strong> {product.category}</p>
        <p><strong>Price:</strong> ${product.price}</p>
        <p><strong>Stock:</strong> {product.stock}</p>
        <p>{product.description}</p>
      </div>
    </div>
  );
}