pipeline {
    agent any

    environment {
        VENV = "${env.WORKSPACE}/venv"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/AngelMerlinO/api_python_get'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    pytest --maxfail=1 --disable-warnings -v
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/test-results.xml', allowEmptyArchive: true
            junit 'test-results.xml'
        }
        cleanup {
            sh 'rm -rf $VENV'
        }
    }
}
