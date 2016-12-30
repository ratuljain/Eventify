node {
   try {
   notifyStarted()
   properties([[$class: 'jenkins.model.BuildDiscarderProperty', strategy:
            [$class: 'LogRotator', numToKeepStr: '50', artifactNumToKeepStr: '20']
           ]])
   stage('Preparation') {
      checkoutProject()
   }

   stage('Build') {
      buildProject()
   }

   stage('Running Tests') {
      runTests()
   }

   stage('Publishing Reports') {
      publishReports()
   }

   if(env.BRANCH_NAME == "master"){
     stage('Deploy') {
       try {
          deployProject()
       } catch(error) {
         echo "First build failed, let's retry if accepted"
         retry(2) {
           input "Retry the job ?"
           deployProject()
         }
       }
     }
   }
   }catch(error) {
      echo "Caught: ${error}"
      currentBuild.result = 'FAILURE'
      notifyFailed()
   }finally {
      // perform workspace cleanup only if the build have passed
      // if the build has failed, the workspace will be kept
      step([$class: 'WsCleanup', cleanWhenFailure: false])
    }
}

def notifyStarted() {
  // send to Slack
    slackSend (color: '#FFFF00', message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

def notifySuccessful() {
    slackSend (color: '#00FF00', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

def notifySuccessfulDeployment() {
    slackSend (color: '#00FF00', message: "SUCCESSFULLY DEPLOYED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

def notifyFailed() {
    slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
}

def checkoutProject(){
    checkout scm
    sh 'sudo su -s /bin/bash jenkins'
    echo "My branch is: ${env.BRANCH_NAME}"
    sh 'cd /var/lib/jenkins/workspace/Eventify_pipeline'
}

def buildProject(){
    sh 'virtualenv -q venv'
    sh '. venv/bin/activate'
    sh 'pip install -r requirements.txt --user'
    sh 'python manage.py makemigrations'
    sh 'python manage.py migrate'
}

def runTests(){
    sh 'python manage.py harvest --with-xunit --with-jsonreport'
}

def publishReports(){
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

    step($class: 'CucumberTestResultArchiver', testResults: 'lettucetests.json')

    notifySuccessful()
}

def deployProject(){
    echo '####### Deploying Project ##########'
    sh 'sudo su -s /bin/bash deployer'
    echo "My branch is: ${USER}"
    sh 'cd /var/lib/jenkins/workspace/fsp-deployment-guide'
    sh 'sudo chmod -R 700 /var/lib/jenkins/workspace/fsp-deployment-guide/ssh_keys'
    sh 'sudo chmod -R 700 /var/lib/jenkins/workspace/fsp-deployment-guide'
    def out = sh script: 'sudo /var/lib/jenkins/workspace/fsp-deployment-guide/deploy_prod.sh', returnStdout: false
    notifySuccessfulDeployment()
}