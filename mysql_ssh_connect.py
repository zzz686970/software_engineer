import MySQLdb
import mysql.connector
import pymysql
import sshtunnel
import pandas as pd

config = configparser.ConfigParser()
config.read('file.ini')

# with sshtunnel.SSHTunnelForwarder(
#             ssh_address_or_host='host',
#             ssh_username='user_name',
#             ssh_pkey='/Users/user_name/.ssh/id_rsa',
#             remote_bind_address=('localhost', 3306)) as tunnel:
#     conn = MySQLdb.connect(host = '127.0.0.1',
#                      user = 'user',
#                      passwd = 'passwd',
#                      db = 'db',
#                      port=tunnel.local_bind_port
#                      )

#     # cur = db.cursor()
#     # cur.execute('select * from test_zz ')

#     # for row in cur.fetchall():
#     #   print(row[0])

#     data = pd.read_sql_query(sql_query, conn)
#     conn.close()


###### ssh user and password
# with sshtunnel.SSHTunnelForwarder(
#             (ssh_host, ssh_port)
#             ssh_username='user_name',
#             ssh_pkey='/Users/user_name/.ssh/id_rsa',
#             remote_bind_address=('localhost', 3306)) as tunnel:
#     conn = MySQLdb.connect(host = '127.0.0.1',
#                      user = 'sql_user',
#                      passwd = 'sql_passwd',
#                      db = 'db',
#                      port=tunnel.local_bind_port
#                      )
#     ## cursor object for query execution
#     # cur = db.cursor()
#     # cur.execute('select * from test_zz ')
#     ## number of rows
#     ## print(cur.rowcount)

#     # for row in cur.fetchall():
#     #   print(row[0])

#     data = pd.read_sql_query(sql_query, conn)
#     conn.close()


## direct connect
conn = MySQLdb.connect(host = 'hostname',
                 user = 'user',
                 passwd = 'passwd',
                 db = 'db_name',
                 port=3306,
                 charset='utf8',
                 use_unicode='FALSE',
                 )

# cur = db.cursor()
# cur.execute('select * from test_zz ')

# for row in cur.fetchall():
#   print(row[0])

data = pd.read_sql_query(sql_query, conn)



## use pymysql
### all references to mysqldb will use pymysql transparently
pymysql.install_as_MySqldb()
connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()



## sqlalchemy
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, scoped_session 

Base = declarative_base()
engine = create_engine("mysql://user_name:passwd@hostname/db_name")
session_obj = sessionmaker(bind=engine)
session = scoped_session(session_obj)

## raw query
session.execute(sql_query)
session.flush()
session.commit()

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

# insert into database
person_obj = Person(id=12, name="name")
session.add(person_obj)
session.flush()
session.commit()


