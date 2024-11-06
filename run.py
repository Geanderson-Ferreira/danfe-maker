from datetime import datetime
import sqlite3

import pandas as pd
from main import get_folios
from oobj import get_cupom, xml_to_dataframe
from doc_models import modelos
from get_token import get_token
from res import get_res_by_confirmation

hotel = input("\n\nDiga o ID do hotel: ")

conn = sqlite3.connect('config.db')
cur = conn.cursor()

hoteis = cur.execute(f"SELECT * FROM HOTEIS WHERE codigohotel = '{hotel}'")
hotel = hoteis.fetchone()

if hotel is None:
    print("Hotel não encontrado")
    exit()

reserva = input("Digite o código de uma Reserva: ")

reserva = get_res_by_confirmation(reserva, hotel[0], get_token())

if reserva is None:
    print("Reserva não encontrada.")
    exit()

folios = get_folios(reserva, hotel[0])

there_are_folios = len([x['folio'] for x in folios if len(x['postings']) > 0]) > 0

if there_are_folios:
    print("\nOs fólios disponíveis para Danfe são:")
    for folio in [x['folio'] for x in folios if len(x['postings']) > 0]:
        print(">>", folio)
    
    print("\nPor favor, informe o folio que vc deseja construir a Danfe:")

    folio_no = input("Folio: ")

    while str(folio_no) not in [str(x['folio']) for x in folios]:
        print("Folio não existe, informe um fólio válido.")
        print("\nOs fólios disponíveis para Danfe são:")
        for folio in [x['folio'] for x in folios if len(x['postings']) > 0]:
            print(">>", folio)
        folio_no = input("Folio: ")

    postings = [x for x in folios if str(x['folio']) == str(folio_no)][0].get('postings')
    
    cupons_importados = []
    
    df_final = pd.DataFrame()

    for post in postings:

        if post['nf'] not in cupons_importados:
            
            cupons_importados.append(post['nf'])

            data_cupom = datetime.strptime(post['date'], "%Y-%m-%d")
            ano_cupom = data_cupom.year

            xml_string = get_cupom(hotel[4], modelos[hotel[0]], ano_cupom, post['serie'], post['nf'])

            frame = xml_to_dataframe(xml_string)
            frame['cupom'] = post['nf']

            df_final = pd.concat([df_final, frame])
    
    if df_final.empty == False:
        print("\n Conteúdo da Danfe:")
        print(df_final)
        # df_final.to_excel('teste.xlsx', index=False)
        
        df_final['vProd'] = pd.to_numeric(df_final['vProd'], errors='coerce')
        print(f"\nTotal previsto para danfe: R$ {df_final['vProd'].sum()}")

        to_excel = input("Deseja converter para Excel? (Sim/Nao): ")

        user_wants_to_excel = {
                'sm': True, 's': True, 'sim': True, 'si': True, 'n': False, 'não': False, 'nao': False, 'na': False, 'nã': False, 'no':False
            }

        while to_excel.lower() not in list(user_wants_to_excel.keys()):
            to_excel = input("Deseja converter para Excel? (Sim/Nao): ")

            
        if user_wants_to_excel[to_excel]:
            df_final.to_excel(f'{folio_no}.xlsx', index=False)
            print(f"Arquivo convertido em {folio_no}.xlsx")
            print("\nProcesso Finalizado.")

        else:
            print("Processo Finalizado.")
        print('\n#######')


else:
    print("Não há folios disponíveis para danfe nessa Reserva.")