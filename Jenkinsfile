pipeline {
        agent any
        stages {
                
          stage('Checkout') {
                steps {
                        script {
                // The below will clone your repo and will be checked out to master branch by default.
                git changelog: false, poll: false, url: 'https://github.com/AlionaKlimouskaya/Test-Automation-project.git'
                // Do a ls -lart to view all the files are cloned. It will be clonned. This is just for you to be sure about it.
                sh "ls -lart ./*" 
                // List all branches in your repo. 
                sh "git branch -a"
                    }
                }
            }
          stage('Build') {
                steps {
                    echo 'Start pipeline ...'
               	    sh 'pip install -r requirements.txt'
                    sh 'pip3 install pytest'
                    sh 'export PATH="/var/jenkins_home/.local/bin:$PATH"'
                }
            }
           stage('Tests_pytest') {
              steps {
                  echo 'Execute tests from pytest ...'
               dir ("${WORKSPACE}/pytest") {
               sh 'pytest test_cases.py'}
                }
            }
          stage('Deploy') {
                steps {
                    echo 'Merge feature branch with master ...'
                     sshagent (['ssh-agent']) {
            sh 'git stash'
            sh 'git remote update'
            sh 'git checkout main'
            sh 'git merge origin/feature'
                sh 'git config user.name "AlionaKlimouskaya"'
                sh 'git config user.email "Aliona_Klimouskaya@epam.com"'
               sh 'git remote set-url origin git@github.com:AlionaKlimouskaya/Test-Automation-project.git'
               sh 'git push origin'
                }
            }
         }
     }
  }
