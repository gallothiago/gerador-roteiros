# Gerador de Roteiros de Viagem

Este é um projeto web Fullstack que permite aos usuários gerar roteiros de viagem personalizados com base em seu destino, datas, orçamento e interesses.

## Visão Geral

O projeto é composto por duas partes principais:

-   **Backend:** Desenvolvido em Python com o framework Flask. Responsável por interagir com a Google Places API para buscar pontos de interesse, aplicar filtros de orçamento e interesses, pontuar os lugares e gerar um roteiro otimizado.
-   **Frontend:** Desenvolvido com React (Vite). Interface de usuário intuitiva para que o viajante possa inserir suas preferências e visualizar o roteiro gerado.

## Funcionalidades

-   Geração de roteiros personalizados por destino, datas de início e fim, orçamento e tipo de viajante.
-   Filtragem de pontos de interesse com base em categorias (Praias, Museus, Gastronomia, etc.).
-   Sugestão de atividades por período do dia (Manhã, Tarde, Noite).
-   Integração com a Google Places API para obter dados de locais (nomes, tipos, níveis de preço).
-   Exibição de links para o Google Maps para cada ponto de interesse no roteiro.

## Tecnologias Utilizadas

**Backend:**
-   Python 3.x
-   Flask
-   Requests (para chamadas HTTP externas, ex: Google APIs)
-   python-dotenv (para carregar variáveis de ambiente)

**Frontend:**
-   React.js (com Vite para um ambiente de desenvolvimento rápido)
-   JavaScript (ES6+)
-   Axios (para requisições HTTP ao backend)
-   HTML5 / CSS3

## Como Rodar o Projeto

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

### Pré-requisitos

-   Python 3.8+
-   Node.js (LTS recomendado)
-   npm ou Yarn
-   Uma chave da Google Cloud Platform (GCP) com as APIs **Places API** e **Geocoding API** ativadas.


