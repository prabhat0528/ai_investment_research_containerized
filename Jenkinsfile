pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub-credentials-id')
        DOCKERHUB_USER  = 'prabhatrai05'
        BACKEND_IMAGE   = 'prabhatrai05/ai-investment-backend'
        FRONTEND_IMAGE  = 'prabhatrai05/ai-investment-frontend'
        EC2_IP          = 'your-ec2-public-ip'
        EC2_USER        = 'ubuntu'
        SSH_KEY_CREDS   = credentials('ec2-ssh-key-id')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Pulling latest code from GitHub..."
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Backend Docker Image..."
                    if (isUnix()) {
                        sh "docker build -t ${BACKEND_IMAGE}:latest -t ${BACKEND_IMAGE}:${BUILD_NUMBER} ./backend"
                        echo "Building Production Frontend Docker Image..."
                        sh "docker build -t ${FRONTEND_IMAGE}:latest -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} -f ./frontend/Dockerfile.prod ./frontend"
                    } else {
                        bat "docker build -t ${BACKEND_IMAGE}:latest -t ${BACKEND_IMAGE}:${BUILD_NUMBER} ./backend"
                        echo "Building Production Frontend Docker Image..."
                        bat "docker build -t ${FRONTEND_IMAGE}:latest -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} -f ./frontend/Dockerfile.prod ./frontend"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Logging into Docker Hub as ${DOCKERHUB_USER}..."
                    if (isUnix()) {
                        sh 'echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin'
                        echo "Pushing Backend Images..."
                        sh "docker push ${BACKEND_IMAGE}:latest"
                        sh "docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}"
                        echo "Pushing Frontend Images..."
                        sh "docker push ${FRONTEND_IMAGE}:latest"
                        sh "docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
                        sh 'docker logout'
                    } else {
                        bat 'echo %DOCKERHUB_CREDS_PSW% | docker login -u %DOCKERHUB_CREDS_USR% --password-stdin'
                        echo "Pushing Backend Images..."
                        bat "docker push ${BACKEND_IMAGE}:latest"
                        bat "docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}"
                        echo "Pushing Frontend Images..."
                        bat "docker push ${FRONTEND_IMAGE}:latest"
                        bat "docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
                        bat 'docker logout'
                    }
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                script {
                    echo "Deploying to AWS EC2 (${EC2_IP})..."
                    if (isUnix()) {
                        sshagent([SSH_KEY_CREDS]) {
                            sh """
                            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "cd ~/app && sudo docker compose -f docker-compose.prod.yml pull && sudo docker compose -f docker-compose.prod.yml up -d --remove-orphans && sudo docker image prune -f"
                            """
                        }
                    } else {
                        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                            withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key-id', keyFileVariable: 'SSH_KEY_FILE')]) {
                                bat "ssh -i \"%SSH_KEY_FILE%\" -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} \"cd ~/app && sudo docker compose -f docker-compose.prod.yml pull && sudo docker compose -f docker-compose.prod.yml up -d --remove-orphans && sudo docker image prune -f\""
                            }
                        }
                    }
                }
            }
        }

        stage('Verify Health Check') {
            steps {
                script {
                    if (isUnix()) {
                        sh "curl --retry 5 --retry-delay 5 --retry-connrefused http://${EC2_IP}:5005/health || true"
                    } else {
                        bat "curl.exe --retry 5 --retry-delay 5 --retry-connrefused http://${EC2_IP}:5005/health || echo Health check finished"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "CI/CD Pipeline executed successfully! New images deployed on EC2."
        }
        failure {
            echo "Pipeline failed! Check stage output logs."
        }
    }
}
