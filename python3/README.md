# TOTP Authenticator in Python

* https://medium.freecodecamp.org/how-time-based-one-time-passwords-work-and-why-you-should-use-them-in-your-app-fdd2b9ed43c3
* https://tools.ietf.org/html/rfc4226
* https://tools.ietf.org/html/rfc6238
* https://github.com/google/google-authenticator/wiki/Key-Uri-Format
* https://security.stackexchange.com/questions/35157/how-does-google-authenticator-work
* https://github.com/robbiev/two-factor-auth/blob/master/main.go
* https://stefansundin.github.io/2fa-qr/ 


```bash
foo@bar:~$ virtualenv sandbox
foo@bar:~$ virtualenv -p $(which python3) sandbox
foo@bar:~$ source sandbox/bin/activate
foo@bar:~$ pip3 install --upgrade pip
foo@bar:~$ pip3 install -r requirements.txt 
foo@bar:~$ python ./pass.py qr.png
foo@bar:~$ deactivate
```
