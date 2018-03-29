VPC created: vpc-7ec55b05
Subnet created: subnet-088b8c27
Subnet created: subnet-f29159b8
Cluster creation succeeded.


  aws ec2 --region us-east-1 create-security-group --group-name "public-80" --description "test ecs fargate" --vpc-id "vpc-7ec55b05"

"GroupId": "sg-112d2a67"

  aws ec2 --region us-east-1 authorize-security-group-ingress --group-id "sg-112d2a67" --protocol tcp --port 80 --cidr 0.0.0.0/0
  ecs-cli compose --project-name docker-flask service up --create-log-groups
