pipeline {
    agent any

    environment {
        IMAGE_NAME = 'dockerforge'
        CONTAINER_NAME = 'dockerforge_app'
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    . venv/bin/activate
                    pytest test_app.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building image...'
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Deploy Container') {
            steps {
                echo 'Deploying...'
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
                sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }
        }
    }

    post {
        always {
            echo "Updating application dashboard with build status..."
            // Send the BUILD_NUMBER and currentBuild.currentResult to the Flask API
            // Using curl pointing to the container mapped on host port 5000
            sh """
                curl -X POST http://localhost:5000/api/update-status \\
                -H "Content-Type: application/json" \\
                -d '{"build_number": "${env.BUILD_NUMBER}", "status": "${currentBuild.currentResult}"}' || true
            """
        }
    }
}
