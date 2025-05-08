pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'jeershri/my-backend:latest'
    }
    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/jeer-15/jeer'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat "docker build -t $DOCKER_IMAGE ."
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'jeershri-dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    bat "docker push $DOCKER_IMAGE"
                }
            }
        }
    }
}

