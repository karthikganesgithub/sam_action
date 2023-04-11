import pymysql
import json
import time
import os
import boto3

client = boto3.client('secretsmanager')

environment = os.environ['ENVIRONMENT']

# Construct the table name based on the environment variable
# table_name = f'{environment}_cpu_util'

#Estabilish connection
#connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)

def lambda_handler(event, context):
    
    # cpu_usage = event['CPU Usage']
    # timestamp = event['Timestamp']
    # print("CPU Usage:", cpu_usage)
    # print("Timestamp:", timestamp)
    # sql = INSERT INTO CPU_Util (CPU_Utilization, Time_stamp) VALUES (%s, %s)
    # values = (cpu_usage, timestamp)
    # cursor.execute(sql, values)
    response = client.get_secret_value(SecretId = f'{environment}/rds/key')
    secret_string = response['SecretString']
    # print(secret_string)
    secrets = json.loads(secret_string)
    endpoint = secrets['host']
    username = secrets['username']
    password = secrets['password']
    database = secrets['dbname']
    print(database)
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO cpu_util (CPU_Utilization, Time_stamp) VALUES (%s, '%s')""" % (event['CPU Usage'], event['Timestamp']))
    connection.commit()
    connection.close()
    print("Successfully Completed")
    #print("Artifact Test")
    print("new deploy")
    return {
        'statusCode': 200
    }  
