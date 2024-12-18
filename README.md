# API de Interclasse Escolar

Este projeto é uma API desenvolvida para gerenciar competições esportivas de interclasse em ambiente escolar. A API permite criar, listar, atualizar e deletar informações sobre partidas, equipes, e resultados, promovendo uma organização eficiente das competições. Além disso, fornece endpoints bem documentados para interação com o sistema.

## 💡 Para que serve no mundo real?

No mundo real, esta API pode ser utilizada por escolas para gerenciar torneios esportivos internos, facilitando a administração e divulgação de informações como:
- Agendamento de partidas.
- Registro de equipes e seus integrantes.
- Controle de resultados e estatísticas de jogos.
- Consulta de informações para alunos, professores e organizadores.

Este projeto pode ser adaptado para atender a qualquer tipo de torneio ou competição esportiva em diversos contextos, promovendo organização e transparência.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação principal.
- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **SQLAlchemy**: ORM para gerenciamento de banco de dados.
- **SQLite** (ou outro banco de dados à sua escolha): Para armazenamento de dados.
- **Pydantic**: Validação e tipagem de dados.
- **Git**: Controle de versão.

---

## 🚀 Como usar o projeto

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.11** ou superior e o **Git** instalados no seu sistema.

### 2. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```
### 3. Configurar o ambiente virtual

#### Windows
```bash
python -m venv venv
venv\Scripts\activate

```
#### Ubuntu
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```
### 5. iniciar o servidor
```bash
uvicorn app.main:app --reload
```
O servidor será iniciado no endereço: http://127.0.0.1:8000

## 🗃️ Informações Salvas no Banco de Dados

### Tabela `times`
| ID  | Nome         | Lugar             |
|-----|--------------|-------------------|
| 1   | Redes        | Campus Boa Viagem |
| 3   | ADS          | Campus Boa Viagem |
| 4   | Química      | Campus Boa Viagem |
| 5   | Servidores   | Campus Boa Viagem |
| 8   | Resenha      | IF Redes          |
| 9   | ADS          | IFCE BV           |
| 2   | ADSzeras     | IFCE              |

### Tabela `jogadores`
| ID  | Nome          | Gols | Time ID |
|-----|---------------|------|---------|
| 1   | Renatin       | 10   | 1       |
| 2   | João Luiz     | 12   | 1       |
| 4   | Wesnei Paiva  | 5    | 3       |
| 8   | Gabriel T.    | 10   | 5       |
| 9   | Gustavo       | 0    | 2       |
| 10  | Yan Uchoa     | 999  | 3       |
| 3   | Vini Samuel   | 1000 | 3       |

### Tabela `partidas`
| ID  | Time 1 ID | Time 2 ID | Data       | Resultado |
|-----|-----------|-----------|------------|-----------|
| 7   | 1         | 2         | 2024-12-15 | 3x3       |
| 11  | 1         | 2         | 2024-12-16 | 2-1       |
| 13  | 3         | 2         | 2024-12-17 | 1x1       |
| 15  | 2         | 5         | 2024-12-17 | 1x0       |
| 16  | 2         | 3         | 2024-12-20 | 1x0       |


### Teste das rotas no docs e no Postman

<div style="display: flex; justify-content: space-around;">
  <div style="text-align: center;">
    <h4>Docs</h4>
    <img src="https://github.com/user-attachments/assets/de0a1c07-1634-4705-a7e3-200f59b39d78" alt="docsg" width="400">
  </div>
  
  ### Link da documentação das rotas no postman
  ```
  https://web.postman.co/workspace/My-Workspace~54174e29-390c-458d-8157-e7602835305e/documentation/40116141-6d6fb095-3ef6-4ad5-bfd6-76cd0a68b049
  ```
  <div style="text-align: center;">
    <h4>Postman</h4>
    <img src="https://github.com/user-attachments/assets/cb1af95d-af8d-46e5-b8de-1e4f8ee7e9ce" alt="teste" width="400">
  </div>
</div>




