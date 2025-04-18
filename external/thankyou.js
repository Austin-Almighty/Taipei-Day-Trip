
document.addEventListener("DOMContentLoaded", checkSignin)
document.addEventListener("DOMContentLoaded", ()=>{fetchOrder(showOrder)})

function fetchOrder(callback) {
    const query = new URLSearchParams(window.location.search);
    let number = query.get('number');
    const orderID = document.getElementById("orderID");
    orderID.textContent = number;
    callback(number)
}

async function showOrder (referenceID) {
    let response = await fetch(`/api/order/${referenceID}`,{
        method: "GET",
        headers: {
            "Content-type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("jwtToken")}`
        }
    });
    const success = document.getElementById("success");
    const orderID = document.getElementById('orderID');
    const orderMessage = document.getElementById('orderMessage');
    const bookingSection = document.getElementById('booking');
    const footer = document.querySelector("footer");
    if (response.ok) {
        let data = await response.json();
        if (!data) {
            success.textContent = "查無此行程";
            orderID.textContent = referenceID;
            orderMessage.textContent = "請再次確認您的行程編號";
            
        } else if (!data.status) {
            success.textContent = "付款尚未成功，可用下列編號查詢";
            orderID.textContent = referenceID;
            orderMessage.textContent = "請完成付款，以確保您的行程";
            renderBooking(data);
            bookingSection.classList.remove("hidden")
            footer.classList.remove("highfooter");
        } else {
            success.textContent = "行程預定成功"
            orderID.textContent = referenceID;
            renderBooking(data);
            bookingSection.classList.remove("hidden");
            footer.classList.remove("highfooter");
        }
    }

}

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
        if (!data) {
            window.location.href = "/";
        }
    }
}

function renderBooking(data) {
    // const userName = document.getElementById('userName');
    // userName.innerText = localStorage.getItem('userName');

    let imageURL = data.data.trip.attraction.images;
    console.log(imageURL)

    const mainImage = document.getElementById("mainImage");
    mainImage.src = imageURL;
    const attractionName = document.getElementById('attractionName');
    attractionName.innerText = data.data.trip.attraction.name;

    const bookingDate = document.getElementById("bookingDate");
    bookingDate.innerText = data.data.trip.date;

    const bookingTime = document.getElementById("bookingTime");
    bookingTime.innerText = (data.data.time === "morning") ? "早上9點到下午4點" : "下午2點到晚上9點";


    const address = document.getElementById("address");
    address.innerText = data.data.trip.attraction.address;

  

    // const hiddenElements = document.querySelectorAll(".hidden");
    // hiddenElements.forEach(el => el.classList.remove("hidden"));
}