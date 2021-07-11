import pymysql
import pandas as pd


conn = pymysql.connect(
    host="127.0.0.1",
    port=3020,
    user="user",
    password="choewy",
    db="schedule_management",
    charset="utf8"
)

curs = conn.cursor()

curs.execute("select * from survey_manual;")
pd.DataFrame(curs.fetchall()).to_excel("survey_manual.xlsx")

curs.execute("select * from survey;")
pd.DataFrame(curs.fetchall()).to_excel("survey.xlsx")

curs.execute("select * from survey_answer;")
pd.DataFrame(curs.fetchall()).to_excel("survey_answer.xlsx")