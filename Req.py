import datetime
import requests
from bs4 import BeautifulSoup


data_atual = datetime.date.today()

data_texto = data_atual.strftime("%m/%d/%Y")
arq = open("dados_ceasa.csv", "w")
linha = "produtos;embalagem;Min;M.c;Max;situacao;mercado;data\n"
arq.write(linha)

while True:
    for i in range(3):
        mercado = ""
        if (i == 0):
            mercado = "211"
        elif (i == 1):
            mercado = "372"
        elif (i == 2):
            mercado = "367"

        r = requests.post("http://200.198.51.71/detec/boletim_completo_es/boletim_completo_es.php",
                          data={
                              "nmgp_url_saida": "http://200.198.51.71/detec/boletim_completo_es/boletim_completo_es.php",
                              "nmgp_parms": "mercod?#?" + mercado + "?@?data?#?" + data_texto + "?@?",
                              "script_case_init": 7647,
                              "script_case_session": "p2jo2bffvn4kgro5d21q02gur1",

                          })

        html_soup = BeautifulSoup(r.text, 'html.parser')
        tabela = html_soup.find("table", class_="scGridTabela")
        if tabela == None:
            continue
        trs = tabela.find_all("tr")

        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            linha = tds[0].text
            for j in range(1, len(tds)):
                linha = linha + ";" + tds[j].text

            data_texto = data_atual.strftime("%d/%m/%Y")
            linha = linha + ";" + mercado + ";" + data_texto +"\n"
            arq.write(linha)

    data_atual = datetime.date.fromordinal(data_atual.toordinal() - 1)
    data_texto = data_atual.strftime("%m/%d/%Y")
