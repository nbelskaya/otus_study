# Подготовка конфигурационных файлов, настроек защити и описание типовых точек атак сайта на wordpress.

### Список location которые буду защищать:
1. /wp-login.php — главная цель DoS и brute‑force.
Сюда идут атаки на подбор пароля администратора, а также дос-атаки, потому что страница тяжёлая (грузит PHP и БД).

Что можно сделать: ограничить частоту запросов и кол-во подключений, включить Fail2Ban, ограничить доступ по IP, настроить basic‑auth.

 2. /xmlrpc.php — вторая по популярности точка атаки.
Этот файл имеет уязвимости, злоумышленник может отправить на сервер вредоносный xsml, 
также подвержен массовому брутфорсу учетных данных, через метод  system.multicall, чтобы в одном HTTP‑запросе отправить сотни попыток подбора логина/пароля.

Что можно сделать: если не используется сайтом, то нужно полностью закрыть доступ к файлу.

 3. /wp-admin/ — панель администратора.
Сюда тоже идут атаки, но реже, чем на wp-login.php.

Что можно сделать: ограничить доступ по IP, включить basic‑auth, ограничить частоту запросов.

4. /wp-json/ — REST API.
REST API часто используют сканеры уязвимостей, боты, парсеры.

Что делать: ограничить частоту запросов, закрыть доступ по IP, если API не нужен публично.

5. /wp-content/uploads/ — атаки на медиа.
Сюда могут идти попытки загрузить вредоносные файлы и DoS на большие файлы.

Что делать:  ограничить размер запроса, ограничить частоту

