## Запуск Angie в docker и локальный curl стартовой страницы

```console
root@angie-start:~# docker ps -a
CONTAINER ID   IMAGE                                COMMAND                  CREATED          STATUS          PORTS                                     NAMES
88eb758f0287   docker.angie.software/angie:latest   "angie -g 'daemon of…"   13 minutes ago   Up 13 minutes   0.0.0.0:8800->80/tcp, [::]:8800->80/tcp   angie
root@angie-start:~# docker port angie
80/tcp -> 0.0.0.0:8800
80/tcp -> [::]:8800
root@angie-start:~# curl -v http://127.0.0.1:8800
*   Trying 127.0.0.1:8800...
* Connected to 127.0.0.1 (127.0.0.1) port 8800
> GET / HTTP/1.1
> Host: 127.0.0.1:8800
> User-Agent: curl/8.5.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Server: Angie/1.10.3
< Date: Fri, 21 Nov 2025 15:19:13 GMT
< Content-Type: text/html
< Content-Length: 27
< Last-Modified: Fri, 21 Nov 2025 14:58:01 GMT
< Connection: keep-alive
< ETag: "69207df9-1b"
< Accept-Ranges: bytes
<
<h1>Hello from Angie!</h1>
* Connection #0 to host 127.0.0.1 left intact
root@angie-start:~#
```
