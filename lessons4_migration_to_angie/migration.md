#Из репо Ubuntu автоматически установлен nginx
```console
root@angie-start:~# nginx -V
nginx version: nginx/1.24.0 (Ubuntu)
built with OpenSSL 3.0.13 30 Jan 2024
TLS SNI support enabled
configure arguments: --with-cc-opt='-g -O2 -fno-omit-frame-pointer -mno-omit-leaf-frame-pointer -ffile-prefix-map=/build/nginx-WLuzPu/nginx-1.24.0=. -flto=auto -ffat-lto-objects -fstack-protector-strong -fstack-clash-protection -Wformat -Werror=format-security -fcf-protection -fdebug-prefix-map=/build/nginx-WLuzPu/nginx-1.24.0=/usr/src/nginx-1.24.0-2ubuntu7.5 -fPIC -Wdate-time -D_FORTIFY_SOURCE=3' --with-ld-opt='-Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -Wl,-z,relro -Wl,-z,now -fPIC' --prefix=/usr/share/nginx --conf-path=/etc/nginx/nginx.conf --http-log-path=/var/log/nginx/access.log --error-log-path=stderr --lock-path=/var/lock/nginx.lock --pid-path=/run/nginx.pid --modules-path=/usr/lib/nginx/modules --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-compat --with-debug --with-pcre-jit --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_auth_request_module --with-http_v2_module --with-http_dav_module --with-http_slice_module --with-threads --with-http_addition_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_secure_link_module --with-http_sub_module --with-mail_ssl_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-stream_realip_module --with-http_geoip_module=dynamic --with-http_image_filter_module=dynamic --with-http_perl_module=dynamic --with-http_xslt_module=dynamic --with-mail=dynamic --with-stream=dynamic --with-stream_geoip_module=dynamic
root@angie-start:~# ps aux | grep nginx
root        2744  0.0  0.3  11196  7040 ?        S    13:42   0:00 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
www-data    2746  0.0  0.1  11532  3764 ?        S    13:42   0:00 nginx: worker process
www-data    2747  0.0  0.1  11532  3764 ?        S    13:42   0:00 nginx: worker process
root        3776  0.0  0.1   7076  2176 pts/1    S+   14:27   0:00 grep --color=auto nginx
```

#Скопированы конфиги из материалов задания в директорию sites-enabled
```console
root@angie-start:/home/navi# ll
total 40
drwxr-x--- 5 navi navi 4096 Nov 26 14:42 ./
drwxr-xr-x 3 root root 4096 Nov 21 11:36 ../
-rw-r--r-- 1 navi navi  220 Mar 31  2024 .bash_logout
-rw-r--r-- 1 navi navi 3771 Mar 31  2024 .bashrc
drwx------ 2 navi navi 4096 Nov 21 11:47 .cache/
-rw-r--r-- 1 navi navi  807 Mar 31  2024 .profile
drwx------ 2 navi navi 4096 Nov 26 12:50 .ssh/
drwxr-xr-x 6 root root 4096 Sep 13  2024 nginx/
-rw-r--r-- 1 navi navi 7172 Nov 26 13:28 nginx_conf.tar-252831-0242cd.gz
root@angie-start:/home/navi# cd /etc/nginx/
root@angie-start:/etc/nginx# ll
total 88
drwxr-xr-x  10 root root 4096 Nov 26 14:42 ./
drwxr-xr-x 113 root root 4096 Nov 26 13:42 ../
drwxr-xr-x   2 root root 4096 Aug 22 12:45 conf.d/
-rw-r--r--   1 root root 1125 Nov 26 14:42 fastcgi.conf
-rw-r--r--   1 root root 1055 Nov 26 14:42 fastcgi_params
drwxr-xr-x   2 root root 4096 Nov 26 14:42 html/
-rw-r--r--   1 root root 2837 Nov 26 14:42 koi-utf
-rw-r--r--   1 root root 2223 Nov 26 14:42 koi-win
-rw-r--r--   1 root root 3957 Nov 26 14:42 mime.types
drwxr-xr-x   2 root root 4096 Aug 22 12:45 modules-available/
drwxr-xr-x   2 root root 4096 Aug 22 12:45 modules-enabled/
-rw-r--r--   1 root root 2393 Nov 26 14:42 nginx.conf
-rw-r--r--   1 root root  180 Nov 26 14:42 proxy_params
-rw-r--r--   1 root root  636 Nov 26 14:42 scgi_params
drwxr-xr-x   2 root root 4096 Nov 26 13:42 sites-available/
drwxr-xr-x   2 root root 4096 Nov 26 14:42 sites-enabled/
drwxr-xr-x   2 root root 4096 Nov 26 13:42 snippets/
-rw-r--r--   1 root root  126 Nov 26 14:42 static-avif.conf
-rw-r--r--   1 root root   78 Nov 26 14:42 static.conf
-rw-r--r--   1 root root  664 Nov 26 14:42 uwsgi_params
-rw-r--r--   1 root root 3610 Nov 26 14:42 win-utf
```

