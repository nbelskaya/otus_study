# Размещение сайта, настройка конфига и тестирование отработки location

#Скопировала файлы сайта и создала две заглушки для редиректов, назначила angie владельцем
```console
root@angie-start:/var/www/static_site-252831-96c1e2# ll
total 44
drwxr-xr-x 5 angie angie  4096 Dec  3 18:39 ./
drwxr-xr-x 5 root  root   4096 Dec  3 18:08 ../
drwxr-xr-x 6 angie angie  4096 Dec  3 18:07 assets/
drwxr-xr-x 2 angie angie  4096 Dec  3 18:07 error/
drwxr-xr-x 2 angie angie  4096 Dec  3 18:07 images/
-rwxr-xr-x 1 angie angie 14532 Dec  3 18:07 index.html*
-rw-r--r-- 1 angie angie    54 Dec  3 18:39 new-location.html
-rw-r--r-- 1 angie angie    46 Dec  3 18:39 new-page.htm

#Прописала сайт в hosts чтобы обращаться по server_name, проверяю работу locationl
```console
root@angie-start:~# curl -I http://static-site.local/
HTTP/1.1 200 OK
Server: Angie/1.10.3
Date: Wed, 03 Dec 2025 19:28:59 GMT
Content-Type: text/html
Content-Length: 14532
Last-Modified: Wed, 03 Dec 2025 18:07:52 GMT
Connection: keep-alive
Vary: Accept-Encoding
ETag: "69307c78-38c4"
Accept-Ranges: bytes

root@angie-start:~# curl -I http://static-site.local/images/pic01.jpg
HTTP/1.1 200 OK
Server: Angie/1.10.3
Date: Wed, 03 Dec 2025 19:29:18 GMT
Content-Type: image/jpeg
Content-Length: 10064
Last-Modified: Wed, 03 Dec 2025 18:07:52 GMT
Connection: keep-alive
ETag: "69307c78-2750"
Expires: Fri, 02 Jan 2026 19:29:18 GMT
Cache-Control: max-age=2592000
X-Image-Detected: Yes
Accept-Ranges: bytes

root@angie-start:~# curl -I http://static-site.local/assets/css/main.css
HTTP/1.1 200 OK
Server: Angie/1.10.3
Date: Wed, 03 Dec 2025 19:30:16 GMT
Content-Type: text/css
Content-Length: 32628
Last-Modified: Wed, 03 Dec 2025 18:07:53 GMT
Connection: keep-alive
Vary: Accept-Encoding
ETag: "69307c79-7f74"
Expires: Wed, 10 Dec 2025 19:30:16 GMT
Cache-Control: max-age=604800
X-CSS-Detected: Yes
Accept-Ranges: bytes

root@angie-start:~# curl -I http://static-site.local/assets/js/main.js
HTTP/1.1 200 OK
Server: Angie/1.10.3
Date: Wed, 03 Dec 2025 19:30:43 GMT
Content-Type: application/javascript
Content-Length: 8801
Last-Modified: Wed, 03 Dec 2025 18:07:54 GMT
Connection: keep-alive
Vary: Accept-Encoding
ETag: "69307c7a-2261"
Expires: Wed, 10 Dec 2025 19:30:43 GMT
Cache-Control: max-age=604800
X-JS-Detected: Yes
Accept-Ranges: bytes

root@angie-start:~# curl -I http://static-site.local/assets/fonts/fontawesome-webfont.woff2
HTTP/1.1 200 OK
Server: Angie/1.10.3
Date: Wed, 03 Dec 2025 19:31:00 GMT
Content-Type: font/woff2
Content-Length: 71896
Last-Modified: Wed, 03 Dec 2025 18:07:55 GMT
Connection: keep-alive
ETag: "69307c7b-118d8"
Expires: Tue, 03 Mar 2026 19:31:00 GMT
Cache-Control: max-age=7776000
X-Font-Detected: Yes
Accept-Ranges: bytes

root@angie-start:~# curl -I http://static-site.local/assets/sass/main.scss
HTTP/1.1 200 OK
Server: Angie/1.10.3
Date: Wed, 03 Dec 2025 19:31:19 GMT
Content-Type: application/octet-stream
Content-Length: 1122
Last-Modified: Wed, 03 Dec 2025 18:07:58 GMT
Connection: keep-alive
ETag: "69307c7e-462"
Expires: Thu, 04 Dec 2025 19:31:19 GMT
Cache-Control: max-age=86400
X-Sass-Detected: Yes
Accept-Ranges: bytes

root@angie-start:~# curl -I http://static-site.local/error/
HTTP/1.1 302 Found
Server: Angie/1.10.3
Date: Wed, 03 Dec 2025 19:31:36 GMT
Content-Type: text/html
Content-Length: 145
Location: http://static-site.local/error/index.html
Connection: keep-alive

root@angie-start:~# curl -v http://static-site.local/old-page
* Host static-site.local:80 was resolved.
* IPv6: (none)
* IPv4: 127.0.0.1
*   Trying 127.0.0.1:80...
* Connected to static-site.local (127.0.0.1) port 80
> GET /old-page HTTP/1.1
> Host: static-site.local
> User-Agent: curl/8.5.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Server: Angie/1.10.3
< Date: Wed, 03 Dec 2025 19:32:55 GMT
< Content-Type: text/html
< Content-Length: 46
< Last-Modified: Wed, 03 Dec 2025 18:39:41 GMT
< Connection: keep-alive
< Vary: Accept-Encoding
< ETag: "693083ed-2e"
< Accept-Ranges: bytes
<
<h1>New Page</h1><p>This is new-page.html</p>
* Connection #0 to host static-site.local left intact

root@angie-start:~# curl -v -L http://static-site.local/moved
* Host static-site.local:80 was resolved.
* IPv6: (none)
* IPv4: 127.0.0.1
*   Trying 127.0.0.1:80...
* Connected to static-site.local (127.0.0.1) port 80
> GET /moved HTTP/1.1
> Host: static-site.local
> User-Agent: curl/8.5.0
> Accept: */*
>
< HTTP/1.1 301 Moved Permanently
< Server: Angie/1.10.3
< Date: Wed, 03 Dec 2025 19:33:24 GMT
< Content-Type: text/html
< Content-Length: 169
< Location: http://static-site.local/new-location.html
< Connection: keep-alive
<
* Ignoring the response-body
* Connection #0 to host static-site.local left intact
* Issue another request to this URL: 'http://static-site.local/new-location.html'
* Found bundle for host: 0x589653fd1af0 [serially]
* Can not multiplex, even if we wanted to
* Re-using existing connection with host static-site.local
> GET /new-location.html HTTP/1.1
> Host: static-site.local
> User-Agent: curl/8.5.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Server: Angie/1.10.3
< Date: Wed, 03 Dec 2025 19:33:24 GMT
< Content-Type: text/html
< Content-Length: 54
< Last-Modified: Wed, 03 Dec 2025 18:39:49 GMT
< Connection: keep-alive
< Vary: Accept-Encoding
< ETag: "693083f5-36"
< Accept-Ranges: bytes
<
<h1>New Location</h1><p>This is new-location.html</p>
* Connection #0 to host static-site.local left intact
