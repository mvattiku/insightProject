def lambda_handler(event, context):
    sourceKey = event['Records'][0]['s3']['object']['key']
    sourceSize = event['Records'][0]['s3']['object']['size']
    if (sourceSize != 0):
        print(event)
        print("key:", sourceKey)
    else:
        print("size: ", sourceSize)