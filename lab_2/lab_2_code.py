import pandas as pd
import re
import matplotlib.pyplot as plt
import math

# загружаем данные
data = pd.read_csv('data.csv')

# присваеваем переменные
abon = '192.168.250.59'
k_under_500Mb = 0.5
k_upper_500_Mb = 1

# подгоняем формат времени к нужному
data['Date_first_seen'] = pd.to_datetime(data['Date_first_seen'], format='%Y-%m-%d %H:%M:%S.%f')
data['session_date'] = data['Date_first_seen'].dt.floor('T')
data['session_time'] = data['session_date'].dt.time

# функция, убирающая порт от адреса источника
def port_remover(adress):
    try:
        return re.search('\d+.\d+.\d+.\d+', adress).group()
    except:
        return '0.0.0.0'

# новый столбик с ip адресом источника
data['abon_ip'] = data['Src_IP_Addr:Port'].apply(port_remover)

# выводим график
data.groupby('session_time').agg({'Bytes':'sum'}).plot(figsize=(15,5), title='График зависимости объема трафика от времени')
plt.show()

# делаем срез данных по интересующему нас абоненту
abon_data = data.query('@abon in abon_ip')
abon_traffic = abon_data['Bytes'].sum()

# фукнция для расчета тарификации
def tarification(bytes):
    Mbytes = math.ceil(bytes / 10**6)
    if Mbytes < 500:
        return Mbytes * k_under_500Mb
    else:
        return (500 * k_under_500Mb) + ((Mbytes - 500) * k_upper_500_Mb)

# вывод нужной информации
print('Выбранный абонент:', abon)
print('Израсходовано трафика: {:.2f} байт ({} Мб)'.format(abon_traffic, math.ceil(abon_traffic / 10**6)))
print('Списание по тарифу составляет: {} руб.'.format(tarification(abon_traffic)))
