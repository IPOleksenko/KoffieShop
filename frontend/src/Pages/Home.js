import axios from 'axios';
import React from 'react';
import '../css/Home.css';
import Cart from '../Components/Cart';
import CartHandler from '../Utils/CartHandler';

const handleAddToCart = (product) => {
    CartHandler.addToCart(product);
    console.log("Product added to cart", CartHandler.getCart());
};

class Home extends React.Component {
    state = { products: [] };

    componentDidMount() {
        axios.get('http://localhost:8000/api/products/')
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
            <Cart/>
                <div className="products-container">
                    {this.state.products.map((product, id) => (
                        <div key={id} className="product-card">
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
                                <button onClick={() => handleAddToCart(product)}>Add to Cart</button>
                            </div>
                        </div>
                    ))}
                </div>
            </>
        );
    }
}

export default Home;
