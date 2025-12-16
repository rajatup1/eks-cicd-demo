pipeline{
    agent any
    environment{
        AWS_REGION = "ap-south-1"
        ECS_REPO_URL = "200227355496.dkr.ecr.ap-south-1.amazonaws.com/flask-eks-demo"
        IMAGE_TAG = "${BUILD_NUMBER}"

    }
    stages{
        stage('Checkout') {
            steps {
                checkout scm
         }
       }
        stage("Build Docker image"){
            steps{
                    sh '''
                        docker buildx build \
                        --platform linux/amd64 \
                        -t $ECR_REPO_URL:$IMAGE_TAG \
                        --load .
                    '''
            }
            

        }
    }
        stage("Login and push to ecr"){
            steps{
                sh '''
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $ECS_REPO_URL
                    docker push $ECS_REPO_URL:$IMAGE_TAG
                '''
            }

        stage("Deploy to EKS"){
            steps{
                sh'''
                    sed -i "s/IMAGE_TAG/$IMAGE_TAG/g" k8s/deployment.yaml
                    kubectl apply -f k8s/deployment.yaml

                '''
            }
        }


        }
}