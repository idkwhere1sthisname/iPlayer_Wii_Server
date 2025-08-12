# iPlayer_Wii_Server
Custom server for the BBC iPlayer for the Wii

# Setup

Install the requirements by running

```cmd
pip install -r requirements.txt
```

Then run

```cmd
py server.py
```

# Certificates

To create a compatible cert, use these commands, you must have OpenSSL installed

```bash
# Certificate Authority (CA)
openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.pem -days 3650 -nodes -subj "/CN=idkPlayer/O=idkPlayer"
openssl x509 -outform der -in ca.pem -out ca.der

# Server Certificate
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr
openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256
openssl x509 -in server.crt -out server.pem -outform PEM

# Certificate for 000000002.app (unfortunately insecure, RSA:1024+md5)
openssl genrsa -out GTEGI.key 1024
openssl req -new -key GTEGI.key -out GTEGI.csr -subj "/C=IT/O=idkPlayer/CN=127.0.0.1"
openssl x509 -req -in GTEGI.csr -CA ca.pem -CAkey ca.key -set_serial 0x01A5 -out GTEGI.pem -days 3650 -md5
openssl x509 -req -in client.csr -CA ca.pem -CAkey ca.key -set_serial 0x01A5 -out GTEGI.cer -days 3650 -md5
```

**Be sure to disable Verify Certificates on Dolphin!**

**DOES NOT WORK ON REAL HARDWARE YET!**

# Credits

idkwh: Server and Patching

YourTooSlow: WiiiPlayer.swf recreation