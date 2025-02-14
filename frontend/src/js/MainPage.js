import axios from 'axios';
import React from 'react';
import '../css/MainPage.css';

class MainPage extends React.Component {
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
                        </div>
                    </div>
                ))}
            </div>
        );
    }
}

export default MainPage;
