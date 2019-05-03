#!/bin/python3
import fastzbarlight
from PIL import Image
import time
import hmac
import hashlib
import urllib.parse as urlparse
import base64

numberOfDigitsRequiredInOTP = 6
lifetimeOfOTPInSeconds = 30
print("OTP length:", numberOfDigitsRequiredInOTP)
print("OTP lifetime:", lifetimeOfOTPInSeconds)

qr_code = fastzbarlight.scan_codes('qrcode', Image.open("./qr.png"))
qr_code = str(qr_code[0].decode())
print("QR code:", qr_code)

parsed = urlparse.urlparse(qr_code)
secret = urlparse.parse_qs(parsed.query)["secret"][0]
print("secret:", secret)
secret = base64.b32decode(secret)

currentUnixTime = int(time.time())
print("Unix time:", currentUnixTime)

counter = currentUnixTime // lifetimeOfOTPInSeconds
print("Counter:", counter)
counter = counter.to_bytes(8, byteorder = 'big')

hash = hmac.new(secret, counter, hashlib.sha1)
digest = hash.digest()
print("HMAC Digest", hash.hexdigest())

offset = digest[19] & 0xf # last nibble operations
print("offset:", offset)
truncatedHash = (digest[offset] & 0x7f) << 24 | (digest[offset+1] & 0xff) << 16 | (digest[offset+2] & 0xff) << 8 | (digest[offset+3] & 0xff)
print("truncatedHash:", hex(truncatedHash))
finalOTP = (truncatedHash % (10 ** numberOfDigitsRequiredInOTP))
print("finalOTP:", finalOTP)


