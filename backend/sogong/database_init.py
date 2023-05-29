import pandas as pd
import sqlite3

df = pd.read_csv('coding_problems.csv', encoding='EUC-KR')
df2 = pd.read_csv('testcases.csv', encoding='EUC-KR')
database = "db.sqlite3"
conn = sqlite3.connect(database)
dtype={
    "title": "CharField PRIMARY KEY" ,
    "level": "IntegerField", 
    "content_problem": "CharField", 
    "content_input":"CharField",
    "content_output" :"CharField",
    "answer": "CharField"
    }

dtype2={
    "problem ": "CharField PRIMARY KEY",
    "case_input1 ": "CharField",
   " case_input2 ": "CharField",
   " case_input3 ": "CharField",
   " case_input4 ": "CharField",
    "case_output1 ": "CharField",
    "case_output2 ": "CharField",
    "case_output3 ": "CharField",
    "case_output4 ": "CharField"
}
conn.execute("DROP TABLE IF EXISTS sogongapp_CodingProblem")
conn.execute("DROP TABLE IF EXISTS sogongapp_CodingTestcase")
df.to_sql(name='sogongapp_CodingProblem', con = conn, if_exists='replace', dtype=dtype, index = True, index_label = "id")
df2.to_sql(name="sogongapp_CodingTestcase", con = conn, if_exists='replace', dtype=dtype2, index=False)
conn.commit()
conn.close()