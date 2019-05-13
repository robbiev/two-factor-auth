#!/bin/python3
import fastzbarlight
from PIL import Image
import time
import hmac
import hashlib
import urllib.parse as urlparse
import base64
import sys

if len(sys.argv) < 2:
    print("Usage: python3 " + sys.argv[0] + " qr-code.png")
    sys.exit(-1)

qr_code = fastzbarlight.scan_codes('qrcode', Image.open(sys.argv[1]))
qr_code = str(qr_code[0].decode())
print("QR code:", qr_code)

secret = None
digits = 6
period = 30
algo = hashlib.sha1
parsed = urlparse.urlparse(qr_code)
qs = urlparse.parse_qs(parsed.query)
for k,v in qs.items():
    if k == "secret":
        secret = v[0]
    if k == "digits":
        digits = int(v[0])
    if k == "period":
        period = int(v[0])
    if k == "algorithm":
        algo = getattr(hashlib, v[0].lower())
print("secret:", secret)
print("OTP length:", digits)
print("OTP lifetime:", period)

secret = base64.b32decode(secret)

currentUnixTime = int(time.time())
print("Unix time:", currentUnixTime)

counter = currentUnixTime // period
print("Counter:", counter)
counter = counter.to_bytes(8, byteorder = 'big')

hash = hmac.new(secret, counter, algo)
digest = hash.digest()
print("HMAC Digest", hash.hexdigest())

offset = digest[19] & 0xf # last nibble operations
print("offset:", offset)
truncatedHash = (digest[offset] & 0x7f) << 24 | (digest[offset+1] & 0xff) << 16 | (digest[offset+2] & 0xff) << 8 | (digest[offset+3] & 0xff)
print("truncatedHash:", hex(truncatedHash))
finalOTP = (truncatedHash % (10 ** digits))
print("finalOTP:", finalOTP)


