import psycopg2
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
ENDPOINT = os.environ.get("DB_ENDPOINT")
PORT = os.environ.get("DB_PORT")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
DBNAME = os.environ.get("DB_DBNAME")



def update_db(email, phone_number):

    try:
        # Connect to the DB instance
        conn = psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, port=PORT, dbname=DBNAME, sslmode='require')
        cur = conn.cursor()

        #Create Table if it doesn't exist
        make_table_query = '''CREATE TABLE IF NOT EXISTS Contact (
        id SERIAL PRIMARY KEY,
        phoneNumber VARCHAR(20),
        email VARCHAR(50), -- Updated length
        linkedId INT,
        linkPrecedence VARCHAR(20),
        createdAt TIMESTAMP,
        updatedAt TIMESTAMP,
        deletedAt TIMESTAMP
        );'''
        cur.execute(make_table_query)

        #Check if a linked record already exists
        check_query = f"SELECT * from Contact where email = '{email}' OR phoneNumber = '{phone_number}'"
        cur.execute(check_query)
        result = cur.fetchall()

        primary_contact_id = None
        emails = set()
        phone_numbers = set()
        secondary_contact_ids = None

        #If not then create record as primary in db else make earliest record primary and all others secondary
        if len(result) == 0:
            link_precedence = "primary"
            created_at = datetime.datetime.now()
            insert_query = f"INSERT into Contact(phoneNumber,email,linkPrecedence,createdAt) VALUES('{phone_number}','{email}','{link_precedence}','{created_at}')"
            cur.execute(insert_query)

            #Getting primary contact id from last record since its auto increment
            last_record_query = "SELECT MAX(id) FROM Contact"
            cur.execute(last_record_query)
            last_record = cur.fetchall()

            primary_contact_id = last_record[0][0]
            emails.add(email)
            phone_numbers.add(phone_number)

        else:
            result.sort(key=lambda x:x[5])
            primary_contact_id = result[0][0]
            emails.add(result[0][2])
            phone_numbers.add(result[0][1])
            secondary_contact_ids = set()

            #Update every other entry besides the oldest to secondary linked precedence. No need to update oldest since its already primary.
            for entry in result[1:]:
                link_precedence = "secondary"
                linked_id = result[0][0]
                updated_at = datetime.datetime.now()
                update_query = f"UPDATE Contact SET linkPrecedence = '{link_precedence}', linkedId = '{linked_id}', updatedAt = '{updated_at}' WHERE id = '{entry[0]}'"
                cur.execute(update_query)                     
                emails.add(entry[2])
                phone_numbers.add(entry[1])
                secondary_contact_ids.add(entry[0])


            #Insert Current record as secondary to db
            linked_id = result[0][0]
            link_precedence = "secondary"
            created_at = datetime.datetime.now()
            insert_query = f"INSERT into Contact(phoneNumber,email,linkedId,linkPrecedence,createdAt) VALUES('{phone_number}','{email}','{linked_id}','{link_precedence}','{created_at}')"
            cur.execute(insert_query)

            #Getting secondary contact id from last record since its auto increment
            last_record_query = "SELECT MAX(id) FROM Contact"
            cur.execute(last_record_query)
            last_record = cur.fetchall()

            emails.add(email)
            phone_numbers.add(phone_number)
            secondary_contact_ids.add(last_record[0][0])

        conn.commit()
        conn.close()

        emails= list(emails)
        phone_numbers = list(phone_numbers)
        secondary_contact_ids = list(secondary_contact_ids) if secondary_contact_ids else None
        data_map = {"contact" : {"primaryContactId" : primary_contact_id, "emails" : emails, "phoneNumbers" : phone_numbers, "secondaryContactIds" : secondary_contact_ids}}
        print(data_map)

        return data_map
    except Exception as e:
        print("Database connection failed due to:", e)

def show_db():

    try:
        # Connect to the DB instance
        conn = psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, port=PORT, dbname=DBNAME, sslmode='require')
        cur = conn.cursor()

        #Create Table if it doesn't exist
        make_table_query = "Select * from Contact"
        cur.execute(make_table_query)
        print(cur.fetchall())
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database connection failed due to:", e)


