const bookingLogin = document.getElementById("login-book");
bookingLogin.addEventListener("click", startBooking);


function startBooking() {
    let token = localStorage.getItem("jwtToken");
    if (token) {
        window.location.href = "/booking";
    } else {
        showDialogue();
    }
}

