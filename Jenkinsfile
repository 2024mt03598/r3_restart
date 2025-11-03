pipeline {

    agent any


    environment {

        IMAGE_NAME = "docker.io/2024mt03598/backend-app-img"

        IMAGE_TAG = "${BUILD_NUMBER}"

        DEPLOY_IMAGE = "docker.io/2024mt03598/podman-kubectl:latest" // Custom image with Podman + kubectl

    }


    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }


        stage('Build Podman Image') {

            steps {

                sh """

                    cd ${WORKSPACE}/backend

                    podman build -t ${IMAGE_NAME}:${IMAGE_TAG} -f Dockerfile .

                """

            }

        }


        stage('Push to Docker Registry') {

            steps {

                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {

                    sh """

                        echo "$DOCKER_PASS" | podman login -u "$DOCKER_USER" --password-stdin docker.io

                        podman push ${IMAGE_NAME}:${IMAGE_TAG}

                    """

                }

            }

        }


        stage('Deploy to Kubernetes') {

            steps {

                withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG')]) {

                    sh """

                        podman run --rm \

                            -v /var/lib/jenkins:/var/lib/jenkins \

                            -v $KUBECONFIG:$KUBECONFIG \

                            ${DEPLOY_IMAGE} \

                            kubectl set image deployment/backend-app-dep backend-app-container=${IMAGE_NAME}:${IMAGE_TAG} --kubeconfig=$KUBECONFIG

                    """

                }

            }

        }

    }

}
