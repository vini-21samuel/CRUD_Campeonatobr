# API de Interclasse Escolar ⚽

Este projeto é uma API desenvolvida para gerenciar competições esportivas de interclasse em ambiente escolar. A API permite criar, listar, atualizar e deletar informações sobre partidas, equipes e resultados, promovendo uma organização eficiente das competições. Além disso, fornece endpoints bem documentados para interação com o sistema.

---

## 💡 Para que serve no mundo real?

No mundo real, esta API pode ser utilizada por escolas para gerenciar torneios esportivos internos, facilitando a administração e divulgação de informações como:
- Agendamento de partidas.
- Registro de equipes e seus integrantes.
- Controle de resultados e estatísticas de jogos.
- Consulta de informações para alunos, professores e organizadores.

Este projeto pode ser adaptado para atender a qualquer tipo de torneio ou competição esportiva em diversos contextos, promovendo organização e transparência.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**: Linguagem de programação principal.
- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **SQLAlchemy**: ORM para gerenciamento de banco de dados.
- **Pydantic**: Validação e tipagem de dados.
- **Docker**: Contêinerização do ambiente de desenvolvimento.
- **PostgreSQL**: Banco de dados relacional.
- **Git**: Controle de versão.

---

## 📌 Documentação das Rotas

### 🏠 Main

| Método  | Rota         | Descrição |
|---------|-------------|-----------|
| GET     | `/`         | Página principal |


### 👤 Usuários

| Método  | Rota                     | Descrição |
|---------|--------------------------|-----------|
| GET     | `/usuarios/register`      | Retorna o formulário de registro de usuários. |
| POST    | `/usuarios/register`      | Cadastra um novo usuário. |
| GET     | `/usuarios/login`         | Retorna o formulário de login. |
| POST    | `/usuarios/login`         | Autentica um usuário. |

### ⚽ Times

| Método  | Rota                | Descrição |
|---------|---------------------|-----------|
| GET     | `/times/`           | Retorna a lista de times. |
| POST    | `/times/`           | Cadastra um novo time. |
| GET     | `/times/{time_id}`  | Retorna detalhes de um time específico. |
| PUT     | `/times/{time_id}`  | Atualiza um time. |
| DELETE  | `/times/{time_id}`  | Remove um time. |

### 🏃 Jogadores

| Método  | Rota                     | Descrição |
|---------|--------------------------|-----------|
| GET     | `/jogadores/`            | Retorna a lista de jogadores. |
| POST    | `/jogadores/`            | Cadastra um novo jogador. |
| GET     | `/jogadores/{jogador_id}` | Retorna detalhes de um jogador. |
| PUT     | `/jogadores/{jogador_id}` | Atualiza um jogador. |
| DELETE  | `/jogadores/{jogador_id}` | Remove um jogador. |

### 🏟️ Partidas

| Método  | Rota                     | Descrição |
|---------|--------------------------|-----------|
| GET     | `/partidas/`             | Retorna a lista de partidas. |
| POST    | `/partidas/`             | Cadastra uma nova partida. |
| GET     | `/partidas/{partida_id}` | Retorna detalhes de uma partida. |
| PUT     | `/partidas/{partida_id}` | Atualiza uma partida. |
| DELETE  | `/partidas/{partida_id}` | Remove uma partida. |



## 🚀 Como usar o projeto

### 1. Pré-requisitos

Certifique-se de ter os seguintes softwares instalados:
- **Docker** e **Docker Compose**
- **Git**

### 2. Clonar o Repositório

```bash
git clone https://github.com/vini-21samuel/CRUD_Campeonatobr.git
cd Projeto
```
### 3. Configuração com Docker

Subir os contêineres:
```bash
  docker-compose up --build
```
Acesse a aplicação no navegador:
```bash
  http://localhost:8000
```
Teste as rotas na documentação interativa:
```bash
    http://localhost:8000/docs
```
### 4. Uso de Jinja2 para Templates
A aplicação utiliza Jinja2 para renderizar templates HTML. A partir de agora, ao acessar o sistema, você pode ver as páginas com o conteúdo dinâmico sendo gerado diretamente pelo servidor.

### 5. resultados dos templates

<p align="center">
  <img src="https://github.com/user-attachments/assets/dd6b7d7b-3435-40c7-85b7-adb23c42a9aa" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/54d147c7-1cfc-4bd8-a124-0d8fd3b2e708" />
</p>



 


