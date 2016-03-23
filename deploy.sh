#! /bin/bash

SHA1=$1

# Deploy image to Docker Hub
docker push cragfinder/development:$SHA1

# Create new Elastic Beanstalk version
EB_BUCKET=crag-finder-dev
DOCKERRUN_FILE=$SHA1-Dockerrun.aws.json
sed "s/<TAG>/$SHA1/" < Dockerrun.aws.json.template > $DOCKERRUN_FILE
aws s3 cp --region eu-west-1 $DOCKERRUN_FILE s3://$EB_BUCKET/$DOCKERRUN_FILE
aws elasticbeanstalk create-application-version --region eu-west-1 --application-name crag-finder --version-label $SHA1 --source-bundle S3Bucket=$EB_BUCKET,S3Key=$DOCKERRUN_FILE

# Update Elastic Beanstalk environment to new version
aws elasticbeanstalk update-environment --region eu-west-1 --environment-name crag-finder-dev --version-label $SHA1