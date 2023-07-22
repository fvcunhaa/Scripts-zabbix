# Nome do Script: Export_Templates
# Descrição: Exporta do Zabbix os templates e salva numa pasta
# Autor: Francisco Cunha
# Data: 08/07/2023
# Versão: V1.0


import os
import requests
import json

def get_template_ids_by_hostgroup(url, auth_token, hostgroup_id):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": ["templateid", "name"],  # Adicionamos "name" aos campos de saída
            "groupids": hostgroup_id
        },
        "auth": auth_token,
        "id": 1
    }

    # Faz a requisição POST para obter a lista de templates pelo Host Group
    response = requests.post(f'{url}/zabbix/api_jsonrpc.php', json=data, headers=headers)

    if response.status_code == 200:
        templates = response.json()['result']
        return templates
    else:
        print(f"Não foi possível obter a lista de templates do Host Group. Código de status: {response.status_code}")
        print(response.text)
        return None

def export_template_to_file(url, auth_token, template_id, template_name):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "jsonrpc": "2.0",
        "method": "configuration.export",
        "params": {
            "options": {
                "templates": [
                    template_id
                ]
            },
            "format": "json",  # Modificamos para exportar em formato JSON
        },
        "auth": auth_token,
        "id": 1
    }

    # Faz a requisição POST para exportar o template no formato JSON
    response = requests.post(f'{url}/zabbix/api_jsonrpc.php', json=data, headers=headers)

    if response.status_code == 200:
        # Limpando o nome do template para conter apenas caracteres válidos para o nome de arquivos
        template_name_cleaned = ''.join(c if c.isalnum() or c in ('_', '-', ' ') else '_' for c in template_name)

        # Caminho para salvar o arquivo no diretório C:\Temp
        output_file_path = os.path.join('C:\\Temp\\templates', f'{template_name_cleaned}.json')

        # Salva a resposta em um arquivo
        with open(output_file_path, 'w') as file:
            file.write(json.dumps(response.json(), indent=4))

        print(f"Template '{template_name}' exportado com sucesso para o arquivo '{output_file_path}'.")
    else:
        print(f"Não foi possível exportar o template {template_name}. Código de status: {response.status_code}")
        print(response.text)

# Informe os detalhes da sua requisição
zabbix_url = 'http://localhost/zabbix/api_jsonrpc.php' # Aqui você deve colocar a URL do seu zabbix
api_token = 'Seu token aqui' # Aqui você irá colocar o token de autenticação
hostgroup_id = '1'  # Substitua pelo ID do Host Group que contém os templates

# Obtém a lista de IDs e nomes dos templates no Host Group
template_infos = get_template_ids_by_hostgroup(zabbix_url, api_token, hostgroup_id)

if template_infos:
    for template_info in template_infos:
        template_id = template_info['templateid']
        template_name = template_info['name']
        export_template_to_file(zabbix_url, api_token, template_id, template_name)
