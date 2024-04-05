
const successList = document.querySelector("li.success");
const btnLogin = document.querySelector(".btn-login");
const form = document.querySelector("form");
const errorList = document.querySelector(".errorlist");



if (successList) {
    const message = successList.textContent;

    Toastify({
        text: message,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        // Prevents dismissing of toast on hover
        style: {
            background: "green",
            color: "white"
        },

    }).showToast();
}

form.addEventListener("submit", function (e) {

    Toastify({
        text: "création de compte en cours ",
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "left", // `left`, `center` or `right`
        // Prevents dismissing of toast on hover
        style: {
            background: "#fcc419",
            color: "white"
        },

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

    }).showToast();
}

