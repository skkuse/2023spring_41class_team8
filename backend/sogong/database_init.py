import pandas as pd
import sqlite3

df = pd.read_csv('coding_problems.csv', encoding='EUC-KR')
database = "db.sqlite3"
conn = sqlite3.connect(database)
dtype={
    "title": "CharField" ,
    "level": "IntegerField", 
    "content_problem": "CharField", 
    "content_input":"CharField",
    "content_output" :"CharField",
    "answer": "CharField"
    }
df.to_sql(name='sogongapp_CodingProblem', con = conn, if_exists='replace', dtype=dtype, index = True, index_label = "id")
conn.commit()
conn.close()