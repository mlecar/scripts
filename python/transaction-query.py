import csv
import requests
import string
import re

#Data from e-commerce v.2.5.4 manual
consulta_xml = '''<?xml version="1.0" encoding="ISO-8859-1"?><requisicao-consulta id="6fcf758e-bc60-4d6a-acf4-496593a40441" versao="1.2.1"><tid>{tid}</tid><dados-ec><numero>{ec}</numero><chave>{chave}</chave></dados-ec></requisicao-consulta>'''

file=open("result2.txt",'w')

def chave(argument):
    switcher = {
        '1006993069': '25fbb99741c739dd84d7b06ec78c9bac718838630f30b112d033ce2e621b34f3'
    }
    return switcher.get(argument, "nothing")

with open('transaction-test.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        try:
            request_xml = consulta_xml.replace('{tid}', row[1]).replace('{ec}', row[0]).replace('{chave}', chave(row[0]))
	    r = requests.post('https://qasecommerce.cielo.com.br/servicos/ecommwsec.do', data = {'mensagem':request_xml})
            if('<erro' not in r.text):
                valor = r.text.split('<valor>')[1].split('</valor>')
                response_xml = r.text.split('<tid>')
                truncated_response_xml = '<?xml version="1.0" encoding="ISO-8859-1"?><transacao><tid>' + response_xml[1]
                file.write(';'.join(row) + valor[0] + ";")
                file.write(truncated_response_xml.replace('\n','').encode('utf8') + "\n")
            else:
                response_xml = r.text.split('<codigo>')
                truncated_response_xml = '<?xml version="1.0" encoding="ISO-8859-1"?><erro><codigo>' + response_xml[1]
                file.write(';'.join(row) + "0000;")
                file.write(r.text.replace('\n','').encode('utf8') + "\n")
        except Exception as inst:
            file.write(';'.join(row) + "0000" + ";")
            file.write(str(inst).replace('\n', '') + "\n")
file.close()
