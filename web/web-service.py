import logging
from flask import Flask, render_template, request, redirect # type: ignore
import requests # type: ignore
import json
import logging
import os

app =  Flask(__name__)
logger = logging.getLogger(__name__)

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Configuración básica del logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=os.path.join(log_dir, 'app.log'),
                    filemode='a')


@app.route("/")
def home():
    try:
        url = f"http://api-service:{81}/"
        res = requests.get(url).json()
        return render_template("table-with-pagination.html", profiles=res)
    except requests.exceptions.HTTPError as err:
        app.logger.debug(err)
        raise SystemExit(err)

@app.route("/reservation")
def reservation():
    try:
        url = f"http://api-service:{81}/reservation"
        res = requests.get(url).json()
        logging.info(f"recibido desde API {res}")
        return render_template("table-with-pagination-reservation.html", profiles=res)
    except requests.exceptions.HTTPError as err:
        app.logger.debug(err)
        raise SystemExit(err)
    
@app.route("/admin")
def admin():
    return render_template("admin.html",context={})

@app.route('/home_page', methods=['GET'])
def shortenurl():
    if request.method == 'GET':
        return redirect('/')


@app.route("/admin/delete_records")
def delete_records():
    try:
        url = f"http://api-service:{81}/admin/borrar_registros"
        res = requests.get(url).json()
        return redirect("/admin")
    except Exception:
        return {"message":"registros eliminados correctamente"}

@app.route("/admin/create_records")
def create_records():
    url = f"http://api-service:{81}/admin/crear_registros"
    res = requests.get(url).json()
    return redirect("/admin")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82, debug=True)