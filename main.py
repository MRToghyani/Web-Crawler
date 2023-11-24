import requests
from bs4 import BeautifulSoup
from urllib import robotparser
import random
import time
import multiprocessing
import traceback
from random import shuffle
import pandas as pd
from multiprocessing import Pool
import mysql.connector
from mysql.connector import pooling
from multiprocessing import Pool, freeze_support
import textwrap

# Connection details
db_config = {
    'host': 'host',
    'user': 'user',
    'password': 'password',
    'database': 'database',
}

def perform_database_operation(data):
    try:
        # Create a new connection pool for each worker process
        connection_pool = pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=15, **db_config)

        # Acquire a connection from the pool
        connection = connection_pool.get_connection()

        # Create a cursor
        cursor = connection.cursor()

        # Example data and query
        insert_query = "INSERT INTO link (source, target) VALUES (%s, %s)"
        cursor.execute(insert_query, data)

        # Commit the changes
        connection.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Release the connection back to the pool
        if connection.is_connected():
            cursor.close()
            connection.close()

def clear_table(table_name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    delete_query = f'DELETE FROM {table_name}'
    reset_auto_increment_query =  f'ALTER TABLE {table_name} AUTO_INCREMENT = 1'
    try:
        cursor.execute(delete_query)
        cursor.execute(reset_auto_increment_query)
        conn.commit()
        print('Table cleared successfully.')

    except mysql.connector.Error as err:
        print(f'Error: {err}')

    finally:
    # Close the cursor and connection
        cursor.close()
        conn.close()


def request_main3(url):
    l=[]
    try:
        if url not in cashe:            
            # url = queaue.get()
            UAS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
                   ]
            ua = UAS[random.randrange(len(UAS))]
            headers = {'user-agent': ua}
        
            response = requests.get(url, headers=headers)
            response = requests.get(url)
            # sleep_time = random.random()          
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')    
                links = soup.find_all('a')
                for link in links:
                    web = link.get('href')
                    if web is not None:
                        if (web.startswith('https'))  and (web not in recent):
                            # print(web) 
                            l.append(web)
                            perform_database_operation((textwrap.shorten(url, width= 255) ,textwrap.shorten(web, width= 255)))
                    # except:
                    #     print(link)
                        
            else:
                print(response.status_code , ' ' , url) #,' moving to tor'

            # print(l)
            return l
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n %s" %url )
        print(str(e))   
        return []
    except requests.Timeout as e:
        print("OOPS!! Timeout Error\n %s" %url)
        print(str(e))
        return []        
    except requests.RequestException as e:
        print("OOPS!! General Error\n %s" %url)
        print(str(e))
        return []
    except KeyboardInterrupt:
        print("Someone closed the program\n %s" %url)
        return []
    

df = pd.read_csv("links.csv")
l0 = list(df.links)
# l0 = ["https://www.tabnak.ir/","https://www.alef.ir/","https://www.hamshahrionline.ir/","https://en.wikipedia.org/wiki/Main_Page"]
l1 = []
cashe = []
recent = []
if __name__ == '__main__':
    freeze_support()
    clear_table("link")
    for i in range(10):
        
        l1= []
        with Pool(processes=10) as pool:
            l1 = pool.map(request_main3,l0)
        pool.join()
        cashe = cashe + l0
        recent = l0
        l1 = sum(l1,[])
        l0 = l1 
        
        shuffle(l0)
        print("depth :", i)
        print(l0)
