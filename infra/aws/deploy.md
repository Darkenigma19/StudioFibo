# AWS Deployment Guide

## Prerequisites

- AWS CLI configured with appropriate credentials
- Docker installed locally
- Terraform installed (optional, for IaC)

## Option 1: AWS Elastic Beanstalk

### Step 1: Create Elastic Beanstalk Application

```bash
eb init studioflow --platform docker --region us-east-1
eb create studioflow-env
```

### Step 2: Configure Environment Variables

```bash
eb setenv \
  STORAGE_BACKEND=s3 \
  AWS_BUCKET_NAME=studioflow-renders \
  AWS_REGION=us-east-1 \
  HUGGINGFACE_TOKEN=your_token_here
```

### Step 3: Deploy

```bash
eb deploy
```

## Option 2: AWS ECS + Fargate

### Step 1: Create ECR Repository

```bash
aws ecr create-repository --repository-name studioflow-backend
aws ecr create-repository --repository-name studioflow-frontend
```

### Step 2: Build and Push Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t studioflow-backend .
docker tag studioflow-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/studioflow-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/studioflow-backend:latest

# Build and push frontend
cd frontend/StudioFlow
docker build -t studioflow-frontend .
docker tag studioflow-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/studioflow-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/studioflow-frontend:latest
```

### Step 3: Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name studioflow-cluster
```

### Step 4: Create Task Definition

See `ecs-task-definition.json` for sample task definition.

### Step 5: Create Service

```bash
aws ecs create-service \
  --cluster studioflow-cluster \
  --service-name studioflow \
  --task-definition studioflow-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

## Option 3: AWS Lambda (Serverless)

Not recommended for this use case due to:

- Large model size (FIBO weights ~4GB)
- Long execution time for image generation
- GPU requirement for optimal performance

Consider AWS SageMaker for serverless GPU inference instead.

## Cost Optimization

### Storage

- Use S3 with lifecycle policies to transition old renders to Glacier
- Enable S3 Intelligent-Tiering

### Compute

- Use ECS with Spot instances for cost savings
- Set up auto-scaling based on queue length
- Consider GPU instances (g4dn.xlarge) for production

### Database

- Use RDS Aurora Serverless for SQLite replacement
- Enable backup retention policies

## Monitoring

### CloudWatch Logs

```bash
aws logs create-log-group --log-group-name /aws/ecs/studioflow
```

### CloudWatch Alarms

- Set up alarms for high CPU/memory
- Monitor render queue length
- Alert on failed renders

## Security

### IAM Roles

Create IAM role with:

- S3 bucket access (PutObject, GetObject)
- CloudWatch Logs write permissions
- Secrets Manager read (for HuggingFace token)

### VPC Configuration

- Run ECS tasks in private subnet
- Use NAT Gateway for outbound internet
- Restrict security groups to necessary ports

### Secrets

Store sensitive values in AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name studioflow/huggingface-token \
  --secret-string "your_token_here"
```

## CI/CD Pipeline

See `.github/workflows/deploy.yml` for automated deployment using GitHub Actions.

## Estimated Costs (us-east-1)

- **ECS Fargate (1 task, 4 vCPU, 8GB RAM)**: ~$100/month
- **S3 Storage (100GB)**: ~$2.30/month
- **RDS Aurora Serverless (minimal usage)**: ~$30/month
- **Data Transfer**: Varies based on traffic
- **GPU Instances (g4dn.xlarge, on-demand)**: ~$0.526/hour

**Total Estimated**: ~$130-150/month + GPU costs
