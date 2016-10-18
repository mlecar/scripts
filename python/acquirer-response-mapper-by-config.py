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
    findResponseMappedIdSQL = config.get('Database', 'find.response.mapped.id').replace('{code}', str(code)).replace('{hintCode}', str(hintCode)).replace('{detailingCode}',detailingCode)
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

with open('cielonovov3-final.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=';')

    for row in reader:
        try:
            responseMapped_id = findResponseMappedId(row[5], row[7], row[6], row[0])
            hint30e10 = insert.replace('{detailingCode}', row[0]).replace('{code}', row[1]).replace('{description}',row[2]).replace('{detail}', row[3]).replace('{channelError}', row[4]).replace('{responseMapped_id}', responseMapped_id).replace('{acquirerChannel_id}', '1').replace('{bank_id}', 'null')
            file.write(hint30e10 + "\n\n")

            if(row[5] == '30'):
                responseMappedHint40_id = findResponseMappedId(40, row[7], row[6], row[0])
                bankId = findBankId('BRADESCO')
                hint40 = insert.replace('{detailingCode}', row[0]).replace('{code}', row[1]).replace('{description}',row[2]).replace('{detail}', row[3]).replace('{channelError}', row[4]).replace('{responseMapped_id}', responseMappedHint40_id).replace('{acquirerChannel_id}', '1').replace('{bank_id}', bankId)
                file.write(hint40 + "\n\n")

        except Exception as inst:
            file.write(''.join(inst) + '\n\n')
cnxn.close()
file.close()

