import React from 'react';
import '../css/CheckoutButton.css';

const CheckoutButton = ({ products, recipientData }) => {
    // Function to validate recipient's data
    const validateRecipientData = () => {
        const { firstName, lastName, phone, country, city, email } = recipientData;
        if (!firstName || !lastName || !phone || !country || !city || !email) {
            alert("Please fill in all recipient fields.");
            return false;
        }
        // Email validation using a regular expression
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert("Please enter a valid email address.");
            return false;
        }
        // Phone number validation: 10 to 15 digits
        const phoneRegex = /^\d{10,15}$/;
        if (!phoneRegex.test(phone)) {
            alert("Please enter a valid phone number (10-15 digits).");
            return false;
        }
        return true;
    };

    const handleCheckout = async () => {
        if (!validateRecipientData()) {
            return;
        }
        try {
            // Convert each product price to a numeric value without separators
            const sanitizedProducts = products.map(product => ({
                ...product,
                price: typeof product.price === 'string'
                    ? parseFloat(product.price.replace(/\./g, ''))
                    : product.price,
            }));

            const response = await fetch(`${process.env.REACT_APP_API_URL}/api/create-checkout-session/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    products: sanitizedProducts,
                    recipient: recipientData  // Sending recipient data
                }),
            });

            const text = await response.text(); // Get raw response text
            console.log("Raw response:", text);

            const data = JSON.parse(text); // Try to parse JSON
            console.log("Parsed JSON:", data);

            if (!response.ok) {
                throw new Error(`Error: ${data.error || response.statusText}`);
            }

            // Redirect user to Stripe checkout page
            window.location.href = data.url;
        } catch (error) {
            console.error('Checkout error:', error);
        }
    };

    return (
        <button onClick={handleCheckout} className="checkout-button">
            Buy
        </button>
    );
};

export default CheckoutButton;
