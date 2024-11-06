import requests
import xml.etree.ElementTree as ET
import pandas as pd
from os import environ
from dotenv import load_dotenv

load_dotenv()
 
def get_cupom(cnpj, doc_model, ano, serie, cupom):
    #cnpj, doc_model, ano, serie, cupom
    # url = "https://rest.oobj-dfe.com.br/api/empresas/80732928004863/docs/prod/65/2024/2/21645"
    
    url = f"https://rest.oobj-dfe.com.br/api/empresas/{cnpj}/docs/prod/{doc_model}/{ano}/{serie}/{cupom}"

    payload = ""
    headers = {
    'x-auth-token': environ['OOBJ_TOKEN']
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()['conteudo']
    else:
        print("Função get_cuppom:", response.text)
        return None

def make_frame_with_xml_cupom(xml_string):

    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Extrair namespaces
    namespaces = {
        'nfe': 'http://www.portalfiscal.inf.br/nfe'
    }

    # Extrair os dados do XML
    dados_ide = root.find('.//nfe:ide', namespaces)
    dados_emit = root.find('.//nfe:emit', namespaces)
    dados_produto = root.find('.//nfe:det/nfe:prod', namespaces)
    dados_imposto = root.find('.//nfe:det/nfe:imposto/nfe:ICMS/nfe:ICMS00', namespaces)

    # Criar o dicionário com os dados extraídos
    data = {
        'cUF': dados_ide.find('nfe:cUF', namespaces).text,
        'cNF': dados_ide.find('nfe:cNF', namespaces).text,
        'nNF': dados_ide.find('nfe:nNF', namespaces).text,
        'dhEmi': dados_ide.find('nfe:dhEmi', namespaces).text,
        'xNome': dados_emit.find('nfe:xNome', namespaces).text,
        'CNPJ': dados_emit.find('nfe:CNPJ', namespaces).text,
        'xProd': dados_produto.find('nfe:xProd', namespaces).text,
        'vProd': dados_produto.find('nfe:vProd', namespaces).text,
        'qCom': dados_produto.find('nfe:qCom', namespaces).text,  # Quantidade
        'vICMS': dados_imposto.find('nfe:vICMS', namespaces).text,
        'vNF': root.find('.//nfe:total/nfe:ICMSTot/nfe:vNF', namespaces).text,
        'vPag': root.find('.//nfe:pag/nfe:detPag/nfe:vPag', namespaces).text
    }


    # Criar o dataframe
    df = pd.DataFrame([data])

    # Exibir o dataframe
    return df


def xml_to_dataframe(xml_string):
    # Fazer o parsing do XML
    root = ET.fromstring(xml_string)
    
    # Namespace do XML
    namespaces = {'': 'http://www.portalfiscal.inf.br/nfe'}
    
    # Lista para armazenar os dados dos itens
    items = []
    
    # Encontrar todos os itens (det) dentro da NFe
    for det in root.findall('.//det', namespaces):
        # Coletar os dados principais do produto (det/prod)
        prod = det.find('.//prod', namespaces)
        if prod is not None:
            item_data = {
                'cProd': prod.find('cProd', namespaces).text if prod.find('cProd', namespaces) is not None else None,
                'cEAN': prod.find('cEAN', namespaces).text if prod.find('cEAN', namespaces) is not None else None,
                'xProd': prod.find('xProd', namespaces).text if prod.find('xProd', namespaces) is not None else None,
                'NCM': prod.find('NCM', namespaces).text if prod.find('NCM', namespaces) is not None else None,
                'CFOP': prod.find('CFOP', namespaces).text if prod.find('CFOP', namespaces) is not None else None,
                'uCom': prod.find('uCom', namespaces).text if prod.find('uCom', namespaces) is not None else None,
                'qCom': prod.find('qCom', namespaces).text if prod.find('qCom', namespaces) is not None else None,
                'vUnCom': prod.find('vUnCom', namespaces).text if prod.find('vUnCom', namespaces) is not None else None,
                'vProd': prod.find('vProd', namespaces).text if prod.find('vProd', namespaces) is not None else None
            }
            
            # Adicionar os dados do item à lista
            items.append(item_data)
    
    # Criar o DataFrame
    df = pd.DataFrame(items)
    
    return df
