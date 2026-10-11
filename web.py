from flask import Flask, request, jsonify
import os, base64

app = Flask(__name__)

# BASE DE DATOS EN MEMORIA VIVA: Guarda el estado de los 24 asientos de tu plano de AutoCAD.
# 'libre' significa disponible para reservar. 'ocupado' significa bloqueado.
ASIENTOS_DB = {
    # Zona Coworking (Mesas C1 y C2 con 4 sillas cada una = 8 puestos)
    **{f"Cowork 1 - Silla {s}": "libre" for s in range(1, 5)},
    **{f"Cowork 2 - Silla {s}": "libre" for s in range(1, 5)},
    # Zona Salón/Cafetería (Mesas S1, S2, S3 y S4 con 4 sillas cada una = 16 puestos)
    **{f"Salón 1 - Silla {s}": "libre" for s in range(1, 5)},
    **{f"Salón 2 - Silla {s}": "libre" for s in range(1, 5)},
    **{f"Salón 3 - Silla {s}": "libre" for s in range(1, 5)},
    **{f"Salón 4 - Silla {s}": "libre" for s in range(1, 5)}
}

# Dejamos un par de asientos bloqueados de inicio como ejemplo
ASIENTOS_DB["Cowork 2 - Silla 2"] = "ocupado"
ASIENTOS_DB["Salón 2 - Silla 3"] = "ocupado"

@app.route("/api/asientos", methods=["GET"])
def obtener_asientos():
    """Ruta interna que consulta la web en vivo para pintar el plano"""
    return jsonify(ASIENTOS_DB)

@app.route("/api/admin/toggle", methods=["POST"])
def toggle_asiento():
    """Ruta secreta que usa el Administrador para bloquear/desbloquear con un clic"""
    datos = request.json
    asiento = datos.get("asiento")
    if asiento in ASIENTOS_DB:
        ASIENTOS_DB[asiento] = "libre" if ASIENTOS_DB[asiento] == "ocupado" else "ocupado"
        return jsonify({"status": "success", "nuevo_estado": ASIENTOS_DB[asiento]})
    return jsonify({"status": "error"}), 400

