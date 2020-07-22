## 1.Introduction

Why use a cloud solution:
- traditional: maintainence cost is high, low capital investment.
- immediate deployment of the infrastructure 
- cost saving for hiring people.

![cloud_service_models](gcp_image/cloud_service_models.png?raw=true "Title")

> easier to setup, shorted setup time, no capitial cost, pay as go  
> Notice some sensitive or critical data can not be stored in the cloud.  

Why GCP?
- Performance 

> network bandwidth, the individual virtual machines and the cloud are generally much faster than other cloud solutions, killer product: bigquery
- Pricing

> flexible sub-hour billing (charged by minute)  
> sustained use discounts  
> custom machine types(compute engine)  

- Power solutions 
- Other benefits of choice

> opensource (tensorflow)    
> robust infrastructure  
> environmental responsibility  

Paas
> Paltform as a service, delpoy sorce code on the platform service for your application to work.   
> Managed services/No-ops and auto-scaling/serverless.  
> Eg. Only need to focus on source code.  
- very difficult to implement custom features.
Iaas
> Infrastructure as a service, computer nodes/vietual machine, need to maintain for your application to work.  
> Eg. website: frontend, backend, load balancer and auto scaling  

![cloud_service_products](gcp_image/google_services_1.png?raw=true "Title") 

![cloud_service_products](gcp_image/google_services_2.png?raw=true "Title") 

## 2.Compute Engine
Why?  
run ad hoc function that is not incorporated into the other GCP products.   
eg. backend operation that requires extra work apart from source code.
create instances (virtual machines).

- region are locations
> zones are actual data centers inside regions, same zones may not be in the same geographical locations, so better deploy them in the same session.
- memory and drive capacity
> SSD performs better in terms of read/write speed, lots of data --> standard disk  
- Preemptive instance
> used when you are processing bach workloads which allows for preemption
> you can create and run at a much lower price than normal instances, self terminate after 24 hours, compute engine might terminate preemptive instance at any time due to 

- encrypt at rest (data in chunked and encrypted with its own key, distributed in storage infrastructure)
- live migrate 

other people's workload on GCP.  
> solution: mix with permanent instance, if job is not finished on preemptive instance, migrate to the permanent instance to continue running.  
- snapshots 
> used for backup or transfer of data 
- image
> save vm disk as an image to be used later or crate a new Vm using a snapshot you created 

QA.  
Difference between an image and a snapshot.  
> image don't have data stored on the disk while a snapshot has.  
> snapshots are differential. (snapshot 2 only contains blocks which is different from snapshot 1)

Best practice:
- use start up scripts. (stopping vm will change ip!).
- backup data to gcs 
- diversify and use load balancer 
- use zone and region 

### migrage a disk to different region
```sh
## create a disk in different region but same zone.
### attach to an instance
## list all disks
lsblk

## format disk which is about to be mounted 
mkfs.ext4 -m 0 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb

mkdir -p /mnt/httpdir 
mount -o discard,defaults /dev/sdb /mnt/httpdir 
chmod a+w /mnt/httpdir
cp /etc/fstab /etc/fstab.backup

blkid /dev/sdb

vim /etc/fstab 
UUID=xxx /mnt/httpdir ext4 discard,defaults,nofail 0 2

cp /var/www/html/index.php /mnt/httpdir/.
vim /etc/apache2/sites-enabled/000-default.conf 
DocumentRoot /mnt/httpdir 

vim /etc/apache2/apache2.conf 
<Directory /mnt/httpdir> ...

## reload
/etc/init.d/apache2 reload 
```

create a disk from a snapshot. 

Question, how to do live migrate:
1. create an image based on boot-image disk 
2. create a snapshot from the disk where actual files are stored 
3. create a disk from the snapshot to a different region. 
4. clone the vm, choose the custom image created (same configuration rule) and the new disk (create from snapshot) 

## 3.IAM
Identity Access Management 
- roles and permissions 
> google account  
> service account   
> google group  

