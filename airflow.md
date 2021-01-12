## why need airflow
- etl jobs fail for different reasons
- job dependencies
- data is getting larger, modern distributed data stacks (HDFS, Hive, Presto) don't work well with cron.


## mysql
```
apt-get install mysql-server
chown -R mysql:mysql /var/lib/mysql

## start mysql service
service mysqld start
mysql -uroot
use mysql;
update user set password=123 where user = 'root';
flush privileges;

create database airflow;
create user 'airflow'@'%' identified by 'airflow';
create user 'airflow'@'localhost' identified by 'airflow';

grant all on airflow.* to 'airflow'@'%';
grant all on airflow.* to 'root'@'%';
flush privileges;
exit;

## airflow
vim /etc/profile

export PYTHON_HOME=...
export PATH=$PATH:$PYTHON_HOME/bin
export airflow_HOME=/root/airflow
export SITE_AIRFLOW_HOME=/python3.../lib/python3.7/site-packages/airflow
export PATH=$PATH:$SITE_AIRFLOW_HOME/bin

source /etc/profile
pip install apace-airflow==1.10.0

pip install 'apache-airflow[mysql]'
pip install mysqlclient
pip install MySqldb
pip install cryptography

## 修改 fernet_key
python -c "from cryptography.fernet import Fernet; 
print(Fernet.generate_key().decode())"

replace fernet_key in airflow.cfg with the new one

sql_alcheny_conn=mysql_mysqldb://airflow:airflow@localhost:3306/airflow

## find mysql.cnf
mysql --help | grep my.cnf

[mysqld]
explicit_defaults_for_timestamp=true


## 用户认证
pip install apache-airflow[password]

## airflow.cfg
[webserver]
authenticate=true
auth_backend=airflow.contrib.auth.backends.password_auth

## user_account.py
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

user = PasswordUser(models.User())
user.username = 'airflow'
user.email = 'test_airflow@wps.cn'
user.password = 'airflow'

session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
#执行add_account.py文件：
python add_account.py

## 启动
#关闭linux防火墙
systemctl stop firewalld.service
systemctl disable firewalld.service

airflow webserver -D
airflow scheduler -D
airflow worker -D
airflow flower -D


```
This repo contains the PropEst evaluation module in `app/`  

~~the AWS Lambda API deployment bundles in `propest_api_lambda_bundle` and `propest_elastic_cache_lambda_bundle`.~~

~~The notebooks to run the evaluation and deploy the AWS Lambda bundles are in `notebooks`~~
~~haha~~

## Executor

### Kubernetes Executor
Relies on a fixed single Pod that dynamically deletegates work and resources.  
For each and every task that needs to run, the Executor talks to the Kubernetes API to dynamically launch an additional Pod, each with its own Scheduler and Webserver, which it terminates when the task is completed.

On the local and celery executors, the scheduler is charged with constantly having to check the status of each task at all time from database backend, with KubeExecutor, the workers pods talk directly to the same database backend as the scheduler, a task failure is handled by its individual Pod. 

### Sequential Executor
Run a single task instance at a time in a linear fashion with no parallelism functionality (A --> B --> C).  
It does identify a single point of failure.  

### airflow tables
```
task_instance (dag_id, state, start_date)

dag (is_paused, dag_id)

xcom (dag_id)

sla_miss (dag_id)

log (dag_id)

job (dag_id)

dag_run (dag_id)

log (dag_id)

task_reschedule (dag_id)

task_fail (dag_id)
```

### logs
- webserver logs 
> AIRFLOW_HOME/logs/scheduler/data/path/file.log 

- scheduler logs 

- task logs (can be seen via VIEW LOG button)
> AIRFLOW_HOME/logs/dag_id/task_id/date_time/1.log

- worker logs


### airflow with docker

```
## file structure
app 
	-- Dockerfile
	-- requirements.txt
docker-compose.yml

## Dockerfile
    driver: "bridge"


## check network, get gateway as host ip
docdkr inspect bridge


## airflow connection in web ui
conn id: mysql_test_conn
conn type: MySQL
host: gateway_ip
schema: testdb
login: root
password: 123
port: 3306

## dag file

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
    dag=dag)
  
t1 >> py1 >> py
```

