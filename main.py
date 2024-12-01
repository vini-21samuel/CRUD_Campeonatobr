from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()


# Dados do campeonato
times = {
    1: {"id": 1, "nome": "Flamengo"},
    2: {"id": 2, "nome": "Fortaleza"},
    3: {"id": 3, "nome": "Corinthians"},
    4: {"id": 4, "nome": "Palmeiras"},
    5: {"id": 5, "nome": "São Paulo"},
    6: {"id": 6, "nome": "Paysandu"}
}


# Dados das partidas do campeonato
partidas = {
    1: {"id": 1, "time 1": "Flamengo", "time_2": "Fortaleza", "data": "2024-11-26", "resultado": "Flamengo 0 x 0 Fortaleza"},
    2: {"id": 2, "time 1": "Corinthians", "time_2": "Palmeiras", "data": "2024-11-18", "resultado": "Corinthians 2 x 0 Palmeiras"},
    3: {"id": 3, "time 1": "São Paulo", "time_2": "Paysandu", "data": "2024-11-22","resultado": "São Paulo 3 x 5 Paysandu"  }
}

#Rota exibir o campeonato
@app.get("/")
def exibir_campeonato():
    return {"times": list(times.values()), "partidas": list(partidas.values())}

@app.get("/times/")
def listar_times():
    return list(times.values())

@app.get("/times/{time_id}")
def buscar_time(time_id: int):
    if time_id in times:
        return times[time_id]
    raise HTTPException(status_code=404, detail="Time não encontrado.") 

@app.post("/times/")
def adicionar_time(nome: str):
    novo_id = max(times.keys()) + 1
    time = {"id": novo_id, "nome": nome}
    times[novo_id] = time
    return time

@app.delete("/times/{time_id}")
def deletar_time(time_id: int):
    if time_id in times:
        return times.pop(time_id)
    raise HTTPException(status_code=404, detail="Time não encontrado.")

# Métodos para Partidas
@app.get("/partidas/")
def listar_partidas():
    return list(partidas.values())

@app.post("/partidas/")
def adicionar_partida(time_1: str, time_2: str, data: str):
    novo_id = max(partidas.keys()) + 1
    partida = {"id": novo_id, "time_1": time_1, "time_2": time_2, "data": data, "resultado": None}
    partidas[novo_id] = partida
    return partida

@app.put("/partidas/{partida_id}")
def atualizar_resultado(partida_id: int, resultado: str):
    if partida_id in partidas:
        partidas[partida_id]["resultado"] = resultado
        return partidas[partida_id]
    raise HTTPException(status_code=404, detail="Partida não encontrada.")

@app.delete("/partidas/{partida_id}")
def deletar_partida(partida_id: int):
    if partida_id in partidas:
        return partidas.pop(partida_id)
    raise HTTPException(status_code=404, detail="Partida não encontrada.")
