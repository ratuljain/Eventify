node {
   def mvnHome
   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      checkout scm
      sh 'sudo su -s /bin/bash jenkins'
      echo "My branch is: ${env.BRANCH_NAME}"
      sh 'cd /var/lib/jenkins/workspace/Eventify_pipeline'
   }

   stage('Build') {
        sh 'virtualenv -q venv'
        sh '. venv/bin/activate'
        sh 'pip install -r requirements.txt --user'
        sh 'python manage.py makemigrations'
        sh 'python manage.py migrate'
   }

   stage('Publishing Reports') {
      publishHTML (target: [
      allowMissing: false,
      alwaysLinkToLastBuild: false,
      keepAll: true,
      reportDir: 'reports/coverage',
      reportFiles: 'index.html',
      reportName: "RCov Report"
    ])
   }

   if(env.BRANCH_NAME == "master"){
     stage('Deploy') {
       echo '####### Deploying Code ##########'

     }
   }
}