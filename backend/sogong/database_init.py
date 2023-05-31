import pandas as pd
import sqlite3

df = pd.read_csv('dataset/coding_problems.csv', encoding='EUC-KR')
df2 = pd.read_csv('dataset/testcases.csv', encoding='EUC-KR')
df3 = pd.read_csv('dataset/ethicsproblems.csv' , encoding= 'EUC-KR')
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
    "case_input2 ": "CharField",
    "case_input3 ": "CharField",
    "case_input4 ": "CharField",
    "case_output1 ": "CharField",
    "case_output2 ": "CharField",
    "case_output3 ": "CharField",
    "case_output4 ": "CharField"
}
dtype3={
    "title": "CharField PRIMARY KEY" ,
    "content" : "CharField",
    "optionA" : "CharField", 
    "optionB" : "CharField", 
    "submissionA" : "CharField",
    "submissionB" : "CharField"
    }
conn.execute("DROP TABLE IF EXISTS sogongapp_CodingProblem")
conn.execute("DROP TABLE IF EXISTS sogongapp_CodingTestcase")
conn.execute("DROP TABLE IF EXISTS sogongapp_ethicsproblem")
# database에 기존에 준비한 dataset 넣기
df.to_sql(name='sogongapp_CodingProblem', con = conn, if_exists='replace', dtype=dtype, index = True, index_label='id')
df2.to_sql(name="sogongapp_CodingTestcase", con = conn, if_exists='replace', dtype=dtype2, index=False)
df3.to_sql(name='sogongapp_ethicsproblem', con = conn, if_exists='replace', dtype=dtype3, index = True, index_label='id')
conn.commit()
conn.close()
print("Success")