roles are made up of a list of permissions, can use predifiend roles or even customize roles.

- primitive roles

> owner  
> editor  
> viewer  

To create a vm instance, if you want to mange default service acccount, then have to grant iam.serviceAccountActor role. 
To create a fireware rule, need to grant compute.network.updatePolicy, compute.firewalls.create and compute.networks.network
> can be able to create fireware rule in shell console.  
> gcloud compute firewall-rules create testrule --allow tcp:8989

summary  
- every resource must belong to a project and a project must have a billing account attached to it.  
- remember hierarchy inheritance of access.
- spending limits can be set for a day, billing is done monthly.
- in terms of across projects, chargs is done on the one who initiates the process. 

## 4.Storage 
- OLTP and OLAP
> OLTP db has strong consistency, allow high throughput of reads and writes.  
> OLAP db is for historical querying, classified as data warehouses, doesn't support high throughput in terms of read and write. 
- strongly consistent and eventually consistent
> strong consistency, write transaction is successful, db guarantees the next read of data is available including the latest write.   
> eventual consistency, after "a period of time", not immediately. 
- transactional database
> strong consistency and used for OLTP purposes.  

### 5.Cloud Storage
![cloud storage](gcp_image/storage_options.png?raw=true "Title")
- blobs (files or images)

![cloud storage](gcp_image/storage-classes-compare.png?raw=true "Title")
> multi-regional: highest availability, geo-redundant, video multimedia.  
> single-region, data frequently accessed within a region.  
> nearline, data accessed less than a month.  
> coldline, data accessed less than a year, disaster recovery.  

- object versioning  
- lifecycle policy  

> perform action to an object  
> eg. downgrade storage class of objects older than 365 days to coldline.  
> delete objects created before certain days.  
> keep only 3 most recent versions of each object. 
- bucket policy & acls
> bucket policy is applied for the whole bucket  
> ACL is object level poloicy so each object has its own permission. 

```sh
# gsutil
gsutil cp  
gsutil mv  
gsutil rewrite -s storage_class gs://bucket_name
```

### bigtable 
1. low latency, manged nosql db that can scale up, handle millions of operations per second.  
1. **usgage: time-series data**  
1. stores data as unstructured columns in rows; each row has a row key.  

> how to retrieve data  
> get a single row by specifying the row key.  
> get multiple rows by specifying a range of row keys with wildcard syntax * .  

1. bigtable is strongly consistent in one region, but replication to another region becomes eventually consistent.  
1. failover bigtable cluster in another region, but it is eventually consistent, this can potentially increase SLA (service agreement level) for uptime.

```sh
#
cbt command:
## create a table 
cbt createtable table_name 
## delete
cbt deletetable table_name 

```

### bigquery 
- data warehousing solution
- automatically backed up and replicated and massively scalable to petabytes of data 
- related with analytics 
- not a transaction database and should not be used for application that require high throughput of read and write 
- cheap to store data however it can be costly when processing the data.  

### cloudsql 
- not a manged service, so it is not automatically replicated, auto-scaled and hightly available 
- create a cloudsql instance, similart like a vm  in compute engine 
- relational db like mysql, postgres 
- OLTP db, has strong consistency and used for transactional db. 
- good solution for migrating sql servers to GCP (note sql server is supported in GCP as well.)

### datastore
- highly scalable nosql db, like mongoDB and aws dynamoDB 
- managed service in GCP so highly available and replicated  
- suport sql like queries and indexes (not sql)  
- eventually consistent, may use in transactional db if meet your requirements.  
> support ACID transactions. 

> indexes  
>  indexes for simple queries are created automatically (querying over a single property)
>  complex queries must be defined in a configuration file called index.yaml 
>  datastore indexes create to update index, compare local index.yaml with production one. (Important)

### cloud spanner 
> relational db that is horizontally scalable. 
> low latency and fully managed, highly available and auto scaling.  
> strong transactional consistency.  
> downside: most expensive storage solution in GCP. 

