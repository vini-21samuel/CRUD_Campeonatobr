# Sistema de Gerenciamento de Campeonatos de futebol, futsal e entre outras modalidades 🏆

Este projeto é um sistema completo para gerenciar competições esportivas escolares, como torneios de interclasse. Ele combina uma API robusta com uma interface de usuário (frontend) interativa, permitindo criar, listar, atualizar e deletar informações sobre torneios, times, jogadores e partidas. O sistema é projetado para promover organização eficiente e oferecer uma experiência acessível para administradores, como professores e organizadores.

---

## 💡 Para que serve no mundo real?

No contexto real, este sistema pode ser usado por escolas para:
- Gerenciar torneios internos, como competições entre turmas ou times.
- Organizar informações sobre times (nome, logo, local), jogadores (nome, posição, gols) e partidas (datas, resultados).
- Facilitar a administração com uma interface visual para adicionar, editar ou remover dados.
- Fornecer transparência e acesso a estatísticas para alunos, professores e organizadores.

O projeto é flexível e pode ser adaptado para outros tipos de competições esportivas, desde eventos locais até torneios regionais.

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.12**: Linguagem principal para o backend.
- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **SQLAlchemy**: ORM para gerenciamento do banco de dados relacional.
- **Pydantic**: Validação e tipagem de dados nas requisições/respostas.
- **PostgreSQL**: Banco de dados relacional para persistência de dados.
- **Docker**: Contêinerização do ambiente de desenvolvimento e produção.

### Frontend
- **HTML5/CSS3**: Estrutura e estilização da interface de usuário.
- **Bootstrap 5.3**: Framework CSS para design responsivo e componentes prontos.
- **JavaScript (Vanilla)**: Lógica dinâmica no cliente, incluindo chamadas à API via `fetch`.
- **Jinja2**: Motor de templates para renderização dinâmica de páginas no backend.

### Controle de Versão
- **Git**: Gerenciamento de versões do código.

---

## 📌 Estrutura do Sistema

O sistema é composto por uma API RESTful (backend) e uma interface web (frontend). O backend fornece endpoints para manipulação de dados, enquanto o frontend consome esses endpoints e oferece uma experiência visual para os usuários.

### Rotas da API (Backend)

#### 🏠 Main
| Método | Rota       | Descrição                  |
|--------|------------|----------------------------|
| GET    | `/`        | Página principal do sistema |

#### 👤 Usuários
| Método | Rota                | Descrição                   |
|--------|---------------------|-----------------------------|
| GET    | `/usuarios/register` | Formulário de registro      |
| POST   | `/usuarios/register` | Cadastra novo usuário       |
| GET    | `/usuarios/login`    | Formulário de login         |
| POST   | `/usuarios/login`    | Autentica um usuário        |

#### ⚽ Times
| Método | Rota             | Descrição                   |
|--------|------------------|-----------------------------|
| GET    | `/times/`        | Lista todos os times        |
| POST   | `/times/`        | Cadastra um novo time       |
| GET    | `/times/{time_id}` | Detalhes de um time       |
| PUT    | `/times/{time_id}` | Atualiza um time          |
| DELETE | `/times/{time_id}` | Remove um time            |

#### 🏃 Jogadores
| Método | Rota                  | Descrição                   |
|--------|-----------------------|-----------------------------|
| GET    | `/jogadores/`         | Lista todos os jogadores    |
| POST   | `/jogadores/`         | Cadastra um novo jogador    |
| GET    | `/jogadores/{jogador_id}` | Detalhes de um jogador  |
| PUT    | `/jogadores/{jogador_id}` | Atualiza um jogador     |
| DELETE | `/jogadores/{jogador_id}` | Remove um jogador       |

#### 🏟️ Partidas
| Método | Rota                  | Descrição                   |
|--------|-----------------------|-----------------------------|
| GET    | `/partidas/`          | Lista todas as partidas     |
| POST   | `/partidas/`          | Cadastra uma nova partida   |
| GET    | `/partidas/{partida_id}` | Detalhes de uma partida  |
| PUT    | `/partidas/{partida_id}` | Atualiza uma partida     |
| DELETE | `/partidas/{partida_id}` | Remove uma partida       |

#### 🏆 Torneios (Adicionado com base no frontend)
| Método | Rota                              | Descrição                   |
|--------|-----------------------------------|-----------------------------|
| GET    | `/torneios/campeonatos`           | Lista os campeonatos        |
| GET    | `/torneios/sobre`                 | Página "Sobre"              |
| GET    | `/torneios/configurar_campeonato/{torneio_id}` | Configuração de torneio |

### Interface Web (Frontend)
O frontend é uma aplicação dinâmica que consome a API e exibe os dados em uma interface amigável. Ele inclui:
- **Navbar**: Navegação com links para "Início", "Campeonatos", "Sobre" e "Logout".
- **Gerenciamento de Torneios**: Exibe informações do torneio (nome, organizador, data, formato, descrição) e permite gerenciar times, jogadores e partidas.
- **Modais**: Formulários para adicionar/editar times, jogadores e partidas, além de confirmações de deleção com aviso de dependências.

---

## 🚀 Como Configurar e Testar o Sistema

### 1. Pré-requisitos
- **Docker** e **Docker Compose**: Para contêinerização.
- **Git**: Para clonar o repositório.
- **Versão Anterior**: Certifique-se de ter a versão anterior da API (CRUD_Campeonatobr) como referência para migrar dados ou ajustar rotas, se necessário.

### 2. Clonar o Repositório
```bash
git clone https://github.com/vini-21samuel/CRUD_Campeonatobr.git
cd CRUD_Campeonatobr/Projeto
```
