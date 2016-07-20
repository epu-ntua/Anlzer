__author__ = 'mpetyx'


import os
from keys import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3
import random, string
from datetime import datetime, timedelta

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

class helper:

    def __init__(self, project = None):

        self.s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                                        )
        self.project = project

    def create(self):
        self.s3.create_bucket(Bucket=self.project.name, CreateBucketConfiguration={
            'LocationConstraint': 'us-west-1'})

        return 201

    def bucket_size(self):

        bucket_name = self.project.name
        cloudwatch = boto3.client('cloudwatch', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                                  )
        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/S3",
            MetricName="BucketSizeBytes",
            Dimensions=[
                {
                    "Name": "BucketName",
                    "Value": bucket_name
                },
                {
                    "Name": "StorageType",
                    "Value": "StandardStorage"
                }
            ],
            StartTime=datetime.now() - timedelta(days=1),
            EndTime=datetime.now(),
            Period=86400,
            Statistics=['Average']
        )

        bucket_size_bytes = response['Datapoints'][-1]['Average']
        return bucket_size_bytes

    def available_policy_on_check_size(self):
        # TODO make this a lamda function
        if self.bucket_size() < self.project.size:

            return True
        else:
            return False

    def upload(self, local_filename):

        # temp_file = open("something_yolo", "w")
        # temp_file.write(local_filename)
        # temp_file.close()

        if self.available_policy_on_check_size():
            self.s3.Object(self.project.name, randomword(20).put(Body=open(local_filename, 'rb')))
            self.index_to_ES(local_filename)

    def index_to_ES(self, local_filename):
        return




