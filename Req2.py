import requests
from bs4 import BeautifulSoup
import datetime
arq = open("dados_ceagesp.csv","w")
data_atual = datetime.date.today()

data_texto = data_atual.strftime('%d/%m/%Y')

linha = "produto;classificação;unidade/peso;menor;comum;maior;quilo;data\n"
arq.write(linha)

cont = 0
while True:
    for i in range(0,6):
        if i==0:
            mercado = "FRUTAS"
        elif i == 1:
            mercado = "LEGUMES"
        elif i == 2:
            mercado = "VERDURAS"
        elif i==3:
            mercado = "DIVERSOS"
        elif i==4:
            mercado = "FLORES"
        elif i==5:
            mercado = "PESCADOS"


        r = requests.post("http://www.ceagesp.gov.br/entrepostos/servicos/cotacoes/",
                          data ={

                            "cot_data":data_texto,
                            "cot_grupo":mercado,
                          })

        html_soup = BeautifulSoup(r.text, 'html.parser')
        tabela = html_soup.find("table", class_="contacao_lista")
        if tabela == None:
            cont += 1
            if cont == 6:
                cont = 0
                data_atual = datetime.date.fromordinal(data_atual.toordinal() - 1)
                data_texto = data_atual.strftime("%d/%m/%Y")
            continue


        trs = tabela.find_all("tr")

        for i in range(2,len(trs)):
            tds = trs[i].find_all("td")
            linha = tds[0].text
            for j in range(1,len(tds)):
                linha = linha+";"+tds[j].text
            linha = linha +";"+ data_texto +"\n"
            arq.write(linha)

        data_atual = datetime.date.fromordinal(data_atual.toordinal() - 1)
        data_texto = data_atual.strftime("%d/%m/%Y")