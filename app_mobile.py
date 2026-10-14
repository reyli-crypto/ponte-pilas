from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
import hashlib
import json
from datetime import datetime

app = FastAPI()

# ==========================================
# BASE DE DATOS Y RUTAS NORMALES
# ==========================================
def encriptar_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def preparar_base_datos():
    conexion = sqlite3.connect("midagri_mobile.db")
    cursor = conexion.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password_hash TEXT)')
    cursor.execute('INSERT OR IGNORE INTO usuarios (email, password_hash) VALUES (?, ?)', ("USMPFILIALNORTE@gmail.com", encriptar_password("alumno")))
    cursor.execute('DROP TABLE IF EXISTS precios_insumos')
    cursor.execute('CREATE TABLE precios_insumos (id INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, precio_actual REAL, precio_optimo REAL, unidad TEXT, estado TEXT, fuente TEXT)')
    
    insumos = [
        ("Aceite Vegetal Premium", "Abarrotes", 8.50, 7.80, "Litro", "rojo", "SISAP-MIDAGRI"),
        ("Harina Panadera", "Panadería", 2.90, 2.76, "Kilo", "amarillo", "SISAP-MIDAGRI"), 
        ("Harina Pastelera", "Panadería", 3.10, 2.96, "Kilo", "rojo", "SISAP-MIDAGRI"), 
        ("Azúcar Rubia", "Abarrotes", 3.60, 2.40, "Kilo", "rojo", "SISAP-MIDAGRI"), 
        ("Azúcar Blanca", "Abarrotes", 3.80, 2.50, "Kilo", "rojo", "SISAP-MIDAGRI"), 
        ("Azúcar Impalpable", "Abarrotes", 4.50, 4.00, "Kilo", "amarillo", "Mercado Mayorista"),
        ("Levadura Fresca", "Panadería", 13.00, 12.00, "Kilo", "verde", "SISAP-MIDAGRI"),
        ("Levadura Seca", "Panadería", 36.00, 33.00, "Kilo", "amarillo", "SISAP-MIDAGRI"),
        ("Polvo para Hornear", "Abarrotes", 8.00, 7.50, "Kilo", "verde", "Mercado Mayorista"),
        ("Bicarbonato de Sodio", "Abarrotes", 4.50, 4.00, "Kilo", "verde", "Mercado Mayorista"),
        ("Sal Fina", "Abarrotes", 1.20, 1.00, "Kilo", "verde", "SISAP-MIDAGRI"),
        ("Mantequilla", "Lácteos", 18.50, 16.00, "Kilo", "rojo", "Mercado Mayorista"),
        ("Margarina Multiusos", "Abarrotes", 8.50, 7.50, "Kilo", "amarillo", "SISAP-MIDAGRI"),
        ("Manteca Vegetal", "Panadería", 9.20, 8.50, "Kilo", "amarillo", "SISAP-MIDAGRI"), 
        ("Leche Líquida", "Lácteos", 3.50, 3.20, "Litro", "verde", "SISAP-MIDAGRI"),
        ("Leche en Polvo", "Lácteos", 22.00, 19.50, "Kilo", "amarillo", "Mercado Mayorista"),
        ("Huevos Rosados", "Avícola", 7.80, 6.50, "Kilo", "rojo", "SISAP-MIDAGRI"),
        ("Cacao en Polvo", "Repostería", 25.00, 22.00, "Kilo", "amarillo", "Mercado Mayorista"),
        ("Chocolate Cobertura", "Repostería", 18.00, 16.00, "Kilo", "verde", "Mercado Mayorista"),
        ("Manjar Blanco", "Repostería", 9.00, 8.00, "Kilo", "rojo", "Mercado Mayorista"), 
        ("Mermelada Horneable", "Repostería", 7.60, 7.00, "Kilo", "amarillo", "Mercado Mayorista"),
        ("Semillas de Ajonjolí", "Frutos Secos", 12.00, 10.50, "Kilo", "verde", "SISAP-MIDAGRI"),
        ("Nueces Peladas", "Frutos Secos", 45.00, 40.00, "Kilo", "rojo", "Mercado Mayorista"),
        ("Esencia de Vainilla", "Repostería", 4.00, 3.50, "Litro", "verde", "Mercado Mayorista"),
        ("Mejorador de Masa", "Panadería", 14.00, 12.50, "Kilo", "amarillo", "Mercado Mayorista")
    ]
    cursor.executemany('INSERT INTO precios_insumos (nombre, categoria, precio_actual, precio_optimo, unidad, estado, fuente) VALUES (?, ?, ?, ?, ?, ?, ?)', insumos)
    conexion.commit()
    conexion.close()

preparar_base_datos()

