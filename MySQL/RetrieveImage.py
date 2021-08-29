import mysql.connector
import sys
from PIL import Image
import base64
import PIL.Image
from io import StringIO

db = mysql.connector.connect(host="fyidev.cj4ghwejxvaa.us-east-2.rds.amazonaws.com",
                             user="admin",
                             password="findyourinvasive",
                             database="MosquitoImages")

cursor=db.cursor()

sql_fetch_blob_query = """SELECT * FROM MosquitoImages.test2"""

cursor.execute(sql_fetch_blob_query)
record = cursor.fetchall()
for row in record:
    print("name = ", row[0], )
    image = row[1]
    #img=PIL.Image.open(image)
    #img.show()
    with open("picture.jpg", 'wb') as file:
        file.write(image)

db.close()
