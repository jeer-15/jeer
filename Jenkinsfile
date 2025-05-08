pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "jeershri/my-backend"  // 🔥 Replace with your actual DockerHub username
        DOCKER_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/jeer-15/jeer'
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
                withCredentials([usernamePassword(credentialsId: 'jeershri-dockerhub', usernameVariable: 'jeershri', passwordVariable: 'DOCKER_PAS')]) {
                    script {
                        bat """
                            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                            docker push %DOCKER_IMAGE%:%DOCKER_TAG%
                        """
                    }
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
