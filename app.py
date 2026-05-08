import os
from flask import Flask, request, render_template_string
from arbol import Nodo

app = Flask(__name__)

# ======================================================
# 🔵 BFS
# ======================================================
def BFS(estado_inicial, solucion):
    frontera = []
    visitados = []

    nodo_inicial = Nodo(estado_inicial)
    frontera.append(nodo_inicial)

    while frontera:

        nodo = frontera.pop(0)
        visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato = nodo.get_datos()

        hijos = [
            [dato[1], dato[0], dato[2], dato[3]],
            [dato[0], dato[2], dato[1], dato[3]],
            [dato[0], dato[1], dato[3], dato[2]]
        ]

        for h in hijos:
            nodo_hijo = Nodo(h)
            nodo_hijo.set_padre(nodo)

            if not nodo_hijo.en_lista(visitados) and not nodo_hijo.en_lista(frontera):
                frontera.append(nodo_hijo)

    return None


# ======================================================
# 🔴 DFS
# ======================================================
def DFS(estado_inicial, solucion):

    visitados = []
    frontera = []

    nodo_inicial = Nodo(estado_inicial)
    frontera.append(nodo_inicial)

    while frontera:

        nodo = frontera.pop()
        visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato = nodo.get_datos()

        hijos = [
            [dato[1], dato[0], dato[2], dato[3]],
            [dato[0], dato[2], dato[1], dato[3]],
            [dato[0], dato[1], dato[3], dato[2]]
        ]

        for h in hijos:
            nodo_hijo = Nodo(h)
            nodo_hijo.set_padre(nodo)

            if not nodo_hijo.en_lista(visitados) and not nodo_hijo.en_lista(frontera):
                frontera.append(nodo_hijo)

    return None


# ======================================================
# ✈️ VUELOS
# ======================================================
def DFS_prof_iter(nodo, solucion, conexiones):

    def buscar_rec(nodo, solucion, visitados, limite):

        if limite < 0:
            return None

        visitados.append(nodo.get_datos())

        if nodo.get_datos() == solucion:
            return nodo

        hijos = []

        for un_hijo in conexiones.get(nodo.get_datos(), []):
            hijo = Nodo(un_hijo)
            hijo.set_padre(nodo)

            if un_hijo not in visitados:
                hijos.append(hijo)

        nodo.set_hijos(hijos)

        for h in nodo.get_hijos():
            sol = buscar_rec(h, solucion, visitados, limite - 1)
            if sol:
                return sol

        return None


    for limite in range(0, 50):
        sol = buscar_rec(nodo, solucion, [], limite)
        if sol:
            return sol

    return None


conexiones = {
    'Jiloyork': {'Celaya', 'CDMX', 'Querétaro'},
    'CDMX': {'Querétaro', 'Celaya'},
    'Sonora': {'Zacatecas', 'Sinaloa'},
    'Guanajuato': {'Aguascalientes'},
    'Oaxaca': {'Querétaro'},
    'Sinaloa': {'Celaya', 'Sonora', 'Jiloyork'},
    'Querétaro': {'Tamaulipas', 'Zacatecas', 'Sinaloa', 'Jiloyork', 'Oaxaca'},
    'Celaya': {'Jiloyork', 'Sinaloa'},
    'Zacacatecas': {'Sonora', 'Monterrey', 'Querétaro'},
    'Monterrey': {'Zacatecas','Sinaloa'},
    'Tamaulipas': {'Querétaro'}
}