# Рядом установлен angie
```console
root@angie-start:/etc/nginx# cd /etc/angie/
root@angie-start:/etc/angie# ll
total 60
drwxr-xr-x   4 root root  4096 Nov 21 12:13 ./
drwxr-xr-x 113 root root  4096 Nov 26 13:42 ../
-rw-r--r--   1 root root  1230 Nov 13 08:37 angie.conf
-rw-r--r--   1 root root  1077 Nov 12 21:04 fastcgi.conf
-rw-r--r--   1 root root  1007 Nov 12 21:04 fastcgi_params
drwxr-xr-x   2 root root  4096 Nov 21 12:13 http.d/
-rw-r--r--   1 root root  5354 Nov 12 21:04 mime.types
lrwxrwxrwx   1 root root    22 Nov 13 08:37 modules -> /usr/lib/angie/modules/
-rw-r--r--   1 root root 15083 Nov 12 21:04 prometheus_all.conf
-rw-r--r--   1 root root   636 Nov 12 21:04 scgi_params
drwxr-xr-x   2 root root  4096 Nov 21 12:13 stream.d/
-rw-r--r--   1 root root   664 Nov 12 21:04 uwsgi_params
root@angie-start:/etc/angie# angie -V
Angie version: Angie/1.10.3
nginx version: nginx/1.27.5
```
# При попытке посмотреть конфигурацию c подставленными инклюдами получила ошибку. Как справить - установить Brotli‑модуль/закоментировать. 
# Для упрощения комментирую. Поскольку мы будем настраивать angie, а не nginx:
```console
root@angie-start:~# nginx -T
2025/11/26 17:18:14 [emerg] 6323#6323: unknown directive "brotli_static" in /etc/nginx/nginx.conf:59
nginx: configuration file /etc/nginx/nginx.conf test failed
root@angie-start:/etc/nginx# grep -r 'brotli'
nginx.conf:    brotli_static		on;
nginx.conf:    brotli				on;
nginx.conf:    brotli_comp_level	5;
nginx.conf:    brotli_types		text/plain text/css text/xml application/javascript application/json image/x-icon image/svg+xml;
root@angie-start:/etc/nginx# vim nginx.conf +59
```
# После этого удалось прочитать конфигурацию командой nginx -T с полным выводом на экран инклюдов. Далее устанавливаю модуль в angie и переношу данные из nginx.conf в angie.conf. Подключаю brotli, запускаю тест:
```console
root@angie-start:/etc/nginx# apt search angie-module-brotli
Sorting... Done
Full Text Search... Done
angie-module-brotli/noble 1.10.3-1~noble amd64
  Angie Brotli dynamic module
root@angie-start:/etc/angie/modules# vim /etc/angie/angie.conf
root@angie-start:/etc/angie/modules# angie -t
angie: the configuration file /etc/angie/angie.conf syntax is ok
angie: configuration file /etc/angie/angie.conf test is successful
```
# Переношу дефолтный конфиг nginx в http.d
root@angie-start:/etc/angie/modules# less /etc/nginx/sites-available/default
root@angie-start:/etc/angie/modules# cp /etc/nginx/sites-available/default /etc/angie/http.d/

