from pydantic import BaseModel


class MpesaSandboxSettings(BaseModel):
    sandbox_url: str = "https://sandbox.safaricom.co.ke/"
    consumer_key: str = "wLs9wxNfPrda0fIy7MUjwWuRWW5xQ8N5v"
    consumer_secret: str = "hQowLbqAnrNvQVOIb"
    basic: str = "d0xzOXd4TmZQcmRhMGZJeTdNVWp3V3VSV1c1eFE4TjU6aFFvd0xicUFuck52UVZPSQ=="


class MpesaProductionSettings(BaseModel):
    production_url: str = "https://sandbox.safaricom.co.ke/"

