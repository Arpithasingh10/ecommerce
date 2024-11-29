// JS to Toggle Dropdown Menu in Navbar for User
document.querySelector('.dropdown-toggle').addEventListener('click', function() {
    const dropdownMenu = document.querySelector('.dropdown-menu');
    dropdownMenu.classList.toggle('show');
});

// Cart Update Example
function updateCart(item) {
    // This function will update the cart count dynamically, based on the number of items in the cart
    const cartCountElement = document.querySelector('.cart-count');
    const cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
    cartItems.push(item);
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    cartCountElement.textContent = cartItems.length;
}

// Adding event listener to cart button
document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', function() {
        const item = this.getAttribute('data-item');
        updateCart(item);
    });
});

// Toggle Cart Details
document.querySelector('.cart-link').addEventListener('click', function() {
    const cartDetails = document.querySelector('.cart-details');
    cartDetails.classList.toggle('show');
});
document.addEventListener('DOMContentLoaded', function() {
    const addressModal = document.getElementById('addressModal');
    const addressForm = document.getElementById('addressForm');
    const addAddressBtn = document.querySelector('.add-address');
    const closeModalBtn = document.querySelector('.close-modal');
    let currentAddressId = null;

    // Open modal for new address
    addAddressBtn.addEventListener('click', () => {
        currentAddressId = null;
        addressForm.reset();
        addressModal.style.display = 'flex';
    });

    // Close modal
    closeModalBtn.addEventListener('click', () => {
        addressModal.style.display = 'none';
    });

    // Handle edit address
    document.querySelectorAll('.edit-address').forEach(button => {
        button.addEventListener('click', (e) => {
            currentAddressId = e.target.dataset.id;
            // Here you would typically fetch the address data and populate the form
            addressModal.style.display = 'flex';
        });
    });

    // Handle delete address
    document.querySelectorAll('.delete-address').forEach(button => {
        button.addEventListener('click', (e) => {
            if (confirm('Are you sure you want to delete this address?')) {
                const addressId = e.target.dataset.id;
                // Here you would typically send a delete request to your backend
            }
        });
    });

    // Handle form submission
    addressForm.addEventListener('submit', (e) => {
        e.preventDefault();
        // Here you would typically send the form data to your backend
        addressModal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === addressModal) {
            addressModal.style.display = 'none';
        }
    });
});