### memorystore
> fully manged in-memory data service for redis  
> building cache systems  
> low latency , highly available across two zones with automatic failover (but not across regions)  
> start using a small memorystore and scale when required.  
> compatible with redis protocol, can be shifted without any changes.  

### firebase
> mobile sdk for both firebase storage and firebase realtime db

![cloud storage](gcp_image/gcp-storage-choose.png?raw=true "Title")

**Notes**
- time-series, sensory data --> bigtable
- analytical workloads or future analytics --> bigquery 
- transactional db --> cloudsql or cloud spanner 
- massive scale --> bigqeury, bigtable or cloud spanner  
- straight port over existing sql db from on-prem --> cloud sql 


## 6.Bigquery 

- serverless and sacles massively
- cheap to store data but costs in processing data
- allows batch inserts (free) and streaming inserts (cost)

> charges for storage (long term costs less), streaming inserts and querying data  
> free of loading, copying and exporting data, as well as metadata operations. 

### authorised views 
> share query results with particular users and groups without access to the actual table.

### partitioned tables 
date partitioned (performance and cost)
> 4000 partitions in total 
> 2000 partition updates per table, per day  
> 50 partiton updates every 10 seconds 

\_PARTITIONTIME  is reserved for the table, need to use an alias to see it.

wildcard tables (union all tables with similar names)

```sql
select * from `project.dataset.table*`
where _table_suffix between '12' and '13'
```

cost saving methods:
```
- use preview options
- query validator to check price of query
- consider partiton table
- avoid using select * 
- hard limit daily bytes
- hard limit members 
```

### temporary tables 
randomly named saved in a special dataset, has a lifetime of about 24 hours, not available for sharing, and not visitable for the standard list or other manipulation methods. Charged for storing them.  

### support file format 
csv, json, avro, parquet and orc 


## 7.Cloud Datalab
built on jupyter notebook, runs on an instance or VM using compute engine and can be connected to bigquery, compute engine and cloud storage. 


pipeline 
> streaming data: cloud pub/sub --> cloud dataflow --> bigquery --> cloud datalab/BI tools  
> batch data: cloud storage --> cloud dataflow --> bigquery --> cloud datalab/BI tools  

## 8.Data Studio
1. dashboard solution for reports of data 
1. can connect to bq, mysql, cloudsql, google sheets and google analytics.  
1. update is automatic, change of source data will change dashboard accordingly. 
1. share reports like files in google drive with limited permission.  


## 9.Cloud Pub/Sub 
- fully managed and real time messaging service, similar like AWs SQS (Simple Queue Service) or kafka. 
- durable and low latency (fast response). 
- global presence. 
- data reliability (get msg at least once)
- security (encryption at rest and on the move/in flight)

> sender and receiver is decoupled, allowing secure and high availability between sender and receiver.  
> change of any publisher/subscriber will not affect each other. 

How it works?  
1. a publisher application creates a topic and send messages to the topic, which contains a payload and optional attributes that describe the payload content. 
1. messages are persisted in a message store until they are delivered and acknowledged by subscribers. 
1. pub/sub forwards message from a topic to all of its subscriptions, individually. 
1. the subscriber receives pending message from its subscription and acknowledges each one to the pub/sub sevice.
1. when a message is acknowledged by the subscriber, it is removed from the subscription's queue of message.  
 
![pub/sub](gcp_image/pub_sub_basic.png?raw=true "Title")

Pub/Sub guarantees the subscriber will receive the message at least once before being deleted from the queue.  

### use cases
- balancing workloads in network clusters  

> load distributed evenly among workers or vms 

- data streaming

> could be intermittent or subsecond (sensor data)

- reliability improvement  

> if a zone(data center) fails, the message will just be transferred to the other zones. 

## hadoop & dataproc 

### hadoop
- HDFS (hadoop distributed file system)


