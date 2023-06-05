import app
import logging
from typing import Optional, List

from datetime import datetime
import pandas as pd
import json

from fastapi import APIRouter

from fastapi import Depends, Response, status, HTTPException
from pydantic import BaseModel


class MpesaSandboxSettings(BaseModel):
    sandbox_url: str = "https://sandbox.safaricom.co.ke/"
    consumer_key: str = "wLs9wxNfPrda0fIy7MUjwWuRWW5xQ8N5"
    consumer_secret: str = "hQowLbqAnrNvQVOI"
    basic: str = "d0xzOXd4TmZQcmRhMGZJeTdNVWp3V3VSV1c1eFE4TjU6aFFvd0xicUFuck52UVZPSQ=="


class MpesaProductionSettings(BaseModel):
    production_url: str = "https://sandbox.safaricom.co.ke/"

