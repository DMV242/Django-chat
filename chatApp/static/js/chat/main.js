"use strict";

const roomName = document.querySelector(".room_name").textContent;
const username = document.querySelector(".username").textContent;
const messageContainer = document.querySelector("#messages");
const messageInputDom = document.querySelector('#message');
const ImageInputDom = document.querySelector('#photo');
const photoForm = document.querySelector('#send-photo-form');



const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);



chatSocket.onmessage = function (e) {


    const data = JSON.parse(e.data);
    let html;
    if (username === data.user) {

        if (data.type !== "chat.image") {
            html = `
            <div class="user-message">
              <div class="chat">
            <div class="chat_info">
                <div class="contact_name">Vous </div>
                <div class="contact_msg">${data.message}</div>
            </div>
            <div class="chat_status">
                <div class="chat_date">${data.time}</div>
            </div>
        </div>
        </div>
        `
        } else {
            html = ` <div class="user-message"><img src="${data.image}" /> </div>`
        }



        messageContainer.insertAdjacentHTML("beforeend", html)
        messageContainer.scrollBy({
            behavior: "smooth",
            top: 9999

        });
    } else {
        Toastify({
            text: "Vous avez 1 nouveau message ",
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "left", // `left`, `center` or `right`
            // Prevents dismissing of toast on hover
            style: {
                background: "green",
                color: "white"
            },
            onClick: function () { } // Callback after click
        }).showToast();
        if (data.type !== "chat.image") {
            html = `
            <div class="other-message">
              <div class="chat">
            <div class="chat_info">
                <div class="contact_name">${data.user} </div>
                <div class="contact_msg">${data.message}</div>
            </div>
            <div class="chat_status">
                <div class="chat_date">${data.time}</div>
            </div>
        </div>
        </div>
        `
        } else {
            html = `
            <div class="other-message">
            <img src="${data.image}" />
            </div>`
        }

        messageContainer.insertAdjacentHTML("beforeend", html)
    }
    messageContainer.scrollBy({
        behavior: "smooth",
        top: 9999
    });

};


chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#message').focus();
document.querySelector('#message').onkeyup = function (e) {
    if (e.key === 'Enter') {
        document.querySelector('#chat-submit').click();
    }
};

document.querySelector('#chat-submit').onclick = function (e) {

    const file = ImageInputDom.files[0];
    const message = messageInputDom.value;
    const reader = new FileReader();
    reader.onload = function (event) {
        const imageData = event.target.result;
        console.log(file.name)
        chatSocket.send(JSON.stringify({ 'image': imageData, 'name': file.name }));

    };

    if (!message && !file) {
        alert("Vous devez saisir un message ou envoyer une image");
        resetfields();
        return;
    }
    if (file && !message) {
        reader.readAsDataURL(file);
        resetfields();
        return;
    }
    if (file && message) {
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        reader.readAsDataURL(file);
        resetfields();
        return;
    }

    chatSocket.send(JSON.stringify({
        'message': message
    }));
    resetfields();


};

function resetfields() {
    messageInputDom.value = '';
    photoForm.reset();
}