> distributed computing software that utilise many nodes and memory to store and process data.  
> HDFS on top of many nodes, combines like one file system.  

- Hive

> data warehouse for querying and analyzing large datasets in HDFS, supports HiveQL, Map-Reduce is a data processing technique used for ETL. 

- Pig 

> enable data workers to write complex data transformations without knowing Java. SQL-like scripting language (Pig Latin). 

- Oozie 

> workflow scheduler system to mange hadoop jobs. 

- Sqoop

> transfers large data into hdfs from relational db. It's a transferring framework.  

### dataproc 
- fully manged cloud service for running hadoop clusters. 
- pay for resources used with per-second billing.
- scale if required.  
- easily migrate existing hadoop workloads onto GCP. 

### spark 
- in-memory distributed data processing engine. 
- spark workloads exist on a hadoop cluster. 


## 10.Dataflow 
dataflow is a manged service and spins up cloud storage and compute engine resources in the background automatically to enable your job to run.  
job can be monitored in **dataflow monitoring interface** and **datafow command-line interface**
```sh
## list of jobs 
gcloud dataflow jobs list 

## descriptions for a job 
gcloud dataflow jobs describe job_id
```
- transform data via streaming or batch mdoes with reliability and auto-scaling/serverless as needed.
- sits between frontend service for high throughput and backend service/data storage like bigquery. 
- parallel data processing. 

Why not use bigquery streaming insert instead?  
Data process is needed. 
> format, transfrom  

note streaming transformations: Apache Nifi and Storm  

major concepts in dataflow
> input --> transform --> pcollection --> transform --> pcollection --> output

- pipelines

> encapulates the whole data process, from input to output 

- pcollections 

> a set of data in pipeline, can represent data sets of unlimited size.  
> it can hold afixed size such as text file or a table or an unbounded data set from a streaming data source such as Pub/Sub. 

- transforms

> data opreations, take one or more pcollections as input and produce an output pcollection. 

- I/O srouces and sinks  

> input sources, output sinks (data received from the dataflow pipeline.)

dataflow optimises a dataflow job in 
- parallelisation and distribution.
> partitions data and distribute job to compute engine instances for parallel processing. 
- optimisation. 
> create execution graph that represents pipeline's pcollections and transforms, optimise the graph for efficient performance and resource usage. 

### udpate a streaming job 
- use the same deployment command and options 
- add in --update option 
- --jobName option in the PipelineOptions to the same name as the job you want to udpate 
- if transform names have changed, supply a transform mapping and pass it using --transformNameMapping option.  

### logging 
- logging console
- stackdriver monitoring console  

```py
python -m apache_beam.examples.wrodcount --input gs://bucket_name/object.txt --output gs://bucket_name/outputs --runner DataflowRunner --project $PROJECT --temp_location gs://bucket_name/tmp/ 

```

## 11.Dateprep 
> running on top Cloud dataflow which runs on compute engine. 

- drag and drop ETL tool, UI based on cleaning data
- visaully explore, clean and prepare structured and unstructured dat. 
- serverless and scalable 
- suggested and predicted data transformation

## 12.Tensorflow 
neural network forms the base for AI algorithm. (layers and nodes)  

overfitting: rules are too specific and too restricting to give the best result for other similar dataset.  

we need general pattern of the data.  
> combat overfitting  
> reduce number of ndoes or layers  
> dropout or early stopping. 

- natural language API

> analyse sentence, sentiment analysis  
> category, entity (syntax)

- translation 
- vision 

> recognise objects within pictures or text in pictures 

- speech

> speech into text. 


## 13.Machine Learning Solutions 

edge computing
- edge refers to individual 
- not scalable, performance downgrade when too many users

distributed computing 
- master/worker (divide and conquer)

- ml models 
> host and serve it at scale and is performance does not degrade.  
- features 
- labels 
- linear regression
- classification
> divide into different classes 
- logistic regression
> binary classification
- clustering/networks  (unsupervised learning)


