pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        ALLURE_RESULTS = 'allure-results'
    }

    stages {

        stage('Checkout') {
            steps {
                // Un-shallow clone to make changeset detection reliable
                checkout([
                    $class: 'GitSCM',
                    branches: scm.branches,
                    extensions: [
                        [$class: 'CloneOption', depth: 0, noTags: false, reference: '', shallow: false]
                    ],
                    userRemoteConfigs: scm.userRemoteConfigs
                ])
            }
        }

        stage('Test Execution Scope') {
            when {
                anyOf {
                    changeset "tests/**"
                    changeset "requirements.txt"
                    triggeredBy 'UserIdCause'
                }
            }

            stages {

                stage('Install dependencies') {
                    steps {
                        script {
                            echo "Installing dependencies..."
                            if (isUnix()) {
                                sh '''
                                python3 -m pip install --upgrade pip
                                if [ -f requirements.txt ]; then
                                    pip3 install -r requirements.txt
                                else
                                    pip3 install pytest allure-pytest
                                fi
                                '''
                            } else {
                                bat '''
                                python -m pip install --upgrade pip
                                if exist requirements.txt (
                                    pip install -r requirements.txt
                                ) else (
                                    pip install pytest allure-pytest
                                )
                                '''
                            }
                        }
                    }
                }

                stage('Run All Tests') {
                    steps {
                        // IMPORTANT: prevents pipeline from stopping on test failure
                        catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                            script {
                                echo "Running test suite..."
                                if (isUnix()) {
                                    sh """
                                    rm -rf ${ALLURE_RESULTS} || true
                                    mkdir -p ${ALLURE_RESULTS}
                                    pytest -v tests/ --alluredir=${ALLURE_RESULTS}
                                    """
                                } else {
                                    bat """
                                    if exist %ALLURE_RESULTS% rmdir /s /q %ALLURE_RESULTS%
                                    mkdir %ALLURE_RESULTS%
                                    pytest -v tests/ --alluredir=%ALLURE_RESULTS%
                                    """
                                }
                            }
                        }
                    }
                }

                stage('Publish Allure Report') {
                    steps {
                        echo "Publishing Allure Report..."
                        allure([
                            results: [[path: "${ALLURE_RESULTS}"]],
                            reportBuildPolicy: 'ALWAYS'
                        ])
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
    }
}
