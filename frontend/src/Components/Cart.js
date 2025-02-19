import React, { useState, useEffect } from 'react';
import CartHandler from '../Utils/CartHandler';
import '../css/Cart.css';

const Cart = () => {
    const [cart, setCart] = useState([]);
    const [totalPrice, setTotalPrice] = useState(0);
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        setCart(CartHandler.getCart());
        setTotalPrice(CartHandler.getTotalPrice());
    }, []);

    const handleRemove = (productId) => {
        CartHandler.removeFromCart(productId);
        setCart([...CartHandler.getCart()]);
        setTotalPrice(CartHandler.getTotalPrice());
    };

    const handleClear = () => {
        CartHandler.clearCart();
        setCart([]);
        setTotalPrice(0);
    };

    const handleQuantityChange = (productId, event) => {
        const quantity = parseInt(event.target.value, 10) || 1;
        CartHandler.updateQuantity(productId, quantity);
        setCart([...CartHandler.getCart()]);
        setTotalPrice(CartHandler.getTotalPrice());
    };

    useEffect(() => {
        const updateCart = () => {
            setCart([...CartHandler.getCart()]);
            setTotalPrice(CartHandler.getTotalPrice());
        };
        window.addEventListener('cartUpdated', updateCart);
        return () => window.removeEventListener('cartUpdated', updateCart);
    }, []);

    const toggleCartVisibility = () => {
        setIsVisible((prev) => !prev);
    };

    return (
        <>
            <button className="cart-float-button" onClick={toggleCartVisibility}>
                🛒
            </button>
            <div className={`cart-container ${isVisible ? 'cart-visible' : 'cart-hidden'}`}>
                <h2>Shopping Cart</h2>
                {cart.length === 0 ? (
                    <p>Your cart is empty.</p>
                ) : (
                    <>
                        <ul className="cart-items-list">
                            {cart.map(item => (
                                <li key={item.id} className="cart-item">
                                    <img src={item.image} alt={item.name} className="cart-image" />
                                    <div>
                                        <h3>{item.name}</h3>
                                        <p>Price: ${item.price}</p>
                                        <p>Total: ${(item.price * item.quantity).toFixed(2)}</p>
                                        <label>Quantity:
                                            <input 
                                                type="number" 
                                                value={item.quantity} 
                                                min="1" 
                                                onChange={(event) => handleQuantityChange(item.id, event)}
                                            />
                                        </label>
                                        <button onClick={() => handleRemove(item.id)}>Remove</button>
                                    </div>
                                </li>
                            ))}
                        </ul>
                        <h3>Total Price: ${totalPrice.toFixed(2)}</h3>
                    </>
                )}
                {cart.length > 0 && <button onClick={handleClear}>Clear Cart</button>}
            </div>
        </>
    );
};

export default Cart;