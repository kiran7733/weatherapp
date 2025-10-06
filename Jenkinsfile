pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
    steps {
        bat 'T:\\py\\python.exe -m pip install --upgrade pip'
        bat 'T:\\py\\python.exe -m pip install -r requirements.txt'
    }
}

        stage('Run Unit Tests') {
    steps {
        bat 'T:\\py\\python.exe -m unittest discover -s . -p "test_*.py"'
    }
}

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t weather-app .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker stop weather-container || exit 0'
                bat 'docker rm weather-container || exit 0'
                bat 'docker run -d -p 8000:8000 --name weather-container weather-app'
            }
        }
    }
}
