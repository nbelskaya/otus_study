## Проверка версии Angie и модулей

```console
$ angie -V
Angie version: 1.10.3
nginx version: 1.27.5
built by angie-build (Angie build system) 13 November 2025
built with OpenSSL 3.0.13 30 Jan 2024
TLS SNI support enabled
configure arguments: --prefix=/etc/angie ...
  --with-http_ssl_module
  --with-http_v2_module
  --with-http_v3_module
  --with-http_gzip_static_module
  --with-http_realip_module
  --with-http_stub_status_module
  --with-stream_ssl_module
  --with-stream_mqtt_preread_module
  --with-mail_ssl_module
```

## Проверка установленных пакетов

```console
$ dpkg -l | grep angie
ii  angie                1.10.3-1~noble   amd64   High performance web server
ii  angie-module-upload  1.10.3-1~noble   amd64   Upload module for Angie
ii  angie-module-zip     1.10.3-1~noble   amd64   Zip module for Angie
```
