import axios from 'axios';
import React from 'react';
import '../css/Home.css';
import Cart from '../Components/Cart';
import CartHandler from '../Utils/CartHandler';

const API_URL = process.env.REACT_APP_API_URL;

const handleAddToCart = (product) => {
    CartHandler.addToCart(product);
    console.log("Product added to cart", CartHandler.getCart());
};

class Home extends React.Component {
    state = { products: [] };

    componentDidMount() {
        axios.get(`${API_URL}/api/products/`)
            .then(res => {
                this.setState({ products: res.data });
            })
            .catch(err => {
                console.error("Error loading data:", err);
            });
    }

    render() { 
        return (
            <>
                {/* We pass the current list of products to the cart component */}
                <Cart products={this.state.products} />
                <div className="products-container">
                    {this.state.products.map((product, index) => (
                        <div key={index} className="product-card">
                            <img 
                                src={product.image} 
                                alt={product.name} 
                                className="product-image"
                            />
                            <div className="product-info">
                                <h1>{product.name}</h1>
                                <p>{product.description}</p>
                                <p><strong>Price:</strong> ${product.price}</p>
                                <p><strong>Stock:</strong> {product.stock}</p>
                                <button 
                                    onClick={() => handleAddToCart(product)}
                                    disabled={product.stock === 0}>
                                    {product.stock === 0 ? "Out of Stock" : "Add to Cart"}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </>
        );
    }
}

export default Home;
