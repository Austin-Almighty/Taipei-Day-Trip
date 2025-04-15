document.addEventListener("DOMContentLoaded", () => {
  TPDirect.setupSDK(
    159797,
    "app_sggHj2NhOh8W2VjiAlAaRUYXYJFEL84xUjIG6lucWcIcxOyFCecWliSF8sSW",
    "sandbox"
  );

  TPDirect.card.setup({
    fields: {
      number: {
        element: "#card-number",
        placeholder: "**** **** **** ****",
      },
      expirationDate: {
        element: "#card-expiration-date",
        placeholder: "MM / YY",
      },
      ccv: {
        element: "#card-ccv",
        placeholder: "CCV",
      },
    },

    styles: {
      input: {
        color: "gray",
        "font-family": "Noto Sans TC",
        "font-weight": 500,
        "font-size": "16px",
        "line-height": "13.3px",
      },

      // style focus state
      ":focus": {
        color: "black",
      },
      // style valid state
      ".valid": {
        color: "green",
      },
      // style invalid state
      ".invalid": {
        color: "red",
      },
      // Media queries
      // Note that these apply to the iframe, not the root window.
      "@media screen and (max-width: 400px)": {
        input: {
          color: "orange",
        },
      },
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
      beginIndex: 6,
      endIndex: 11,
    },
  });

  TPDirect.card.onUpdate((update) => {
    const paymentBtn = document.getElementById("paymentBtn");
    if (update.canGetPrime) {
      paymentBtn.removeAttribute("disabled");
    } else {
      paymentBtn.setAttribute("disabled", true);
    }

    updateFieldStatus("card-number", update.status.number);
    updateFieldStatus("card-expiration-date", update.status.expiry);
    updateFieldStatus("card-ccv", update.status.ccv);
  });

  function updateFieldStatus(fieldId, status) {
    const field = document.getElementById(fieldId);
    field.classList.remove("valid", "invalid");

    if (status === 0) {
      field.classList.remove("valid", "invalid");
      field.classList.add("valid");
    } else if (status === 2) {
      field.classList.remove("valid", "invalid");
      field.classList.add("invalid");
    } else {
      field.classList.remove("valid", "invalid");
    }
  }
});

const paymentBtn = document.getElementById('paymentBtn');
paymentBtn.addEventListener("click", sendPrime);

function sendPrime() {
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('連線失敗')
        return
    }
    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }
        alert('get prime 成功，prime: ' + result.card.prime)

        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })

}
