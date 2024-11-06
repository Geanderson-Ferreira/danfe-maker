def extrair_serie_nf(texto):
    serie = None
    nf = None
    
    # Percorrer cada caractere da string
    i = 0
    while i < len(texto):
        # Se encontrar "Serie:", capture o valor após
        if texto[i:i+6] == "Serie:":
            i += 6  # Pular a palavra "Serie:"
            valor_serie = ""
            while i < len(texto) and texto[i].isdigit():  # Captura até o primeiro espaço
                valor_serie += texto[i]
                i += 1
            serie = valor_serie.strip()
        
        # Se encontrar "NF:", capture o valor após
        elif texto[i:i+3] == "NF:":
            i += 3  # Pular a palavra "NF:"
            valor_nf = ""
            while i < len(texto) and texto[i].isdigit():  # Captura até o primeiro espaço
                valor_nf += texto[i]
                i += 1
            nf = valor_nf.strip()
        
        else:
            i += 1  # Avança para o próximo caractere
    
    return {"serie":serie, "nf": nf}

