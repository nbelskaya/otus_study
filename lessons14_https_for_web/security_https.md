# Этап подготовки
Выпустила самоподписной сертификат, потому как домена нет, командой:
```console
openssl s_client -connect 178.154.224.92:443 -servername 178.154.224.92 -tls1_2 
```
Основные параметры HTTPS, оптимизация сессий, HTTP -> HTTPS redirect - остался с прошлого ДЗ.
HSTS - HTTP Strict Transport Security - заголовок для поведения браузера также был ранее добавлен в конфиг файл.
Ограничилась включением HTTP/2, этого достаточно для большенства ресурсов. В процессе первого тестирования обнаружила, что не работает ALPN.
В ответе было No ALPN negotiated. Исправила строку в блоке listen.

# Результаты проверки TLS (openssl s_client)
1. Сертификат загружается корректно
2. Используется самоподписной сертификат
3. Соединение устанавливается по протоколу TLS 1.3
4. Применяется современный безопасный шифр (AES‑GCM)
5. Безопасный обмен ключами — X25519
6. ALPN согласован, включена поддержка HTTP/2 
7. Session resumption работает — сервер выдаёт session tickets
```console
root@docker-wordpress:~# curl -I -k --http2 https://178.154.224.92/
HTTP/2 200
server: Angie/1.10.3
date: Fri, 16 Jan 2026 17:56:04 GMT
content-type: text/html; charset=UTF-8
vary: Accept-Encoding
link: <https://158.160.51.153/index.php?rest_route=/>; rel="https://api.w.org/"
vary: Accept-Encoding
x-cache-status: HIT
---
openssl s_client -connect 178.154.224.92:443 -servername 178.154.224.92 -tls1_2
CONNECTED(00000003)
depth=0 C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
verify error:num=18:self-signed certificate
verify return:1
depth=0 C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
verify return:1
---
Certificate chain
 0 s:C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
   i:C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Jan 16 11:49:49 2026 GMT; NotAfter: Jan 16 11:49:49 2027 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
subject=C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
issuer=C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: RSA-PSS
Server Temp Key: X25519, 253 bits
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
ALPN protocol: h2
Early data was not sent
Verify return code: 18 (self-signed certificate)
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    TLS session ticket lifetime hint: 3600 (seconds)
```
# Тестирование внешним сервисом WebPageTest
Протестировать не удалось, поскольку этим сервисом не поддерживается обрещение через самоподписной сертификат.
Получаю ошибку ERR_CERT_AUTHORITY_INVALID.

