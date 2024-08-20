#!/bin/bash
# This script simulates a load test on the cluster by sending a POST request
# to the Kubernetes API server every second, creating a new Job with a pod. The amount of jobs created per second is increased by
# 500 every minute.
echo "Start executing CURL: 1 req/s"
for i in {0..59..1}
do
 curl \
      -s \
      --cacert /tmp/kube-api-ca.pem \
      --cert /tmp/kube-api-cert.pem \
      --key /tmp/kube-api-key.pem \
      -X POST \
      --config curl_configs/1.txt \
      -H 'Content-Type: application/yaml' \
      -d '---
apiVersion: batch/v1
kind: Job
metadata:
  generateName: empty-
spec:
  template:
    metadata:
      name: empty
    spec:
      containers:
      - name: empty
        image: 192.168.1.101:5000/empty
        imagePullPolicy: Never
        resources:
          requests:
            memory: "1Mi"
            cpu: 0.01
        env:
        - name: SLEEP_TIME
          value: "0"
      restartPolicy: Never
'
sleep 1
done
echo "DONE"
echo "Start executing CURL: 500 reqs/s"
for i in {0..59..1}
do
 curl \
      -s \
      --cacert /tmp/kube-api-ca.pem \
      --cert /tmp/kube-api-cert.pem \
      --key /tmp/kube-api-key.pem \
      -X POST \
      --config curl_configs/500.txt \
      -H 'Content-Type: application/yaml' \
      -d '---
apiVersion: batch/v1
kind: Job
metadata:
  generateName: empty-
spec:
  template:
    metadata:
      name: empty
    spec:
      containers:
      - name: empty
        image: 192.168.1.101:5000/empty
        imagePullPolicy: Never
        resources:
          requests:
            memory: "1Mi"
            cpu: 0.01
        env:
        - name: SLEEP_TIME
          value: "0"
      restartPolicy: Never
'
sleep 1
done
echo "DONE"
echo "Start executing CURL: 500 reqs/s"
for i in {0..59..1}
do
 curl \
      -s \
      --cacert /tmp/kube-api-ca.pem \
      --cert /tmp/kube-api-cert.pem \
      --key /tmp/kube-api-key.pem \
      -X POST \
      --config curl_configs/1000.txt \
      -H 'Content-Type: application/yaml' \
      -d '---
apiVersion: batch/v1
kind: Job
metadata:
  generateName: empty-
spec:
  template:
    metadata:
      name: empty
    spec:
      containers:
      - name: empty
        image: 192.168.1.101:5000/empty
        imagePullPolicy: Never
        resources:
          requests:
            memory: "1Mi"
            cpu: 0.01
        env:
        - name: SLEEP_TIME
          value: "0"
      restartPolicy: Never
'
sleep 1
done
echo "DONE"