# ======================================================
# 🏠 UNA SOLA PÁGINA
# ======================================================
@app.route("/", methods=["GET", "POST"])
def index():

    bfs_result = dfs_result = vuelos_result = None

    if request.method == "POST":

        tipo = request.form.get("tipo")

        # ---------------- BFS ----------------
        if tipo == "bfs":
            inicio = list(map(int, request.form["inicio"].split(",")))
            objetivo = list(map(int, request.form["objetivo"].split(",")))

            nodo = BFS(inicio, objetivo)

            if nodo:
                camino = []
                while nodo.get_padre():
                    camino.append(nodo.get_datos())
                    nodo = nodo.get_padre()
                camino.reverse()
                bfs_result = camino

        # ---------------- DFS ----------------
        if tipo == "dfs":
            inicio = list(map(int, request.form["inicio"].split(",")))
            objetivo = list(map(int, request.form["objetivo"].split(",")))

            nodo = DFS(inicio, objetivo)

            if nodo:
                camino = []
                while nodo.get_padre():
                    camino.append(nodo.get_datos())
                    nodo = nodo.get_padre()
                camino.reverse()
                dfs_result = camino

        # ---------------- VUELOS ----------------
        if tipo == "vuelos":
            origen = request.form["origen"]
            destino = request.form["destino"]

            nodo = DFS_prof_iter(Nodo(origen), destino, conexiones)

            if nodo:
                ruta = []
                while nodo.get_padre():
                    ruta.append(nodo.get_datos())
                    nodo = nodo.get_padre()

                ruta.append(origen)
                ruta.reverse()
                vuelos_result = " → ".join(ruta)

            else:
                vuelos_result = "No se encontró ruta"


    return render_template_string("""
    <html>
    <head>
        <title>IA BUSQUEDAS</title>
        <style>
            body{
                font-family:Arial;
                background:#0f172a;
                color:white;
                text-align:center;
                padding:30px;
            }

            .card{
                background:#1e293b;
                padding:20px;
                margin:20px auto;
                width:350px;
                border-radius:12px;
                box-shadow:0 5px 15px rgba(0,0,0,0.5);
            }

            input{
                padding:8px;
                margin:5px;
                border-radius:6px;
                border:none;
                width:90%;
            }

            button{
                padding:8px 15px;
                border:none;
                border-radius:6px;
                cursor:pointer;
                background:#22c55e;
                color:white;
                margin-top:5px;
            }

            .dfs-btn{background:#ef4444;}
            .bfs-btn{background:#3b82f6;}
            .v-btn{background:#f59e0b;}

            h1{margin-bottom:30px;}
            h2{margin-top:30px;}

        </style>
    </head>
    <body>

        <h1>🧠 SISTEMA DE BÚSQUEDAS IA</h1>

        <!-- ================= BFS ================= -->
        <div class="card">
            <h2>🔵 BFS</h2>
            <form method="POST">
                <input name="inicio" placeholder="Inicio ej: 4,2,3,1">
                <input name="objetivo" placeholder="Objetivo ej: 1,2,3,4">
                <input type="hidden" name="tipo" value="bfs">
                <button class="bfs-btn">Resolver BFS</button>
            </form>
            {% if bfs_result %}
                <pre>{{ bfs_result }}</pre>
            {% endif %}
        </div>

        <!-- ================= DFS ================= -->
        <div class="card">
            <h2>🔴 DFS</h2>
            <form method="POST">
                <input name="inicio" placeholder="Inicio ej: 4,2,3,1">
                <input name="objetivo" placeholder="Objetivo ej: 1,2,3,4">
                <input type="hidden" name="tipo" value="dfs">
                <button class="dfs-btn">Resolver DFS</button>
            </form>
            {% if dfs_result %}
                <pre>{{ dfs_result }}</pre>
            {% endif %}
        </div>

        <!-- ================= VUELOS ================= -->
        <div class="card">
            <h2>✈️ VUELOS</h2>
            <form method="POST">
                <input name="origen" placeholder="Origen">
                <input name="destino" placeholder="Destino">
                <input type="hidden" name="tipo" value="vuelos">
                <button class="v-btn">Buscar ruta</button>
            </form>
            {% if vuelos_result %}
                <h3>{{ vuelos_result }}</h3>
            {% endif %}
        </div>

    </body>
    </html>
    """,
    bfs_result=bfs_result,
    dfs_result=dfs_result,
    vuelos_result=vuelos_result)


# ======================================================
# 🚀 RAILWAY READY
# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)