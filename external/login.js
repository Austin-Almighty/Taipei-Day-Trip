function showDialogue() {
  const dialogue = document.getElementById("login-dialogue");
  dialogue.showModal();
}

function closeDialogue() {
  const dialogue = document.getElementById("login-dialogue");
  dialogue.close();
  const existingError = document.querySelector("#login-dialogue p.error");
  if (existingError) existingError.remove();
}

const register = document.querySelector("#login-register");
register.addEventListener("click", showDialogue);

const closeDialog = document.querySelector("dialog img");
closeDialog.addEventListener("click", closeDialogue);

function sendCredentials() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  return [email, password];
}

async function loginAttempt(callback) {
  let credentials = callback();
  let response = await fetch("/api/user/auth", {
    method: "PUT",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify({
      email: credentials[0],
      password: credentials[1],
    }),
  });
  if (response.ok) {
    let data = await response.json();
    localStorage.setItem("jwtToken", data.token);
    closeDialogue();
    setTimeout(() => {
        window.location.reload();
      }, 100);
  } else {
    let data = await response.json();
    let errorMessage = data.message;
    const existingError = document.querySelector("#login-dialogue p.error");
    if (existingError) existingError.remove();
    const displayError = document.createElement("p");
    displayError.textContent = errorMessage;
    displayError.style.color = "red";
    displayError.classList.add("error");
    const prompt = document.querySelector("#login-dialogue p");
    prompt.insertAdjacentElement("afterend", displayError);
  }
}

function newCredentials(){
    const newUser = document.getElementById("newName").value.trim();
    const newEmail = document.getElementById("newEmail").value.trim();
    const newPassword = document.getElementById("newPassword").value.trim();
    return [newUser, newEmail, newPassword]
}


async function registerNewUser(callback){
    let credentials = callback();
    let response = await fetch("/api/user", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            name: credentials[0],
            email: credentials[1],
            password: credentials[2],
        })
    });
    if (response.ok){
        const successMessage = "註冊成功";
        const currentMessage = document.querySelector("#signup-dialog p.success");
        if (currentMessage) currentMessage.remove();
        const displaySuccess = document.createElement("p");
        displaySuccess.textContent = successMessage;
        displaySuccess.style.color = "green";
        displaySuccess.classList.add("success");
        const prompt = document.querySelector("#signup-dialog p");
        prompt.insertAdjacentElement("afterend", displaySuccess);
    } else {
        let data = await response.json();
        let errorMessage = data.message;
        const existingError = document.querySelector("#signup-dialog p.error");
        if (existingError) existingError.remove();
        const displayError = document.createElement("p");
        displayError.textContent = errorMessage;
        displayError.style.color = "red";
        displayError.classList.add("error");
        const prompt = document.querySelector("#signup-dialog p");
        prompt.insertAdjacentElement("afterend", displayError);
    }
}

const loginButton = document.querySelector("#login-dialogue button");
loginButton.addEventListener("click", (event) => {
  event.preventDefault();
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  if (!emailInput.value || !passwordInput.value){
    alert("請輸入電子信箱和密碼");
  } else {
    loginAttempt(sendCredentials);
  }
});

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

emailInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    loginAttempt(sendCredentials);
  }
});

passwordInput.addEventListener("keydown", (e)=>{
    if (e.key === "Enter") {
        e.preventDefault();
        loginAttempt(sendCredentials);
    }
})

const registerBtn = document.querySelector("#signup-dialog button");
registerBtn.addEventListener("click", (e)=>{
    e.preventDefault();
    const newName = document.getElementById("newName");
    const newEmail = document.getElementById("newEmail");
    const newPassword = document.getElementById("newPassword");
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!newName.value||!newEmail.value||!newPassword.value){
        alert("請輸入姓名、電子郵件、密碼");
    } else if (!emailPattern.test(newEmail.value.trim())){
      alert("請輸入有效的電子郵件地址");
    } else {
        registerNewUser(newCredentials);
    }
})

function showRegister(){
    const signup = document.getElementById("signup-dialog");
    signup.showModal();
}

function closeRegister(){
    const signup = document.getElementById("signup-dialog");
    signup.close();
}

const closeRegisterBtn = document.querySelector("#signup-dialog img");
closeRegisterBtn.addEventListener('click', closeRegister);

const moveToRegister = document.getElementById("moveToRegister");
moveToRegister.addEventListener('click', ()=>{
    closeDialogue();
    showRegister();
})

const moveToLogin = document.getElementById("moveToLogin");
moveToLogin.addEventListener('click', ()=>{
    closeRegister();
    showDialogue();
})
