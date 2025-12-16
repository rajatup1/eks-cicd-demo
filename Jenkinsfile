pipeline {
  agent any

  environment {
    AWS_REGION = "ap-south-1"
    ECR_REPO_URL = "200227355496.dkr.ecr.ap-south-1.amazonaws.com/flask-eks-demo"
    IMAGE_TAG = "${BUILD_NUMBER}"
    DOCKER = "/usr/local/bin/docker"
    DOCKER_CONFIG = "/Users/rajatupadhyay/.jenkins/.docker
    
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          $DOCKER buildx build \
            --platform linux/amd64 \
            -t $ECR_REPO_URL:$IMAGE_TAG \
            --load .
        '''
      }
    }

    stage('Login to ECR') {
      steps {
        sh '''
          aws ecr get-login-password --region $AWS_REGION \
          | $DOCKER login --username AWS --password-stdin $ECR_REPO_URL
        '''
      }
    }

    stage('Push Image') {
      steps {
        sh '''
          $DOCKER push $ECR_REPO_URL:$IMAGE_TAG
        '''
      }
    }

    stage('Deploy to EKS') {
      steps {
        sh '''
          kubectl set image deployment/flask-app \
            flask=$ECR_REPO_URL:$IMAGE_TAG
        '''
      }
    }

  }
}