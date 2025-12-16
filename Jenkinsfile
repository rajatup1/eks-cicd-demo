pipeline {
  agent any

  environment {
    AWS_REGION = "ap-south-1"
    ECR_REPO_URL = "200227355496.dkr.ecr.ap-south-1.amazonaws.com/flask-eks-demo"
    IMAGE_TAG = "${BUILD_NUMBER}"
    DOCKER = "/usr/local/bin/docker"
    AWS = "/opt/homebrew/bin/aws"
    KUBECTL = "/usr/local/bin/kubectl"
    DOCKER_CONFIG = "/Users/rajatupadhyay/.jenkins/.docker"
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
          $DOCKER build -t $ECR_REPO_URL:$IMAGE_TAG .
        '''
      }
    }

    stage('Login to ECR') {
      steps {
        sh '''
           $AWS ecr get-login-password --region $AWS_REGION \
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
    stage('Update kubeconfig') {
      steps {
        sh '''
         $AWS eks update-kubeconfig --region $AWS_REGION --name eks-cicd-demo
       '''
   }
 }


    stage('Deploy to EKS') {
      steps {
        sh '''
            $KUBECTL set image deployment/flask-app \
            flask=$ECR_REPO_URL:$IMAGE_TAG
        '''
      }
    }

  }
}