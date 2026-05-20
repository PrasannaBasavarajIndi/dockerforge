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
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint Code') {
            steps {
                echo 'Linting code with flake8...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    flake8 app.py test_app.py --max-line-length=120
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Running tests...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest test_app.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building image...'
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Deploy Container') {
            steps {
                echo 'Deploying...'
                bat returnStatus: true, script: "docker stop ${CONTAINER_NAME}"
                bat returnStatus: true, script: "docker rm ${CONTAINER_NAME}"
                bat "docker run -d -p 5000:5000 -v dockerforge_data:/app/data --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }
        }
    }

    post {
        always {
            echo "Updating application dashboard with build status..."
            bat returnStatus: true, script: """
                powershell -Command "Start-Sleep -Seconds 5"
                curl -X POST http://localhost:5000/api/update-status -H "Content-Type: application/json" -d "{\\"build_number\\": \\"${env.BUILD_NUMBER}\\", \\"status\\": \\"${currentBuild.currentResult}\\"}"
            """
        }
    }
}
