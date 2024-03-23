# FlaskAPI_for_Dating

This is back-end code, separate from "Dating" project.

"Dating" project fork from https://github.com/CHUNG-HAO/Dating

### SSL GET commands

This is the method of create the SSL certificate for testing:

* Step1: Build the ssl.conf in your project

* Step2: Run this command to build the server.key and server.crt
```
openssl req -x509 -new -nodes -sha256 -utf8 -days 3650 -newkey rsa:2048 -keyout server.key -out server.crt -config ssl.conf
```
* Step3: Run this command to build the server.pfx
```
openssl pkcs12 -export -in server.crt -inkey server.key -out server.pfx
```

* Step4: Run this command by system administer in powershell
```
certutil -addstore -f "ROOT" server.crt
```
Now you can transfer the URL http to https in your test browser for a few minutes.

### RF

> 1. https://medium.com/@charming_rust_oyster_221/flask-%E9%85%8D%E7%BD%AE-https-%E7%B6%B2%E7%AB%99-ssl-%E5%AE%89%E5%85%A8%E8%AA%8D%E8%AD%89-36dfeb609fa8

> 2. https://blog.miniasp.com/post/2019/02/25/Creating-Self-signed-Certificate-using-OpenSSL

> 3. https://hackmd.io/@bessyhuang/Bk2ZnTFwV#%E7%94%A8Flask-Mail%E4%BE%86%E6%94%AF%E6%8F%B4email

> 4. https://www.freecodecamp.org/news/setup-email-verification-in-flask-app/

> 5. https://github.com/ashutoshkrris/Flask-User-Authentication-With-Email-Verification

> 6. https://itsdangerous.palletsprojects.com/en/2.1.x/

> 7. https://blog.csdn.net/Lin_Hv/article/details/105119396

> 8. https://github.com/wobin1/flask-login-for-flutter/tree/master