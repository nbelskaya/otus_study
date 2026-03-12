from flask import Flask, request, make_response, render_template_string
import os
import psycopg2  # если используете БД, иначе уберите

app = Flask(__name__)
# Для каждого контейнера задайте свои значения:
BACKEND_NAME = os.environ.get('BACKEND_NAME', 'green')   # set in docker-compose
COLOR = os.environ.get('COLOR', '#00ff00')

TEMPLATE = """
<html>
<body style="background:{{ color }}; font-family:Arial; text-align:center;">
  <h1>Backend: {{ backend }}</h1>
  <h2>Color: {{ color }}</h2>
  <h3>Total requests: {{ hits }}</h3>
  <p>Your IP: {{ ip }}</p>
  <hr>
  <p><b>Received cookie srv_id:</b> {{ srv_id }}</p>
</body>
</html>
"""

def get_hits_and_inc(backend_name):
    # Простой stub: замените на реальную запись в Postgres
    # Здесь можно делать INSERT INTO hits(backend) VALUES(backend_name) RETURNING count...
    # Для демонстрации вернём фиктивное число
    return 1

@app.route("/")
def index():
    srv_id = request.cookies.get('srv_id', '')
    hits = get_hits_and_inc(BACKEND_NAME)
    html = render_template_string(TEMPLATE,
                                  backend=BACKEND_NAME,
                                  color=COLOR,
                                  hits=hits,
                                  ip=request.remote_addr,
                                  srv_id=srv_id)
    resp = make_response(html)
    # Если пришёл параметр route — ставим cookie с Domain (для тестов по IP)
    route = request.args.get('route')
    if route:
        # Укажите domain равный IP или домен, по которому тестируете
        resp.set_cookie('srv_id', route, max_age=3600, path='/', domain='158.160.79.161')
    # Добавляем заголовок для логирования в Angie
    resp.headers['X-Backend-Name'] = BACKEND_NAME
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

