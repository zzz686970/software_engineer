## Introduction

Why use a cloud solution:
- traditional: maintainence cost is high, low capital investment.
- immediate deployment of the infrastructure 
- cost saving for hiring people.
> easier to setup, shorted setup time, no capitial cost, pay as go  
> Notice some sensitive or critical data can not be stored in the cloud.


Why GCP
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

## Compute Engine
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
> you can create and run at a much lower price than normal instances, self terminate after 24 hours, compute engine might terminate preemptive instance at any time due to other people's workload on GCP.  
> solution: mix with permanent instance, if job is not finished on preemptive instance, migrate to the permanent instance to continue running.  
- snapshots 
> used for backup or transfer of data 
- image
> save vm disk as an image to be used later or crate a new Vm using a snapshot you created 

QA.  
Difference between an image and a snapshot.  
> image don't have data stored on the disk while a snapshot has.

## IAM
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

summary  
- every resource must belong to a project and a project must have a billing account attached to it.  
- remember hierarchy inheritance of access.
- spending limits can be set for a day, billing is done monthly.
- in terms of across projects, chargs is done on the one who initiates the process. 

## Storage 
- OLTP and OLAP
> OLTP db has strong consistency, allow high throughput of reads and writes.  
> OLAP db is for historical querying, classified as data warehouses, doesn't support high throughput in terms of read and write. 
- strongly consistent and eventually consistent
> strong consistency, write transaction is successful, db guarantees the next read of data is available including the latest write.   
> eventual consistency, after "a period of time", not immediately. 
- transactional database
> strong consistency and used for OLTP purposes.  

### cloud storage
![cloud storage](gcp_image/storage_options.png?raw=true "Title")
- blobs (files or images)

