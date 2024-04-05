"use strict";

const roomName = document.querySelector(".room_name").textContent;
const username = document.querySelector(".username").textContent;
const messageContainer = document.querySelector("#messages");




const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);



chatSocket.onmessage = function (e) {

    const data = JSON.parse(e.data);
    if (username === data.user) {
        messageContainer.insertAdjacentHTML("beforeend", `
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
    `)
        messageContainer.scrollBy({
            behavior: "smooth",
            top: 9999

        });
    } else {
        messageContainer.insertAdjacentHTML("beforeend", `
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
    `)
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
    const messageInputDom = document.querySelector('#message');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};


// TOAST

