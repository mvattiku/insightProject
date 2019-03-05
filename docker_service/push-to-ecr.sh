#!/bin/bash

if [ $# -ne 4 ]
  then
    echo "Not all arguments supplied"
    echo "Provide Arg1-AWS account id, Arg2-Image name, Arg3-Repo name, Arg4-version"
    exit
fi

echo "Arguments provided: \n\tAWS account if- $1, Image name- $2, Repo name- $3, Version- $4"

#Retrieve the login command to use to authenticate your Docker client to your registry
$(aws ecr get-login --no-include-email --region us-west-2)

#After the build completes, tag your image so you can push the image to this repository
#docker tag <image-arg-read:latest> 628998090559.dkr.ecr.us-west-2.amazonaws.com/<repo-arg-read>:<version-latest>
docker tag $2 $1.dkr.ecr.us-west-2.amazonaws.com/$3:$4

#Run the following command to push this image to your newly created AWS repository
docker push $1.dkr.ecr.us-west-2.amazonaws.com/$3:$4

: << 'END'
if [ $# -ne 3 ]
  then
    echo "Not all arguments supplied"
    echo "Provide Arg1-AWS account id, Arg2-Image name, Arg3-Repo name, Arg4-version"
    echo "WARNING! If version not provided, image will be uploaded as the 'latest' version"
    exit
fi

if [ -z "$4" ]; then
    echo "WARNING! Version not provided, so image uploaded as the 'latest' version"
fi
ARG4=${4:-latest}
'END'