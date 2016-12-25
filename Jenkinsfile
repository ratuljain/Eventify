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

   if(env.BRANCH_NAME == "master"){
     stage('Deploy') {
       echo '####### Deploying Code ##########'
       sh 'sudo su -s /bin/bash deployer'
       echo "My branch is: ${USER}"
       sh 'cd /var/lib/jenkins/workspace/fsp-deployment-guide'
       sh 'sh ./deploy_prod.sh'
     }
   }
}