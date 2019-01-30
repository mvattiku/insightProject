import time
import sys
import random

sleepTime = random.randint(5, 30)
print("Sleeping for", sleepTime, "seconds.")
time.sleep(sleepTime)
print("Slept for", sleepTime, "seconds.")
input_arg = ['NONE']
try:
    if("/" in sys.argv[1]):
        arg = sys.argv[1].split("/")
        file = arg[-1]
    else:
        file = sys.argv[1]
    input_arg = [file]
    print ("Argument:", sys.argv[1], " - File:", input_arg)
except Exception as e:
    print ("Exception:", e, end=" -- ")
    print ("No arguments provided")

#output a csv file (similar to the model output)
import csv
import pandas as pd

print ("Creating DataFrame")
cols = ['name', 'mean_le', 'lower_bound', 'upper_bound', 'observations',
        'condition1', 'condition2', 'condition3', 'conditions_matched',
        'min_age', 'max_age', 'min_bmi', 'max_bmi', 'lifestyle', 'smoker', 'sex']
results = [[0000,3.28989579318182,2.5464318524,4.0419858704,99,'overuse or chronic use of prescribed narcotics for pain relief','diabetes','psychosis or psychotic disorder',1,94,102,'','','','','M']]
output_df = pd.DataFrame(data=results, columns=cols)

print ("Writing to file")

filename = input_arg[0]+'_output_file.csv'
output_df.to_csv(filename, index=False)
print ("Wrote to file --", filename) 

#save csv to S3
import boto3
s3_client = boto3.client('s3')
bucket = 'batch-output'
s3_client.upload_file(filename, bucket, filename)
print ("Output saved to s3.")
