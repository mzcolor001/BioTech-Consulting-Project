#!/bin/sh
# use google API to talk to the GCP buckets

pip install google-cloud-storage

# initiate the instance where your raw data resides
gcloud compute instances start instance-1

# access the instance
ssh instance-1.xxxxxxxx.xxxxx

# copy file on this instance to the local sever 
gsutil cp [src] [dst]
