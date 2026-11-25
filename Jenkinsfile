pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub-credentials-id')
        DOCKERHUB_USER  = 'prabhatrai05'
        BACKEND_IMAGE   = "${DOCKERHUB_USER}/ai-investment-backend"
        FRONTEND_IMAGE  = "${DOCKERHUB_USER}/ai-investment-frontend"
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
                    sh "docker build -t ${BACKEND_IMAGE}:latest -t ${BACKEND_IMAGE}:${BUILD_NUMBER} ./backend"

                    echo "Building Production Frontend Docker Image..."
                    sh "docker build -t ${FRONTEND_IMAGE}:latest -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} -f ./frontend/Dockerfile.prod ./frontend"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Logging into Docker Hub as ${DOCKERHUB_USER}..."
                    sh 'echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin'
                    
                    echo "Pushing Backend Images..."
                    sh "docker push ${BACKEND_IMAGE}:latest"
                    sh "docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}"

                    echo "Pushing Frontend Images..."
                    sh "docker push ${FRONTEND_IMAGE}:latest"
                    sh "docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
                    
                    sh 'docker logout'
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                sshagent([SSH_KEY_CREDS]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} << 'EOF'
                        mkdir -p ~/app
                        cd ~/app
                        # Copy production compose & configs if needed
                        docker compose -f docker-compose.prod.yml pull
                        docker compose -f docker-compose.prod.yml up -d --remove-orphans
                        docker image prune -f
                    EOF
                    """
                }
            }
        }

        stage('Verify Health Check') {
            steps {
                sh "curl --retry 5 --retry-delay 5 --retry-connrefused http://${EC2_IP}:5005/health"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "CI/CD Pipeline executed successfully! New images deployed on EC2."
        }
        failure {
            echo "Pipeline failed! Check stage output logs."
        }
    }
}
