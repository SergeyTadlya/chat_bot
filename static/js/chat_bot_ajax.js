// START email authorization
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.has('email')) {
    const email = urlParams.get('email');
    EmailAjax(email);
}
if(document.getElementById('user-auth').hidden == false){
    document.getElementsByClassName('added-email')[0].style = "display: none";
    document.getElementsByClassName('chat-box__field')[0].style = "display: none";
    document.getElementsByClassName('cart-open')[0].style = "display: none";

    $("#user-auth-form").submit(function (event) {
        event.preventDefault();
        const email = $("#user-email").val();
        EmailAjax(email);
    });
}
var ChatID;
function EmailAjax(email) {
    $.ajax({
        url: '/send_email/',
        type: 'POST',
        data: {
            'email': email,
        },
        success: function (data) {
            if(data.is_valid == true) {
                ChatID = data.chat_id;
                WebSocketConnect(ChatID);
                document.getElementsByClassName('added-email')[0].innerHTML = data.email_block;
                document.getElementsByClassName('added-email')[0].style = "";
                document.getElementsByClassName('chat-box__field')[0].style = "";
                document.getElementsByClassName('cart-open')[0].style = "";
                document.getElementById('user-auth').style = "display: none";
                document.getElementById('cart-count').innerText = data.quantity_service_in_cart;
                if (data.services_in_cart != "") {
                    $('#chat-cart-content').append(data.services_in_cart);
                }
                preloader();
                setTimeout(function () {
                    $('#preloader').hide();
                    $('#preloader').remove();
                    if (data.message_history != "") {
                        $('#chat-box-content').append(data.message_history);
                    }
                    if (data.first_message_block != "") {
                        $('#chat-box-content').append(data.first_message_block);
                    }
                }, 2000);
            }else{
                document.getElementById('not_valid_email').style = "display: block";
            }
        },
        error: function(error) {
            console.log('ajax email', error);
        }
    });
}
// END email authorization

// START send message in chat
// send ajax using "enter" keydown
$("#new-user-message-form").keydown(function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      sendMessage();
    }
});
// send ajax using button click
$("#send-user-message").click(function(event) {
    event.preventDefault();
    sendMessage();
});
// ajax function
var chat_socket;
function sendMessage() {
    console.log(chat_socket);
    $.ajax({
        url: '/send_user_message/',
        type: 'POST',
        data: {
            'user_message': $("#new-user-message").val(),
            'user_email': document.getElementById("saved-email").innerText,
        },
        success: function (data) {
            // clear message in textarea
            document.getElementById('new-user-message').value = '';
            // add user message in chat
            if(data.user_message_text != ""){
                $('#chat-box-content').append(data.user_message_block);
                if(data.type == "manager") {
                    // send message from websocket
                    chat_socket.send(JSON.stringify({
                        message: data.user_message_text,
                        username: data.username,
                        sender: "client",
                        message_block: "message_block",
                    }));
                }
            }
            if(data.message_text != ""){
                // preloader before bot or manager answer
                preloader();
                // add bot or manager answer in chat
                setTimeout(function(){
                    $('#preloader').hide();
                    $('#preloader').remove();
                    $('#chat-box-content').append(data.message_block);
                }, 2000);
            }
        },
        error: function(error) {
            console.log('ajax send message', error);
        }
    });
}
// preloader
function preloader(){
    const ul = document.createElement("ul");
    ul.setAttribute("class", "messages__list");
    ul.id = "preloader";

    const li = document.createElement("li");
    li.setAttribute("class", "messages__item");
    ul.append(li);

    const p = document.createElement("p");
    p.setAttribute("class", "message");
    li.append(p);

    const span = document.createElement("span");
    span.innerText = "...";
    span.id = "loading";
    p.append(span);

    $('#chat-box-content').append(ul);
    $('#preloader').show();
}
// END send message in chat

// START cart
var cart_count = 0; // if cart is empty
function AddToCart(service_id){
    // cart_count++;
    // document.getElementById('cart-count').innerText = cart_count;
    $.ajax({
        url: '/add_service_to_cart/',
        type: 'POST',
        data: {
            'service_id': service_id,
            'user_email': document.getElementById("saved-email").innerText,
        },
        success: function (data) {
            const added_service = document.getElementById(data.added_service_id);
            if (added_service !== null) {
                added_service.remove();
            }
            $('#chat-cart-content').append(data.added_service_block);

            // change quantity
            let total = 0;
            const chat_cart = document.querySelector('#chat-cart-content');
            const quantity = chat_cart.querySelectorAll('.purchase__price-field');
            quantity.forEach((field) => {
                total = total + parseInt(field.value);
            })
            document.getElementById("cart-count").innerText = `${total}`;
        },
        error: function(error) {
            console.log('ajax add to cart', error);
        }
    });
}
// END cart

// START buy from Stripe
document.getElementsByClassName('button--buy')[0].addEventListener('click', () => {
    // get added services in cart
    const ServiceData = [];
    const allServices = document.getElementById("chat-cart-content").querySelectorAll('.chat-cart__purchase');
    allServices.forEach((Service) => {
        ServiceData.push({
            'id': Service.id,
            'name': Service.firstElementChild.innerText,
            'price': Service.lastElementChild.dataset.price * 100,
            'quantity': Service.lastElementChild.firstElementChild.firstElementChild.nextElementSibling.value,
        })
    });
    const data = {
        'services': JSON.stringify(ServiceData),
        'total_price': document.getElementsByClassName("price")[0].innerText,
        'user_email': document.getElementById("saved-email").innerText,
    }

    // generate stripe url for pay
    $.ajax({
        url: '/stripe_pay/',
        type: 'POST',
        data: data,
        success: function (data) {
            const stripe = Stripe(data.public_key);
            return stripe.redirectToCheckout({ sessionId: data.session_id });
        },
        error: function(error) {
            console.log('ajax add to cart', error);
        }
    });
});
// END buy from Stripe