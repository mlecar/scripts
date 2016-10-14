import csv
import string
import pypyodbc
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.properties')

insert = config.get('Database', 'insert.acquirer.response')

file=open("acquirer-response-mapper-insert-by-config.txt",'w')
cnxn = pypyodbc.connect(config.get('Database', 'database.connection.url'))

def findResponseMappedId(hintCode, detailingCode, code, acquirerCode):
    cursor = cnxn.cursor()
    findResponseMappedIdSQL = config.get('Database', 'find.response.mapped.id').replace('{code}', str(code)).replace('{hintCode}', str(hintCode)).replace('{detailingCode}',str(detailingCode))
    cursor.execute(findResponseMappedIdSQL)
    select = cursor.fetchone()
    if not select:
       raise Exception('Registro nao existe: acquirerCode ' + acquirerCode + ' code ' + str(code) + ', detalingCode ' + str(detailingCode) + ', hint ' + str(hintCode))
    responseMappedId = str(select[0])
    cursor.close()
    return responseMappedId;

def findBankId(bankName):
    cursor = cnxn.cursor()
    findBankIdSQL = config.get('Database', 'find.bank.id').replace('{bankName}', 'BRADESCO')
    cursor.execute(findBankIdSQL)
    select = cursor.fetchone()
    if not select:
       raise Exception('Banco ' + bankName + ' nao existe')
    bankId = str(select[0])
    cursor.close()
    return bankId;

with open('cielonovov3-csv.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=';')

    for row in reader:
        try:
            values='\'' + row[0] + '\',\'' + row[1] + '\',\'' + row[2] + '\',\'' + row[3] + '\',' + row[4]
            values += ',' + findResponseMappedId(row[5], row[7], row[6], row[0])
            values += ',1,null)'
            file.write(insert + values + "\n\n")

            if(row[6] == '30'):
                values='\'' + row[0] + '\',\'' + row[1] + '\',\'' + row[2] + '\',\'' + row[3] + '\',' + row[4]
                values += ',' + findResponseMappedId(40, row[7], row[6], row[0])
                values += ',1,' + findBankId('BRADESCO') + ')'
                file.write(insert + values + "\n\n")

        except Exception as inst:
            file.write(''.join(inst) + '\n\n')
cnxn.close()
file.close()

