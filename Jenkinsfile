pipeline {
  agent any

  environment {
    AWS_REGION = "ap-south-1"
    ECR_REPO_URL = "200227355496.dkr.ecr.ap-south-1.amazonaws.com/flask-eks-demo"
    IMAGE_TAG = "${BUILD_NUMBER}"
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
          docker build -t $ECR_REPO_URL:$IMAGE_TAG .
        '''
      }
    }

    stage('Login to ECR') {
      steps {
        sh '''
          aws ecr get-login-password --region $AWS_REGION \
          | docker login --username AWS --password-stdin $ECR_REPO_URL
        '''
      }
    }
    stage('Push Image') {
      steps {
        sh '''
          docker push $ECR_REPO_URL:$IMAGE_TAG
        '''
      }
    }
    stage("Deploy to EKS"){
      steps{
        withCredentials([file(credentialsId: 'eks-kubeconfig', variable: 'KUBECONFIG')]) {
            sh '''
            export KUBECONFIG=$KUBECONFIG
            kubectl set image deployment/flask-app flask=$ECR_REPO_URL:$IMAGE_TAG
            kubectl rollout status deployment/flask-app --timeout=120s
            '''
          }
        }
     }
   }
  post {
        failure {
            echo "Deployment failed — rolling back"
            withCredentials([file(credentialsId: 'eks-kubeconfig', variable: 'KUBECONFIG')]) {
                sh '''
                kubectl rollout undo deployment/flask-app
                '''
            }
        }

        success {
            echo "Deployment successful 🎉"
        }
    }
}