### cloud machine learning engine 
aim for ml expoerts to quickly train and deploy models.  
**AI platform training** and **AI platform prediction**

### Bigquery ML 
create and execute ml models in bq using standard sql queries.

### kubeflow 
ml toolkit for Kubernetes, make ml workflow on kubernetes simple, portable and scalable. 
- distribute ml training among multiple workers to increase training speed 

### Spark ML 
ml toolkit for spark programming.

### cloud automl
train custom ml models specific, does the training for you automatically, only need to provide input data and output.  

- vision
- video intelligence 
- natural language 
- translation
- tables 

### dialogflow 
chatbot builder application, also includes an analytics tools that can measure the engagement or session metrics like usage patterns. 

### cloud TPU
cloud tensor processing unit is custom-designed ml device that powers translate, photos, search, assistant and gmail.  
optimised for deep learning or tf algorithms.  
A setp up from GPU.  


## 14.Cloud composer
- managed airflow service
- directed acyclic graphs of tasks 
- scheduler executes tasks on cluster of workers following specified dependencies.  
- user interface: monitor jobs 

1. end-to-end integration: storage, dataflow.  
1. hybrid and multi-cloud environments: connect pipelines and break down silos regardless of workflow living on-premises or in multiple clouds. 
1. easy workflow orchestration  
1. open source

## 15.migration into GCP

## data transfer 
same like AWS snowball, transfer data to cloud. 
> USB stick, physical hard disk that downloads all data from on-prem and compressed, encrypted as rest and transported to gcp data ceter to get uploaded.  
> uploaded to gcp storage using a process called rehydration, decryp data and de-compress to a useable state.  
> use case: upload data over 20TB 
## storage transfer
transfer online data to cloud storage, like aws s3.
> note other services all ingest data from on-prem data to gcp

## 16.security 
- least privilege and separation of duties 

> least amount of permissions
> eg. ACL to control object in bucket instead of bucket policy. 
> separate prod resources from all other environments.  
> individual projects, easy for access control, billing purposes, debugging and external audits. 

- interact with cloud storage 

> bucket policy  
> ACL, particular objects within the bucket
> signed URL, time limited access to an object, note anyone can access it.

- key management service 

> cloud-hosts key management sevice to mange crytographic keys, set a schedule to automatically rotate keys.
> don't upload credential to source repository. 
> encrypt credentials using kms keys and the keys are rotated automatically by KMS. upload encrypted strings to repo and at runtime the keys can be decrypted via KMS so the real keys will be inserted into runtime environment. 

- penetration test 

> perform tests and create a vulnerabilities report 
> eg. test web application externally to gcp network and attack the user endpoint. 

- using bastion/jumphost 

> private vpc should not have external ingress access, meaning cann't reach the instance or vms deployed into a private vpc.  
> deploy worker instance or database layer (instance that interact with database) into private vpc so there are no ports or endpoints exposed externally.  
> deploy bastion or jumphost in public vpc, limit potential hackers to workers.  

- data loss prevention api, encryption and compliance 

> manage sensitive data, classification and redaction for sensitive data (redact data from data stream and classify them)
> prevent PII from hitting storage due to compliance issues.  
> all products encrypted at reat or streaming. there is difference between default encryption keys, customer managed keys and customer supplied keys. 

google manged encryption keys: default keys, cannot see.  

customer managed encryption keys: managed by google but owned by customer, can be seen as they are stored in KMS. 

customer supplied encryption keys: owned and managed by customer, not allowed by many products.

data compliance: EU GDPR(general data protection regulation), google will do their end of securing actual infrastructure but you have to design your own architecture so that it is compliant. 
> eg. required to delete data after a month, then you have to set up lifecycle policy to delete data as google will not automatically delete data for you.  
> for PII data, not recommended to store (data loss prevention api can redact these), can store them using KMS to perform an encryption procedure.  

- live migration for compute engine 

