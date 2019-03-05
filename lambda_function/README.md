# Lambda Function

The lambda function in invoked when there are new files added to the particular S3 bucket and folder. 
- This configuration must be done on AWS console. Configure the lambda function by telling which S3 bucket and folder and what event will trigger it. 
    - So in this case, the event is an update to the indicated bucket and folder in S3. 

Once function is invoked, a AWS Batch Job is created where the new file is passed in as input to the ML model.