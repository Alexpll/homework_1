import sqlite3


con = sqlite3.connect("MyDataBase.db")
cur = con.cursor()
lst_1 = cur.execute("""INSERT INTO salon VALUES (14, "Александра", 15, "улица Мира 75")""").fetchall()
lst_2 = cur.execute("""INSERT INTO salon VALUES (15, "Полина", 10, "улица Попова 27")""").fetchall()
lst_3 = cur.execute("""INSERT INTO salon VALUES (16, "Ульяна", 12, "улица Кояновская 15")""").fetchall()
lst_4 = cur.execute("""INSERT INTO person VALUES (31, "Саша", 89824752510, "хочется красивый макияж")""").fetchall()
lst_5 = cur.execute("""INSERT INTO person VALUES (32, "Поля", 89524956540, "хочется красивый маникюр")""").fetchall()
lst_6 = cur.execute("""INSERT INTO person VALUES (33, "Уля", 88005553535, "хочется красивую укладку")""").fetchall()

first = cur.execute("""UPDATE person SET preferences = "хочется сходить к косметологу" WHERE id_person= 32""").fetchall()
second = cur.execute("""DELETE FROM person WHERE id_person = 31""").fetchall()
con.commit()
con.close()