node {
   def mvnHome
   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      sh 'sudo su -s /bin/bash jenkins'
      echo "My branch is: ${env.BRANCH_NAME}"
      if(env.BRANCH_NAME == "master"){
        echo "My branch is master"
      }
      checkout scm
      sh 'cd /var/lib/jenkins/workspace/Eventify_pipeline'
      sh 'virtualenv -q venv'
      sh '. venv/bin/activate'
      sh 'pip install -r requirements.txt --user'
      sh 'python manage.py makemigrations'
      sh 'python manage.py migrate'
    //   sh 'pip install -r requirements.txt'
    //   sh 'python manage.py migrate'

   }
   stage('Build') {
      sh 'echo oops'
   }
   stage('Results') {
       sh 'pwd'
   }
}