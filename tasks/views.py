from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from datetime import datetime, timedelta
import os
import time
from tqdm import tqdm

def pncp(data_inicial, data_final, codigo_modalidade, tamanho_pagina, cod_municipio_ibge, esfera):

    data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').strftime('%Y%m%d')
    data_final = datetime.strptime(data_final, '%Y-%m-%d').strftime('%Y%m%d')
    
    url = 'https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao'
    headers = {'accept': '*/*'}
    todos_os_registros = []

    params = {
        'dataInicial': data_inicial,
        'dataFinal': data_final,
        'codigoModalidadeContratacao': codigo_modalidade,
        'pagina': '1',
        'tamanhoPagina': tamanho_pagina,
        'codigoMunicipioIbge': cod_municipio_ibge
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        dados = response.json()
        total_paginas = dados['totalPaginas']
        todos_os_registros.extend(dados['data'])
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

    for pagina in tqdm(range(2, total_paginas+1), desc="Consultando páginas"):
        params['pagina'] = str(pagina)
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            dados = response.json()
            todos_os_registros.extend(dados['data'])
            time.sleep(1)  # Adiciona um atraso para evitar ultrapassar o limite de requisições
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    registros_filtrados = [
        item for item in todos_os_registros
        if item['orgaoEntidade']['esferaId'] == esfera
    ]

    pasta = 'pncp_dados'
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    nome_arquivo = f"contratacoes_{cod_municipio_ibge}_{codigo_modalidade}_{data_inicial}_{data_final}.json" 
    file_path = os.path.join(pasta, nome_arquivo)

    dados_para_salvar = {
        'totalPaginas': total_paginas,
        'totalRegistrosFiltrados': len(registros_filtrados),
        'registros': registros_filtrados
    }

    with open(file_path, "w") as file:
        json.dump(dados_para_salvar, file, indent=4)

    return {
        'totalRegistrosFiltrados': len(registros_filtrados),
        'totalPaginas': total_paginas,
        'file_path': file_path
    }

def pncp(data_inicial, data_final, tamanho_pagina, cod_municipio_ibge, esfera):

    data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').strftime('%Y%m%d')
    data_final = datetime.strptime(data_final, '%Y-%m-%d').strftime('%Y%m%d')
    
    url = 'https://pncp.gov.br/api/consulta/v1/contratos'
    headers = {'accept': '*/*'}
    todos_os_registros = []

    params = {
        'dataInicial': data_inicial,
        'dataFinal': data_final,
        'pagina': '1',
        'tamanhoPagina': tamanho_pagina
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        dados = response.json()
        total_paginas = dados['totalPaginas']
        todos_os_registros.extend(dados['data'])
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

    for pagina in tqdm(range(2, total_paginas+1), desc="Consultando páginas"):
        params['pagina'] = str(pagina)
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            dados = response.json()
            todos_os_registros.extend(dados['data'])
            time.sleep(1)  # Adiciona um atraso para evitar ultrapassar o limite de requisições
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    registros_filtrados = [
        item for item in todos_os_registros
        if item['orgaoEntidade']['esferaId'] == esfera
        if item['unidadeOrgao']['codigoIbge'] == cod_municipio_ibge
    ]

    pasta = 'pncp_dados'
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    nome_arquivo = f"contratos{cod_municipio_ibge}_{data_inicial}_{data_final}.json" 
    file_path = os.path.join(pasta, nome_arquivo)

    dados_para_salvar = {
        'totalPaginas': total_paginas,
        'totalRegistrosFiltrados': len(registros_filtrados),
        'registros': registros_filtrados
    }

    with open(file_path, "w") as file:
        json.dump(dados_para_salvar, file, indent=4)

    return {
        'totalRegistrosFiltrados': len(registros_filtrados),
        'totalPaginas': total_paginas,
        'file_path': file_path
    }


def consulta_view(request):
    if request.method == 'POST':
        data_inicial = request.POST.get('data-inicial')
        data_final = request.POST.get('data-final')
        codigo_modalidade = request.POST.get('modalidade-contratacao')
        tamanho_pagina = request.POST.get('tamanho-pagina')
        cod_municipio_ibge = request.POST.get('municipios')
        esfera = request.POST.get('esfera')

        resultado = pncp(data_inicial, data_final, codigo_modalidade, tamanho_pagina, cod_municipio_ibge, esfera)

        return JsonResponse(resultado)
    return render(request, 'tasks/task_list.html')

def contrato_view(request):
    if request.method == 'POST':
        data_inicial = request.POST.get('data-inicial')
        data_final = request.POST.get('data-final')
        tamanho_pagina = request.POST.get('tamanho-pagina')
        cod_municipio_ibge = request.POST.get('municipios')
        esfera = request.POST.get('esfera')

        resultado = pncp(data_inicial, data_final, tamanho_pagina, cod_municipio_ibge, esfera)

        return JsonResponse(resultado)
    return render(request, 'tasks/contratos.html')
