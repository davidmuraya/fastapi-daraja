from pydantic import BaseModel


class MpesaSandboxSettings(BaseModel):
    """
    Please consider storing these values in a secure location e.g. firestore
    """

    sandbox_url: str = "https://sandbox.safaricom.co.ke/"
    c2b_consumer_key: str = "wLs9wxNfPrda0fIy7MUjwWuRWW5xQ8N5"
    c2b_consumer_secret: str = "hQowLbqAnrNvQVOI"
    lipa_na_mpesa_consumer_key: str = "j0Nk3MmfUSiEpYSSavzXGSyO47pPeGZD"
    lipa_na_mpesa_consumer_secret: str = "kOCIt9T5pJ919L8m"
    lipa_na_mpesa_passkey: str = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    c2b_confirmation_url = ""
    c2b_validation_url = ""
    lipa_na_mpesa_callback_url = "https://demo.bima-mo.com/receipts/payment-confirmation?authorization_code=v&confirmation_code=c"
    lipa_na_mpesa_business_short_code = "503100"


class MpesaProductionSettings(BaseModel):
    production_url: str = "https://sandbox.safaricom.co.ke/"

