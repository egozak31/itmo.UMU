# имопрт библиотек
import pandas as pd
import math

# загружаем данные
data = pd.read_csv('data.csv')
display(data)

abon = 915642913

# тарифы
k = 1
sms_5 = 0
sms5_10 = 1
sms10_ = 2

incoming_stat = data.query('msisdn_dest == @abon')
outcoming_stat = data.query('msisdn_origin == @abon')

print("Входящие звонки выбранного абонента:")
display(incoming_stat)
print()
print("Исходящие звонки и смс выбранного абонента:")
display(outcoming_stat)

# считаем тариф по исходящим звонкам
outcoming_calls_bill = math.ceil(outcoming_stat['call_duration']) * k
# считаем тариф по входящим звонкам
incoming_calls_bill = math.ceil(incoming_stat['call_duration']) * k
# считаем общий тариф по звонкам
total_calls_bill = outcoming_calls_bill + incoming_calls_bill

def sms_biller(sms_number):
  try:
    if sms_number < 6:
      return sms_number * sms_5
    elif sms_number < 11:
      return (sms_number - 5) * sms5_10
    elif sms_number >= 11:
      return 5 + (sms_number - 10) * sms10_
  except:
    print('incorrect input')


total_sms_bill = sms_biller(int(outcoming_stat['sms_number']))

total_bill = total_calls_bill + total_sms_bill

print("За выбранный период у абонента с номером {} списано {} руб. 00 коп.".format(abon, total_bill))

