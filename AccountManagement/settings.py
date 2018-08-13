import os

debug = False
port = 80
db_host = os.environ['DB_HOSTNAME']
db_port = os.environ['DB_PORT']
db_user = os.environ['DB_USERNAME']
db_pass = os.environ['DB_PASSWORD']
db_name = os.environ['DB_DATABASE']
database = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4'
# database = 'sqlite:///users.sqlite'

mail_host = os.environ['SMTP_HOST']
smtp_port = os.environ['SMTP_PORT']
email = os.environ['SMTP_EMAIL']
email_password = os.environ['SMTP_PASSWORD']
