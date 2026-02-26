# Подготовка окружения
1. Установила angie в систему - балансировщик
2. Установила docker-compose и запустила контейнеры бекендов:
```console
docker run -d --name b1 -p 9001:80 hashicorp/http-echo -text="backend1" -listen=:80
docker run -d --name b2 -p 9002:80 hashicorp/http-echo -text="backend2" -listen=:80
docker run -d --name b3 -p 9003:80 hashicorp/http-echo -text="backend3" -listen=:80
```
3. Проверила, что контейнеры отвечают:
```console
root@angie-balancer:~# curl 127.0.0.1:9001
backend1
root@angie-balancer:~# curl 127.0.0.1:9002
backend2
root@angie-balancer:~# curl 127.0.0.1:9003
backend3
```
4. Для каждого типа балансировки создала отдельный конфиг-файл, чтобы можно было между ними переключаться. 
Один активный конфигурационный файл за раз, остальные переименовыаны в .conf.disabled.
```console
root@angie-balancer:/etc/angie/http.d# tree
.
├── backup.conf
├── default.conf
├── hash.conf
├── random.conf
└── rr.conf

1 directory, 5 files
```
# Тестирование балансировки

### Round Robin
Каждый новый запрос идёт на следующий сервер по кругу, не учитывая нагрузку.
Отключила все конфигурации кроме нужной и запустила reload.
``` console
root@angie-balancer:/etc/angie/http.d# ll
total 28
drwxr-xr-x 2 root root 4096 Feb 26 17:29 ./
drwxr-xr-x 4 root root 4096 Feb 26 12:04 ../
-rw-r--r-- 1 root root  224 Feb 26 15:53 backup.conf.disabled
-rw-r--r-- 1 root root 1177 Feb  6 07:05 default.conf.disabled
-rw-r--r-- 1 root root  234 Feb 26 15:50 hash.conf.disabled
-rw-r--r-- 1 root root  223 Feb 26 15:52 random.conf.disabled
-rw-r--r-- 1 root root  211 Feb 26 15:49 rr.conf
root@angie-balancer:/etc/angie/http.d#
root@angie-balancer:/etc/angie/http.d# systemctl reload angie.service
```
Запустила curl в однострочнике, чтобы было видно частоту запросов.
```console
root@angie-balancer:/etc/angie/http.d# seq 1 5 | xargs -I {} sh -c 'echo "$(date +"%T") -> $(curl 178.154.199.14)"; sleep 1'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6965      0 --:--:-- --:--:-- --:--:--  9000
17:32:20 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   4400      0 --:--:-- --:--:-- --:--:--  4500
17:32:21 -> backend1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6711      0 --:--:-- --:--:-- --:--:--  9000
17:32:22 -> backend2
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6716      0 --:--:-- --:--:-- --:--:--  9000
17:32:23 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   7544      0 --:--:-- --:--:-- --:--:--  9000
17:32:24 -> backend1
root@angie-balancer:/etc/angie/http.d#
```
По ответу от команды видно, что запросы с частотой раз в секунду приходят по очереди на каждый бэкенд. 

### Hash
Здесь Angie берёт $request_uri, считает хеш и выбирает сервер.
Переключилась на нужный конфиг и запустила тесты.
```console
root@angie-balancer:/etc/angie/http.d# mv rr.conf rr.conf.disabled
root@angie-balancer:/etc/angie/http.d# mv hash.conf.disabled hash.conf
root@angie-balancer:/etc/angie/http.d# systemctl reload angie.service
-------------------------------
root@angie-balancer:/etc/angie/http.d# seq 1 5 | xargs -I {} sh -c 'echo "$(date +"%T") -> $(curl 178.154.199.14/a)"; sleep 1'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   5847      0 --:--:-- --:--:-- --:--:--  9000
17:42:59 -> backend2
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   5379      0 --:--:-- --:--:-- --:--:--  9000
17:43:00 -> backend2
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6151      0 --:--:-- --:--:-- --:--:--  9000
17:43:01 -> backend2
-------------------------------
root@angie-balancer:/etc/angie/http.d# seq 1 5 | xargs -I {} sh -c 'echo "$(date +"%T") -> $(curl 178.154.199.14/b)"; sleep 1'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   5806      0 --:--:-- --:--:-- --:--:--  9000
17:43:15 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6651      0 --:--:-- --:--:-- --:--:--  9000
17:43:16 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
root@angie-balancer:/etc/angie/http.d#
```
В результате тестов видно, что каждый запрос приходит на один и тот же сервер. Один и тот же URI → один и тот же backend.

