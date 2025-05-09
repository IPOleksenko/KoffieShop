import React, { useState, useEffect } from 'react';
import CartHandler from '../Utils/CartHandler';
import CheckoutButton from './CheckoutButton';
import RecipientForm from './RecipientForm';
import '../css/Cart.css';

const Cart = ({ products }) => {
  const [cartItems, setCartItems] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  // Load recipientData from localStorage on initialization
  const [recipientData, setRecipientData] = useState(() => {
    const saved = localStorage.getItem('recipientData');
    return saved ? JSON.parse(saved) : {
      firstName: '',
      lastName: '',
      phone: '',
      country: '',
      city: '',
      street: '',
      house: '',
      email: '',
    };
  });

  // Save recipientData to localStorage on every change
  useEffect(() => {
    localStorage.setItem('recipientData', JSON.stringify(recipientData));
  }, [recipientData]);

  const mergeCartWithProducts = () => {
    if (!products || products.length === 0) return [];
    CartHandler.syncCart(products);
    const rawCart = CartHandler.getCart();
    return rawCart
      .map(item => {
        const product = products.find(p => p.id === item.id);
        return product ? { ...product, quantity: item.quantity } : null;
      })
      .filter(item => item !== null);
  };

  const updateCartState = () => {
    const merged = mergeCartWithProducts();
    setCartItems(merged);
    const total = merged.reduce((acc, item) => acc + item.price * item.quantity, 0);
    setTotalPrice(total);
  };

  useEffect(() => {
    updateCartState();
  }, [products]);

  useEffect(() => {
    const updateCart = () => updateCartState();
    window.addEventListener('cartUpdated', updateCart);
    return () => window.removeEventListener('cartUpdated', updateCart);
  }, [products]);

  const handleRemove = (productId) => {
    CartHandler.removeFromCart(productId);
    updateCartState();
  };

  const handleClear = () => {
    CartHandler.clearCart();
    updateCartState();
  };

  const handleQuantityChange = (productId, event) => {
    const inputQuantity = parseInt(event.target.value, 10) || 1;
    const product = products.find(p => p.id === productId);
    if (!product) return;
    const quantity = Math.min(Math.max(1, inputQuantity), product.stock);
    CartHandler.updateQuantity(productId, quantity, product.stock);
    updateCartState();
  };

  const toggleCartVisibility = () => {
    setIsVisible(prev => !prev);
  };

  const minimalCartData = cartItems.map(item => ({
    id: item.id,
    quantity: item.quantity
  }));

  return (
    <>
      <button className="cart-float-button" onClick={toggleCartVisibility}>
        🛒
      </button>

      <div className={`cart-container ${isVisible ? 'cart-visible' : 'cart-hidden'}`}>
        <h2>Shopping Cart</h2>
        {cartItems.length === 0 ? (
          <p>Your cart is empty.</p>
        ) : (
          <>
            <ul className="cart-items-list">
              {cartItems.map(item => (
                <li key={item.id} className="cart-item">
                  <img src={item.image} alt={item.name} className="cart-image" />
                  <div>
                    <h3>{item.name}</h3>
                    <p>Price: ${item.price}</p>
                    <p>Total: ${(item.price * item.quantity).toFixed(2)}</p>
                    <label>
                      Quantity:
                      <input
                        type="number"
                        value={item.quantity}
                        min="1"
                        max={item.stock}
                        onChange={(event) => handleQuantityChange(item.id, event)}
                      />
                    </label>
                    <button onClick={() => handleRemove(item.id)}>Remove</button>
                  </div>
                </li>
              ))}
            </ul>
            <h3>Total Price: ${totalPrice.toFixed(2)}</h3>
            <div className="cart-actions">
              <button onClick={handleClear} className="clear-cart-button">Clear Cart</button>
              <CheckoutButton products={minimalCartData} recipientData={recipientData} />
            </div>
          </>
        )}
      </div>

      <RecipientForm
        isVisible={isVisible}
        recipientData={recipientData}
        setRecipientData={setRecipientData}
      />
    </>
  );
};

export default Cart;
