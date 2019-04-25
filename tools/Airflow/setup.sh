pip install "apache-airflow"

export AIRFLOW_HOME = "$(pwd)"

airflow initdb
# if airflow doesn't start, do # export SLUGIFY_USES_TEXT_UNIDECODE=yes

# turn on the airflow webserver

airflow webserver -p 8080

# start webserver on the web browser

localhost:8080

# start an airflow web server
airflow web server

# start an airflow scheduler
airflow scheduler
