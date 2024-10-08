#!/bin/bash
<<<<<<<<<<<<<<  ✨ Codeium Command ⭐ >>>>>>>>>>>>>>>>
# This script simulates a load test on the cluster by sending a POST request
# to the Serverless API server every second, creating a new Job with a pod. The amount of jobs created per second is increased by
# 500 every minute.
<<<<<<<  30d5d417-c269-4c0e-99f4-76bb41b0f385  >>>>>>>
echo "Start executing CURL: 1 req/s"
for i in {0..59..1}
do
  curl \
      -s \
      --config curl_configs/1.txt \
      -X POST \
      -H 'Authorization: allow' \
      -H 'Content-Type: application/json' \
      -d '
{
  "apiVersion": "batch/v1",
  "kind": "Job",
  "metadata": {
    "generateName": "empty-"
  },
  "spec": {
    "template": {
      "metadata": {
        "name": "empty"
      },
      "spec": {
        "containers": [
          {
            "name": "empty",
            "image": "192.168.1.101:5000/empty",
            "imagePullPolicy": "Never",
            "resources": {
              "requests": {
                "memory": "400Mi",
                "cpu": 0.08
              }
            },
            "env": [
              {
                "name": "SLEEP_TIME",
                "value": "0"
              }
            ]
          }
        ],
        "restartPolicy": "Never"
      }
    }
  }
}
'
sleep 1
done
echo "DONE"
echo "Start executing CURL: 500 reqs/s"
for i in {0..59..1}
do
  curl \
      -s \
      --parallel \
      --parallel-immediate \
      --parallel-max 500 \
      --config curl_configs/500.txt \
      -X POST \
      -H 'Authorization: allow' \
      -H 'Content-Type: application/json' \
      -d '
{
  "apiVersion": "batch/v1",
  "kind": "Job",
  "metadata": {
    "generateName": "empty-"
  },
  "spec": {
    "template": {
      "metadata": {
        "name": "empty"
      },
      "spec": {
        "containers": [
          {
            "name": "empty",
            "image": "192.168.1.101:5000/empty",
            "imagePullPolicy": "Never",
            "resources": {
              "requests": {
                "memory": "400Mi",
                "cpu": 0.08
              }
            },
            "env": [
              {
                "name": "SLEEP_TIME",
                "value": "0"
              }
            ]
          }
        ],
        "restartPolicy": "Never"
      }
    }
  }
}
'
sleep 1
done
echo "DONE"
echo "Start executing CURL: 500 reqs/s"
for i in {0..59..1}
do
  curl \
      -s \
      --parallel \
      --parallel-immediate \
      --parallel-max 1000 \
      --config curl_configs/1000.txt \
      -X POST \
      -H 'Authorization: allow' \
      -H 'Content-Type: application/json' \
      -d '
{
  "apiVersion": "batch/v1",
  "kind": "Job",
  "metadata": {
    "generateName": "empty-"
  },
  "spec": {
    "template": {
      "metadata": {
        "name": "empty"
      },
      "spec": {
        "containers": [
          {
            "name": "empty",
            "image": "192.168.1.101:5000/empty",
            "imagePullPolicy": "Never",
            "resources": {
              "requests": {
                "memory": "400Mi",
                "cpu": 0.08
              }
            },
            "env": [
              {
                "name": "SLEEP_TIME",
                "value": "0"
              }
            ]
          }
        ],
        "restartPolicy": "Never"
      }
    }
  }
}
'
sleep 1
done
echo "DONE"