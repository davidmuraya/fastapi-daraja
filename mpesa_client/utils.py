import base64
from pydantic import BaseModel

# used for encrypting the request sent: A base64 encoded string.
# (The base64 string is a combination of Shortcode+Passkey+Timestamp)


def base64encoder(string_to_encode: str):

    string_to_encode_bytes = string_to_encode.encode("ascii")
    base64_bytes = base64.b64encode(string_to_encode_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string

