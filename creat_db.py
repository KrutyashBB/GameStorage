import sqlite3
from parser import lst_information, lst_name, lst_description

con = sqlite3.connect('library_db.db')
cur = con.cursor()

for i in range(107):
    cur.execute(
        'INSERT INTO Games(Title, Description, Platforms, Developer, Game_Mode, Release_date) VALUES(?, ?, ?, ?, ?, ?)',
        (lst_name[i], lst_description[i], lst_information[i][0], lst_information[i][1], lst_information[i][2],
         lst_information[i][3]))
    con.commit()

con.close()
