Gerador de Roteiros de Viagem
Um aplicativo web full-stack para gerar roteiros de viagem personalizados com base no destino, datas, orçamento e interesses do usuário.

🚀 Tecnologias
Backend (Python)
Python 3.x: Linguagem de programação.

Flask: Framework para o desenvolvimento da API.

Requests: Biblioteca para fazer requisições HTTP para a API do Google Places.

python-dotenv: Para gerenciar variáveis de ambiente.

Frontend (React)
React.js (Vite): Biblioteca JavaScript para construir a interface de usuário.

JavaScript (ES6+): Linguagem de programação.

Axios: Cliente HTTP para fazer requisições à API do backend.

HTML5 e CSS3: Estrutura e estilização.

🛠️ Funcionalidades
Backend:

Interage com a API do Google Places para buscar pontos de interesse.

Filtra e pontua os locais com base no orçamento e nos interesses do usuário.

Gera um roteiro otimizado.

Frontend:

Interface amigável para o usuário inserir suas preferências.

Exibe o roteiro de viagem gerado de forma clara e intuitiva.

⚙️ Pré-requisitos
Para rodar o projeto localmente, você precisará ter instalado:

Python 3.8+

Node.js (LTS recomendado)

npm ou Yarn

Uma chave da Google Cloud Platform (GCP) com as APIs Places e Geocoding ativadas.

🔧 Configuração e Instalação
1. Backend
Clone o repositório.

Navegue até a pasta do backend (backend/).

Crie um ambiente virtual e ative-o:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat  # Windows

Instale as dependências:
pip install -r requirements.txt

Crie um arquivo .env na pasta backend/ com sua chave da API do Google:
GOOGLE_API_KEY="SUA_CHAVE_AQUI"

Inicie o servidor:
flask run

2. Frontend
Navegue até a pasta do frontend (frontend/).

Instale as dependências:
npm install
# ou
yarn install

Inicie o aplicativo React:
npm run dev
# ou
yarn dev


