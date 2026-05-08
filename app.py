import os
from flask import Flask, request, render_template_string, jsonify
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
# ✈️ VUELOS (CORREGIDO REALMENTE)
# ======================================================
def DFS_prof_iter(nodo, solucion, conexiones):

    def buscar_rec(nodo, solucion, visitados, limite):

        if limite < 0:
            return None

        estado = nodo.get_datos()

        if estado == solucion:
            return nodo

        visitados.add(estado)

        hijos = []

        for un_hijo in conexiones.get(estado, []):
            if un_hijo not in visitados:
                hijo = Nodo(un_hijo)
                hijo.set_padre(nodo)
                hijos.append(hijo)

        nodo.set_hijos(hijos)

        for h in hijos:
            sol = buscar_rec(h, solucion, visitados.copy(), limite - 1)
            if sol:
                return sol

        return None

    for limite in range(1, 10):
        sol = buscar_rec(nodo, solucion, set(), limite)
        if sol:
            return sol

    return None


# ======================================================
# 🌍 GRAFO (CAMBIO IMPORTANTE: ORDEN FIJO, NO SET)
# ======================================================
conexiones = {
    'Jiloyork': ['Celaya', 'CDMX', 'Querétaro'],
    'CDMX': ['Querétaro', 'Celaya'],
    'Sonora': ['Zacatecas', 'Sinaloa'],
    'Guanajuato': ['Aguascalientes'],
    'Oaxaca': ['Querétaro'],
    'Sinaloa': ['Celaya', 'Sonora', 'Jiloyork'],
    'Querétaro': ['Tamaulipas', 'Zacatecas', 'Sinaloa', 'Jiloyork', 'Oaxaca'],
    'Celaya': ['Jiloyork', 'Sinaloa'],
    'Zacatecas': ['Sonora', 'Monterrey', 'Querétaro'],
    'Monterrey': ['Zacatecas','Sinaloa'],
    'Tamaulipas': ['Querétaro']
}


# ======================================================
# 🧠 UI
# ======================================================
@app.route("/")
def index():
    return render_template_string("""
<html>
<head>
<title>IA Busquedas</title>

<style>
body{
    font-family:Arial;
    background:#0f172a;
    color:white;
    text-align:center;
    padding:20px;
}

.container{
    display:flex;
    justify-content:center;
    gap:20px;
    flex-wrap:wrap;
}

.card{
    background:#1e293b;
    padding:20px;
    border-radius:12px;
    width:300px;
    box-shadow:0 5px 15px rgba(0,0,0,0.5);
}

input{
    width:90%;
    padding:8px;
    margin:5px;
    border-radius:6px;
    border:none;
}

button{
    padding:8px 12px;
    border:none;
    border-radius:6px;
    cursor:pointer;
    margin-top:5px;
}

.bfs{background:#3b82f6;color:white;}
.dfs{background:#ef4444;color:white;}
.v{background:#22c55e;color:white;}

.result{
    margin-top:10px;
    font-size:14px;
    color:#38bdf8;
    white-space:pre-wrap;
}
</style>

</head>

<body>

<h1>🧠 Sistemas de Búsqueda IA</h1>

<div class="container">

<!-- BFS -->
<div class="card">
<h2>🔵 BFS</h2>
<input id="bfs_i" placeholder="4,2,3,1">
<input id="bfs_o" placeholder="1,2,3,4">
<button class="bfs" onclick="runBFS()">Resolver</button>
<div id="bfs_r" class="result"></div>
</div>

<!-- DFS -->
<div class="card">
<h2>🔴 DFS</h2>
<input id="dfs_i" placeholder="4,2,3,1">
<input id="dfs_o" placeholder="1,2,3,4">
<button class="dfs" onclick="runDFS()">Resolver</button>
<div id="dfs_r" class="result"></div>
</div>

<!-- VUELOS -->
<div class="card">
<h2>✈️ Vuelos</h2>
<input id="v_i" placeholder="Origen">
<input id="v_o" placeholder="Destino">
<button class="v" onclick="runV()">Buscar</button>
<div id="v_r" class="result"></div>
</div>

</div>

<script>

async function runBFS(){
    const res = await fetch("/bfs",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            i:document.getElementById("bfs_i").value,
            o:document.getElementById("bfs_o").value
        })
    })
    const data = await res.json()
    document.getElementById("bfs_r").innerText = JSON.stringify(data.result)
}

async function runDFS(){
    const res = await fetch("/dfs",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            i:document.getElementById("dfs_i").value,
            o:document.getElementById("dfs_o").value
        })
    })
    const data = await res.json()
    document.getElementById("dfs_r").innerText = JSON.stringify(data.result)
}

async function runV(){
    const res = await fetch("/vuelos",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            i:document.getElementById("v_i").value,
            o:document.getElementById("v_o").value
        })
    })
    const data = await res.json()
    document.getElementById("v_r").innerText = data.result
}

</script>

</body>
</html>
""")


# ======================================================
# API BFS
# ======================================================
@app.route("/bfs", methods=["POST"])
def bfs_api():
    data = request.json
    i = list(map(int, data["i"].split(",")))
    o = list(map(int, data["o"].split(",")))

    nodo = BFS(i, o)

    if not nodo:
        return jsonify({"result":"No encontrado"})

    camino = []
    while nodo.get_padre():
        camino.append(nodo.get_datos())
        nodo = nodo.get_padre()

    camino.reverse()
    return jsonify({"result": camino})


# ======================================================
# API DFS
# ======================================================
@app.route("/dfs", methods=["POST"])
def dfs_api():
    data = request.json
    i = list(map(int, data["i"].split(",")))
    o = list(map(int, data["o"].split(",")))

    nodo = DFS(i, o)

    if not nodo:
        return jsonify({"result":"No encontrado"})

    camino = []
    while nodo.get_padre():
        camino.append(nodo.get_datos())
        nodo = nodo.get_padre()

    camino.reverse()
    return jsonify({"result": camino})


# ======================================================
# API VUELOS
# ======================================================
@app.route("/vuelos", methods=["POST"])
def vuelos_api():
    data = request.json

    nodo = DFS_prof_iter(Nodo(data["i"]), data["o"], conexiones)

    if not nodo:
        return jsonify({"result":"No ruta encontrada"})

    ruta = []
    while nodo.get_padre():
        ruta.append(nodo.get_datos())
        nodo = nodo.get_padre()

    ruta.append(data["i"])
    ruta.reverse()

    return jsonify({"result":" → ".join(ruta)})


# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)