> live migraiton to keep vm instance running even updating system.  
> move running instance to another host in the same zone instead of rebooting the system directly!

## 17.Stackdriver
- monitoring, logging and diagnostics solution. 
- health, performace and availability. 

### debugger
inspect state of a running application in real time without stopping or slowing it down.  
it allow you to inspect the production source code without slowing down your application.  
monitor variable in running programs.  
### error reporting 
counts, analyzes and aggregates the crashes in cloud services.  
email, mobile alerts on new erros. 
### monitoring 
overview performance, uptime and health, collects metrics, events and metadata, displays them via a dashboard.  
monitor updates of gcp services.  
### alerting  
create policy to notify.
### tracing  
how requests propagate throught application and receive detailed **near real time** performance insights.  
auto analyses to generate latency reports to show performace degradations on vms.  
### logging 
store, search, analyse, monitor and alert on log data and events from GCP.  
scale and ingest from thousands of VMs.  
can also analyse this in **real-time**.  

- export logs to bigquery 
> create an export sink, automatically send filtered logs to bq.  

## 18.Cloud functions
- run code in an envrionment taht does not require setting up vms or kubernetes clusters. 
- run code in response to an event. 
- short process 

```sh
def hello_gcs(evemt, context):
	file = event 
	print(f"process file: {file['name']}")

## zip python code 
gcloud functions deploy hello_gcs --runtime=python37 --trigger-resource=ace-exam-prep-bucket-1 --trigger-event=google.storage.object.finalize --source=gs://ace-exam-prep-bucket-1/main.zip
```

## 19.App Engine
- app and container that need to run for extended periods of time 
- conform to specific runtime 
- PAAS 
## Kubernetes Engine
- hybird compute

What are the components of an App Engine Standard application?
> Application, Service, Version and Instance


## 20.GKE 
it consists multiple machine grouped together to form a cluster.  
- node auto-repair 
- load-balancing 
- node pools 
- auto scaling
- auto upgrade 
- logging and monitoring

```sh
## enable container registry api
## enable kubernetes engine api

## log into google shell
git clont https://github.com/GoogleCloudPlatform/kubernetes-engine-samples

cd kubernetes-engine-samples/hello-app

## build docker image 
export PROJECT_ID=project_id
docker build -t gcr.io/${PROJECT_ID}/hello-app:v1 . 

## check docker images 
docker iamges 

## container registry authentication
gcloud auth configure-docker 

## puh image to registry
docker push gcr.io/${PROJECT_ID}/hello-app:v1 

## run image as container
docekr run --rm -p 8080:8080 gcr.io/${PROJECT_ID}/hello-app:v1

## deploy on kubernetes 
gcloud config set project ${PROJECT_ID}
gcloud config set conpute/zone us-east1 

## create instances 
gcloud container clusters create my-cluster --num-nodes=2

## list instances
gcloud compute instances list 

## deploy image 
kubectl create deployment hello-web --image=gcr.io/${PROJECT_ID}/hello-app:v1

kubectl get pods 

## expose to public, external ip addr
kubectl expose deployment hello-web --type=LoadBalancer --port 80 --target-port 8080

kubectl get service 

## scale up 
kubectl scale deployment hello-web --replicas=3

kubectl get deployment hello-web 

```

## 21. Network
TCP before BBR, TCP sends data at lower bandwidth because the 1980s-era algorithm assumes that packet loss means network congestion.  
BBR models the network to send as fast as the available bandwidth and is 2700x faster than previous TCPs on a 10Gb, 100ms link with 1% loss. 

hight network throughput and shorter network queues (reducing round-trip time), faster responses and lower delays for latency-sensitive applications. 
> from gcp services to cloud users  
> from google cloud to internet users  

![network](gcp_image/network.png?raw=true "Title")

Each side of a peering association is set up independently. Note that peering will only be active when the configuration from both sides matches. Either side can choose to delete the peering association at any time to tear that peer.

