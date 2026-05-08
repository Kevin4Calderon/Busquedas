import os
from flask import Flask, request, render_template_string
from arbol import Nodo

app = Flask(__name__)

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
    'Zacatecas': {'Sonora', 'Monterrey', 'Querétaro'},
    'Monterrey': {'Zacatecas','Sinaloa'},
    'Tamaulipas': {'Querétaro'}
}

@app.route("/")
def index():
    return """
    <html>
    <head>
        <title>IA Busquedas</title>
        <style>
            body{
                font-family:Arial;
                background:#0f172a;
                color:white;
                text-align:center;
                padding:60px;
            }

            h1{
                margin-bottom:30px;
            }

            a{
                display:block;
                margin:15px;
                padding:12px;
                background:#1e293b;
                border-radius:10px;
                color:#38bdf8;
                text-decoration:none;
                font-size:18px;
                width:250px;
                margin-left:auto;
                margin-right:auto;
                transition:0.3s;
            }

            a:hover{
                background:#334155;
                color:#22c55e;
            }
        </style>
    </head>
    <body>

        <h1>🧠 Sistemas de Búsqueda IA</h1>

        <a href="/bfs">🔵 BFS Puzzle</a>
        <a href="/dfs">🔴 DFS Puzzle</a>
        <a href="/vuelos">✈️ Vuelos (DFS Iterativo)</a>

    </body>
    </html>
    """

@app.route("/bfs", methods=["GET", "POST"])
def bfs_page():

    resultado = None

    if request.method == "POST":

        inicio = list(map(int, request.form["inicio"].split(",")))
        objetivo = list(map(int, request.form["objetivo"].split(",")))

        nodo = BFS(inicio, objetivo)

        if nodo:

            camino = []
            while nodo.get_padre():
                camino.append(nodo.get_datos())
                nodo = nodo.get_padre()

            camino.reverse()
            resultado = camino

    return render_template_string("""
    <html>
    <head>
        <title>BFS</title>
        <style>
            body{
                font-family:Arial;
                background:#0f172a;
                color:white;
                text-align:center;
                padding:40px;
            }

            input{
                padding:10px;
                margin:10px;
                border-radius:8px;
                border:none;
            }

            button{
                padding:10px 20px;
                border:none;
                border-radius:8px;
                background:#22c55e;
                color:white;
                cursor:pointer;
            }

            .card{
                margin-top:20px;
                background:#1e293b;
                display:inline-block;
                padding:15px;
                border-radius:12px;
            }
        </style>
    </head>
    <body>

        <h1>🔵 BFS Puzzle</h1>

        <form method="POST">
            <input name="inicio" placeholder="Ej: 4,2,3,1">
            <input name="objetivo" placeholder="Ej: 1,2,3,4">
            <button>Resolver</button>
        </form>

        {% if resultado %}
            <div class="card">{{ resultado }}</div>
        {% endif %}

    </body>
    </html>
    """, resultado=resultado)


# ======================================================
# 🔴 DFS
# ======================================================
@app.route("/dfs", methods=["GET", "POST"])
def dfs_page():

    resultado = None

    if request.method == "POST":

        inicio = list(map(int, request.form["inicio"].split(",")))
        objetivo = list(map(int, request.form["objetivo"].split(",")))

        nodo = DFS(inicio, objetivo)

        if nodo:

            camino = []
            while nodo.get_padre():
                camino.append(nodo.get_datos())
                nodo = nodo.get_padre()

            camino.reverse()
            resultado = camino

    return render_template_string("""
    <html>
    <head>
        <title>DFS</title>
        <style>
            body{
                font-family:Arial;
                background:#0f172a;
                color:white;
                text-align:center;
                padding:40px;
            }

            input{
                padding:10px;
                margin:10px;
                border-radius:8px;
                border:none;
            }

            button{
                padding:10px 20px;
                border:none;
                border-radius:8px;
                background:#ef4444;
                color:white;
                cursor:pointer;
            }

            .card{
                margin-top:20px;
                background:#1e293b;
                display:inline-block;
                padding:15px;
                border-radius:12px;
            }
        </style>
    </head>
    <body>

        <h1>🔴 DFS Puzzle</h1>

        <form method="POST">
            <input name="inicio">
            <input name="objetivo">
            <button>Resolver</button>
        </form>

        {% if resultado %}
            <div class="card">{{ resultado }}</div>
        {% endif %}

    </body>
    </html>
    """, resultado=resultado)


# ======================================================
# ✈️ VUELOS
# ======================================================
@app.route("/vuelos", methods=["GET", "POST"])
def vuelos():

    resultado = None

    if request.method == "POST":

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
            resultado = " → ".join(ruta)

        else:
            resultado = "No se encontró ruta"

    return render_template_string("""
    <html>
    <head>
        <title>Vuelos</title>
    </head>
    <body style="font-family:Arial;background:#111;color:white;text-align:center;padding:40px;">
        <h1>✈️ Vuelos</h1>

        <form method="POST">
            <input name="origen">
            <input name="destino">
            <button>Buscar</button>
        </form>

        {% if resultado %}
            <h2>{{ resultado }}</h2>
        {% endif %}
    </body>
    </html>
    """, resultado=resultado)


# ======================================================
# 🚀 RUN (RAILWAY READY)
# ======================================================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)