@app.route("/")
def mi_pagina():
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_img = os.path.join(ruta_actual, "images.jfif")
    img_b64 = ""
    if os.path.exists(ruta_img):
        with open(ruta_img, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
    url_fondo = f"data:image/jpeg;base64,{img_b64}" if img_b64 else ""

    def crear_mesas(tipo, cantidad):
        html = ""
        for i in range(1, cantidad + 1):
            html += f"<div class='bloque-mesa'><h4>Mesa {tipo} {i}</h4><div class='grid-asientos-mesa'>"
            for s in range(1, 5):
                html += f"<div class='asiento' id='asiento-{tipo}-{i}-{s}'>S{s}</div>"
            html += "</div></div>"
        return html

    html_cowork = crear_mesas("Cowork", 2)
    html_salon = crear_mesas("Salón", 4)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Café Coworking Josmel</title>
        <link rel="preconnect" href="https://googleapis.com">
        <link rel="preconnect" href="https://gstatic.com" crossorigin>
        <link href="https://googleapis.com/css2?family=Oswald:wght@700&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Quicksand', sans-serif; text-align: center; margin: 0; background: #fff; color: #000; scroll-behavior: smooth; }}
            nav {{ position: fixed; top: 0; left: 0; width: 100%; background: rgba(255, 255, 255, 0.95); border-bottom: 1px solid #000; padding: 15px 0; z-index: 100; }}
            nav a {{ color: #000; text-decoration: none; font-weight: 700; font-size: 13px; text-transform: uppercase; margin: 0 15px; letter-spacing: 1px; }}
            .portada {{ height: 60vh; position: relative; display: flex; align-items: center; justify-content: center; padding-top: 60px; }}
            .portada::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{url_fondo}'); background-size: cover; background-position: center; filter: blur(4px); z-index: -1; }}
            .contenedor-portada {{ background: #fff; padding: 45px; border-radius: 16px; border: 1px solid #000; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
            h1 {{ font-family: 'Oswald', sans-serif; font-size: 20px; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 5px; color: #555555; }}
            .subtitulo {{ font-family: 'Oswald', sans-serif; font-size: 64px; font-weight: 700; color: #000000; text-transform: uppercase; letter-spacing: 2px; margin-top: 5px; margin-bottom: 5px; display: inline-block; line-height: 1.1; }}
            .eslogan {{ font-size: 24px; color: #222222; margin: 20px 0 25px 0; font-weight: 500; letter-spacing: 0.5px; }}
            section {{ padding: 60px 20px; border-bottom: 1px solid #e0e0e0; }}
            section:nth-child(even) {{ background-color: #f9f9f9; }}
            .titulo-seccion {{ font-size: 24px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; }}
            .grid-menu {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 800px; margin: 0 auto; text-align: left; }}
            .item-menu {{ background: #fff; padding: 15px; border: 1px solid #000; border-radius: 8px; }}
            .precio {{ float: right; font-weight: 700; }}
            .grid-reseñas {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; max-width: 900px; margin: 0 auto; text-align: left; }}
            .tarjeta-reseña {{ background: #fff; padding: 20px; border: 1px solid #000; border-radius: 8px; }}
            
            .box-reserva {{ background: #fff; border: 2px solid #000; padding: 35px; max-width: 480px; margin: 0 auto; border-radius: 12px; text-align: left; }}
            .grupo {{ margin-bottom: 15px; }}
            .grupo label {{ display: block; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }}
            .grupo input, .grupo select {{ width: 100%; padding: 10px; border: 1px solid #000; box-sizing: border-box; font-family: 'Quicksand', sans-serif; border-radius: 6px; background: #fff; color: #000; outline: none; }}
            
            .subventana-mapa {{ display: none; margin-top: 15px; padding: 20px; border: 1px dashed #000; border-radius: 10px; background: #fffbf7; }}
            .barra-referencia {{ border: 2px solid #000; text-align: center; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 6px 0; margin-bottom: 25px; background: #000; color: #fff; letter-spacing: 2px; border-radius: 4px; }}
            .ambiente-titulo {{ font-size: 11px; font-weight: 700; text-transform: uppercase; margin: 0 0 10px 0; color: #000; border-bottom: 1px solid #000; padding-bottom: 4px; letter-spacing: 0.5px; }}
            .distribucion-mesas {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            .bloque-mesa {{ border: 1px solid #000; padding: 10px; border-radius: 8px; background: #ffffff; text-align: center; }}
            .bloque-mesa h4 {{ margin: 0 0 8px 0; font-size: 11px; text-transform: uppercase; color: #000; }}
            .grid-asientos-mesa {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; }}
            .asiento {{ border: 1px solid #000; padding: 8px 2px; text-align: center; font-size: 11px; font-weight: 700; border-radius: 4px; cursor: pointer; background: #fff; color: #000; user-select: none; }}
            .asiento:hover:not(.ocupado) {{ background: #000; color: #fff; }}
            .asiento.seleccionado {{ background: #000 !important; color: #fff !important; }}
            .asiento.ocupado {{ background: #e0e0e0; color: #aaa; border-color: #ccc; cursor: not-allowed; font-weight: 400; }}
            .btn-formulario {{ width: 100%; background: #000; color: #fff; border: none; padding: 14px; font-weight: 700; text-transform: uppercase; cursor: pointer; border-radius: 6px; font-family: 'Quicksand', sans-serif; margin-top: 15px; letter-spacing: 1px; }}
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
                <a href="#reserva" style="display:inline-block; background:#000; color:#fff; padding:12px 30px; text-decoration:none; font-weight:700; text-transform:uppercase; font-size:12px; border-radius: 6px;">Reservar ya</a>
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
                <div class="grupo"><label>Tu Nombre</label><input type="text" id="nombre" placeholder="Ej. Juan Pérez"></div>
                <div class="grupo"><label>Teléfono</label><input type="tel" id="telefono" placeholder="Ej. 600 000 000"></div>
                <div class="grupo"><label>Fecha y Hora</label><input type="datetime-local" id="fecha"></div>
                
                <div class="grupo">
                    <label>Selecciona el espacio</label>
                    <select id="selectZona" onchange="cambiarZona(this.value)">
                        <option value="">-- Elige un espacio --</option>
                        <option value="cowork">💻 Zona Coworking (8 Asientos)</option>
                        <option value="salon">☕ Zona Salón (16 Asientos)</option>
                    </select>
                </div>

                <div id="subventanaMapa" class="subventana-mapa">
                    <div class="barra-referencia">☕ BARRA CENTRAL / COCINA 🍳</div>
                    <div id="mapaTitulo" class="ambiente-titulo">Plano de Asientos</div>
                    <div id="planoCineGrid" class="distribucion-mesas"></div>
                </div>

                <button class="btn-formulario" onclick="guardarLocal()">Confirmar Reserva</button>
            </div>
        </section>

        <script>
            var asientoSeleccionado = "";
            var zonaActual = "";
            var baseDatosAsientos = {{}};

            function cargarAsientosServidor() {{
                fetch('/api/asientos')
                    .then(res => res.json())
                    .then(data => {{
                        baseDatosAsientos = data;
                        if(zonaActual) {{ renderizarPlanoCine(zonaActual); }}
                    }});
            }}

            function cambiarZona(zona) {{
                zonaActual = zona;
                asientoSeleccionado = "";
                var contenedor = document.getElementById('subventanaMapa');
                if(!zona) {{ contenedor.style.display = 'none'; return; }}
                contenedor.style.display = 'block';
                document.getElementById('mapaTitulo').innerText = zona === "cowork" ? "💻 PLANO: ZONA COWORKING" : "☕ PLANO: SALÓN PRINCIPAL";
                renderizarPlanoCine(zona);
            }}

            function renderizarPlanoCine(zona) {{
                var grid = document.getElementById('planoCineGrid');
                grid.innerHTML = zona === "cowork" ? `{html_cowork}` : `{html_salon}`;
                
                // Actualizar los estados (libre/ocupado) de forma dinámica tipo cine
                for (var clave in baseDatosAsientos) {{
                    var estado = baseDatosAsientos[clave];
                    var mesaNum = clave.split(" ")[1];
                    var sillaNum = clave.split(" ")[4];
                    var tipoPrefijo = clave.startsWith("Cowork") ? "Cowork" : "Salón";
                    
                    var idBuscado = "asiento-" + tipoPrefijo + "-" + mesaNum + "-" + sillaNum;
                    var elementoSilla = document.getElementById(idBuscado);
                    
                    if(elementoSilla) {{
                        if(estado === "ocupado") {{
                            elementoSilla.className = "asiento ocupado";
                            elementoSilla.innerText = "X";
                            elementoSilla.onclick = null;
                        }} else {{
                            elementoSilla.className = "asiento";
                            var pfxShort = tipoPrefijo === "Cowork" ? "C" : "M";
                            elementoSilla.innerText = pfxShort + mesaNum + "-S" + sillaNum;
                            elementoSilla.setAttribute('onclick', 'marcarSilla(this, "' + clave + '")');
                        }}
                    }}
                }}
            }}

            function marcarSilla(elemento, nombreAsiento) {{
                var asientos = document.getElementsByClassName('asiento');
                for (var i = 0; i < asientos.length; i++) {{ asientos[i].classList.remove('seleccionado'); }}
                elemento.classList.add('seleccionado');
                asientoSeleccionado = nombreAsiento;
            }}

            function guardarLocal() {{
                var nombre = document.getElementById('nombre').value;
                var telefono = document.getElementById('telefono').value;
                var fecha = document.getElementById('fecha').value;
                var selectZona = document.getElementById('selectZona').value;

                if(nombre == "" || telefono == "" || fecha == "" || selectZona == "") {{ alert("Por favor, rellena tus datos."); return; }}
                if(asientoSeleccionado == "") {{ alert("Por favor, elige tu asiento."); return; }}

                fetch('/guardar_reserva', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ nombre: nombre, telefono: telefono, zona: asientoSeleccionado, fecha: fecha }})
                }})
                .then(response => response.json())
                .then(data => {{
                    alert("¡Excelente! Has reservado el " + asientoSeleccionado);
                    baseDatosAsientos[asientoSeleccionado] = "ocupado";
                    document.getElementById('nombre').value = "";
                    document.getElementById('telefono').value = "";
                    document.getElementById('fecha').value = "";
                    document.getElementById('selectZona').value = "";
                    cambiarZona("");
                }});
            }}
            cargarAsientosServidor();
        </script>
    </body>
    </html>
    """
# =====================================================================
# 🔐 PÁGINA OCULTA DEL ADMINISTRADOR (PANEL DE CONTROL DE GERENCIA)
# =====================================================================
@app.route("/admin-josmel-secreto")
def panel_administrador():
    """Ruta secreta para que tú gestiones y desbloquees los asientos con un clic"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Panel de Control | Josmel</title>
        <link rel="preconnect" href="https://googleapis.com">
        <link rel="preconnect" href="https://gstatic.com" crossorigin>
        <link href="https://googleapis.com/css2?family=Oswald:wght@700&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Quicksand', sans-serif; text-align: center; background: #f9f9f9; padding: 40px 10px; margin: 0; color: #000; }
            .panel { background: #fff; border: 2px solid #000; border-radius: 16px; max-width: 600px; margin: 0 auto; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
            h2 { font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; }
            p { font-size: 14px; color: #666; margin-bottom: 30px; }
            .seccion { font-size: 12px; font-weight: 700; text-transform: uppercase; border-bottom: 2px solid #000; padding-bottom: 5px; margin: 25px 0 15px 0; text-align: left; letter-spacing: 1px; }
            .grid-admin { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
            .item-admin { border: 1px solid #000; padding: 12px 2px; border-radius: 6px; font-weight: 700; font-size: 11px; cursor: pointer; transition: all 0.2s; text-align: center; user-select: none; }
            .item-admin.libre { background: #ffffff; color: #000000; }
            .item-admin.ocupado { background: #000000; color: #ffffff; border-color: #000; }
        </style>
    </head>
    <body>
        <div class="panel">
            <h2>Panel de Gerencia Secreto</h2>
            <p>💡 Haz clic sobre cualquier asiento para cambiar su estado en vivo.<br>
            🟢 <b>Blanco</b> = Disponible para clientes | ⚫ <b>Negro</b> = Bloqueado/Ocupado</p>
            
            <div class="seccion">💻 Escritorios Coworking</div>
            <div id="gridAdminCowork" class="grid-admin"></div>
            
            <div class="seccion">☕ Mesas del Salón</div>
            <div id="gridAdminSalon" class="grid-admin"></div>
        </div>

        <script>
            function cargarPanelAdmin() {
                fetch('/api/asientos')
                    .then(res => res.json())
                    .then(data => {
                        var gridCowork = document.getElementById('gridAdminCowork');
                        var gridSalon = document.getElementById('gridAdminSalon');
                        gridCowork.innerHTML = "";
                        gridSalon.innerHTML = "";

                        for (var clave in data) {
                            var estado = data[clave];
                            var div = document.createElement('div');
                            div.className = "item-admin " + estado;
                            
                            var prefijo = clave.startsWith("Cowork") ? "C" : "M";
                            var mesaNum = clave.split(" ")[1];
                            var sillaNum = clave.split(" ")[4];
                            div.innerText = prefijo + mesaNum + "-S" + sillaNum;
                            
                            div.setAttribute('onclick', 'cambiarEstadoAsiento("' + clave + '")');
                            
                            if(clave.startsWith("Cowork")) {
                                gridCowork.appendChild(div);
                            } else {
                                gridSalon.appendChild(div);
                            }
                        }
                    });
            }

            function cambiarEstadoAsiento(nombreAsiento) {
                fetch('/api/admin/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ asiento: nombreAsiento })
                })
                .then(res => res.json())
                .then(data => {
                    cargarPanelAdmin(); // Refresca los estados visuales en vivo
                });
            }

            window.onload = cargarPanelAdmin;
        </script>
    </body>
    </html>
    """

@app.route("/guardar_reserva", methods=["POST"])
def guardar_reserva():
    datos = request.json
    asiento = datos.get("zona")

    # Si el cliente reserva, se marca automáticamente como ocupado en la base de datos viva
    if asiento in ASIENTOS_DB:
        ASIENTOS_DB[asiento] = "ocupado"

    ruta_inicio = os.path.expanduser("~")
    ruta_txt = os.path.join(ruta_inicio, "reservas.txt")
    with open(ruta_txt, "a", encoding="utf-8") as f:
        f.write(f"Nombre: {datos['nombre']} | Teléfono: {datos['telefono']} | Ubicación: {datos['zona']} | Fecha: {datos['fecha']}\n")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
