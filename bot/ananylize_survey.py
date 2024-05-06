import pandas as pd
import pandas as pd
from datetime import datetime
from datetime import timedelta

def generate_excel(data):
    # Преобразование списка в DataFrame
    timestamp = (datetime.now() + timedelta(hours=0)).strftime("%Y%m%d_%H%M%S")

    df = pd.DataFrame(data)

    comments_df = df[['FIO teacher', 'comment']].dropna()
    import os
    print(os.getcwd())
    comments_file_name = f'./bot/files/izoh_{timestamp}.xlsx'
    comments_df.to_excel(comments_file_name, index=False)

    # Удаление столбца 'comment'
    df.drop(columns=['comment'], inplace=True)

    grouped_df_1 = df.groupby('FIO teacher').mean()

    count = df.groupby('FIO teacher').size().reset_index(name='Кол-во опросов')

    grouped_df = pd.merge(count, grouped_df_1, on='FIO teacher')

    # Сохранение средних значений вопросов в Excel
    file_name = f"./bot/files/so'rov_natijasi_{timestamp}.xlsx"
    with pd.ExcelWriter(file_name) as writer:
        grouped_df.to_excel(writer, sheet_name='Teacher Scores')