### Random
Каждый запрос идёт на случайный сервер. Для тестирования выбрала простой random. Переключилась на конфиг random.conf и запустила проверку:
```console
root@angie-balancer:/etc/angie/http.d# seq 1 5 | xargs -I {} sh -c 'echo "$(date +"%T") -> $(curl 178.154.199.14)"; sleep 1'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6151      0 --:--:-- --:--:-- --:--:--  9000
17:52:09 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6378      0 --:--:-- --:--:-- --:--:--  9000
17:52:10 -> backend1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   7031      0 --:--:-- --:--:-- --:--:--  9000
17:52:11 -> backend1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   4891      0 --:--:-- --:--:-- --:--:--  9000
17:52:12 -> backend2
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   5960      0 --:--:-- --:--:-- --:--:--  9000
17:52:13 -> backend3
root@angie-balancer:/etc/angie/http.d#
```
Тестирование показало, что запросы приходят в случайной последовательности, бекенд может повторяться.

### Backup / Down

В конфигурации backup.conf я отключила второй бекенд (9002 down) и пометила бекапным третий (9003 backup), соответственно, пока жив 9001
запросы будут приходить только на него, в бекапный запрос должен попасть если отключится основной. 
Запустила тесты:
```console
root@angie-balancer:/etc/angie/http.d# docker ps -a
CONTAINER ID   IMAGE                 COMMAND                  CREATED       STATUS       PORTS                                               NAMES
5a9a637a44b5   hashicorp/http-echo   "/http-echo -text=ba…"   5 hours ago   Up 5 hours   5678/tcp, 0.0.0.0:9003->80/tcp, [::]:9003->80/tcp   b3
140b0e3fb70f   hashicorp/http-echo   "/http-echo -text=ba…"   5 hours ago   Up 5 hours   5678/tcp, 0.0.0.0:9002->80/tcp, [::]:9002->80/tcp   b2
6304ebc1cd0c   hashicorp/http-echo   "/http-echo -text=ba…"   5 hours ago   Up 5 hours   5678/tcp, 0.0.0.0:9001->80/tcp, [::]:9001->80/tcp   b1
root@angie-balancer:/etc/angie/http.d# seq 1 5 | xargs -I {} sh -c 'echo "$(date +"%T") -> $(curl 178.154.199.14)"; sleep 1'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   5005      0 --:--:-- --:--:-- --:--:--  9000
18:18:29 -> backend1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6109      0 --:--:-- --:--:-- --:--:--  9000
18:18:30 -> backend1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6155      0 --:--:-- --:--:-- --:--:--  9000
18:18:31 -> backend1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6382      0 --:--:-- --:--:-- --:--:--  9000
18:18:32 -> backend1
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6917      0 --:--:-- --:--:-- --:--:--  9000
18:18:33 -> backend1
```
Теперь я остановлю контейнер с портом 9001 и посмотрю как работает резервирование:
```console
root@angie-balancer:/etc/angie/http.d# docker stop b1
b1
root@angie-balancer:/etc/angie/http.d# docker ps -a
CONTAINER ID   IMAGE                 COMMAND                  CREATED       STATUS                     PORTS                                               NAMES
5a9a637a44b5   hashicorp/http-echo   "/http-echo -text=ba…"   5 hours ago   Up 5 hours                 5678/tcp, 0.0.0.0:9003->80/tcp, [::]:9003->80/tcp   b3
140b0e3fb70f   hashicorp/http-echo   "/http-echo -text=ba…"   5 hours ago   Up 5 hours                 5678/tcp, 0.0.0.0:9002->80/tcp, [::]:9002->80/tcp   b2
6304ebc1cd0c   hashicorp/http-echo   "/http-echo -text=ba…"   5 hours ago   Exited (2) 3 seconds ago                                                       b1
root@angie-balancer:/etc/angie/http.d# seq 1 5 | xargs -I {} sh -c 'echo "$(date +"%T") -> $(curl 178.154.199.14)"; sleep 1'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   5235      0 --:--:-- --:--:-- --:--:--  9000
18:23:38 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6280      0 --:--:-- --:--:-- --:--:--  9000
18:23:39 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6032      0 --:--:-- --:--:-- --:--:--  9000
18:23:40 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6211      0 --:--:-- --:--:-- --:--:--  9000
18:23:41 -> backend3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     9  100     9    0     0   6147      0 --:--:-- --:--:-- --:--:--  9000
18:23:42 -> backend3
root@angie-balancer:/etc/angie/http.d#
```
Результаты показали, что резервирование работатет, запросы переключаются на бекапный бекенд.

