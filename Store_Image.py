import mysql.connector

import mysql.connector


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(name, photo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='554',
                                             user='root',
                                             password='888888')
        ##conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='123456',db='imooc',charset='utf8')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO Customer_image
                          (id, name, photo) VALUES (%s,%s,%s)"""

        empPicture = convertToBinaryData(photo)
        from datetime import datetime
        now = datetime.now()

        # Convert data into tuple format
        insert_blob_tuple = (str(now), name, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into Customer_iamge table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



