node {
   def mvnHome
   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      sh 'sudo su -s /bin/bash jenkins'
      sh 'whoami'
      git 'https://github.com/ratuljain1991/Eventify.git'
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