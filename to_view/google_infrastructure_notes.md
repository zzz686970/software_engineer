Google Infrastructure

gcloud beta compute --project "qwiklabs-gcp-01-1b574a0a8610" ssh --zone "us-central1-a" "lampstack-2-vm"


Ip  10.0.0.0/24
子网划分的过程将IP地址分块
IP地址计算， 32中减去前缀（由于IP地址是32位数）结果作为2的指数，您将获得该范围内的IP数量。


Notice that the output of the ping command reveals that the complete hostname of my-vm-1 is my-vm-1.c.PROJECT_ID.internal, where PROJECT_ID is the name of your Google Cloud Platform project. GCP automatically supplies Domain Name Service (DNS) resolution for the internal IP addresses of VM instances.

Modify the Access Control List of the object you just created so that it is readable by everyone:
gsutil acl ch -u allUsers:R gs://$DEVSHELL_PROJECT_ID/my-excellent-blog.png



```sh
## download an editable Deployment Manager template
gsutil cp gs://cloud-training/gcpfcoreinfra/mydeploy.yaml mydeploy.yaml

## insert your Google Cloud Platform project ID into the file in place of the string PROJECT_ID using this command
sed -i -e 's/PROJECT_ID/'$DEVSHELL_PROJECT_ID/ mydeploy.yaml
## Insert your assigned Google Cloud Platform zone into the file in place of the string ZONE
sed -i -e 's/ZONE/'$MY_ZONE/ mydeploy.yaml

## Build a deployment from the template
gcloud deployment-manager deployments create my-first-depl --config mydeploy.yaml

## pdate your deployment to install the new startup script
gcloud deployment-manager deployments update my-first-depl --config mydeploy.yaml

## create a CPU load:
# This Linux pipeline forces the CPU to work on compressing a continuous stream of random data.
dd if=/dev/urandom | gzip -9 >> /dev/null &

## kill workload
kill %1


```