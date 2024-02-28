from pgvector.psycopg2 import register_vector
import psycopg2
from configparser import ConfigParser, Error
import psycopg2.extras as extras
import time


"""Function reads the properties file"""
def config(filename='data/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

"""Connect to db and return the connection object"""
def connect_to_db():
    
    params = config()
    return psycopg2.connect(**params)


"""Function to check DB Connection , used when intial script developing , obselete"""
def checkDBConnection():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        
        # connect to the database
        print('Connecting to the PostgreSQL database...')
        conn = connect_to_db()
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def data_ingestion(final_texts, embeddings):
    try:
        conn= connect_to_db()
        register_vector(conn)
        cursor = conn.cursor()
        
        count=0
        for content, embedding in zip(final_texts,embeddings):
            cursor.execute('INSERT INTO public.documents_fixed_len_chunks (content,embedding) VALUES (%s,%s)', (content,embedding))
            count = count+cursor.rowcount
            conn.commit()                
        
        print(count, "Record inserted successfully into document table")

    except (Exception, psycopg2.DatabaseError) as error:
        
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
            print('Database connection cursor closed.')  
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            

def batch_data_ingestion(final_texts, embeddings,tablename):
    start_time = time.perf_counter
    print(f"Started the batch_data_ingestion process ")
    try:
        
        data = [(final_texts[i], " ") for i in range(0, len(final_texts))]
        cols= ["content" , "embedding"]
        colList = ','.join(cols)
        print(colList)
        query="INSERT INTO %s(%s) VALUES %%s" % (tablename, colList)
       
          
        print(query)
    
        conn= connect_to_db()
        register_vector(conn)
        cursor = conn.cursor()
        extras.execute_values(cursor,query,data)
        conn.commit
        
    
    
    except (Exception, psycopg2.DatabaseError) as error:
        
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
            print('Database connection cursor closed.')  
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
    end_time = time.perf_counter
    print(f"Ended the batch_data_ingestion process ")