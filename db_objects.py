import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db3')

# Create a cursor object
cursor = conn.cursor()

# Execute SQL query to select data from the teachers table
cursor.execute("""SELECT q.question, a.answer
FROM answers a
JOIN questions q ON a.qid = q.qid;
""")

# Fetch all rows from the result set
rows = cursor.fetchall()

result_dict = {}

for key, value in rows:
    if key not in result_dict:
        result_dict[key] = [value]
    else:
        result_dict[key].append(value)

# print(result_dict)

cursor.close()
conn.close()

"""
{
    "O‘qituvchining dars o‘tish qobiliyati mahorati": ["Qoniqarli", "Qoniqarsiz"],
    "Talabalar bilan muloqot qilish madaniyati": ["Qoniqarli", "Qoniqarsiz"],
    "O‘qituvchining darsga tayyorgarlik ko‘rib kirishi": ["Qoniqarli", "Qoniqarsiz"],
    "O‘qituvchining dars jarayoniga jiddiy qarashi, darslarning o‘z vaqtida tashkillashtirilishi": ["Qoniqarli", "Qoniqarsiz"],
    "O‘qituvchining talabani adolatli baxolashi": ["Qoniqarli", "Qoniqarsiz"],
    "Mashg‘ulotning mavzu doirasida olib borilishi": ["Darsni mavzu doirasida olib boradi", "Ko‘p hollarda darsni mavzu doirasida olib bormaydi"],
    "Mavzuni auditoriyaga eshitilarli, qiziqarli, mazmunli darajada yetkazib berishi": ["Qoniqarli", "Qoniqarsiz"],
    "Mavzuni hozirgi dolzarb masalalarga bog‘lab tushuntirishi": ["Qoniqarli", "Qoniqarsiz"],
    "O‘qituvchining ta’magirlikka moyilligi": ["Ta’magirlikka moyil emas", "Ta’magirlikka moyi"]
}
"""