pipeline {

    agent any


    environment {

        IMAGE_NAME = 'docker.io/2024mt03598/backend-app-img'

        IMAGE_TAG = "${env.BUILD_NUMBER}"

    }


    stages {

        stage('Check Branch') {

            when {

                branch 'main'

            }

            steps {

                echo "Branch is main. Proceeding with build and deployment."

            }

        }


        stage('Checkout') {

            when {

                branch 'main'

            }

            steps {

                checkout scm

            }

        }


        stage('Build Docker Image') {

            when {

                branch 'main'

            }

            steps {

                script {

                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."

                }

            }

        }


        stage('Push to Docker Registry') {

            when {

                branch 'main'

            }

            steps {

                script {

                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {

                        sh """

                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                            docker push ${IMAGE_NAME}:${IMAGE_TAG}

                        """

                    }

                }

            }

        }


        stage('Deploy to Kubernetes') {

            when {

                branch 'main'

            }

            steps {

                withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG')]) {

                    sh """

                        kubectl set image deployment/backend-app-dep backend-app-container=${IMAGE_NAME}:${IMAGE_TAG} --kubeconfig=$KUBECONFIG

                    """

                }

            }

        }

    }

}
