from datetime import datetime
import sqlite3
import pandas as pd
import requests
import json
from pprint import pprint

from oobj import get_cupom, make_frame_with_xml_cupom, xml_to_dataframe
from res import get_res
from utils import extrair_serie_nf
from get_token import get_token
from doc_models import modelos

reservation_conf = '126746236'
reservation_id = '6737105'
RPS_Number = '476947'
valor = '73'
window = '1'

token = get_token()

def get_folios(reservation_id, hotel_id):

    payee_info = None
    postings_list = []

    for window in [1,2,3,4,5,6,7,8]:

        url = f"https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com/csh/v1/hotels/{hotel_id}/reservations/{reservation_id}/folios?folioWindowNo={window}&limit=10000&fetchInstructions=Account&fetchInstructions=Postings&fetchInstructions=Totalbalance&fetchInstructions=Transactioncodes&fetchInstructions=Windowbalances&fetchInstructions=Payment&fetchInstructions=Reservation&fetchInstructions=Payee&guestPayOnly=Y&reservationBalanceOnly=false&includeFolioHistory=false"

        payload = ""
        headers = {
        'Content-Type': 'application/json',
        'x-hotelid': hotel_id,
        'x-app-key': '5502014f-a4f1-4135-9d45-ae5fd594eba5',
        'x-externalsystem': 'TARS',
        'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        windows = response.json()['reservationFolioInformation']['folioWindows']
        # print(f"\nReserva {reservation_id}")
        window_number = 1

        for window in windows:
            folios = window.get('folios', False)

            if folios != False:
                folios_list = []
                fake_number = 1
                for folio in folios:
                    
                    folio_number = folio.get('folioNo',f'folio{fake_number}')
                    fake_number += 1
                    payee_info = folio.get('payeeInfo', 'Sem pagador')
                    payee_name = payee_info.get('payeeName')
                    payee_id = payee_info.get('')

                    postings = folio['postings']
                    # print("\n"*2, folio_number)
                    # print('Pagador:', payee_name)
                    # print(folio)

                    # pprint(f'Qtdade de Itens: {len(postings)}')

                    for post in postings:
                        reference = post.get('reference')
                        date = post.get('transactionDate')
                        checkNo = post.get('checkNo')

                        if reference is not None:
                            
                            if "CHECK#" in reference:
                                # print(checkNo)
                                dados = extrair_serie_nf(reference)
                                dados['date'] = date
                                postings_list.append(dados)

                                
                    folios_list.append({'folio': folio_number,'payee': payee_info if payee_info is not None else None, 'postings': postings_list})

            window_number += 1

    return folios_list


"""
conn = sqlite3.connect('config.db')
cur = conn.cursor()

hoteis = cur.execute("SELECT * FROM HOTEIS WHERE servidorhotel = 'ACC2'")
# for hotel in hoteis.fetchall():
#     print(hotel)


for hotel in hoteis:

    if hotel[0] != 'H9564':
        continue

    print(hotel[0])
    cnpj = hotel[4]
    cupons_importados = []
    doc_model = modelos[hotel[0]]

    for res in get_res(hotel[0], token):

        folio = get_folios(res, hotel[0])
        
        df_final = pd.DataFrame()

        for post in folio['postings']:

            if post['nf'] not in cupons_importados:
                
                cupons_importados.append(post['nf'])

                data_cupom = datetime.strptime(post['date'], "%Y-%m-%d")
                ano_cupom = data_cupom.year

                xml_string = get_cupom(cnpj, doc_model, ano_cupom, post['serie'], post['nf'])
                try:
                    frame = xml_to_dataframe(xml_string)
                    frame['cupom'] = post['nf']

                    df_final = pd.concat([df_final, frame])

                    # print(frame, '\n\n')
                except:
                    print(cnpj, doc_model, ano_cupom, post['serie'], post['nf'])
        if df_final.empty:
            continue
        
        print(df_final)
"""