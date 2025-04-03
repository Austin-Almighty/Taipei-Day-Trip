window.addEventListener("DOMContentLoaded", checkStatus);


async function checkStatus(){
    let token = localStorage.getItem("jwtToken");
    if (!token){
        showLogin();
        return;
    }
    let response = await fetch("/api/user/auth", {
        method: "GET",
        headers: {
            "Content-type": "application/json",
            "Authorization": `Bearer ${token}`
        },
    });
    if (response.ok){
        let data = await response.json();
        if (data){
            showLogout();
        } else {
            showLogin();
        }
    } else {
        showLogin();
    }
}


function showLogin(){
    const login = document.getElementById("signout");
    login.textContent = "登入/註冊";
    login.id = "login-register";
}

function showLogout(){
    const login = document.getElementById("login-register");
    login.textContent = "登出系統";
    login.id = "signout";
    login.addEventListener("click", logoutUser);
}

function logoutUser(){
    localStorage.clear();
    setTimeout(() => {
        window.location.reload();
      }, 100);
}


