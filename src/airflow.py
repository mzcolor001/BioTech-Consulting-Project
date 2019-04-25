import time

from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.python_operator import BashOperator



default_args = {
	'owner': 'users',
	'depends_on_past': False,
	'start_date': datetime(2019, 3, 1, 0, 0),
	'schedule_interval': '@daily',

	'email': ['please type your email here'], # please add your email here, you will receive an email if
											  # the system fails
	'email_on_failure': False,
	'email_on_retry': False,

	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}


with DAG('Persephone_tool', default_args = default_args) as dag:
	excel2json = BashOperator(
	task_id = 'testairflow',
	bash_command = './create_file.sh',
	dag=dag)
