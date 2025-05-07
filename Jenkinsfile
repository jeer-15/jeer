pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my-backend"  // Replace with a name like my-backend
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git ''  // Replace with your actual repo URL
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh 'docker push $DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }

        stage('Deploy to Cloud') {
            steps {
                script {
                    sh 'gcloud run deploy your-service --image=gcr.io/your-project-id/$DOCKER_IMAGE:$DOCKER_TAG --platform managed --region us-central1 --allow-unauthenticated'
                }
            }
        }
    }
}
