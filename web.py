from flask import Flask, request, jsonify
import os, base64

app = Flask(__name__)

@app.route("/")
def mi_pagina():
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_img = os.path.join(ruta_actual, "images.jfif")
    img_b64 = ""
    if os.path.exists(ruta_img):
        with open(ruta_img, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
    url_fondo = f"data:image/jpeg;base64,{img_b64}" if img_b64 else ""

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Café Coworking Josmel</title>
        <link rel="preconnect" href="https://googleapis.com">
        <link rel="preconnect" href="https://gstatic.com" crossorigin>
        <!-- Importamos Oswald (alta, condensada y con el estilo de la imagen 2) y Quicksand -->
        <link href="https://googleapis.com" rel="stylesheet">
        <style>
            body {{ font-family: 'Quicksand', sans-serif; text-align: center; margin: 0; background: #fff; color: #000; scroll-behavior: smooth; }}
            nav {{ position: fixed; top: 0; left: 0; width: 100%; background: rgba(255, 255, 255, 0.95); border-bottom: 1px solid #000; padding: 15px 0; z-index: 100; }}
            nav a {{ color: #000; text-decoration: none; font-weight: 700; font-size: 13px; text-transform: uppercase; margin: 0 15px; letter-spacing: 1px; }}
            .portada {{ height: 60vh; position: relative; display: flex; align-items: center; justify-content: center; padding-top: 60px; }}
            .portada::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{url_fondo}'); background-size: cover; background-position: center; filter: blur(4px); z-index: -1; }}
            .contenedor-portada {{ background: #fff; padding: 45px; border-radius: 16px; border: 1px solid #000; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
            
            /* Título superior estilizado */
            h1 {{ 
                font-family: 'Oswald', sans-serif;
                font-size: 20px; 
                font-weight: 700; 
                margin: 0; 
                text-transform: uppercase; 
                letter-spacing: 5px; 
                color: #555555; 
            }}
            
            /* JOSMEL: Recreación exacta del estilo condensado y alto de la imagen 2 */
            .subtitulo {{ 
                font-family: 'Oswald', sans-serif; 
                font-size: 64px; 
                font-weight: 700; 
                color: #000000; 
                text-transform: uppercase; 
                letter-spacing: 2px; /* Espaciado elegante entre letras altas */
                margin-top: 5px; 
                margin-bottom: 5px; 
                display: inline-block;
                line-height: 1.1;
            }}
            
            /* Eslogan a juego, limpio e informal */
            .eslogan {{ 
                font-size: 24px; 
                color: #222222; 
                margin: 20px 0 25px 0; 
                font-weight: 500; 
                letter-spacing: 0.5px;
            }}
            
            section {{ padding: 60px 20px; border-bottom: 1px solid #e0e0e0; }}
            section:nth-child(even) {{ background-color: #f9f9f9; }}
            .titulo-seccion {{ font-size: 24px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; }}
            .grid-menu {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 800px; margin: 0 auto; text-align: left; }}
            .item-menu {{ background: #fff; padding: 15px; border: 1px solid #000; border-radius: 8px; }}
            .precio {{ float: right; font-weight: 700; }}
            .grid-reseñas {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; max-width: 900px; margin: 0 auto; text-align: left; }}
            .tarjeta-reseña {{ background: #fff; padding: 20px; border: 1px solid #000; border-radius: 8px; }}
            .box-reserva {{ background: #fff; border: 2px solid #000; padding: 30px; max-width: 400px; margin: 0 auto; border-radius: 8px; text-align: left; }}
            .grupo {{ margin-bottom: 12px; }}
            .grupo label {{ display: block; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }}
            .grupo input, .grupo select {{ width: 100%; padding: 10px; border: 1px solid #000; box-sizing: border-box; font-family: 'Quicksand', sans-serif; border-radius: 6px; }}
            .btn-formulario {{ width: 100%; background: #000; color: #fff; border: none; padding: 12px; font-weight: 700; text-transform: uppercase; cursor: pointer; border-radius: 6px; font-family: 'Quicksand', sans-serif; }}
        </style>
    </head>
    <body>
        <nav>
            <a href="#inicio">Inicio</a>
            <a href="#menu">Menú</a>
            <a href="#reseñas">Reseñas</a>
            <a href="#reserva">Reservar</a>
        </nav>

        <div id="inicio" class="portada">
            <div class="contenedor-portada">
                <h1>Café Coworking</h1>
                <div><span class="subtitulo">Josmel</span></div>
                <p class="eslogan">Tu pausa favorita</p>
                <a href="#reserva" style="display:inline-block; background:#000; color:#fff; padding:12px 30px; text-decoration:none; font-weight:700; text-transform:uppercase; font-size:12px; letter-spacing: 1px; border-radius: 6px;">Reservar ya</a>
            </div>
        </div>

        <section id="menu">
            <div class="titulo-seccion">📋 Nuestra Carta</div>
            <div class="grid-menu">
                <div class="item-menu"><h3><span class="precio">1.80€</span>☕ Espresso</h3><p>Café de especialidad notas achocolatadas.</p></div>
                <div class="item-menu"><h3><span class="precio">2.20€</span>🥛 Latte</h3><p>Leche cremosa con un shot de espresso.</p></div>
                <div class="item-menu"><h3><span class="precio">3.50€</span>🥐 Combo Desayuno</h3><p>Café americano con croissant del día.</p></div>
                <div class="item-menu"><h3><span class="precio">12.00€</span>📅 Pase Diario</h3><p>Acceso ilimitado al espacio todo el día.</p></div>
            </div>
        </section>

        <section id="reseñas">
            <div class="titulo-seccion">⭐ Opiniones</div>
            <div class="grid-reseñas">
                <div class="tarjeta-reseña"><div>★★★★★</div><p>"El café es espectacular y el internet vuela."</p><span>- Carlos R.</span></div>
                <div class="tarjeta-reseña"><div>★★★★★</div><p>"Ambiente minimalista muy agradable y silencioso."</p><span>- Ana M.</span></div>
                <div class="tarjeta-reseña"><div>★★★★★</div><p>"Excelente concepto. Súper cómodo para trabajar."</p><span>- David L.</span></div>
            </div>
        </section>

        <section id="reserva">
            <div class="titulo-seccion">📅 Solicitar Reserva</div>
            <div class="box-reserva">
                <div class="grupo"><label>Tu Nombre</label><input type="text" id="nombre" required></div>
                <div class="grupo"><label>Teléfono</label><input type="tel" id="telefono" required></div>
                <div class="grupo"><label>Zona</label><select id="zona"><option value="Coworking">Espacio Coworking</option><option value="Cafetería">Mesa Cafetería</option></select></div>
                <div class="grupo"><label>Fecha y Hora</label><input type="datetime-local" id="fecha" required></div>
                <button class="btn-formulario" onclick="guardarLocal()">Confirmar Reserva</button>
            </div>
        </section>

        <script>
            function guardarLocal() {{
                var nombre = document.getElementById('nombre').value;
                var telefono = document.getElementById('telefono').value;
                var zona = document.getElementById('zona').value;
                var fecha = document.getElementById('fecha').value;
                if(nombre == "" || telefono == "" || fecha == "") {{ alert("Por favor, rellena todos los campos."); return; }}
                
                fetch('/guardar_reserva', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ nombre: nombre, telefono: telefono, zona: zona, fecha: fecha }})
                }})
                .then(response => response.json())
                .then(data => {{
                    alert("¡Gracias " + nombre + "! Tu reserva ha sido registrada.");
                    document.getElementById('nombre').value = "";
                    document.getElementById('telefono').value = "";
                    document.getElementById('fecha').value = "";
                }});
            }}
        </script>
    </body>
    </html>
    """

@app.route("/guardar_reserva", methods=["POST"])
def guardar_reserva():
    datos = request.json
    ruta_inicio = os.path.expanduser("~")
    ruta_txt = os.path.join(ruta_inicio, "reservas.txt")
    with open(ruta_txt, "a", encoding="utf-8") as f:
        f.write(f"Nombre: {datos['nombre']} | Teléfono: {datos['telefono']} | Zona: {datos['zona']} | Fecha: {datos['fecha']}\n")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    # Lee el puerto que le asigne Render de forma automática
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
    

