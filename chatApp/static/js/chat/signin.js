"use strict";
const errorList = document.querySelector(".errorlist ")
const btnLogin = document.querySelector(".btn-login");
const form = document.querySelector("form");

form.addEventListener("submit", function (e) {

    Toastify({
        text: "Authentification en cours ",
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        // Prevents dismissing of toast on hover
        style: {
            background: "#fcc419",
            color: "white"
        },
        onClick: function () { } // Callback after click
    }).showToast();
})

if (errorList) {
    const message = errorList.textContent;
    errorList.style.display = "none";
    Toastify({
        text: message,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        stopOnFocus: true,
        duration: 5000, // Prevents dismissing of toast on hover
        style: {
            background: "red",
            color: "white"
        },
        onClick: function () { } // Callback after click
    }).showToast();
}