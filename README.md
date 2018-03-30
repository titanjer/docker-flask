
  ecs-cli configure --cluster docker-flask --region us-east-1 --default-launch-type FARGATE --config-name docker-flask
  ecs-cli up

    VPC created: vpc-7ec55b05
    Subnet created: subnet-088b8c27
    Subnet created: subnet-f29159b8
    Cluster creation succeeded.

  aws ec2 --region us-east-1 create-security-group --group-name "public-80" --description "test ecs fargate" --vpc-id "vpc-7ec55b05"

    "GroupId": "sg-112d2a67"

  aws ec2 --region us-east-1 authorize-security-group-ingress --group-id "sg-112d2a67" --protocol tcp --port 80 --cidr 0.0.0.0/0

  aws elbv2 create-load-balancer --region us-east-1 --name my-load-balancer \
        --subnets subnet-088b8c27 subnet-f29159b8 --security-groups sg-112d2a67

    arn:aws:elasticloadbalancing:us-east-1:473024607515:loadbalancer/app/my-load-balancer/1a25392ec076e729

  aws elbv2 create-target-group --region us-east-1 --name my-targets \
        --protocol HTTP --port 80 --vpc-id vpc-7ec55b05 --target-type ip

    arn:aws:elasticloadbalancing:us-east-1:473024607515:targetgroup/my-targets/980db2cf65acf986

  aws elbv2 create-listener --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:473024607515:loadbalancer/app/my-load-balancer/1a25392ec076e729 \
        --protocol HTTP --port 80  --region us-east-1 \
        --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:473024607515:targetgroup/my-targets/980db2cf65acf986

    arn:aws:elasticloadbalancing:us-east-1:473024607515:listener/app/my-load-balancer/1a25392ec076e729/d881eb287070179b

  ecs-cli compose --project-name docker-flask service up --create-log-groups
  ecs-cli compose --project-name docker-flask service scale 5

  ecs-cli compose --project-name docker-flask service up --create-log-groups --force-deployment
  ecs-cli compose -f docker-compose-ecs.yml --project-name docker-flask service up \
        --create-log-groups --force-deployment \
        --target-group-arn arn:aws:elasticloadbalancing:us-east-1:473024607515:targetgroup/my-targets/980db2cf65acf986 \
        --container-name nginx --container-port 80
