# Код для загрузки с обработкой кодировок
import pandas as pd
import numpy as np

def load_csv_robust(filename):
    encodings = ['utf-8', 'cp1251', 'latin-1']
    for encoding in encodings:
        try:
            df = pd.read_csv(filename, encoding=encoding)
            print(f"✓ Успешно загружено: {df.shape[0]} строк")
            return df
        except:
            continue

df_users = load_csv_robust('unidraw_users.csv')
df_visits = load_csv_robust('unidraw_visits.csv')
df_templates = load_csv_robust('unidraw_templates.csv')

# Данные в закрытом виде, а также некоторые значения смоделированы из-за коммерческой тайны, но близки к оригинальным данным

# График 1: Распределение по устройствам

import plotly.express as px

device_counts = df_visits['device_type_code'].value_counts().reset_index()
device_counts.columns = ['device_type', 'count']

fig = px.pie(device_counts, names='device_type', values='count',
             title='Распределение визитов по типам устройств',
             hole=0.4)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.write_image('images/eda_device_distribution.png', width=800, height=600)
fig.show()

# График 2: Тепловая карта активности (день × час)

df_visits['event_dttm'] = pd.to_datetime(df_visits['event_dttm'])
df_visits['day_of_week'] = df_visits['event_dttm'].dt.dayofweek
df_visits['hour'] = df_visits['event_dttm'].dt.hour

heatmap_data = df_visits.groupby(['day_of_week', 'hour']).size().reset_index(name='count')
pivot_data = heatmap_data.pivot(index='day_of_week', columns='hour', values='count')

fig = px.imshow(pivot_data, color_continuous_scale='YlOrRd',

title='Тепловая карта активности (день недели × час)')
fig.write_image('images/eda_activity_heatmap.png', width=1000, height=600)
fig.show()

# График 3: Распределение по возрастным сегментам

fig = px.pie(df_users, names='age_segment',
             title='Распределение пользователей по возрастным группам',
             hole=0.4)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.write_image('images/eda_age_distribution.png', width=800, height=600)
fig.show()

# График 4: Топ сфер деятельности

# Парсинг сфер деятельности
import ast
df_users['activity_parsed'] = df_users['array_field_of_activity_ru'].apply(
    lambda x: ast.literal_eval(x) if pd.notna(x) and x != 'nan' else []
)

activity_exploded = df_users.explode('activity_parsed')
activity_counts = activity_exploded['activity_parsed'].value_counts().head(10).reset_index()
activity_counts.columns = ['activity', 'count']

fig = px.bar(activity_counts, x='count', y='activity',
             title='Топ-10 сфер деятельности пользователей',
             orientation='h', color='count')
fig.write_image('images/eda_top_industries.png', width=800, height=600)
fig.show()


## Desktop-first продукт (84% PC). Пик активности 17:00-19:00. Основная аудитория 18-24 года. Преподавание — топовая сфера. 96% пользователей не создают шаблоны - 
