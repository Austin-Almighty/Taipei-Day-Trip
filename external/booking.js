window.addEventListener("DOMContentLoaded", checkSignin)


async function checkSignin() {
    let token = localStorage.getItem("jwtToken");
    let response = await fetch("/api/user/auth", {
        method: "GET",
        headers: {
            "Content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
    });
    if (response.ok) {
        let data = await response.json();
        if (data) {
            getBooking(token);
        } else {
            window.location.href = "/";
        }
    }
}

async function getBooking(token) {
    let response = await fetch("/api/booking", {
        method: "GET",
        headers: {
            "Content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
    });
    if (response.ok) {
        let data = await response.json();
        if (data) {
            renderBooking(data);
        } else {
            const footer = document.querySelector("footer");
            footer.classList.toggle("highfooter");

            const booking = document.getElementById("booking");
            const noBooking = document.createElement('p');
            noBooking.innerText = "目前沒有任何待預訂的行程";
            booking.appendChild(noBooking);
        }
    }
}

function renderBooking(data) {
    let imageURL = data.data.attraction.images;

    const mainImage = document.getElementById("mainImage");
    mainImage.src = imageURL;
    const attractionName = document.getElementById('attractionName');
    attractionName.innerText = data.data.attraction.name;

    const bookingDate = document.getElementById("bookingDate");
    bookingDate.innerText = data.data.date;

    const bookingTime = document.getElementById("bookingTime");
    bookingTime.innerText = data.data.time;

    const tourCost = document.getElementById('tourCost');
    tourCost.innerText = data.data.price;

    const address = document.getElementById("address");
    address.innerText = data.data.attraction.name;

    // const infographicDiv = document.createElement("div");
    // infographicDiv.classList.remove("hidden");

    // const hr = document.querySelectorAll("hr");
    // hr.classList.remove("hidden");

    // const contact = document.getElementById("contact");
    // contact.classList.remove("hidden");

    // const payment = document.getElementById('payment');
    // payment.classList.remove('hidden');

    const finalPrice = document.getElementById("finalPrice");
    finalPrice.innerText = data.data.price;

    const hiddenElements = document.querySelectorAll(".hidden");
    hiddenElements.classList.remove("hidden");
}