### Что сделано:
1. fail2ban
/etc/fail2ban/filter.d/nginx-limit-req.conf - приехал стандартный, в нем уже есть failregex и переменная (ngx_limit_req_zones = [^"]+)-  подходит для angie
/etc/fail2ban/jail.local - помещена конфингурация для nginx-limit-req
2. HTTP‑авторизация
htpasswd -c /etc/angie/htpasswd admin - создала файл паролей для basic‑auth и пользователя admin
Далее включаю HTTP‑авторизацию в Angie через конфигурационный файл /etc/angie/http.d/wordpress.conf:
- разрешено только ip виртуальной машины, остальные запрещены
- basic‑auth
- защищённый location /wp-admin/
3. Написан конфиг для angie wordpress в котором настроены ограничения на частоту запросов и подключения

### Тестирование защиты, запуск утилиты Apache Benchmark.
Все тесты запускаю со своего ноутбука к вм яндекса, в логах будет мой ip:
```console
loomee@~ $
 $ curl 2ip.ru
188.242.98.168
```
1. Тест DoS‑защиты wp-login.php (limit_req).. 
Тест выполнялся по HTTPS, так как HTTP перенаправляет на HTTPS и limit_req не срабатывает.
```console
loomee@~ $
 $ ab -k -n 200 -c 20 https://46.21.247.233/wp-login.php
This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 46.21.247.233 (be patient)
Completed 100 requests
Completed 200 requests
Finished 200 requests


Server Software:        Angie/1.10.3
Server Hostname:        46.21.247.233
Server Port:            443
SSL/TLS Protocol:       TLSv1.2,ECDHE-RSA-CHACHA20-POLY1305,2048,256
Server Temp Key:        ECDH X25519 253 bits

Document Path:          /wp-login.php
Document Length:        0 bytes

Concurrency Level:      20
Time taken for tests:   0.569 seconds
Complete requests:      200
Failed requests:        194
   (Connect: 0, Receive: 0, Length: 194, Exceptions: 0)
Non-2xx responses:      200
Keep-Alive requests:    200
Total transferred:      86126 bytes
HTML transferred:       33562 bytes
Requests per second:    351.72 [#/sec] (mean)
Time per request:       56.863 [ms] (mean)
Time per request:       2.843 [ms] (mean, across all concurrent requests)
Transfer rate:          147.91 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   12  36.4      0     183
Processing:    15   21   5.6     20      67
Waiting:       15   20   5.5     20      67
Total:         15   32  38.1     20     248

Percentage of the requests served within a certain time (ms)
  50%     20
  66%     21
  75%     21
  80%     22
  90%    122
  95%    136
  98%    143
  99%    157
 100%    248 (longest request)
```
В результате теста получено:
1. Failed requests: 194 - angie отклонил запросы по limit_req
2. Non‑2xx responses: 200 - ни один запрос не вернул 200 OK
3. Document Length: 0 bytes - означает, angie отдавал не страницу логина, а ошибку
4. Requests per second: 351.72 - Angie выдержал нагрузку

В логах:
```console
/var/log/angie/wordpress_error.log:
2026/03/02 15:10:05 [error] 8168#8168: *1207 limiting requests, excess: 10.175 by zone "req_limit", client: 188.242.98.168, server: wordpress.local, request: "GET /wp-login.php HTTP/1.0", host: "46.21.247.233"
/var/log/angie/wordpress_access.log:
188.242.98.168 - - [02/Mar/2026:15:10:05 +0000] "GET /wp-login.php HTTP/1.0" 302 0 "-" "ApacheBench/2.3"
188.242.98.168 - - [02/Mar/2026:15:10:05 +0000] "GET /wp-login.php HTTP/1.0" 503 173 "-" "ApacheBench/2.3"
```
302 в access‑log — это редирект с HTTP → HTTPS

2. Тест ограничения подключений (limit_conn).
```console
loomee@~ $
 $ ab -k -n 50 -c 10 https://46.21.247.233/wp-login.php
This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 46.21.247.233 (be patient).....done


Server Software:        Angie/1.10.3
Server Hostname:        46.21.247.233
Server Port:            443
SSL/TLS Protocol:       TLSv1.2,ECDHE-RSA-CHACHA20-POLY1305,2048,256
Server Temp Key:        ECDH X25519 253 bits

Document Path:          /wp-login.php
Document Length:        0 bytes

Concurrency Level:      10
Time taken for tests:   0.350 seconds
Complete requests:      50
Failed requests:        43
   (Connect: 0, Receive: 0, Length: 43, Exceptions: 0)
Non-2xx responses:      50
Keep-Alive requests:    50
Total transferred:      21097 bytes
HTML transferred:       7439 bytes
Requests per second:    142.66 [#/sec] (mean)
Time per request:       70.094 [ms] (mean)
Time per request:       7.009 [ms] (mean, across all concurrent requests)
Transfer rate:          58.79 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   16  32.6      0     107
Processing:    16   22   9.1     19      57
Waiting:       16   22   9.0     19      56
Total:         16   38  36.3     20     164

Percentage of the requests served within a certain time (ms)
  50%     20
  66%     22
  75%     38
  80%     86
  90%    100
  95%    112
  98%    164
  99%    164
 100%    164 (longest request)
```
Тест показал, что limit_conn сработал — Angie отклонил часть запросов. Все ответы были не 200 OK — значит, защита активна.
```console
Failed requests:        43
Non-2xx responses:      50
Document Length:        0 bytes
```
Логи:
```console
root@docker-wordpress:~# grep "limiting connections" /var/log/angie/wordpress_error.log
2026/03/02 17:02:10 [error] 8167#8167: *1244 limiting connections by zone "conn_limit", client: 188.242.98.168, server: wordpress.local, request: "GET /wp-login.php HTTP/1.0", host: "46.21.247.233"
2026/03/02 17:02:10 [error] 8167#8167: *1245 limiting connections by zone "conn_limit", client: 188.242.98.168, server: wordpress.local, request: "GET /wp-login.php HTTP/1.0", host: "46.21.247.233"
root@docker-wordpress:~# tail -n 20 /var/log/angie/wordpress_access.log | grep  503
188.242.98.168 - - [02/Mar/2026:17:02:10 +0000] "GET /wp-login.php HTTP/1.0" 503 173 "-" "ApacheBench/2.3"
188.242.98.168 - - [02/Mar/2026:17:02:10 +0000] "GET /wp-login.php HTTP/1.0" 503 173 "-" "ApacheBench/2.3"
188.242.98.168 - - [02/Mar/2026:17:02:10 +0000] "GET /wp-login.php HTTP/1.0" 503 173 "-" "ApacheBench/2.3"
root@docker-wordpress:~# tail -n 20 /var/log/angie/wordpress_access.log | grep  302
188.242.98.168 - - [02/Mar/2026:17:02:10 +0000] "GET /wp-login.php HTTP/1.0" 302 0 "-" "ApacheBench/2.3"
```
3. Тест Fail2Ban.
Создаю нагрузку, чтобы Fail2Ban увидел много 503
```console
loomee@~ $
 $ ab -k -n 500 -c 50 https://46.21.247.233/wp-login.php
This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 46.21.247.233 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Finished 500 requests


Server Software:        Angie/1.10.3
Server Hostname:        46.21.247.233
Server Port:            443
SSL/TLS Protocol:       TLSv1.2,ECDHE-RSA-CHACHA20-POLY1305,2048,256
Server Temp Key:        ECDH X25519 253 bits

Document Path:          /wp-login.php
Document Length:        0 bytes

Concurrency Level:      50
Time taken for tests:   0.555 seconds
Complete requests:      500
Failed requests:        494
   (Connect: 0, Receive: 0, Length: 494, Exceptions: 0)
Non-2xx responses:      500
Keep-Alive requests:    500
Total transferred:      216026 bytes
HTML transferred:       85462 bytes
Requests per second:    901.31 [#/sec] (mean)
Time per request:       55.475 [ms] (mean)
Time per request:       1.110 [ms] (mean, across all concurrent requests)
Transfer rate:          380.28 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   18  53.7      0     198
Processing:    15   20   5.7     20     126
Waiting:       15   20   5.7     20     126
Total:         15   38  54.3     20     222

Percentage of the requests served within a certain time (ms)
  50%     20
  66%     21
  75%     22
  80%     22
  90%    163
  95%    199
  98%    210
  99%    218
 100%    222 (longest request)
```
Проверяю статус jail:
```console
root@docker-wordpress:~# fail2ban-client status nginx-limit-req
Status for the jail: nginx-limit-req
|- Filter
|  |- Currently failed:	1
|  |- Total failed:	487
|  `- File list:	/var/log/angie/wordpress_error.log /var/log/angie/error.log
`- Actions
   |- Currently banned:	1
   |- Total banned:	1
   `- Banned IP list:	188.242.98.168
```
Только после исправления файла jail.local, добавив  backend = polling, блокировка сработала, потому
 что Fail2Ban стал читать логи. До этого не читал (backend был journal, а Angie пишет в файлы).
Мой IP в списке блокировок, это подтверждает, что фильтр nginx-limit-req работает корректно,  jail активен,
 Fail2Ban успешно блокирует IP‑адреса, превышающие лимиты Angie.
Дополнительно, проверка фильтра:
```console
root@docker-wordpress:~# fail2ban-regex /var/log/angie/wordpress_error.log /etc/fail2ban/filter.d/nginx-limit-req.conf

Running tests
=============

Use   failregex filter file : nginx-limit-req, basedir: /etc/fail2ban
Use      datepattern : {^LN-BEG} : Default Detectors
Use         log file : /var/log/angie/wordpress_error.log
Use         encoding : UTF-8


Results
=======

Failregex: 713 total
|-  #) [# of hits] regular expression
|   1) [713] ^\s*\[[a-z]+\] \d+#\d+: \*\d+ limiting requests, excess: [\d\.]+ by zone "(?:[^"]+)", client: <HOST>,
`-

Ignoreregex: 0 total

Date template hits:
|- [# of hits] date format
|  [732] {^LN-BEG}ExYear(?P<_sep>[-/.])Month(?P=_sep)Day(?:T|  ?)24hour:Minute:Second(?:[.,]Microseconds)?(?:\s*Zone offset)?
`-

Lines: 732 lines, 0 ignored, 713 matched, 19 missed
[processed in 0.02 sec]
```
В результате вижу, что 713 строк успешно совпали с шаблоном failregex, фильтр корректно распознаёт сообщения вида:
limiting requests, excess: ...
19 missed -  пропущенные строки относятся к другим механизмам (например, limit_conn).
Это подтверждает, что фильтр Fail2Ban работает корректно и способен блокировать IP‑адреса, превышающие лимиты Angie.

4. Тест блокировки xmlrpc.php.
Столкнулась с проблемой обращения курлом к файлам вм из за того, что  Angie с самоподписанным сертификатом + curl по умолчанию 
использует HTTP/2 иногда ломает соединение → PROTOCOL_ERROR.
При обращении к файлам столкнулась с недоступностью HTTPS - получала PROTOCOL_ERROR. Оказалось, что curl по умолчанию использует HTTP/2,
а Angie 1.10.3 иногда ломает HTTP/2 с самоподписанными сертификатами.
```console
$ curl -I http://46.21.247.233/xmlrpc.php
HTTP/1.1 301 Moved Permanently
Server: Angie/1.10.3
Date: Mon, 02 Mar 2026 18:21:36 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: https://46.21.247.233/xmlrpc.php
loomee@~ $
 $ curl -I https://46.21.247.233/wp-admin/
curl: (60) SSL certificate problem: self signed certificate
More details here: https://curl.se/docs/sslcerts.html
```
Чтобы обойти это, принудительно обратилась командой curl по http1.1:
```console
 $ curl -I --http1.1 -k https://46.21.247.233/xmlrpc.php
curl: (52) Empty reply from server
```
Empty reply from server означает, что Angie закрывает соединение на уровне TCP (код 444), не отдавая HTTP‑ответ.
Таким образом, мне удалось убедиться, что доступ к xmlrpc.php полностью заблокирован.

5. Тестирование HTTP‑auth и IP‑фильтрации /wp-admin/ 
В конфигурации Angie для /wp-admin/ включены два механизма защиты:
- IP‑фильтрация — доступ разрешён только с IP администратора
- HTTP‑авторизация (basic‑auth) — требуется логин/пароль для входа

satisfy all — означает, что должны выполняться оба условия: IP разрешён и пройдена basic‑auth.

Из‑за того, что Angie блокирует curl по User‑Agent (правило limit_bots), для тестирования использован браузерный User‑Agent (-A "Mozilla/5.0"). Также принудительно включён HTTP/1.1 (--http1.1), чтобы обойти баг HTTP/2:
```console
$ curl -I --http1.1 -k -A "Mozilla/5.0" https://46.21.247.233/wp-admin/
HTTP/1.1 401 Unauthorized
Server: Angie/1.10.3
WWW-Authenticate: Basic realm="Restricted"
```
Результат: Angie корректно требует basic‑auth.
IP‑фильтрация пропускает запрос, но без логина/пароля доступ запрещён.

```console
$ curl -I --http1.1 -k -A "Mozilla/5.0" -u admin:*** https://46.21.247.233/wp-admin/
HTTP/1.1 302 Found
Server: Angie/1.10.3
Location: https://127.0.0.1:8080/wp-admin/
```
Результат: Angie принимает логин/пароль и передаёт запрос в WordPress.
WordPress возвращает стандартный редирект /wp-admin/ → внутренний адрес (127.0.0.1:8080).

6. Тестирование защиты wp-admin по HTTP (редирект на HTTPS)
Так как весь трафик должен идти только по HTTPS, важно убедиться, что прямой доступ к /wp-admin/ по HTTP невозможен и Angie корректно перенаправляет запросы на защищённый протокол.
```console
 $  curl -I http://46.21.247.233/wp-admin/
HTTP/1.1 301 Moved Permanently
Server: Angie/1.10.3
Date: Mon, 02 Mar 2026 19:57:11 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: https://46.21.247.233/wp-admin/
```  
Тестирование показывает, что Angie корректно перенаправляет HTTP → HTTPS.
Это гарантирует, что панель администратора никогда не будет доступна по незащищённому протоколу.

7. Тестирование работы WordPress через reverse‑proxy Angie
Цель теста — убедиться, что Angie корректно принимает HTTPS‑запросы, проксирует их в контейнер WordPress (127.0.0.1:8080), передаёт заголовки и возвращает ответ клиенту.
```console
loomee@~ $
 $ curl -I --http1.1 -k -A "Mozilla/5.0" https://46.21.247.233/
HTTP/1.1 200 OK
Server: Angie/1.10.3
Date: Mon, 02 Mar 2026 20:01:32 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
Vary: Accept-Encoding
X-Powered-By: PHP/8.3.28
Link: <https://46.21.247.233/index.php?rest_route=/>; rel="https://api.w.org/"
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```
Логи:
```console
188.242.98.168 - - [02/Mar/2026:20:01:32 +0000] "HEAD / HTTP/1.1" 200 0 "-" "Mozilla/5.0"
```
В результате теста видно, что:
- Angie принял HTTPS‑запрос на корень сайта /.
- Передал его в WordPress через proxy_pass http://127.0.0.1:8080.
- WordPress вернул корректный ответ 200 OK.
- В ответе присутствуют заголовки WordPress (X-Powered-By, Link)заголовки безопасности, добавленные Angie (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection)

Это подтверждает, что цепочка клиент → Angie → WordPress → Angie → клиент работает корректно.
В access‑log видно успешную обработку запроса:
```console
188.242.98.168 - - [02/Mar/2026:20:01:32 +0000] "HEAD / HTTP/1.1" 200 0 "-" "Mozilla/5.0"
```
Это подтверждает, что конфигурация reverse‑proxy завершена и работает.
