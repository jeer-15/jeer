pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my-backend"  // Replace with a name like my-backend
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/jeer-15/jeer'  // Replace with your actual repo URL
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    bat 'docker push %DOCKER_IMAGE%:%DOCKER_TAG%'
                }
            }
        }

        stage('Deploy to Cloud') {
            steps {
                script {
                    bat 'gcloud run deploy jeer-backend --image=gcr.io/my-gcp-project-459116/%DOCKER_IMAGE%:%DOCKER_TAG% --platform managed --region us-central1 --allow-unauthenticated'
                }
            }
        }
    }
}
