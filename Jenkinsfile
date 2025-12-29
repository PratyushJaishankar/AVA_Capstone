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
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                script {
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
                        @echo off
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

        stage('Detect changed test files') {
            steps {
                script {
                    // Windows-safe detection with guaranteed exit code 0
                    env.TEST_FILES = bat(
                        script: '''
                        @echo off
                        setlocal EnableDelayedExpansion

                        REM Get changed files (safe for first build)
                        git diff --name-status HEAD~1 HEAD > changes.txt 2>nul || git diff --name-status HEAD > changes.txt

                        set FOUND=

                        for /f "usebackq tokens=1,* delims= " %%A in ("changes.txt") do (
                            if "%%A"=="A" set FOUND=1& echo %%B
                            if "%%A"=="M" set FOUND=1& echo %%B
                        ) | findstr /R "^tests\\.*\\.py" | findstr /V "__init__ utils conftest"

                        REM Always exit 0 so Jenkins does not fail
                        exit /b 0
                        ''',
                        returnStdout: true
                    ).trim()

                    if (!env.TEST_FILES) {
                        echo "No new or modified test files detected. Skipping pytest."
                    } else {
                        echo "Tests to execute:"
                        echo env.TEST_FILES
                    }
                }
            }
        }

        stage('Run pytest for detected files') {
            when {
                expression { env.TEST_FILES?.trim() }
            }
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    script {
                        if (isUnix()) {
                            sh """
                            rm -rf ${ALLURE_RESULTS} || true
                            mkdir -p ${ALLURE_RESULTS}
                            pytest -v ${TEST_FILES} --alluredir=${ALLURE_RESULTS}
                            """
                        } else {
                            bat """
                            @echo off
                            if exist %ALLURE_RESULTS% rmdir /s /q %ALLURE_RESULTS%
                            mkdir %ALLURE_RESULTS%

                            pytest -v %TEST_FILES% --alluredir=%ALLURE_RESULTS%
                            """
                        }
                    }
                }
            }
        }

        stage('Archive Allure results') {
            when {
                expression { env.TEST_FILES?.trim() }
            }
            steps {
                archiveArtifacts artifacts: "${ALLURE_RESULTS}/**", allowEmptyArchive: true
            }
        }

        stage('Publish Allure Report') {
            when {
                expression { env.TEST_FILES?.trim() }
            }
            steps {
                allure([
                    results: [[path: "${ALLURE_RESULTS}"]],
                    reportBuildPolicy: 'ALWAYS'
                ])
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
