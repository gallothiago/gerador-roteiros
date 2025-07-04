import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    print("ERRO: GOOGLE_API_KEY não configurada nas variáveis de ambiente.")

PLACES_API_BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
GEOCODING_API_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

INTERESTS_TO_PLACE_TYPES = {
    "praias": ["beach", "natural_feature"],
    "museus": ["museum", "art_gallery"],
    "trilhas": ["park", "natural_feature", "point_of_interest"],
    "vida-noturna": ["night_club", "bar"],
    "compras": ["shopping_mall", "store", "department_store"],
    "gastronomia": ["restaurant", "food", "cafe", "bakery"],
    "monumentos": ["point_of_interest", "tourist_attraction", "historic_site"],
    "historia": ["historic_site", "museum", "church", "synagogue", "hindu_temple", "mosque"],
    "fotografia": ["tourist_attraction", "point_of_interest", "park", "natural_feature"],
    "relax": ["spa", "park", "beach", "beauty_salon"],
    "romance": ["restaurant", "point_of_interest", "park", "bar"],
    "arte": ["art_gallery", "museum"],
    "parques": ["amusement_park", "park", "zoo"],
    "diversao": ["amusement_park", "park", "aquarium", "bowling_alley", "movie_theater"],
    "natureza": ["natural_feature", "park"],
    "aventura": ["park", "natural_feature", "amusement_park"]
}

TIPO_VIAJANTE_PESOS = {
    "familia": {"park": 4, "amusement_park": 5, "zoo": 4, "aquarium": 4, "museum": 3, "beach": 3},
    "aventureiro": {"natural_feature": 5, "park": 4, "beach": 4, "night_club": 3, "bar": 3},
    "cultural": {"museum": 5, "art_gallery": 4, "historic_site": 4, "point_of_interest": 3},
    "gastronomico": {"restaurant": 6, "food": 5, "cafe": 4, "bakery": 3},
    "casais": {"restaurant": 4, "point_of_interest": 4, "park": 3, "bar": 3, "spa": 3},
    "relax": {"spa": 5, "park": 4, "beach": 4, "beauty_salon": 3}
}

PRICE_LEVEL_MAP = {
    0: "Grátis",
    1: "Barato",
    2: "Moderado",
    3: "Caro",
    4: "Muito Caro"
}