## killing webserver
```sh
## kill the pid in webserver.pid file
lsof -i tcp:<port number>
docker run -d -p 8080:8080 -e AIRFLOW__CORE__SQL_ALCHEMY_CONN=sqlite:////usr/local/airflow/db/airflow.db -v /home/user/airflow/dags:/usr/local/airflow/dags -v /home/user/airflow/db:/usr/local/airflow/db puckel/docker-airflow webserver
```


## airflow official container

#### sripts/airflow-entrypoint.sh

```
#!/usr/bin/env bash

airflow upgradedb
airflow webserver

```


#### .env

```
AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgres+psycopg2://airflow:airflow@postgres:5432/airflow
AIRFLOW__CORE__FERNET_KEY=81HqDtbqAywKSOumSha3BhWNOdQ26slT6K0YaZeZyPs=
AIRFLOW_CONN_METADATA_DB=postgres+psycopg2://airflow:airflow@postgres:5432/airflow
AIRFLOW_VAR__METADATA_DB_SCHEMA=airflow
AIRFLOW__SCHEDULER__SCHEDULER_HEARTBEAT_SEC=10

```


#### hello-airflow.py
```
import codecs
import logging
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils import dates
logging.basicConfig(format="%(name)s-%(levelname)s-%(asctime)s-%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_dag(dag_id):
    default_args = {
        "owner": "jyoti",
        "description": (
            "DAG to explain airflow concepts"
        ),
        "depends_on_past": False,
        "start_date": dates.days_ago(1),
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
        "provide_context": True,
    }

    new_dag = DAG(
        dag_id,
        default_args=default_args,
        schedule_interval=timedelta(minutes=5),
    )

    def task_1(**kwargs):
        logger.info('=====Executing Task 1=============')
        return kwargs['message']

    def task_2(**kwargs):
        logger.info('=====Executing Task 2=============')
        task_instance = kwargs['ti']
        result = task_instance.xcom_pull(key=None, task_ids='Task_1')
        logger.info('Extracted the value from task 1')
        logger.info(result)

    with new_dag:
        task1 = PythonOperator(task_id='Task_1',
                                                    python_callable=task_1,
                                                    op_kwargs=
                                                    {
                                                        'message': 'hellow airflow'
                                                    },
                                                    provide_context=True)

        task2 = PythonOperator(task_id='Task_2',
                                            python_callable=task_2,
                                            op_kwargs=None,
                                            provide_context=True)
        task2.set_upstream(task1)
        return new_dag

dag_id = "hello_airflow1"
globals()[dag_id] = create_dag(dag_id)

```


## restart airflow webserver

check port first
```
sudo lsof -i tcp:8080
kill -9 pid
rm -rf $AIRFLOW_HOME/airflow-webserver.pid
```

```bash

- to start systemctl start airflow
- to stop systemctl stop airflow
- to restart systemctl restart airflow

## put it in /lib/systemd/system/airflow.service

[Unit]
Description=Airflow webserver daemon
After=network.target postgresql.service mysql.service redis.service rabbitmq-server.service
Wants=postgresql.service mysql.service redis.service rabbitmq-server.service
[Service]
PIDFile=/run/airflow/webserver.pid
EnvironmentFile=/home/airflow/airflow.env
User=airflow
Group=airflow
Type=simple
ExecStart=/bin/bash -c 'export AIRFLOW_HOME=/home/airflow ; airflow webserver --pid /run/airflow/webserver.pid'
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
Restart=on-failure
RestartSec=42s
PrivateTmp=true
[Install]
WantedBy=multi-user.target
```

restart airflow server by check folder `$AIRFLOW_HOME/airflow-webserver.pid`
```bash
## cat /var/run/airflow-webserver.pid | xargs kill -HUP
cat $AIRFLOW_HOME/airflow-webserver.pid | xargs kill -9
cat /var/run/airflow-webserver.pid | xargs kill -HUP
airflow webserver -p 8080 -D

```

## restart airflow scheduler
```bash
kill $(ps -ef | grep "airflow scheduler" | awk '{print $2}')

cat airflow-scheduler.pid | xargs kill
```




