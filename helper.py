import pandas as pd
import os
from airflow.providers.postgres.hooks.postgres import PostgresHook
def _process_user(ti):
    user = ti.xcom_pull('extract_user')
    print(user)
    user = user['results'][0]
    processed_user = pd.json_normalize({
        'firstname':user['name']['first'],
        'lastname':user['name']['last'],
        'country':user['location']['country'],
        'username':user['login']['username'],
        'password':user['login']['password'],
        'email':user['email']
    })
    output_dir = '/tmp'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    processed_user.to_csv(f'{output_dir}/processed_user.csv', index=None, header=False)




def _store_user():
    hook = PostgresHook(postgres_conn_id='postgres') 
    hook.copy_expert(
        sql="COPY users FROM stdin WITH DELIMITER as ','",
        filename='/tmp/processed_user.csv'
    )



    