import base64
import re


def base64encoder(string_to_encode: str) -> str:
    # used for encrypting the request sent: A base64 encoded string.
    # (The base64 string is a combination of Shortcode+Passkey+Timestamp)

    string_to_encode_bytes = string_to_encode.encode("ascii")
    base64_bytes = base64.b64encode(string_to_encode_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def validate_phone_number(phone_number: str) -> bool:
    """Validate phone number"""
    pattern = r"^(?:254|\+254|0)?((?:(?:7(?:(?:[01249][0-9])|(?:5[789])|(?:6[89])))|(?:1(?:[1][0-5])))[0-9]{6})$"
    if re.match(pattern, phone_number):
        return True

    return False


def format_phone_number(phone_number: str) -> str:
    """Format phone number"""
    if phone_number.startswith("+"):
        return phone_number.strip("+")
    if phone_number.startswith("0"):
        return phone_number.replace("0", "254", 1)

    return phone_number
