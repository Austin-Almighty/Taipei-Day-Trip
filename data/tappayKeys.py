headers = {
        "Content-Type": "application/json",
        "x-api-key": "partner_NZRFRtYjwaKeiTcI2BHytBFT6FXrLBzQ27uBARm4hd5tECXuueWvaXbg"  
    }

payload = {
    # "prime": "e875c674851ab5a93191b0f8ed7d140f128a0aced84c6ce28486206b1c5b0e71",
    "partner_key": "partner_NZRFRtYjwaKeiTcI2BHytBFT6FXrLBzQ27uBARm4hd5tECXuueWvaXbg",
    "merchant_id": "tppf_tim479863_GP_POS_2",  
    "details": "TapPay Test",
    # "amount": 2000,
    "cardholder": {
        # "phone_number": "+886923456789",
        # "name": "王小明",
        # "email": "LittleMing@Wang.com"
    },
    "remember": False
}

tappay_URL = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"

