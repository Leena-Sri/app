pipeline {
  agent any

  stages {
    stage('Build Docker Image') {
      steps {
        bat "docker build -t sampleflaskapp ."
      }
    }

    stage('Run Docker Container') {
      steps {
        bat "docker rm -f sampleflaskapp-container || echo no-container"
        bat "docker run -d -p 5000:5000 --name sampleflaskapp-container sampleflaskapp"
      }
    }
  }

  post {
    success { echo 'Pipeline completed successfully' }
    failure { echo 'Pipeline failed' }
  }
}
