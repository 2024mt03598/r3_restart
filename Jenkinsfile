pipeline {

    agent any


    environment {

        IMAGE_NAME = "docker.io/2024mt03598/backend-app-img"

        IMAGE_TAG = "${BUILD_NUMBER}"

    }


    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }


        stage('Build Podman Image') {

            steps {

                script {

                    sh """

                        cd ${WORKSPACE}/backend

                        podman build -t ${IMAGE_NAME}:${IMAGE_TAG} -f Dockerfile .

                    """

                }

            }

        }


        stage('Push to Docker Registry') {

            steps {

                script {

                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {

                        sh """

                            echo "$DOCKER_PASS" | podman login -u "$DOCKER_USER" --password-stdin docker.io

                            podman push ${IMAGE_NAME}:${IMAGE_TAG}

                        """

                    }

                }

            }

        }


        stage('Deploy to Kubernetes') {

            steps {

                script {

                    // Use a Docker container with kubectl installed

                    docker.image('bitnami/kubectl:latest').inside('-v /var/lib/jenkins:/var/lib/jenkins') {

                        withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG')]) {

                            sh '''

                                kubectl set image deployment/backend-app-dep backend-app-container=$IMAGE_NAME:$IMAGE_TAG --kubeconfig=$KUBECONFIG

                            '''

                        }

                    }

                }

            }

        }

    }

}
