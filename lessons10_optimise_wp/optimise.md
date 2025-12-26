#В качестве теста нагрузила wp несколькими статьями и картинками, добавила в конфигурацию сайта сжатие, кеширование разных директорий со статикой и время жизни кеша
#Проверяю заголовки кеширования запросом к статическому элементу на сайте, установлен самоподписной сертификат, поэтому в резульат помещаю часть ответа без рукопожатий:
```consol
curl -kv -I https://158.160.51.153/wp-content/uploads/2025/12/5.jpg
*   Certificate level 0: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://158.160.51.153/wp-content/uploads/2025/12/5.jpg
* [HTTP/2] [1] [:method: HEAD]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: 158.160.51.153]
* [HTTP/2] [1] [:path: /wp-content/uploads/2025/12/5.jpg]
* [HTTP/2] [1] [user-agent: curl/8.5.0]
* [HTTP/2] [1] [accept: */*]
> HEAD /wp-content/uploads/2025/12/5.jpg HTTP/2
> Host: 158.160.51.153
> User-Agent: curl/8.5.0
> Accept: */*
>
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
< HTTP/2 200
HTTP/2 200
< server: Angie/1.10.3
server: Angie/1.10.3
< date: Fri, 26 Dec 2025 18:21:43 GMT
date: Fri, 26 Dec 2025 18:21:43 GMT
< content-type: image/jpeg
content-type: image/jpeg
< content-length: 60116
content-length: 60116
< last-modified: Fri, 26 Dec 2025 17:30:52 GMT
last-modified: Fri, 26 Dec 2025 17:30:52 GMT
< etag: "ead4-646de4148cc46"
etag: "ead4-646de4148cc46"
< accept-ranges: bytes
accept-ranges: bytes
< expires: Sat, 26 Dec 2026 18:21:43 GMT
expires: Sat, 26 Dec 2026 18:21:43 GMT
< cache-control: max-age=31536000
cache-control: max-age=31536000
< vary: Accept
vary: Accept
< cache-control: public, max-age=31536000, immutable
cache-control: public, max-age=31536000, immutable
```
# Проверка по If-Modified-Since
```console
curl -I -k -H "If-Modified-Since: Fri, 26 Dec 2025 17:30:52 GMT" https://158.160.51.153/wp-content/uploads/2025/12/5.jpg
HTTP/2 304
server: Angie/1.10.3
date: Fri, 26 Dec 2025 18:25:31 GMT
last-modified: Fri, 26 Dec 2025 17:30:52 GMT
etag: "ead4-646de4148cc46"
accept-ranges: bytes
expires: Sat, 26 Dec 2026 18:25:31 GMT
cache-control: max-age=31536000
vary: Accept
cache-control: public, max-age=31536000, immutable
```
# Проверка по If-None-Match (ETag-уникальная метка ресурса) экономия трафика и ускорение загрузки
```console
root@docker-wordpress:~# curl -I -k -H 'If-None-Match: "ead4-646de4148cc46"' https://158.160.51.153/wp-content/uploads/2025/12/5.jpg
HTTP/2 304
server: Angie/1.10.3
date: Fri, 26 Dec 2025 18:27:35 GMT
last-modified: Fri, 26 Dec 2025 17:30:52 GMT
etag: "ead4-646de4148cc46"
accept-ranges: bytes
expires: Sat, 26 Dec 2026 18:27:35 GMT
cache-control: max-age=31536000
vary: Accept
cache-control: public, max-age=31536000, immutable
```
#Проверяю настройки сжатия GZIP и  Первый запрос - MISS, второй HIT:
```console
root@docker-wordpress:~# curl -kv -H "Accept-Encoding: gzip" -I https://178.154.241.206
HTTP/2 200
< server: Angie/1.10.3
server: Angie/1.10.3
< date: Thu, 25 Dec 2025 18:55:39 GMT
date: Thu, 25 Dec 2025 18:55:39 GMT
< content-type: text/html; charset=UTF-8
content-type: text/html; charset=UTF-8
< vary: Accept-Encoding
vary: Accept-Encoding
< x-powered-by: PHP/8.3.28
x-powered-by: PHP/8.3.28
< link: <https://178.154.241.206/index.php?rest_route=/>; rel="https://api.w.org/"
link: <https://178.154.241.206/index.php?rest_route=/>; rel="https://api.w.org/"
< strict-transport-security: max-age=31536000; includeSubDomains; preload
strict-transport-security: max-age=31536000; includeSubDomains; preload
< x-frame-options: SAMEORIGIN
x-frame-options: SAMEORIGIN
< x-content-type-options: nosniff
x-content-type-options: nosniff
< x-xss-protection: 1; mode=block
x-xss-protection: 1; mode=block
< referrer-policy: strict-origin-when-cross-origin
referrer-policy: strict-origin-when-cross-origin
< content-encoding: gzip
content-encoding: gzip
< x-cache-status: MISS
x-cache-status: MISS
-------
HTTP/2 200
< server: Angie/1.10.3
server: Angie/1.10.3
< date: Fri, 26 Dec 2025 18:44:32 GMT
date: Fri, 26 Dec 2025 18:44:32 GMT
< content-type: text/html; charset=UTF-8
content-type: text/html; charset=UTF-8
< content-length: 13684
content-length: 13684
< x-powered-by: PHP/8.3.28
x-powered-by: PHP/8.3.28
< link: <https://158.160.51.153/index.php?rest_route=/>; rel="https://api.w.org/"
link: <https://158.160.51.153/index.php?rest_route=/>; rel="https://api.w.org/"
< vary: Accept-Encoding
vary: Accept-Encoding
< content-encoding: gzip
content-encoding: gzip
< x-cache-status: HIT
x-cache-status: HIT
```
#Нагрузить сайт так чтобы можно было заметно сжать и ускорить не вышло, нужно очень много контента наплодить и установить различных плагинов. Того что сделала было мало, при проверке Lighthouse (Chrome DevTools) -  отдает 99 Perfomance.
#Для выполенения пункта кеширования конкретной страницы - включена зона прокси‑кеша proxy_cache_path /var/www/cache в angie.conf, в конфиге виртуального хоста добавлен отдельный локейшен "location = /"  с директивами proxy_cache, proxy_cache_key, proxy_cache_valid. Добавлен заголовок X-Cache-Status для мониторинга (показывает MISS/HIT/BYPASS). Настроены правила proxy_cache_use_stale и proxy_cache_background_update для устойчивости при ошибках бэкенда. Также добавлен пропуск кеша для пользователей с кукой wordpress_logged_in_ (чтобы авторизованные пользователи всегда видели свежую страницу).
#Кеширование главной страницы
```console
root@docker-wordpress:~# curl -I -k https://158.160.51.153/
HTTP/2 200
server: Angie/1.10.3
date: Fri, 26 Dec 2025 18:46:46 GMT
content-type: text/html; charset=UTF-8
vary: Accept-Encoding
x-powered-by: PHP/8.3.28
link: <https://158.160.51.153/index.php?rest_route=/>; rel="https://api.w.org/"
vary: Accept-Encoding
x-cache-status: MISS
root@docker-wordpress:~# curl -I -k https://158.160.51.153/
HTTP/2 200
server: Angie/1.10.3
date: Fri, 26 Dec 2025 18:46:48 GMT
content-type: text/html; charset=UTF-8
vary: Accept-Encoding
x-powered-by: PHP/8.3.28
link: <https://158.160.51.153/index.php?rest_route=/>; rel="https://api.w.org/"
vary: Accept-Encoding
x-cache-status: HIT
```
#Проверяю обход кеша для авторизованного пользователя - получила BYPASS
```console
root@docker-wordpress:/etc/angie# curl -I -k -H "Cookie: wordpress_logged_in_abc=1" https://158.160.51.153/
HTTP/2 200
server: Angie/1.10.3
date: Fri, 26 Dec 2025 19:03:01 GMT
content-type: text/html; charset=UTF-8
vary: Accept-Encoding
x-powered-by: PHP/8.3.28
link: <https://158.160.51.153/index.php?rest_route=/>; rel="https://api.w.org/"
vary: Accept-Encoding
x-cache-status: BYPASS
```
# Проверяю скопление файлов кеша на диске:
```console
root@docker-wordpress:/etc/angie# ls -la /var/www/cache
total 20
drwxr-xr-x 5 angie root  4096 Dec 26 18:46 .
drwxr-xr-x 3 root  root  4096 Dec 25 19:07 ..
drwx------ 3 angie angie 4096 Dec 26 18:43 4
drwx------ 3 angie angie 4096 Dec 26 18:46 8
drwx------ 3 angie angie 4096 Dec 26 18:41 e
```
