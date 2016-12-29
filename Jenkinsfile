node {
   properties([[$class: 'jenkins.model.BuildDiscarderProperty', strategy:
            [$class: 'LogRotator', numToKeepStr: '50', artifactNumToKeepStr: '20']
           ]])
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

   stage('Running Tests') {
        sh 'python manage.py harvest --with-xunit'
   }

   stage('Publishing Reports') {
        sh 'python manage.py jenkins  --enable-coverage   --coverage-format html'

        publishHTML (target: [
        allowMissing: false,
        alwaysLinkToLastBuild: false,
        keepAll: true,
        reportDir: 'reports/coverage',
        reportFiles: 'index.html',
        reportName: "RCov Report"
        ])

        step([$class: 'XUnitBuilder',
        thresholds: [[$class: 'FailedThreshold', unstableThreshold: '1']],
        tools: [[$class: 'JUnitType', pattern: 'lettucetests.xml']]])
   }

   if(env.BRANCH_NAME == "master"){
     stage('Deploy') {
         try {
           echo '####### Deploying Code ##########'
           sh 'sudo su -s /bin/bash deployer'
           echo "My branch is: ${USER}"
           sh 'cd /var/lib/jenkins/workspace/fsp-deployment-guide'
           sh 'sudo chmod -R 700 /var/lib/jenkins/workspace/fsp-deployment-guide/ssh_keys'
           sh 'sudo chmod -R 700 /var/lib/jenkins/workspace/fsp-deployment-guide'
           def out = sh script: 'sudo /var/lib/jenkins/workspace/fsp-deployment-guide/deploy_prod.sh', returnStdout: false
       } catch(error) {
         echo "First build failed, let's retry if accepted"
         retry(2) {
           input "Retry the job ?"
           echo '####### Deploying Code ##########'
           sh 'sudo su -s /bin/bash deployer'
           echo "My branch is: ${USER}"
           sh 'cd /var/lib/jenkins/workspace/fsp-deployment-guide'
           sh 'sudo chmod -R 700 /var/lib/jenkins/workspace/fsp-deployment-guide/ssh_keys'
           sh 'sudo chmod -R 700 /var/lib/jenkins/workspace/fsp-deployment-guide'
           def out = sh script: 'sudo /var/lib/jenkins/workspace/fsp-deployment-guide/deploy_prod.sh', returnStdout: false
         }
       }
     }
   }

   step([$class: 'WsCleanup'])
}