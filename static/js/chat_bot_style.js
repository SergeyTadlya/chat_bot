const chatBox = document.querySelector('.chat-box-wrapper');
const chatBoxButton = chatBox.querySelector('.chat-box-button');

chatBoxButton.addEventListener('click', () => {
    chatBox.classList.contains('active')
        ? chatBox.classList.remove('active')
        : chatBox.classList.add('active')
});

const fieldArea = chatBox.querySelector('.field__area');
const sendButton = chatBox.querySelector('.field__button');
fieldArea.addEventListener('keyup', (e) => {
    const values = fieldArea.value;

    if (values.length) {
        sendButton.classList.add('show');
    } else {
        sendButton.classList.remove('show');
    }
});

const cartBox = chatBox.querySelector('.chat-cart');
const cartShow = chatBox.querySelector('.cart-open__button');
const cartHide = chatBox.querySelector('.chat-cart__close');
const cartBuy = chatBox.querySelector('.cart-buy');
const chatField = chatBox.querySelector('.chat-box__field');

cartHide.addEventListener('click', () => {
    cartBox.classList.remove('active');
    cartBuy.classList.remove('show');
    chatField.classList.remove('hide');
});

cartShow.addEventListener('click', () => {
    cartBox.classList.add('active');
    cartBuy.classList.add('show');
    chatField.classList.add('hide');

    const allPurchase = cartBox.querySelectorAll('.chat-cart__purchase');
    allPurchase.forEach((Purchase) => {
        const addPurchase = Purchase.querySelector('.count--add');
        const removePurchase = Purchase.querySelector('.count--remove');
        const countPurchase = Purchase.querySelector('.purchase__price-field');
        const priceSum = Purchase.querySelector('.purchase__price-value');
        const priceOfPurchase = Purchase.querySelector('.purchase__price').dataset.price;
        const sumOfBuy = chatBox.querySelector('.price');
        const buttonsRemove = chatBox.querySelectorAll('.purchase__remove');

        sum()
        countThePrice()

        buttonsRemove.forEach((button) => {
            button.addEventListener('click', () => {
                button.closest('.chat-cart__purchase').remove();
                cartAjax("remove", button.closest('.chat-cart__purchase').id, "x");
                sum();
                countTotal();
            })
        })

        function sum() {
            let total = 0;

            const fields = cartBox.querySelectorAll('.purchase__price-value');

            fields.forEach((field) => {
                total = total + parseInt(field.innerText);
            })
            sumOfBuy.textContent = `${total} €`;
        }


        function countThePrice() {
            priceSum.textContent = `${priceOfPurchase * countPurchase.value}` + ' €';
            sum();
        }
        addPurchase.addEventListener('click', () => {
            countPurchase.value = parseInt(countPurchase.value) + 1;

            cartAjax(countPurchase.value, countPurchase.parentElement.parentElement.parentElement.id, "+")
            countThePrice()
            countTotal()
        })

        removePurchase.addEventListener('click', () => {
            parseInt(countPurchase.value) === 1
                ? Purchase.closest('.chat-cart__purchase').remove()
                : countPurchase.value = parseInt(countPurchase.value) - 1;

            cartAjax(countPurchase.value, countPurchase.parentElement.parentElement.parentElement.id, "-")
            countThePrice()
            countTotal()
        })

        function countTotal() {
            let countTotal = 0;
            const total = cartBox.querySelectorAll('.purchase__price-field');
            total.forEach((field) => {
                countTotal = countTotal + parseInt(field.value);
            })
            document.getElementById("cart-count").innerText = `${countTotal}`;
        }

        function cartAjax(service_count, service_id, functions){
            $.ajax({
                url: '/update_cart/',
                type: 'POST',
                data: {
                    'functions': functions,
                    'service_count': service_count,
                    'service_id': service_id,
                    'user_email': document.getElementById("saved-email").innerText,
                },
                success: function (data) {},
                error: function(error) {
                    console.log('ajax update cart', error);
                }
            });
        }
    })
});