const bookingBtn = document.getElementById("login-book");
bookingBtn.addEventListener("click", startBooking);


function startBooking() {
    let token = localStorage.getItem("jwtToken");
    if (token) {
        window.location.href = "/booking";
    } else {
        showDialogue();
    }
}

