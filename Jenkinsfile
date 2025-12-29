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
                // We must un-shallow the clone to ensure change detection works reliably
                checkout([
                    $class: 'GitSCM',
                    branches: scm.branches,
                    extensions: [[$class: 'CloneOption', depth: 0, noTags: false, reference: '', shallow: false]],
                    userRemoteConfigs: scm.userRemoteConfigs
                ])
            }
        }

        stage('Test Execution Scope') {
            // This logic determines if the stages inside run or skip
            when {
                anyOf {
                    // Run if any file inside 'tests' folder changes
                    changeset "tests/**"
                    // Also run if dependencies change
                    changeset "requirements.txt"
                    // IMPORTANT: Always run if a Human manually triggers the build
                    triggeredBy 'UserIdCause' 
                }
            }
            stages {
                stage('Install dependencies') {
                    steps {
                        script {
                            echo "Changes detected in tests/ or requirements.txt. Installing dependencies..."
                            if (isUnix()) {
                                sh '''
                                python3 -m pip install --upgrade pip
                                if [ -f requirements.txt ]; then pip3 install -r requirements.txt; else pip3 install pytest allure-pytest; fi
                                '''
                            } else {
                                bat '''
                                python -m pip install --upgrade pip
                                if exist requirements.txt ( pip install -r requirements.txt ) else ( pip install pytest allure-pytest )
                                '''
                            }
                        }
                    }
                }

                stage('Run All Tests') {
                    steps {
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

                stage('Publish Allure Report') {
                    steps {
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
            cleanWs()
        }
    }
}