ot@angie-start:/etc/angie/http.d# ll
total 16
drwxr-xr-x 2 root root 4096 Nov 26 18:27 ./
drwxr-xr-x 4 root root 4096 Nov 26 18:21 ../
-rw-r--r-- 1 root root 1412 Nov 26 18:27 default
-rw-r--r-- 1 root root 1177 Nov 13 08:37 default.conf
root@angie-start:/etc/angie/http.d# cp default default.bak
root@angie-start:/etc/angie/http.d# cp default default.conf
root@angie-start:/etc/angie/http.d# ls -la
-rw-r--r-- 1 root root 1412 Nov 26 18:27 default
-rw-r--r-- 1 root root 1412 Nov 26 18:37 default.bak
-rw-r--r-- 1 root root 1412 Nov 26 18:37 default.conf
root@angie-start:/etc/angie/http.d# rm default.bak defaul
root@angie-start:/etc/angie/http.d# diff /etc/nginx/uwsgi_params ../uwsgi_params
root@angie-start:/etc/angie/http.d#
root@angie-start:/etc/angie/http.d#
root@angie-start:~$ diff /etc/nginx/fastcgi.conf /etc/angie/fastcgi.conf
17c17
< fastcgi_param  SERVER_SOFTWARE    nginx/$nginx_version;
---
> fastcgi_param  SERVER_SOFTWARE    Angie/$angie_version;
21d20
< fastcgi_param  REMOTE_USER        $remote_user;
root@angie-start:/etc/angie# cp -R /etc/nginx/snippets/ .
root@angie-start:/etc/angie# ll /etc/angie/snippets/
total 16
drwxr-xr-x 2 root root 4096 Nov 26 18:55 ./
drwxr-xr-x 5 root root 4096 Nov 26 18:55 ../
-rw-r--r-- 1 root root  423 Nov 26 18:55 fastcgi-php.conf
-rw-r--r-- 1 root root  217 Nov 26 18:55 snakeoil.conf
root@angie-start:/etc/angie# rm /etc/angie/snippets/snakeoil.conf
```

# У меня возникла другая ошибка при тестировании конфигурации:
```console
root@angie-start:/etc/angie# angie -t
angie: [emerg] "try_files" directive is duplicate in /etc/nginx/static-avif.conf:3
angie: configuration file /etc/angie/angie.conf test failed
root@angie-start:/etc/angie# grep -r try_files .
./snippets/fastcgi-php.conf:try_files $fastcgi_script_name =404;
./snippets/fastcgi-php.conf:# Bypass the fact that try_files resets $fastcgi_path_info
./http.d/default.conf:		#try_files $uri $uri/ =404;
./http.d/default.conf:	try_files $uri$avif_suffix $uri$webp_suffix $uri =404;
```
# Закоментировала в ./snippets/fastcgi-php.conf строку try_files $fastcgi_script_name =404; и перенесла ее в http.d/default.conf
# При проверке angie ругался на директиву в nginx конфиге со статикой, поэтому пришлось ее там закоментировать
```console
root@angie-start:/etc/angie# angie -t
angie: [emerg] "try_files" directive is duplicate in /etc/nginx/static-avif.conf:3
angie: configuration file /etc/angie/angie.conf test failed
root@angie-start:/etc/angie# grep -r try_files /etc/nginx/static-avif.conf
try_files $uri$avif_suffix $uri$webp_suffix $uri =404;
root@angie-start:/etc/angie# nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
root@angie-start:/etc/angie# vim /etc/nginx/static-avif.conf +3
root@angie-start:/etc/angie# angie -t
angie: the configuration file /etc/angie/angie.conf syntax is ok
angie: configuration file /etc/angie/angie.conf test is successful
```
# Ищу вхождения /nginx/ в конфигах angie и исправляю что нужно (static-avif.conf удаляю, директива try_files есть), проверяю.
```console
root@angie-start:~# grep -rn '/nginx/' /etc/angie/
/etc/angie/snippets/fastcgi-php.conf:8:# see: http://trac.nginx.org/nginx/ticket/321
/etc/angie/http.d/default.conf:19:	access_log /var/log/nginx/default.log;
/etc/angie/http.d/default.conf:41:        include /etc/nginx/static-avif.conf;
root@angie-start:~# vim /etc/angie/http.d/default.conf +41
root@angie-start:~# vim /etc/angie/snippets/fastcgi-php.conf +8
root@angie-start:~# angie -t
angie: the configuration file /etc/angie/angie.conf syntax is ok
angie: configuration file /etc/angie/angie.conf test is successful

#Проверяю права и директорию для статики, в данном случае ничего не меняем, так как пользователь не www-data, а root, доступ есть.
root@angie-start:/etc/angie# grep -r html
http.d/default.conf:	root /var/www/html;
root@angie-start:/etc/angie# ls -la /var/www/html
drwxr-xr-x 4 root root 4096 Nov 26 17:38 ..
-rw-r--r-- 1 root root   27 Nov 21 14:58 index.html
-rw-r--r-- 1 root root  615 Nov 26 13:42 index.nginx-debian.html
```
# Пробую открыть статику, но получаю ошибку. Она связана со строкой proxy_pass http://backend; в блоке server, закоментировала, релоад, работает:
```console
root@angie-start:/etc/angie# curl http://127.0.0.1/index.html
<html>
<head><title>502 Bad Gateway</title></head>
<body>
<center><h1>502 Bad Gateway</h1></center>
<hr><center>Angie/1.10.3</center>
</body>
</html>
root@angie-start:/etc/angie# vim http.d/default.conf
root@angie-start:/etc/angie# systemctl reload angie.service
root@angie-start:/etc/angie# curl http://127.0.0.1/index.html
<h1>Hello from Angie!</h1>
--------------------------------------
root@angie-start:/etc/angie# curl -I http://127.0.0.1/index.html
HTTP/1.1 200 OK
Server: Angie/1.10.3
Date: Thu, 27 Nov 2025 10:47:05 GMT
```
# Отключила автозагрузку nginx и включила angie
