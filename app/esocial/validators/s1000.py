def validar_s1000(evento):
    erros = []

    if not evento.get("tpAmb"):
        erros.append("Ambiente do eSocial não informado.")

    if not evento.get("procEmi"):
        erros.append("Processo de emissão não informado.")

    if not evento.get("verProc"):
        erros.append("Versão do processo não informada.")

    if not evento.get("tpInsc"):
        erros.append("Tipo de inscrição do empregador não informado.")

    if not evento.get("nrInsc"):
        erros.append("Número de inscrição do empregador não informado.")

    if not evento.get("iniValid"):
        erros.append("Início de validade não informado.")

    if not evento.get("classTrib"):
        erros.append("Classificação tributária não informada.")

    return erros