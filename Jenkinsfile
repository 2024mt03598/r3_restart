pipeline {

    agent any


    environment {

        IMAGE_NAME = "docker.io/2024mt03598/backend-app-img"

        IMAGE_TAG = "${BUILD_NUMBER}"

        DEPLOY_IMAGE = "docker.io/2024mt03598/podman-kubectl:latest"

    }


    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }


        stage('Build Podman Image') {

            steps {

                sh '''

                    cd ${WORKSPACE}/backend

                    podman build -t $IMAGE_NAME:$IMAGE_TAG -f Dockerfile .

                '''

            }

        }


        stage('Push to Docker Registry') {

            steps {

                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {

                    sh '''

                        echo "$DOCKER_PASS" | podman login -u "$DOCKER_USER" --password-stdin docker.io

                        podman push $IMAGE_NAME:$IMAGE_TAG

                    '''

                }

            }

        }


        stage('Validate Deploy Image') {

            steps {

                sh '''

                    echo "Checking if deploy image exists..."

                    podman pull docker.io/2024mt03598/podman-kubectl:latest

                '''

            }

        }


        stage('Deploy to Kubernetes') {

            steps {

                withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG')]) {

                    sh '''

                        echo "Running kubectl inside Podman container..."

                        podman run --rm -v /var/lib/jenkins:/var/lib/jenkins -v $KUBECONFIG:$KUBECONFIG docker.io/2024mt03598/podman-kubectl:latest kubectl set image deployment/backend-app-dep backend-app-container=$IMAGE_NAME:$IMAGE_TAG --kubeconfig=$KUBECONFIG                            

                    '''

                }

            }

        }

    }


    post {

        success {

            echo " Deployment completed successfully!"

        }

        failure {

            echo " Pipeline failed. Please check the logs."

        }

    }

}
