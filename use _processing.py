from airflow import DAG
import json
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from helper import _process_user, _store_user

with DAG(
    'user_processing',
    start_date = datetime(2024,1,1),
    schedule_interval='@daily',
    catchup=False,
    start_date = datetime(2024,1,10)
) as dag:
    
    create_table = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id = 'postgres',
        sql = """
            CREATE TABLE IF NOT EXISTS users(
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            country TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
            );
        """
    )
    
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',  # Connection ID should be set up in Airflow Connections
        endpoint='api/',  # This is fine as the base URL is in the connection
        response_check=lambda response: response.status_code == 200,  # Check for a successful response
        poke_interval=5,  # Check every 5 seconds
        timeout=300,      # Timeout after 300 seconds
    )
# host: https://randomuser.me/
    extract_user = SimpleHttpOperator(
        task_id = 'extract_user',
        http_conn_id = 'user_api',
        endpoint = 'api/',
        method = 'GET',
        response_filter = lambda response:json.loads(response.text),
        log_response = True
    )

    process_user = PythonOperator(
        task_id = 'process_user',
        python_callable= _process_user
    )

    store_user = PythonOperator(
        task_id='store_user',
        python_callable=_store_user
    )


    create_table >> is_api_available >> extract_user >> process_user >> store_user