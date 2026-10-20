from app.esocial.validators.s1000 import validar_s1000

evento = {
    "tpAmb": "2",
    "procEmi": "3",
    "verProc": "1.0",
    "tpInsc": "1",
    "nrInsc": "08806721",
    "iniValid": "2021-07",
    "classTrib": "85",
}

erros = validar_s1000(evento)

if erros:
    for erro in erros:
        print(erro)
else:
    print("Validação básica do S-1000 concluída.")