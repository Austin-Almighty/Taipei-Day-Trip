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
            localStorage.setItem("booking", JSON.stringify(data));
        } else {
            const footer = document.querySelector("footer");
            footer.classList.toggle("highfooter");

            const userName = document.getElementById('userName');
            userName.innerText = localStorage.getItem('userName');

            const booking = document.getElementById("booking");
            const noBooking = document.createElement('p');
            noBooking.innerText = "目前沒有任何待預訂的行程";
            booking.appendChild(noBooking);
        }
    }
}

function renderBooking(data) {
    const userName = document.getElementById('userName');
    userName.innerText = localStorage.getItem('userName');

    let imageURL = data.data.attraction.images;

    const mainImage = document.getElementById("mainImage");
    mainImage.src = imageURL;
    const attractionName = document.getElementById('attractionName');
    attractionName.innerText = data.data.attraction.name;

    const bookingDate = document.getElementById("bookingDate");
    bookingDate.innerText = data.data.date;

    const bookingTime = document.getElementById("bookingTime");
    bookingTime.innerText = (data.data.time === "morning") ? "早上9點到下午4點" : "下午2點到晚上9點";

    const tourCost = document.getElementById('tourCost');
    tourCost.innerText = data.data.price;

    const address = document.getElementById("address");
    address.innerText = data.data.attraction.address;

    const finalPrice = document.getElementById("finalPrice");
    finalPrice.innerText = data.data.price;

    const hiddenElements = document.querySelectorAll(".hidden");
    hiddenElements.forEach(el => el.classList.remove("hidden"));
}

const deleteBtn = document.getElementById("deleteBtn");
deleteBtn.addEventListener('click', deleteBooking);

async function deleteBooking() {
    let token = localStorage.getItem("jwtToken");
    let response = await fetch("/api/booking", {
        method: "DELETE",
        headers: {
            "Content-type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        let data = await response.json();
        console.log(data.error);
        alert("刪除失敗");
    } else {
        window.location.reload();
    }
}