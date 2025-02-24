import React from 'react';

const CheckoutButton = ({ products }) => {
    const handleCheckout = async () => {
        try {
            // Transform each product so that the price becomes a number without dot separators
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
                body: JSON.stringify({ products: sanitizedProducts }),
            });

            const text = await response.text(); // Get the raw response text
            console.log("Raw response:", text);

            const data = JSON.parse(text); // Try to parse JSON
            console.log("Parsed JSON:", data);

            if (!response.ok) {
                throw new Error(`Error: ${data.error || response.statusText}`);
            }

            // Redirect the user to the Stripe payment page
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