@app.get("/", response_class=HTMLResponse)
def pantalla_login():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Login - Ponte las Pilas</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root { --primary: #800020; --bg-color: #f5f5f5; --text-muted: #777; --white: #ffffff; }
            body { font-family: 'Roboto', sans-serif; background-color: #e0e0e0; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .app-container { width: 100%; max-width: 400px; height: 850px; background-color: var(--white); border-radius: 35px; box-shadow: 0 20px 50px rgba(0,0,0,0.3); overflow: hidden; position: relative; display: flex; flex-direction: column; border: 8px solid #222; }
            .header-login { background-color: var(--primary); color: white; padding: 60px 20px 40px; text-align: center; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            .logo-icon { font-size: 45px; margin-bottom: 15px; color: #f1c40f; }
            .header-login h1 { margin: 0; font-size: 28px; font-weight: 900; letter-spacing: -0.5px; }
            .header-login p { margin: 5px 0 0; font-size: 13px; opacity: 0.9; }
            .login-form { padding: 40px 25px; flex: 1; display: flex; flex-direction: column; gap: 20px; }
            .input-group { position: relative; }
            .input-group i { position: absolute; left: 15px; top: 16px; color: #aaa; font-size: 18px; }
            .input-group input { width: 100%; padding: 15px 15px 15px 45px; border: 1px solid #ddd; border-radius: 12px; font-size: 15px; box-sizing: border-box; outline: none; transition: 0.3s; }
            .input-group input:focus { border-color: var(--primary); }
            .btn-ingresar { background-color: var(--primary); color: white; border: none; border-radius: 12px; padding: 16px; font-size: 16px; font-weight: bold; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 10px; transition: 0.2s; }
            .btn-ingresar:active { transform: scale(0.98); }
            .footer { position: absolute; bottom: 25px; width: 100%; text-align: center; font-size: 12px; color: var(--text-muted); }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header-login">
                <i class="fa-solid fa-bolt logo-icon"></i>
                <h1>Ponte Pilas</h1>
                <p>Gestión Financiera & Abastecimiento B2B</p>
            </div>
            
            <form class="login-form" method="POST" action="/api/login">
                <div class="input-group">
                    <i class="fa-solid fa-envelope"></i>
                    <input type="email" name="email" value="USMPFILIALNORTE@gmail.com" required>
                </div>
                <div class="input-group">
                    <i class="fa-solid fa-lock"></i>
                    <input type="password" name="password" value="alumno" required>
                </div>
                <button type="submit" class="btn-ingresar">Acceder al Sistema <i class="fa-solid fa-arrow-right-to-bracket"></i></button>
            </form>
            <div class="footer">
                Proyecto Académico - <strong>USMP Filial Norte</strong>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/api/login")
def procesar_login(email: str = Form(...), password: str = Form(...)):
    conexion = sqlite3.connect("midagri_mobile.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND password_hash = ?", (email, encriptar_password(password)))
    usuario_valido = cursor.fetchone()
    conexion.close()
    
    if usuario_valido:
        return RedirectResponse(url="/dashboard", status_code=303)
    else:
        return HTMLResponse("<div style='text-align: center; margin-top: 50px;'><h2 style='color: #800020; font-family:sans-serif;'>Credenciales incorrectas</h2><a href='/'>Volver</a></div>")

@app.get("/dashboard", response_class=HTMLResponse)
def mostrar_dashboard():
    conexion = sqlite3.connect("midagri_mobile.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, categoria, precio_actual, precio_optimo, unidad, estado, fuente FROM precios_insumos")
    datos_insumos = cursor.fetchall()
    conexion.close()

    insumos_json = json.dumps([{"id": d[0], "nombre": d[1], "categoria": d[2], "precio": d[3], "optimo": d[4], "unidad": d[5], "estado": d[6], "fuente": d[7]} for d in datos_insumos])
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Dashboard - Ponte las Pilas</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root {{ 
                --primary: #800020; --bg-color: #f1f5f9; --text-main: #1e293b; --text-muted: #64748b; 
                --card-bg: #ffffff; --green: #10b981; --yellow: #f59e0b; --red: #ef4444; 
            }}
            body {{ font-family: 'Roboto', sans-serif; background-color: #e2e8f0; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }}
            .app-container {{ width: 100%; max-width: 400px; height: 850px; background-color: var(--bg-color); border-radius: 35px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3); overflow: hidden; position: relative; display: flex; flex-direction: column; border: 4px solid #1a202c; }}
            
            .header {{ background-color: var(--primary); color: white; padding: 40px 20px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); z-index: 10; }}
            .header-title {{ display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 900; }}
            .btn-logout {{ color: white; text-decoration: none; font-size: 14px; font-weight: 500; background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 8px; }}
            
            .content {{ flex: 1; overflow-y: auto; padding: 20px; padding-bottom: 90px; }}
            .content::-webkit-scrollbar {{ display: none; }}
            .view {{ display: none; animation: fadeIn 0.3s ease-out; }}
            .view.active {{ display: block; }}
            @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

            .section-title {{ font-size: 18px; font-weight: 900; margin-bottom: 18px; display: flex; align-items: center; gap: 8px; color: var(--primary); letter-spacing: -0.5px; }}
            
            .premium-card {{ background: var(--card-bg); border-radius: 20px; padding: 22px; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); position: relative; overflow: hidden; }}
            
            .pc-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }}
            .pc-icon-box {{ width: 45px; height: 45px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 20px; }}
            .pc-title-box {{ flex: 1; }}
            .pc-title {{ font-size: 16px; font-weight: 900; color: var(--text-main); margin: 0; line-height: 1.2; }}
            .pc-subtitle {{ font-size: 10px; color: var(--text-muted); font-weight: 600; display: flex; align-items: center; gap: 4px; margin-top: 3px; }}
            .pc-badge {{ padding: 5px 10px; border-radius: 8px; font-size: 9px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px; }}
            
            .pc-units {{ display: flex; gap: 6px; margin-bottom: 15px; background: #f1f5f9; padding: 6px; border-radius: 12px; }}
            .pc-pill {{ flex: 1; text-align: center; padding: 10px 4px; border-radius: 8px; border: none; background: transparent; color: #94a3b8; font-size: 12px; font-weight: 800; cursor: pointer; transition: all 0.3s ease; }}
            .pc-pill.active {{ background: #ffffff; color: var(--primary); box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
            
            .pc-footer {{ display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px dashed #e2e8f0; padding-top: 15px; }}
            .pc-savings-label {{ font-size: 10px; color: #94a3b8; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px; }}
            .pc-savings-val {{ font-size: 14px; font-weight: 900; color: var(--green); display: flex; align-items: center; gap: 4px; }}
            .pc-price {{ font-size: 28px; font-weight: 900; color: var(--text-main); font-family: 'Roboto Mono', monospace; letter-spacing: -1.5px; }}
            .pc-price span {{ font-size: 14px; color: var(--text-muted); font-weight: 700; vertical-align: top; }}

            .ahorro-card {{ background: linear-gradient(135deg, #800020 0%, #5a0016 100%); color: white; border-radius: 20px; padding: 25px 20px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; position: relative; overflow: hidden; box-shadow: 0 10px 20px rgba(128,0,32,0.15); }}
            .ahorro-card h4 {{ margin: 0 0 5px 0; font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.9); }}
            .ahorro-card .monto {{ font-size: 38px; font-weight: 900; margin: 0; font-family: monospace; letter-spacing: -2px; }}
            .live-dot {{ display: inline-block; width: 8px; height: 8px; background-color: #2ecc71; border-radius: 50%; margin-left: 8px; animation: blink 1.5s infinite; vertical-align: middle; }}
            @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
            
            .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 24px; }}
            .stat-box {{ background: var(--card-bg); border-radius: 16px; padding: 18px; text-align: left; box-shadow: 0 4px 10px rgba(0,0,0,0.03); position: relative; overflow: hidden; }}
            
            .search-container {{ background: var(--card-bg); border-radius: 20px; padding: 20px; margin-bottom: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }}
            .search-select {{ width: 100%; padding: 14px; border-radius: 12px; border: 2px solid #e2e8f0; font-family: 'Roboto'; font-size: 14px; font-weight: 700; color: #333; outline: none; margin-bottom: 15px; appearance: none; background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="%23800020" viewBox="0 0 16 16"><path d="M8 11.5l-5-5h10l-5 5z"/></svg>') no-repeat right 15px center/12px; background-color: #f8fafc; }}
            .search-select:focus {{ border-color: var(--primary); }}
            .search-result {{ display: none; background: #f8fafc; border-radius: 12px; padding: 15px; border-left: 5px solid var(--primary); animation: fadeIn 0.3s; }}
            
            .charts-slider {{ display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; }}
            .charts-slider::-webkit-scrollbar {{ height: 4px; }}
            .charts-slider::-webkit-scrollbar-thumb {{ background-color: #cbd5e1; border-radius: 10px; }}
            .mini-chart-card {{ min-width: 250px; background: var(--card-bg); border-radius: 20px; padding: 18px; scroll-snap-align: start; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }}
            .mini-chart-title {{ font-size: 14px; font-weight: 800; color: #333; margin-bottom: 2px; display: flex; justify-content: space-between; }}
            .mini-chart-subtitle {{ font-size: 11px; color: var(--text-muted); font-weight: 600; }}

            .midagri-badge {{ display: inline-flex; align-items: center; gap: 6px; background: #ecfdf5; color: #059669; padding: 6px 14px; border-radius: 20px; font-size: 10px; font-weight: 800; margin-bottom: 20px; border: 1px solid #a7f3d0; }}

            .calc-search-box {{ position: relative; margin-bottom: 0; flex: 1; }}
            .calc-search-box i {{ position: absolute; left: 15px; top: 14px; color: #94a3b8; font-size: 15px; }}
            .calc-search-input {{ width: 100%; padding: 14px 14px 14px 45px; border-radius: 12px; border: 2px solid #e2e8f0; font-size: 14px; font-weight: 600; outline: none; box-sizing: border-box; transition: 0.3s; background-color: #f8fafc; }}
            .calc-search-input:focus {{ border-color: var(--primary); background-color: white; box-shadow: 0 0 0 3px rgba(128,0,32,0.05); }}
            
            .btn-clear-cart {{ background: #fee2e2; color: #ef4444; border: none; padding: 0 18px; border-radius: 12px; font-size: 13px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: 0.2s; }}
            .btn-clear-cart:active {{ transform: scale(0.95); background: #fca5a5; }}

            .calc-row-container {{ padding: 16px 0; border-bottom: 1px solid #f1f5f9; }}
            .calc-title {{ font-size: 15px; font-weight: 900; color: var(--text-main); margin-bottom: 10px; line-height: 1.2; }}
            .calc-controls {{ display: flex; justify-content: space-between; align-items: center; gap: 10px; }}
            
            .cart-unit-select {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 4px 8px; font-size: 11px; font-weight: 800; color: var(--text-main); outline: none; cursor: pointer; transition: 0.2s; max-width: 110px; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; }}
            .cart-unit-select:focus {{ border-color: var(--primary); }}
            
            .qty-control {{ display: flex; align-items: center; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; height: 38px; flex-shrink: 0; min-width: 105px; justify-content: space-between; }}
            .qty-btn {{ background: transparent; border: none; width: 35px; height: 100%; display: flex; justify-content: center; align-items: center; font-size: 16px; color: var(--primary); cursor: pointer; font-weight: 900; transition: 0.2s; padding: 0; }}
            .qty-btn:active {{ background: #e2e8f0; }}
            .calc-input {{ width: 35px; border: none; background: transparent; text-align: center; font-weight: 900; font-size: 16px; color: #333; outline: none; padding: 0; }}
            
            .calc-subtotal {{ text-align: right; min-width: 85px; font-weight: 900; font-size: 16px; color: var(--text-main); flex-shrink: 0; }}

            .btn-sync {{ background: var(--green); color: white; width: 100%; border: none; padding: 18px; border-radius: 16px; font-size: 16px; font-weight: 900; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 24px; box-shadow: 0 10px 15px -3px rgba(16,185,129,0.3); transition: 0.2s; letter-spacing: 0.5px; }}
            .btn-sync:active {{ transform: scale(0.98); }}

            .table-container {{ overflow-x: auto; margin-top: 10px; border-radius: 12px; border: 1px solid #e2e8f0; background: white; }}
            .niif-table {{ width: 100%; border-collapse: collapse; font-size: 12px; text-align: left; }}
            .niif-table th {{ background-color: var(--primary); color: white; padding: 14px 12px; font-weight: 800; white-space: nowrap; }}
            .niif-table td {{ padding: 14px 12px; border-bottom: 1px solid #f1f5f9; font-weight: 600; color: var(--text-main); }}

            .bottom-nav {{ position: absolute; bottom: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-top: 1px solid #e2e8f0; display: flex; justify-content: space-around; padding: 12px 0 25px 0; z-index: 10; }}
            .nav-item {{ text-align: center; color: #cbd5e1; cursor: pointer; flex: 1; transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
            .nav-item i {{ font-size: 22px; display: block; margin-bottom: 4px; transition: 0.3s; }}
            .nav-item span {{ font-size: 10px; font-weight: 800; }}
            .nav-item.active {{ color: var(--primary); }}
            .nav-item.active i {{ transform: translateY(-4px); filter: drop-shadow(0 4px 6px rgba(128,0,32,0.2)); }}

            .modal {{ display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); justify-content: center; align-items: center; z-index: 100; }}
            .modal-content {{ background: white; padding: 25px; border-radius: 20px; width: 80%; max-height: 70%; overflow-y: auto; text-align: center; }}
            .btn-close-modal {{ width: 100%; background: var(--primary); color: white; border: none; padding: 14px; border-radius: 12px; font-weight: bold; margin-top: 20px; cursor: pointer; }}

            #toast {{ visibility: hidden; min-width: 250px; background-color: #2E7D32; color: #fff; text-align: center; border-radius: 12px; padding: 16px; position: absolute; z-index: 100; left: 50%; bottom: 100px; transform: translateX(-50%); font-size: 14px; font-weight: 600; box-shadow: 0 10px 20px rgba(0,0,0,0.15); display: flex; align-items: center; justify-content: center; gap: 10px; }}
            #toast.show {{ visibility: visible; animation: fadein 0.5s, fadeout 0.5s 3.5s; }}
            @keyframes fadein {{ from {{ bottom: 80px; opacity: 0; }} to {{ bottom: 100px; opacity: 1; }} }}
            @keyframes fadeout {{ from {{ bottom: 100px; opacity: 1; }} to {{ bottom: 80px; opacity: 0; }} }}

            /* ESTILOS DE LA PESTAÑA MÁS */
            .profile-card {{ display: flex; align-items: center; gap: 16px; margin-bottom: 25px; padding: 20px; background: var(--card-bg); border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #f1f5f9; }}
            .profile-avatar {{ width: 56px; height: 56px; border-radius: 16px; background: linear-gradient(135deg, var(--primary) 0%, #5a0016 100%); color: white; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; }}
            .profile-info h4 {{ margin: 0 0 4px 0; font-size: 18px; font-weight: 900; color: var(--text-main); }}
            .profile-info p {{ margin: 0; font-size: 12px; font-weight: 600; color: var(--text-muted); }}

            .settings-group {{ background: var(--card-bg); border-radius: 20px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #f1f5f9; }}
            .setting-item {{ display: flex; align-items: center; justify-content: space-between; padding: 18px 20px; border-bottom: 1px solid #f1f5f9; cursor: pointer; transition: background 0.2s; }}
            .setting-item:active {{ background: #f8fafc; }}
            .setting-item:last-child {{ border-bottom: none; }}
            .setting-left {{ display: flex; align-items: center; gap: 16px; }}
            .setting-icon {{ width: 42px; height: 42px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 18px; }}
            .setting-text {{ font-size: 15px; font-weight: 800; color: var(--text-main); line-height: 1.2; }}
            .setting-subtext {{ font-size: 11px; color: var(--text-muted); font-weight: 600; margin-top: 4px; }}
            .setting-chevron {{ color: #cbd5e1; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header">
                <div class="header-title" style="margin-left: 110px;"><i class="fa-solid fa-bolt" style="color: #f1c40f;"></i> San José</div>
                <a href="/" class="btn-logout"><i class="fa-solid fa-right-from-bracket"></i></a>
            </div>

            <div class="content">
                <!-- VISTA 1: INICIO -->
                <div id="view-inicio" class="view active">
                    <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-weight: 700;">
                        <span>Resumen Financiero</span>
                        <span style="font-size: 10px; background: #e2e8f0; padding: 4px 10px; border-radius: 12px; color: #334155;">OCTUBRE 2026</span>
                    </div>
                    
                    <div class="ahorro-card">
                        <div>
                            <h4>Ahorro Estimado (En vivo) <span class="live-dot"></span></h4>
                            <p class="monto" id="live-ahorro">S/ 485.50</p>
                        </div>
                        <i class="fa-solid fa-chart-line" style="font-size: 45px; opacity: 0.15; position: absolute; right: 20px; top: 25px;"></i>
                    </div>

                    <div class="grid-2">
                        <div class="stat-box" id="sunat-box">
                            <div style="font-size: 10px; color: var(--text-muted); font-weight: 800; margin-bottom: 8px;">TIPO DE CAMBIO (SUNAT)</div>
                            <div style="display: flex; gap: 15px;">
                                <div><div style="font-size: 9px; color: #94a3b8; font-weight:800;">COMPRA</div><div style="font-size: 16px; font-weight: 900; color: var(--text-main);">S/ 3.44</div></div>
                                <div><div style="font-size: 9px; color: #94a3b8; font-weight:800;">VENTA</div><div style="font-size: 16px; font-weight: 900; color: var(--text-main);">S/ 3.45</div></div>
                            </div>
                        </div>
                        <div class="stat-box">
                            <div style="font-size: 10px; color: var(--text-muted); font-weight: 800; margin-bottom: 8px;">FLETE / DIÉSEL</div>
                            <div style="font-size: 22px; font-weight: 900; color: var(--text-main);">S/ 16.20 <i class="fa-solid fa-caret-down" style="font-size:14px; color:var(--green);"></i></div>
                        </div>
                    </div>

                    <div class="search-container">
                        <div style="font-size: 14px; font-weight: 900; color: var(--primary); margin-bottom: 15px;"><i class="fa-solid fa-magnifying-glass"></i> Buscador B2B</div>
                        <select id="quick-search-select" class="search-select" onchange="actualizarConsultaRapida()"></select>
                        <div id="quick-search-result" class="search-result">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                                <div><div id="qs-name" style="font-size: 16px; font-weight: 900; color: var(--text-main);">Insumo</div><div id="qs-unit" style="font-size: 12px; color: var(--text-muted); font-weight: 700;">Unidad</div></div>
                                <div style="text-align: right;"><div id="qs-price" style="font-size: 24px; font-weight: 900; font-family: monospace;">S/ 0.00</div><div id="qs-status" style="display: inline-block; font-size: 9px; font-weight: 900; padding: 4px 10px; border-radius: 8px; color: white; margin-top: 4px;">ESTADO</div></div>
                            </div>
                            <div id="qs-rec" style="font-size: 12px; font-weight: 700; padding-top: 12px; border-top: 1px solid #e2e8f0;"></div>
                        </div>
                    </div>

                    <div class="section-title"><i class="fa-solid fa-server"></i> Terminal de Insumos</div>
                    <div class="charts-slider" id="charts-slider-render"></div>
                </div>

                <!-- VISTA 2: INSUMOS -->
                <div id="view-insumos" class="view">
                    <h3 class="section-title"><i class="fa-solid fa-boxes-stacked"></i> Abastecimiento Mayorista</h3>
                    <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 20px; font-weight: 500; line-height: 1.4;">Selecciona la presentación para calcular el impacto financiero en tiempo real.</p>
                    <div class="midagri-badge" id="fecha-act">Actualizado: {fecha_actual}</div>
                    <div id="lista-insumos-render" style="padding-bottom: 50px;"></div>
                </div>

                <!-- VISTA 3: SIMULADOR (INDEPENDIENTE) -->
                <div id="view-simulador" class="view">
                    <h3 class="section-title"><i class="fa-solid fa-calculator"></i> Proforma de Compras</h3>
                    <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 20px; font-weight: 500; line-height: 1.4;">Ajusta unidades y cantidades para simular presupuestos.</p>
                    
                    <div class="premium-card" style="margin-bottom: 50px; padding: 20px;">
                        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                            <div class="calc-search-box">
                                <i class="fa-solid fa-magnifying-glass"></i>
                                <input type="text" id="calc-filter-input" class="calc-search-input" placeholder="Buscar insumo..." onkeyup="filtrarCalculadora()">
                            </div>
                            <button class="btn-clear-cart" onclick="limpiarCalculadora()">
                                <i class="fa-solid fa-trash-can"></i> Vaciar
                            </button>
                        </div>

                        <div id="calculadora-render" style="max-height: 320px; overflow-y: auto; padding-right: 8px;"></div>
                        
                        <div style="border: 2px solid var(--primary); border-radius: 20px; padding: 22px; margin-top: 25px; box-shadow: 0 4px 15px rgba(128,0,32,0.05);">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 15px;">
                                <span style="font-size: 14px; font-weight: 700; color: var(--text-muted);">Total a Invertir (Gasto)</span>
                                <span id="calc-inversion" style="font-size: 18px; font-weight: 900; color: var(--text-main); font-family: monospace;">S/ 0.00</span>
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-size: 12px; font-weight: 800; color: var(--green); text-transform: uppercase; letter-spacing: 1px;">Ahorro Generado</div>
                                    <div style="font-size: 10px; color: var(--text-muted); font-weight: 600; margin-top: 3px;">Optimización MIDAGRI</div>
                                </div>
                                <div id="calc-total" style="font-size: 28px; font-weight: 900; color: var(--green); font-family: monospace; letter-spacing: -1px;">S/ 0.00</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- VISTA 4: REPORTES -->
                <div id="view-reportes" class="view">
                    <h3 class="section-title"><i class="fa-solid fa-chart-pie"></i> Análisis y Forecasting</h3>
                    
                    <div class="premium-card" style="padding: 20px 18px;">
                        <div class="section-title" style="padding-left: 5px; font-size: 14px;">Top 5 Impactos de Mercado (S/)</div>
                        <div style="height: 180px;"><canvas id="barChart"></canvas></div>
                    </div>

                    <div class="premium-card" style="padding: 20px 18px; margin-bottom: 50px;">
                        <div class="section-title" style="padding-left: 5px; font-size: 14px;"><i class="fa-solid fa-table"></i> Proyección NIIF (+7 Días)</div>
                        <div class="table-container">
                            <table class="niif-table">
                                <thead><tr><th>Insumo</th><th>Hace 7D</th><th>Actual</th><th>Proyección</th></tr></thead>
                                <tbody id="tabla-proyecciones-render"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- VISTA 5: MÁS -->
                <div id="view-mas" class="view">
                    <h3 class="section-title"><i class="fa-solid fa-sliders"></i> Panel de Control</h3>
                    
                    <div class="profile-card">
                        <div class="profile-avatar">SJ</div>
                        <div class="profile-info">
                            <h4>San José</h4>
                            <p>Cuenta Corporativa • Chiclayo</p>
                        </div>
                    </div>

                    <button class="btn-sync" onclick="iniciarScrapingMIDAGRI()">
                        <i class="fa-solid fa-bolt"></i> Sincronizar MIDAGRI / SUNAT
                    </button>

                    <div class="settings-group">
                        <div class="setting-item" onclick="abrirModalEtica()">
                            <div class="setting-left">
                                <div class="setting-icon" style="background: #fef2f2; color: #ef4444;"><i class="fa-solid fa-scale-balanced"></i></div>
                                <div>
                                    <div class="setting-text">Transparencia y Ética</div>
                                    <div class="setting-subtext">Políticas de uso de datos NIIF</div>
                                </div>
                            </div>
                            <i class="fa-solid fa-chevron-right setting-chevron"></i>
                        </div>
                        
                        <div class="setting-item" onclick="alert('Generando reporte en PDF para auditoría...')">
                            <div class="setting-left">
                                <div class="setting-icon" style="background: #eff6ff; color: #3b82f6;"><i class="fa-solid fa-file-pdf"></i></div>
                                <div>
                                    <div class="setting-text">Exportar Historial (PDF)</div>
                                    <div class="setting-subtext">Documentación de Auditoría</div>
                                </div>
                            </div>
                            <i class="fa-solid fa-chevron-right setting-chevron"></i>
                        </div>

                        <div class="setting-item" onclick="alert('Vinculando con WhatsApp Business...')">
                            <div class="setting-left">
                                <div class="setting-icon" style="background: #ecfdf5; color: #10b981;"><i class="fa-brands fa-whatsapp"></i></div>
                                <div>
                                    <div class="setting-text">Alertas Financieras</div>
                                    <div class="setting-subtext">Notificaciones de sobrecostos</div>
                                </div>
                            </div>
                            <i class="fa-solid fa-chevron-right setting-chevron"></i>
                        </div>
                    </div>

                    <div style="text-align: center; margin-top: 35px; padding: 20px;">
                        <i class="fa-solid fa-building-columns" style="font-size: 40px; color: var(--primary); margin-bottom: 15px; opacity: 0.8;"></i>
                        <h4 style="color: var(--primary); font-weight: 900; margin: 0; font-size: 16px;">USMP Filial Norte - Chiclayo</h4>
                        <p style="font-size: 11px; color: var(--text-muted); margin-top: 5px; font-weight: 600; line-height: 1.4;">Proyecto de Contabilidad y Finanzas<br>Versión 2.0.0 (Desacoplada)</p>
                    </div>
                </div>
            </div>

            <!-- MODAL ÉTICA -->
            <div id="modal-etica" class="modal">
                <div class="modal-content">
                    <i class="fa-solid fa-scale-balanced" style="font-size: 40px; color: var(--primary); margin-bottom: 15px;"></i>
                    <h3 style="color: var(--primary); margin-bottom: 15px;">Política de Ética y Transparencia</h3>
                    <p style="font-size: 13px; line-height: 1.5; color: #555; text-align: justify;">
                        <strong>1. Fuente de Datos Oficial:</strong> Precios extraídos del <b>SISAP</b> (MIDAGRI) y SUNAT.<br><br>
                        <strong>2. Trazabilidad Contable Total:</strong> Todas las proyecciones financieras, tablas NIIF y gráficos de impacto se calculan rigurosamente en base a la unidad seleccionada.
                    </p>
                    <button class="btn-close-modal" onclick="cerrarModalEtica()">Entendido</button>
                </div>
            </div>

            <div id="toast"><i class="fa-solid fa-cloud-arrow-down"></i> <span id="toast-msg">Mensaje</span></div>

            <div class="bottom-nav">
                <div class="nav-item active" onclick="switchNav('inicio', this)"><i class="fa-solid fa-chart-pie"></i><span>Resumen</span></div>
                <div class="nav-item" onclick="switchNav('insumos', this)"><i class="fa-solid fa-store"></i><span>Mercado</span></div>
                <div class="nav-item" onclick="switchNav('simulador', this)"><i class="fa-solid fa-calculator"></i><span>Proforma</span></div>
                <div class="nav-item" onclick="switchNav('reportes', this)"><i class="fa-solid fa-chart-line"></i><span>Reportes</span></div>
                <div class="nav-item" onclick="switchNav('mas', this)"><i class="fa-solid fa-bars"></i><span>Más</span></div>
            </div>
        </div>

        <script>
            let datosBD = {insumos_json};
            let chartsInstancias = [];
            let barChartInstancia = null; 
            
            function getIconoCategoria(categoria) {{
                const iconos = {{
                    'Abarrotes': 'fa-box-open', 'Panadería': 'fa-bread-slice', 'Lácteos': 'fa-cheese',
                    'Avícola': 'fa-egg', 'Repostería': 'fa-cookie-bite', 'Frutos Secos': 'fa-seedling'
                }};
                return iconos[categoria] || 'fa-box';
            }}

            function obtenerVariantesWholesale(nombre) {{
                if(nombre.includes("Harina") || nombre.includes("Azúcar")) return [{{label: 'Kilo', mult: 1}}, {{label: 'Saco 25kg', mult: 25}}, {{label: 'Saco 50kg', mult: 50}}];
                if(nombre.includes("Aceite") || nombre.includes("Vainilla")) return [{{label: 'Litro', mult: 1}}, {{label: 'Galón', mult: 3.78}}, {{label: 'Bidón 20L', mult: 20}}];
                if(nombre.includes("Manteca") || nombre.includes("Margarina") || nombre.includes("Mermelada") || nombre.includes("Manjar") || nombre.includes("Polvo") || nombre.includes("Cacao")) return [{{label: 'Kilo', mult: 1}}, {{label: 'Balde 5kg', mult: 5}}, {{label: 'Caja 10kg', mult: 10}}];
                if(nombre.includes("Huevos")) return [{{label: 'Kilo', mult: 1}}, {{label: 'Docena', mult: 0.8}}, {{label: 'Jaba 30kg', mult: 30}}];
                if(nombre.includes("Levadura")) return [{{label: 'Bloque 500g', mult: 0.5}}, {{label: 'Caja 10kg', mult: 10}}];
                if(nombre.includes("Leche")) return [{{label: 'Litro', mult: 1}}, {{label: 'Six-Pack', mult: 6}}, {{label: 'Caja 24u', mult: 24}}];
                return [{{label: 'Kilo', mult: 1}}, {{label: 'Docena', mult: 12}}]; 
            }}

            datosBD.forEach(item => {{
                item.variantes = obtenerVariantesWholesale(item.nombre);
                item.unidadSeleccionada = item.variantes.length - 1; 
            }});

            let ahorroBase = 485.50;
            setInterval(() => {{
                ahorroBase += (Math.random() * 0.20) - 0.05;
                document.getElementById('live-ahorro').innerText = 'S/ ' + ahorroBase.toFixed(2);
            }}, 2500);

            function switchNav(viewName, element) {{
                document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
                document.getElementById('view-' + viewName).classList.add('active');
                document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
                element.classList.add('active');
            }}

            function abrirModalEtica() {{ document.getElementById('modal-etica').style.display = 'flex'; }}
            function cerrarModalEtica() {{ document.getElementById('modal-etica').style.display = 'none'; }}
            function mostrarToast(mensaje) {{
                const toast = document.getElementById("toast");
                document.getElementById("toast-msg").innerText = mensaje;
                toast.className = "show";
                setTimeout(function(){{ toast.className = toast.className.replace("show", ""); }}, 4000);
            }}

            window.cambiarUnidad = function(index, varIndex) {{
                datosBD[index].unidadSeleccionada = parseInt(varIndex);
                
                let contentEl = document.querySelector('.content');
                let scrollPos = contentEl ? contentEl.scrollTop : 0;
                renderizarMercado();
                if(contentEl) contentEl.scrollTop = scrollPos;
                
                let selectCart = document.getElementById(`cart-select-${{index}}`);
                if(selectCart) selectCart.value = varIndex;
                actualizarPrecioUnidadCart(index);
                calcularSumaTotal();
                
                renderizarReporteNIIF(); 
                renderizarGraficoVolatilidad(); 
            }}

            window.cambiarUnidadCart = function(index, varIndex) {{
                datosBD[index].unidadSeleccionada = parseInt(varIndex);
                actualizarPrecioUnidadCart(index);
                calcularSumaTotal();
                
                let contentEl = document.querySelector('.content');
                let scrollPos = contentEl ? contentEl.scrollTop : 0;
                renderizarMercado(); 
                if(contentEl) contentEl.scrollTop = scrollPos;
                
                renderizarReporteNIIF(); 
                renderizarGraficoVolatilidad(); 
            }}

            window.cambiarCant = function(index, delta) {{
                let input = document.getElementById(`input-${{index}}`);
                let val = parseInt(input.value || 0) + delta;
                if(val < 0) val = 0;
                input.value = val > 0 ? val : '';
                calcularSumaTotal();
            }}

            window.inputDirecto = function(index) {{
                calcularSumaTotal();
            }}

            window.limpiarCalculadora = function() {{
                datosBD.forEach((item, index) => {{
                    let inputEl = document.getElementById(`input-${{index}}`);
                    if(inputEl) inputEl.value = '';
                }});
                calcularSumaTotal();
                mostrarToast("Proforma vaciada localmente.");
            }}

            function actualizarPrecioUnidadCart(index) {{
                let item = datosBD[index];
                let vAct = item.variantes[item.unidadSeleccionada];
                let precioUnidad = (item.precio * vAct.mult).toFixed(2);
                let priceDisplay = document.getElementById(`precio-unidad-display-${{index}}`);
                if(priceDisplay) priceDisplay.innerText = `S/ ${{precioUnidad}}`;
            }}

            function crearMicroGrafico(ctxId, color, dataPoints) {{
                let ctx = document.getElementById(ctxId).getContext('2d');
                let chart = new Chart(ctx, {{
                    type: 'line', 
                    data: {{ 
                        labels: ['Sem1', 'Sem2', 'Sem3', 'Hoy'], 
                        datasets: [{{ data: dataPoints, borderColor: color, tension: 0.4, borderWidth: 3, pointRadius: 4, pointBackgroundColor: color }}] 
                    }},
                    options: {{ 
                        responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, 
                        scales: {{ 
                            x: {{ display: true, grid: {{ display: true, color: '#f1f5f9' }}, ticks: {{ font: {{ size: 10 }}, color: '#94a3b8' }} }}, 
                            y: {{ display: true, grid: {{ display: true, color: '#f1f5f9' }}, ticks: {{ font: {{ size: 10 }}, color: '#94a3b8', maxTicksLimit: 4 }} }} 
                        }}, 
                        layout: {{ padding: 5 }} 
                    }}
                }});
                chartsInstancias.push(chart);
            }}

            function renderizarReporteNIIF() {{
                const tablaHTML = document.getElementById('tabla-proyecciones-render');
                tablaHTML.innerHTML = '';
                
                datosBD.forEach((item) => {{
                    let vAct = item.variantes[item.unidadSeleccionada];
                    let precioBase = parseFloat(item.precio * vAct.mult);
                    let precioProy = (precioBase * (1 + (Math.random() * 0.12 - 0.06))).toFixed(2);
                    let precioAnt = (precioBase * 0.95).toFixed(2);
                    let icon = parseFloat(precioProy) > precioBase ? '<i class="fa-solid fa-arrow-trend-up" style="color:var(--red);"></i>' : '<i class="fa-solid fa-arrow-trend-down" style="color:var(--green);"></i>';
                    
                    tablaHTML.innerHTML += `
                        <tr>
                            <td style="font-weight: 800; line-height: 1.2;">${{item.nombre}} <br><span style="font-size:9px; color:var(--primary); font-weight:900;">${{vAct.label}}</span></td>
                            <td style="color: var(--text-muted);">S/ ${{precioAnt}}</td>
                            <td style="color: var(--text-main); font-weight:900;">S/ ${{precioBase.toFixed(2)}}</td>
                            <td style="font-weight:900;">S/ ${{precioProy}} ${{icon}}</td>
                        </tr>`;
                }});
            }}

            function renderizarGraficoVolatilidad() {{
                let volatilidades = datosBD.map(item => {{
                    let vAct = item.variantes[item.unidadSeleccionada];
                    let varSoles = (item.precio - item.optimo) * vAct.mult;
                    let nombreCorto = item.nombre.length > 12 ? item.nombre.substring(0, 12) + '...' : item.nombre;
                    return {{ nombre: `${{nombreCorto}} (${{vAct.label}})`, variacion: parseFloat(varSoles.toFixed(2)), absVar: Math.abs(varSoles) }};
                }});

                volatilidades.sort((a, b) => b.absVar - a.absVar);
                let top5 = volatilidades.slice(0, 5);

                let labels = top5.map(v => v.nombre);
                let data = top5.map(v => v.variacion);
                let colors = top5.map(v => v.variacion > 0 ? '#ef4444' : '#10b981'); 

                if (barChartInstancia) {{ barChartInstancia.destroy(); }}

                barChartInstancia = new Chart(document.getElementById('barChart').getContext('2d'), {{
                    type: 'bar',
                    data: {{ labels: labels, datasets: [{{ data: data, backgroundColor: colors, borderRadius: 6 }}] }},
                    options: {{
                        responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }},
                        scales: {{
                            x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 9 }}, color: '#64748b', maxRotation: 45, minRotation: 45 }} }},
                            y: {{ grid: {{ borderDash: [4, 4], color: '#e2e8f0' }}, ticks: {{ font: {{ size: 10 }}, color: '#94a3b8' }} }}
                        }}
                    }}
                }});
            }}

            function actualizarConsultaRapida() {{
                const select = document.getElementById('quick-search-select');
                const resultDiv = document.getElementById('quick-search-result');
                if (select.value === "") {{ resultDiv.style.display = 'none'; return; }}
                
                const item = datosBD[select.value];
                let varAct = item.variantes[item.unidadSeleccionada];
                
                document.getElementById('qs-name').innerText = item.nombre;
                document.getElementById('qs-unit').innerText = "Por " + varAct.label;
                document.getElementById('qs-price').innerText = "S/ " + (item.precio * varAct.mult).toFixed(2);
                
                const statusEl = document.getElementById('qs-status');
                const recEl = document.getElementById('qs-rec');
                
                if (item.estado === 'rojo') {{
                    statusEl.style.backgroundColor = 'var(--red)'; statusEl.innerText = "SOBRECOSTO"; resultDiv.style.borderLeftColor = 'var(--red)'; recEl.style.color = 'var(--red)';
                    recEl.innerHTML = '<i class="fa-solid fa-hand"></i> Frenar compras masivas. Riesgo alto.';
                }} else if (item.estado === 'verde') {{
                    statusEl.style.backgroundColor = 'var(--green)'; statusEl.innerText = "ÓPTIMO"; resultDiv.style.borderLeftColor = 'var(--green)'; recEl.style.color = 'var(--green)';
                    recEl.innerHTML = '<i class="fa-solid fa-cart-arrow-down"></i> Excelente momento para abastecer.';
                }} else {{
                    statusEl.style.backgroundColor = 'var(--yellow)'; statusEl.innerText = "ATENCIÓN"; resultDiv.style.borderLeftColor = 'var(--yellow)'; recEl.style.color = '#d35400';
                    recEl.innerHTML = '<i class="fa-solid fa-scale-balanced"></i> Comprar estrictamente lo necesario.';
                }}
                resultDiv.style.display = 'block';
            }}

            function renderizarMercado() {{
                const listaHTML = document.getElementById('lista-insumos-render');
                listaHTML.innerHTML = '';
                datosBD.forEach((item, index) => {{
                    let cBase = item.estado === 'rojo' ? 'var(--red)' : item.estado === 'amarillo' ? 'var(--yellow)' : 'var(--green)';
                    let cLight = item.estado === 'rojo' ? '#fee2e2' : item.estado === 'amarillo' ? '#fef3c7' : '#d1fae5';
                    let txtStatus = item.estado === 'rojo' ? 'SOBRECOSTO' : item.estado === 'amarillo' ? 'ATENCIÓN' : 'COMPRAR';
                    
                    let botones = '';
                    item.variantes.forEach((v, vIdx) => {{
                        let active = vIdx === item.unidadSeleccionada ? 'active' : '';
                        botones += `<button class="pc-pill ${{active}}" onclick="cambiarUnidad(${{index}}, ${{vIdx}})">${{v.label}}</button>`;
                    }});

                    let vAct = item.variantes[item.unidadSeleccionada];
                    let precioCalc = item.precio * vAct.mult;
                    let ahorroCalc = ((item.precio - item.optimo) * vAct.mult).toFixed(2);
                    let ahorroDisplay = ahorroCalc > 0 ? `<div class="pc-savings"><span class="pc-savings-label">Evitas gastar</span><span class="pc-savings-val"><i class="fa-solid fa-shield-check"></i> S/ ${{ahorroCalc}}</span></div>` : `<div></div>`;

                    listaHTML.innerHTML += `
                        <div class="premium-card" id="item-${{index}}" style="border-left: 6px solid ${{cBase}};">
                            <div class="pc-header">
                                <div class="pc-icon-box" style="background:${{cLight}}; color:${{cBase}};">
                                    <i class="fa-solid ${{getIconoCategoria(item.categoria)}}"></i>
                                </div>
                                <div class="pc-title-box">
                                    <h4 class="pc-title">${{item.nombre}}</h4>
                                    <span class="pc-subtitle"><i class="fa-solid fa-building-wheat"></i> ${{item.fuente}}</span>
                                </div>
                                <div class="pc-badge" style="background:${{cLight}}; color:${{cBase}};">${{txtStatus}}</div>
                            </div>
                            <div class="pc-units">${{botones}}</div>
                            <div class="pc-footer">
                                ${{ahorroDisplay}}
                                <div class="pc-price"><span>S/</span> ${{precioCalc.toFixed(2)}}</div>
                            </div>
                        </div>`;
                }});
            }}

            window.filtrarCalculadora = function() {{
                let filtro = document.getElementById('calc-filter-input').value.toLowerCase();
                let items = document.querySelectorAll('.calc-row-container');
                items.forEach(item => {{
                    let nombre = item.getAttribute('data-name').toLowerCase();
                    item.style.display = nombre.includes(filtro) ? 'block' : 'none';
                }});
            }}

            function renderizarCalculadora() {{
                const calcHTML = document.getElementById('calculadora-render');
                calcHTML.innerHTML = '';
                
                datosBD.forEach((item, index) => {{
                    let vAct = item.variantes[item.unidadSeleccionada];
                    let precioUnidad = (item.precio * vAct.mult).toFixed(2);
                    
                    let opcionesDropdown = '';
                    item.variantes.forEach((v, vIdx) => {{
                        let sel = (vIdx === item.unidadSeleccionada) ? 'selected' : '';
                        opcionesDropdown += `<option value="${{vIdx}}" ${{sel}}>${{v.label}}</option>`;
                    }});

                    calcHTML.innerHTML += `
                        <div class="calc-row-container" data-name="${{item.nombre}}">
                            <div class="calc-title">${{item.nombre}}</div>
                            <div class="calc-controls">
                                <div style="display: flex; flex-direction: column; gap: 4px; flex: 1;">
                                    <select id="cart-select-${{index}}" class="cart-unit-select" onchange="cambiarUnidadCart(${{index}}, this.value)">
                                        ${{opcionesDropdown}}
                                    </select>
                                    <span id="precio-unidad-display-${{index}}" style="font-size: 13px; font-weight: 900; color: var(--primary);">S/ ${{precioUnidad}}</span>
                                </div>
                                <div class="qty-control">
                                    <button class="qty-btn" onclick="cambiarCant(${{index}}, -1)"><i class="fa-solid fa-minus"></i></button>
                                    <input type="number" class="calc-input" id="input-${{index}}" oninput="inputDirecto(${{index}})" min="0">
                                    <button class="qty-btn" onclick="cambiarCant(${{index}}, 1)"><i class="fa-solid fa-plus"></i></button>
                                </div>
                                <div class="calc-subtotal" id="inversion-${{index}}">
                                    S/ 0.00
                                </div>
                            </div>
                        </div>`;
                }});
                calcularSumaTotal();
                filtrarCalculadora(); 
            }}

            function inicializarVistas() {{
                const sliderHTML = document.getElementById('charts-slider-render');
                const searchSelect = document.getElementById('quick-search-select');
                
                chartsInstancias.forEach(chart => chart.destroy());
                chartsInstancias = [];
                sliderHTML.innerHTML = '';
                
                let currentSearchVal = searchSelect.value;
                searchSelect.innerHTML = '<option value="">Selecciona un producto del catálogo...</option>';
                
                renderizarMercado();
                renderizarCalculadora();
                renderizarReporteNIIF();
                renderizarGraficoVolatilidad(); 

                datosBD.forEach((item, index) => {{
                    let cBase = item.estado === 'rojo' ? '#e74c3c' : item.estado === 'amarillo' ? '#f59e0b' : '#10b981';
                    searchSelect.innerHTML += `<option value="${{index}}">${{item.nombre}}</option>`;

                    sliderHTML.innerHTML += `
                        <div class="mini-chart-card">
                            <div class="mini-chart-title">${{item.nombre}} <span style="color:${{cBase}};">S/ ${{item.precio.toFixed(2)}}</span></div>
                            <div class="mini-chart-subtitle">Histórico (Precio x Base)</div>
                            <div style="height: 120px; width: 100%; margin-top: 15px;"><canvas id="chart-mini-${{index}}"></canvas></div>
                        </div>
                    `;
                }});

                if(currentSearchVal !== "") {{ searchSelect.value = currentSearchVal; actualizarConsultaRapida(); }}

                datosBD.forEach((item, index) => {{
                    let cBase = item.estado === 'rojo' ? '#e74c3c' : item.estado === 'amarillo' ? '#f59e0b' : '#10b981';
                    crearMicroGrafico(`chart-mini-${{index}}`, cBase, [item.precio*0.9, item.precio*0.95, item.precio*1.02, item.precio]);
                }});
            }}

            window.calcularSumaTotal = function() {{
                let totalAhorro = 0;
                let totalInversion = 0;
                
                datosBD.forEach((item, index) => {{
                    let inputEl = document.getElementById(`input-${{index}}`);
                    if(!inputEl) return;
                    let cantidad = parseInt(inputEl.value || 0);
                    let vAct = item.variantes[item.unidadSeleccionada];
                    
                    let subInversion = cantidad * (item.precio * vAct.mult);
                    document.getElementById(`inversion-${{index}}`).innerText = `S/ ${{subInversion.toFixed(2)}}`;
                    totalInversion += subInversion;

                    let subAhorro = cantidad * ((item.precio - item.optimo) * vAct.mult);
                    if(subAhorro > 0) totalAhorro += subAhorro;
                }});
                
                document.getElementById('calc-inversion').innerText = `S/ ${{totalInversion.toFixed(2)}}`;
                document.getElementById('calc-total').innerText = `S/ ${{totalAhorro.toFixed(2)}}`;
            }}

            function iniciarScrapingMIDAGRI() {{
                document.querySelector('.btn-sync').innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Ejecutando Scraping...';
                document.getElementById('sunat-box').style.backgroundColor = '#ecfdf5';
                
                // Simula una petición al servidor para refrescar los precios
                setTimeout(() => {{
                    // En una app real en producción, aquí harías un window.location.reload() 
                    // para jalar los nuevos precios de la base de datos para todos.
                    document.getElementById('sunat-box').style.backgroundColor = 'var(--card-bg)';
                    datosBD.forEach(item => {{
                        item.precio = parseFloat((item.precio * (1 + (Math.random() * 0.06 - 0.03))).toFixed(2));
                        let ratio = item.precio / item.optimo;
                        item.estado = ratio > 1.10 ? 'rojo' : ratio < 1.03 ? 'verde' : 'amarillo';
                    }});
                    
                    let hoy = new Date();
                    document.getElementById('fecha-act').innerText = "Actualizado: " + hoy.toLocaleDateString() + " " + hoy.getHours() + ":" + (hoy.getMinutes()<10?'0':'') + hoy.getMinutes();
                    
                    let contentEl = document.querySelector('.content');
                    let scrollPos = contentEl ? contentEl.scrollTop : 0;
                    inicializarVistas(); 
                    if(contentEl) contentEl.scrollTop = scrollPos;
                    
                    actualizarConsultaRapida();
                    document.querySelector('.btn-sync').innerHTML = '<i class="fa-solid fa-bolt"></i> Sincronizar MIDAGRI / SUNAT';
                    mostrarToast("Bases de datos B2B, MIDAGRI y SUNAT sincronizadas.");
                }}, 2500);
            }}

            window.onload = () => {{
                inicializarVistas();
            }};
        </script>
    </body>
    </html>
    """