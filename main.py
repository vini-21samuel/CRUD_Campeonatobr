from fastapi import FastAPI, HTTPException
from typing import Optional, List

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
    1: {
        "id": 1,
        "time_1": "Flamengo",
        "time_2": "Fortaleza",
        "data": "2024-11-26",
        "resultado": "Flamengo 0 x 0 Fortaleza",
        "gols": []
    },
    2: {
        "id": 2,
        "time_1": "Corinthians",
        "time_2": "Palmeiras",
        "data": "2024-11-18",
        "resultado": "Corinthians 2 x 0 Palmeiras",
        "gols": [
            {"jogador": "Garro", "time": "Corinthians"},
            {"jogador": "Yuri Alberto", "time": "Corinthians"}
        ]
    }
}

# Dados dos jogadores
jogadores = {
    1: {"id": 1, "nome": "Gabigol", "posicao": "Atacante", "time": "Flamengo", "gols": 10},
    2: {"id": 2, "nome": "Calleri", "posicao": "Atacante", "time": "São Paulo", "gols": 8},
    3: {"id": 3, "nome": "Yuri Alberto", "posicao": "Atacante", "time": "Corinthians", "gols": 12}
}
@app.get("/", tags=["Principal"])
def exibir_campeonato():
    return {"times": list(times.values()), "partidas": list(partidas.values()), "jogadores": list(jogadores.values())}

# Rotas para Times
@app.get("/times/", tags=["Times"])
def listar_times():
    return list(times.values())

@app.get("/times/{time_id}", tags=["Times"])
def buscar_time(time_id: int):
    if time_id in times:
        return times[time_id]
    raise HTTPException(status_code=404, detail="Time não encontrado.") 

@app.post("/times/", tags=["Times"])
def adicionar_time(nome: str):
    novo_id = max(times.keys()) + 1
    time = {"id": novo_id, "nome": nome}
    times[novo_id] = time
    return time

@app.delete("/times/{time_id}", tags=["Times"])
def deletar_time(time_id: int):
    if time_id in times:
        return times.pop(time_id)
    raise HTTPException(status_code=404, detail="Time não encontrado.")

# Rotas para Partidas
@app.get("/partidas/", tags=["Partidas"])
def listar_partidas():
    return list(partidas.values())

@app.post("/partidas/", tags=["Partidas"])
def adicionar_partida(time_1: str, time_2: str, data: str):
    novo_id = max(partidas.keys()) + 1
    partida = {"id": novo_id, "time_1": time_1, "time_2": time_2, "data": data, "resultado": None, "gols": []}
    partidas[novo_id] = partida
    return partida

@app.put("/partidas/{partida_id}", tags=["Partidas"])
def atualizar_resultado(partida_id: int, resultado: str):
    if partida_id in partidas:
        partidas[partida_id]["resultado"] = resultado
        return partidas[partida_id]
    raise HTTPException(status_code=404, detail="Partida não encontrada.")

@app.put("/partidas/{partida_id}/gols", tags=["Partidas"])
def registrar_gols(partida_id: int, gols: List[dict]):
    if partida_id in partidas:
        partidas[partida_id]["gols"] = gols
        return partidas[partida_id]
    raise HTTPException(status_code=404, detail="Partida não encontrada.")

@app.delete("/partidas/{partida_id}", tags=["Partidas"])
def deletar_partida(partida_id: int):
    if partida_id in partidas:
        return partidas.pop(partida_id)
    raise HTTPException(status_code=404, detail="Partida não encontrada.")

# Rotas para Jogadores
@app.get("/jogadores/", tags=["Jogadores"])
def listar_jogadores():
    return list(jogadores.values())

@app.get("/jogadores/{jogador_id}", tags=["Jogadores"])
def buscar_jogador(jogador_id: int):
    if jogador_id in jogadores:
        return jogadores[jogador_id]
    raise HTTPException(status_code=404, detail="Jogador não encontrado.")

@app.post("/jogadores/", tags=["Jogadores"])
def adicionar_jogador(nome: str, posicao: str, time: str, gols: int):
    novo_id = max(jogadores.keys()) + 1
    jogador = {"id": novo_id, "nome": nome, "posicao": posicao, "time": time, "gols": gols}
    jogadores[novo_id] = jogador
    return jogador

@app.delete("/jogadores/{jogador_id}", tags=["Jogadores"])
def deletar_jogador(jogador_id: int):
    if jogador_id in jogadores:
        return jogadores.pop(jogador_id)
    raise HTTPException(status_code=404, detail="Jogador não encontrado.")
