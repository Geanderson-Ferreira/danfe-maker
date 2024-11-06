from datetime import datetime
import pandas as pd
import streamlit as st
import sqlite3
from oobj import get_cupom, xml_to_dataframe
from res import get_res_by_confirmation
from get_token import get_token
from main import get_folios
from doc_models import modelos

st.set_page_config(layout='wide')
st.sidebar.title("Filtros")

hotel = st.sidebar.text_input("Hotel ID")
reserva_input = st.sidebar.text_input("Reserva")
search = st.sidebar.button("Buscar")

if search:
    conn = sqlite3.connect('config.db')
    cur = conn.cursor()

    hoteis = cur.execute(f"SELECT * FROM HOTEIS WHERE codigohotel = '{hotel}'")
    hotel = hoteis.fetchone()

    if hotel is None:
        st.write("Hotel não encontrado")
        exit()
    st.title(f"{hotel[1]}")

    reserva = get_res_by_confirmation(reserva_input, hotel[0], get_token())

    if reserva is None:
        st.write("Reserva não encontrada.")
        exit()

    folios = get_folios(reserva, hotel[0])

    there_are_folios = len([x['folio'] for x in folios if len(x['postings']) > 0]) > 0

    if there_are_folios:
        for folio in folios:
            # st.write(f" Numero: {folio['folio']}")
            # st.write(f"Tomador: {folio['payee']['payeeName']}")
            postings = folio['postings']

            df_final = pd.DataFrame()
            cupons_importados = []
            for post in postings:

                if post['nf'] not in cupons_importados:
                    
                    cupons_importados.append(post['nf'])

                    data_cupom = datetime.strptime(post['date'], "%Y-%m-%d")
                    ano_cupom = data_cupom.year

                    xml_string = get_cupom(hotel[4], modelos[hotel[0]], ano_cupom, post['serie'], post['nf'])

                    frame = xml_to_dataframe(xml_string)
                    frame['cupom'] = post['nf']

                    df_final = pd.concat([df_final, frame])
                    df_final['vProd'] = pd.to_numeric(df_final['vProd'], errors='coerce')



            st.dataframe({'RPS': [folio['folio']], 'Tomador': [folio['payee']['payeeName']], 'Valor Estimado': [df_final['vProd'].sum()]})
            st.dataframe(df_final, hide_index=True, use_container_width=True)