def get_coordinates(city_name):
    """Obtém as coordenadas geográficas de uma cidade usando a Geocoding API."""
    params = {
        "address": city_name,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(GEOCODING_API_BASE_URL, params=params)
    data = response.json()

    if data['status'] == 'OK' and data['results']:
        location = data['results'][0]['geometry']['location']
        return f"{location['lat']},{location['lng']}"
    print(f"DEBUG: Não foi possível obter coordenadas para '{city_name}'. Status: {data.get('status', 'N/A')}, Mensagem: {data.get('error_message', 'N/A')}")
    return None

def search_places(query, location_bias=None, place_types=None, min_price=None, max_price=None):
    """
    Busca lugares usando a Google Places Text Search API.
    """
    params = {
        "query": query,
        "key": GOOGLE_API_KEY,
        "language": "pt-BR"
    }
    
    if location_bias:
        params["locationbias"] = location_bias

    if min_price is not None:
        params["minprice"] = min_price
    if max_price is not None:
        params["maxprice"] = max_price

    print(f"DEBUG: Enviando query para Google Places API: '{query}' com params: {params}")
    response = requests.get(PLACES_API_BASE_URL, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        print(f"DEBUG: Search for '{query}' returned {len(data['results'])} results.")
        return data['results']
    else:
        print(f"Erro ao buscar lugares (query: '{query}'): {data.get('error_message', data['status'])}")
        return []

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Backend Flask está rodando!")

@app.route('/api/generate_roteiro', methods=['POST'])
def generate_roteiro():
    print("DEBUG: Requisição para generate_roteiro recebida.")
    data = request.json
    destino = data.get('destino', '').lower()
    data_inicio_str = data.get('dataInicio')
    data_fim_str = data.get('dataFim')
    orcamento_usuario = float(data.get('orcamento'))
    tipo_viajante = data.get('tipoViajante')
    interesses_usuario = data.get('interesses', [])
    print(f"DEBUG: Destino: '{destino}', Interesses Selecionados: {interesses_usuario}, Orçamento: {orcamento_usuario}, Tipo Viajante: {tipo_viajante}")

    if not GOOGLE_API_KEY:
        return jsonify({"mensagem": "Erro: Chave de API do Google não configurada no backend."}), 500
    
    try:
        data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d')
        dias_viagem = (data_fim - data_inicio).days + 1
    except (ValueError, TypeError):
        return jsonify({"mensagem": "Formato de data inválido."}), 400

    coords = get_coordinates(destino)
    if not coords:
        return jsonify({"mensagem": f"Não foi possível encontrar coordenadas para o destino '{destino}'."}), 404

    location_bias_str = f"point:{coords}"

    max_price_level = 4
    if orcamento_usuario < 600:
        max_price_level = 1
    elif orcamento_usuario < 2000:
        max_price_level = 2
    elif orcamento_usuario < 4000:
        max_price_level = 3
    print(f"DEBUG: Max Price Level Calculado (baseado no orçamento): {max_price_level}")
    
    # --- Coleta de Pontos de Interesse da Google Places API ---
    all_places_from_api = []
    
    # Priorizar buscas específicas baseadas nos interesses do usuário
    for interesse in interesses_usuario:
        print(f"DEBUG: Processando interesse: '{interesse}'")
        if interesse == "praias":
            all_places_from_api.extend(search_places(f"praias em {destino}", location_bias=location_bias_str, max_price=max_price_level))
            all_places_from_api.extend(search_places(f"orla de {destino}", location_bias=location_bias_str, max_price=max_price_level))
            all_places_from_api.extend(search_places(f"piscinas naturais em {destino}", location_bias=location_bias_str, max_price=max_price_level))
        elif interesse == "museus":
            print(f"DEBUG: Iniciando busca por museus para '{destino}' (sem restrição de preço inicial)") # NOVO LOG
            # REMOVIDO: max_price=max_price_level para Museus
            all_places_from_api.extend(search_places(f"museu {destino}", location_bias=location_bias_str)) 
            all_places_from_api.extend(search_places(f"galeria de arte {destino}", location_bias=location_bias_str))
            all_places_from_api.extend(search_places(f"centro cultural {destino}", location_bias=location_bias_str))
            all_places_from_api.extend(search_places(f"sítio histórico {destino}", location_bias=location_bias_str))
            all_places_from_api.extend(search_places(f"casa de cultura {destino}", location_bias=location_bias_str))
            all_places_from_api.extend(search_places(f"atrações culturais em {destino}", location_bias=location_bias_str))
        elif interesse == "gastronomia":
            all_places_from_api.extend(search_places(f"melhores restaurantes em {destino}", location_bias=location_bias_str, max_price=max_price_level))
            all_places_from_api.extend(search_places(f"bares e restaurantes em {destino}", location_bias=location_bias_str, max_price=max_price_level))
            all_places_from_api.extend(search_places(f"cafes em {destino}", location_bias=location_bias_str, max_price=max_price_level))
            all_places_from_api.extend(search_places(f"padarias e docerias em {destino}", location_bias=location_bias_str, max_price=max_price_level))
        elif interesse == "natureza":
            all_places_from_api.extend(search_places(f"parques naturais em {destino}", location_bias=location_bias_str, max_price=max_price_level))
            all_places_from_api.extend(search_places(f"reservas ecológicas em {destino}", location_bias=location_bias_str, max_price=max_price_level))
            all_places_from_api.extend(search_places(f"trilhas em {destino}", location_bias=location_bias_str, max_price=max_price_level))
            all_places_from_api.extend(search_places(f"jardins botânicos em {destino}", location_bias=location_bias_str, max_price=max_price_level))
        elif interesse == "historia":
            print(f"DEBUG: Iniciando busca por história para '{destino}' (sem restrição de preço inicial)") # NOVO LOG
            # REMOVIDO: max_price=max_price_level para Historia
            all_places_from_api.extend(search_places(f"pontos históricos em {destino}", location_bias=location_bias_str))
            all_places_from_api.extend(search_places(f"igrejas históricas em {destino}", location_bias=location_bias_str))
            all_places_from_api.extend(search_places(f"monumentos históricos em {destino}", location_bias=location_bias_str))
        else:
            for place_type in INTERESTS_TO_PLACE_TYPES.get(interesse, []):
                query_str = f"{place_type.replace('_', ' ')} em {destino}"
                all_places_from_api.extend(search_places(query_str, location_bias=location_bias_str, max_price=max_price_level))
    
    # Buscas gerais para o destino
    print(f"DEBUG: Iniciando buscas gerais para '{destino}' (sem restrição de preço inicial)") # NOVO LOG
    # REMOVIDO: max_price=max_price_level para buscas gerais
    all_places_from_api.extend(search_places(f"atrações turísticas em {destino}", location_bias=location_bias_str))
    all_places_from_api.extend(search_places(f"melhores lugares para visitar em {destino}", location_bias=location_bias_str))
    all_places_from_api.extend(search_places(f"pontos turísticos em {destino}", location_bias=location_bias_str))

    # Remove duplicatas
    unique_places_map = {place['place_id']: place for place in all_places_from_api if 'place_id' in place}
    pontos_disponiveis = list(unique_places_map.values())
    print(f"DEBUG: Total de pontos únicos coletados da API: {len(unique_places_map)}")

    if not pontos_disponiveis:
        print(f"DEBUG: Nenhum ponto disponível após a coleta inicial da API para {destino} com os interesses {interesses_usuario}.")
        return jsonify({"mensagem": f"Não foram encontrados pontos de interesse para '{destino}' com os critérios fornecidos. Tente interesses diferentes ou um orçamento maior."}), 404
    
    pontos_para_roteiro_com_scores = []
    for place in pontos_disponiveis:
        nome_ponto = place.get('name', 'Ponto Desconhecido')
        google_types = place.get('types', [])
        price_level = place.get('price_level', None)
        
        price_level_text = PRICE_LEVEL_MAP.get(price_level, "Não Informado")
        
        custo_estimado_inferido = "desconhecido"
        if price_level is not None:
            if price_level >= 3:
                custo_estimado_inferido = "alto"
            elif price_level == 2:
                custo_estimado_inferido = "medio"
            elif price_level <= 1:
                custo_estimado_inferido = "baixo"

        interesses_inferidos = []
        for interesse_key, google_types_list in INTERESTS_TO_PLACE_TYPES.items():
            if any(gt in google_types for gt in google_types_list):
                interesses_inferidos.append(interesse_key)
        
        score = 0
        
        # SUPER IMPULSO para correspondências diretas com os interesses do usuário
        for interesse_key in interesses_usuario:
            if interesse_key in INTERESTS_TO_PLACE_TYPES:
                if any(gt in google_types for gt in INTERESTS_TO_PLACE_TYPES[interesse_key]):
                    score += 200
            
        # Pontuação aprimorada: Maior peso para tipo de viajante
        if tipo_viajante and tipo_viajante in TIPO_VIAJANTE_PESOS:
            for google_type_peso, peso in TIPO_VIAJANTE_PESOS[tipo_viajante].items():
                if google_type_peso in google_types:
                    score += peso

        # Penalidade se o preço for muito acima do orçamento do usuário
        # Esta penalidade continua a ser aplicada na fase de pontuação,
        # mas só depois que os lugares foram coletados SEM a restrição de preço inicial.
        if price_level is not None and price_level > max_price_level:
            score = max(0, score - (price_level - max_price_level) * 10)

        duracao_horas_inferida = 2
        if any(t in google_types for t in ["museum", "art_gallery", "historic_site"]):
            duracao_horas_inferida = random.choice([2, 3])
        if any(t in google_types for t in ["shopping_mall", "amusement_park", "park", "zoo"]):
            duracao_horas_inferida = random.choice([3, 4, 5])
        if any(t in google_types for t in ["beach", "natural_feature"]):
            duracao_horas_inferida = random.choice([3, 4])
        if any(t in google_types for t in ["restaurant", "food", "bar", "night_club"]):
            duracao_horas_inferida = random.choice([1, 2])

        melhor_periodo_dia_inferido = ["manha", "tarde"]
        if any(t in google_types for t in ["night_club", "bar"]):
            melhor_periodo_dia_inferido = ["noite"]
        if any(t in google_types for t in ["restaurant", "food", "cafe"]):
            melhor_periodo_dia_inferido = random.choice([["manha", "tarde"], ["tarde", "noite"]])
        if any(t in google_types for t in ["restaurant", "food"]) and "dinner" in google_types:
             melhor_periodo_dia_inferido.append("noite")
        
        if any(t in google_types for t in ["amusement_park"]):
            melhor_periodo_dia_inferido = ["dia_inteiro"]

        # Pontuação base mínima para garantir que o item seja considerado
        if score == 0:
            score = 10
        elif score < 25:
            score = 25


        pontos_para_roteiro_com_scores.append({
            "ponto": {
                "nome": nome_ponto,
                "interesses": interesses_inferidos,
                "duracao_horas": duracao_horas_inferida,
                "custo_estimado": custo_estimado_inferido,
                "custo_detalhado": price_level_text,
                "ideal_para": google_types,
                "melhor_periodo_dia": melhor_periodo_dia_inferido,
                "place_id": place.get('place_id')
            },
            "score": score
        })

    # Filtrar pontos com score muito baixo
    pontos_filtrados_por_score = [item for item in pontos_para_roteiro_com_scores if item['score'] >= 30] 
    print(f"DEBUG: Pontos após filtragem por score (>=30): {len(pontos_filtrados_por_score)}")
    
    if not pontos_filtrados_por_score:
        print(f"DEBUG: Nenhum ponto disponível após a filtragem por score (mínimo 30) para {destino} com os interesses {interesses_usuario}.")
        return jsonify({"mensagem": f"Não foram encontrados pontos de interesse relevantes para '{destino}' com os critérios fornecidos (após pontuação). Tente interesses diferentes ou um orçamento maior."}), 404

    # Ordenar por score
    pontos_filtrados_por_score.sort(key=lambda x: x["score"], reverse=True)
    
    pontos_para_roteiro = pontos_filtrados_por_score

    # --- Geração do Roteiro ---
    roteiro_gerado = []
    atividades_usadas_geral = set()

    for dia_num in range(1, dias_viagem + 1):
        pontos_disponiveis_hoje = [item for item in pontos_para_roteiro if item['ponto']['place_id'] not in atividades_usadas_geral]
        pontos_disponiveis_hoje.sort(key=lambda x: x['score'], reverse=True)

        manha_slot = None
        tarde_slot = None
        noite_slot = None

        # Tentar preencher atividades de "dia_inteiro" primeiro
        for item in pontos_disponiveis_hoje:
            ponto = item['ponto']
            if "dia_inteiro" in ponto.get('melhor_periodo_dia', []) and not manha_slot and not tarde_slot and ponto['place_id'] not in atividades_usadas_geral:
                manha_slot = ponto
                tarde_slot = {"nome": "marcador_ocupado_dia_inteiro"}
                atividades_usadas_geral.add(ponto['place_id'])
                break
        
        # Preencher slots restantes por prioridade e score
        
        # Noite
        for item in pontos_disponiveis_hoje:
            ponto = item['ponto']
            if ponto['place_id'] not in atividades_usadas_geral and "noite" in ponto.get('melhor_periodo_dia', []) and not noite_slot:
                noite_slot = ponto
                atividades_usadas_geral.add(ponto['place_id'])
                break
        
        # Manhã
        for item in pontos_disponiveis_hoje:
            ponto = item['ponto']
            if ponto['place_id'] not in atividades_usadas_geral and "manha" in ponto.get('melhor_periodo_dia', []) and not manha_slot:
                manha_slot = ponto
                atividades_usadas_geral.add(ponto['place_id'])
                break
        
        # Tarde
        for item in pontos_disponiveis_hoje:
            ponto = item['ponto']
            if ponto['place_id'] not in atividades_usadas_geral and "tarde" in ponto.get('melhor_periodo_dia', []) and not tarde_slot:
                tarde_slot = ponto
                atividades_usadas_geral.add(ponto['place_id'])
                break

        # Preencher slots vazios com qualquer ponto restante de alto score
        pontos_restantes_para_dia = [item for item in pontos_disponiveis_hoje if item['ponto']['place_id'] not in atividades_usadas_geral]
        pontos_restantes_para_dia.sort(key=lambda x: x['score'], reverse=True)

        for item in pontos_restantes_para_dia:
            ponto = item['ponto']
            if not manha_slot and ponto['duracao_horas'] <= 3:
                manha_slot = ponto
                atividades_usadas_geral.add(ponto['place_id'])
            elif not tarde_slot and ponto['duracao_horas'] <= 4:
                tarde_slot = ponto
                atividades_usadas_geral.add(ponto['place_id'])
            elif not noite_slot and ponto['duracao_horas'] <= 3:
                noite_slot = ponto
                atividades_usadas_geral.add(ponto['place_id'])

        final_activities = []

        # Formato do link do Google Maps
        MAPS_LINK_BASE = "http://maps.google.com/?q=place_id:" # CORREÇÃO FINAL NO LINK DO GOOGLE MAPS

        if manha_slot and manha_slot["nome"] != "marcador_ocupado_dia_inteiro":
            link = f"<a href='{MAPS_LINK_BASE}{manha_slot['place_id']}' target='_blank' rel='noopener noreferrer'>{manha_slot['nome']}</a>" if manha_slot.get('place_id') else manha_slot['nome']
            final_activities.append(f"8h da Manhã: {link} ({manha_slot['duracao_horas']}h, {manha_slot['custo_detalhado']})")
        
        if tarde_slot and tarde_slot["nome"] != "marcador_ocupado_dia_inteiro":
            link = f"<a href='{MAPS_LINK_BASE}{tarde_slot['place_id']}' target='_blank' rel='noopener noreferrer'>{tarde_slot['nome']}</a>" if tarde_slot.get('place_id') else tarde_slot['nome']
            final_activities.append(f"13h da Tarde: {link} ({tarde_slot['duracao_horas']}h, {tarde_slot['custo_detalhado']})")
        
        if noite_slot:
            link = f"<a href='{MAPS_LINK_BASE}{noite_slot['place_id']}' target='_blank' rel='noopener noreferrer'>{noite_slot['nome']}</a>" if noite_slot.get('place_id') else noite_slot['nome']
            final_activities.append(f"19h da Noite: {link} ({noite_slot['duracao_horas']}h, {noite_slot['custo_detalhado']})")
        
        if not final_activities:
            final_activities.append("Nenhuma atividade específica sugerida para este dia. Explore por conta própria!")


        roteiro_gerado.append({
            "dia": dia_num,
            "atividades": final_activities
        })

    sugestao_orcamento = "Seu orçamento parece adequado para as atividades sugeridas."
    if max_price_level == 4:
        sugestao_orcamento = "Com seu orçamento, você tem muitas opções de luxo e atividades exclusivas!"
    elif max_price_level == 3:
        sugestao_orcamento = "Ótimo orçamento! Você poderá aproveitar muitas experiências sem se preocupar tanto."
    elif max_price_level == 2:
        sugestao_orcamento = "Seu orçamento médio permite uma boa variedade de atividades e conforto. Explore bem as opções!"
    else:
        sugestao_orcamento = "Com um orçamento mais restrito, priorize atividades gratuitas e econômicas. Há muitas opções charmosas!"


    return jsonify({"roteiro": roteiro_gerado, "sugestao_orcamento": sugestao_orcamento})

if __name__ == '__main__':
    app.run(debug=True, port=5000)