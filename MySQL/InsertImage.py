def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(name, photo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host="fyidev.cj4ghwejxvaa.us-east-2.rds.amazonaws.com",
                                             user="admin",
                                             password="findyourinvasive",
                                             database="MosquitoImages")

        cursor = connection.cursor()
        sql = "CREATE TABLE IF NOT EXISTS test3 (name VARCHAR(255), photo LONGBLOB NOT NULL)"

        cursor.execute(sql)
        sql_insert_blob_query = """ INSERT INTO test3 (name, photo) VALUES (%s,%s) """

        pic = convertToBinaryData(photo)


        # Convert data into tuple format
        insert_blob_tuple = (name, pic)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB ", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
  
print ("Taking Screenshot...")
name=time.strftime("%c").replace (":", "_").replace (" ","_")
file=name+".jpg"
cv.imwrite(file, img)
counter=0
insertBLOB(name, file)
print ("Number of larvae: "+str (len (persons)))
