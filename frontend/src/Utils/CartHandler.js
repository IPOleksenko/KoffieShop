class CartHandler {
    constructor() {
        this.cart = JSON.parse(localStorage.getItem('cart')) || [];
    }

    addToCart(product) {
        const existingProduct = this.cart.find(item => item.id === product.id);
        if (existingProduct) {
            existingProduct.quantity += 1;
        } else {
            this.cart.push({ ...product, quantity: 1 });
        }
        this.saveCart();
        window.dispatchEvent(new Event('cartUpdated'));
    }

    updateQuantity(productId, quantity) {
        const product = this.cart.find(item => item.id === productId);
        if (product) {
            product.quantity = Math.max(1, quantity);
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

    getCart() {
        return this.cart;
    }

    getTotalPrice() {
        return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
    }

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
    }
}

export default new CartHandler();