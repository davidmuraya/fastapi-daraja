from pydantic import BaseModel


class MpesaSandboxSettings(BaseModel):
    """
    Please consider storing these values in a secure location e.g. firestore
    """

    sandbox_url: str = "https://sandbox.safaricom.co.ke/"
    consumer_key: str = "wLs9wxNfPrda0fIy7MUjwWuRWW5xQ8N5v"
    consumer_secret: str = "hQowLbqAnrNvQVOIb"


class MpesaProductionSettings(BaseModel):
    production_url: str = "https://sandbox.safaricom.co.ke/"

