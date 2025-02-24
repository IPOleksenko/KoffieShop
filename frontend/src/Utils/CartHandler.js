class CartHandler {
    constructor() {
        // Load only id and quantity from localStorage
        this.cart = JSON.parse(localStorage.getItem('cart')) || [];
    }

    addToCart(product) {
        if (product.stock <= 0) return; // Product unavailable
        const existingItem = this.cart.find(item => item.id === product.id);
        if (existingItem) {
            if (existingItem.quantity < product.stock) {
                existingItem.quantity += 1;
            }
        } else {
            this.cart.push({ id: product.id, quantity: 1 });
        }
        this.saveCart();
        window.dispatchEvent(new Event('cartUpdated'));
    }

    // When updating the quantity, also pass stock for validation
    updateQuantity(productId, quantity, stock) {
        const cartItem = this.cart.find(item => item.id === productId);
        if (cartItem) {
            if (quantity < 1) {
                this.removeFromCart(productId);
                return;
            }
            // Do not allow quantity greater than available stock
            cartItem.quantity = Math.min(quantity, stock);
            this.saveCart();
            window.dispatchEvent(new Event('cartUpdated'));
        }
    }

    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.id !== productId);
        this.saveCart();
        window.dispatchEvent(new Event('cartUpdated'));
    }

    clearCart() {
        this.cart = [];
        this.saveCart();
        window.dispatchEvent(new Event('cartUpdated'));
    }

    // Return the "raw" cart with id and quantity
    getCart() {
        return this.cart;
    }

    // Synchronize the cart with the current product list:
    // if the product is not found or its stock is 0 – remove the product,
    // if the quantity exceeds the available amount – adjust it.
    syncCart(productList) {
        let updated = false;
        this.cart = this.cart.filter(cartItem => {
            const product = productList.find(p => p.id === cartItem.id);
            if (!product || product.stock <= 0) {
                updated = true;
                return false; // remove the product
            }
            if (cartItem.quantity > product.stock) {
                cartItem.quantity = product.stock;
                updated = true;
            }
            return true;
        });
        if (updated) {
            this.saveCart();
            window.dispatchEvent(new Event('cartUpdated'));
        }
    }

    // Calculate the total price using current product data
    getTotalPrice(productList) {
        return this.cart.reduce((total, item) => {
            const product = productList.find(p => p.id === item.id);
            return product ? total + product.price * item.quantity : total;
        }, 0);
    }

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
    }
}

export default new CartHandler();
