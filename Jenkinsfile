// ============================================================
// CryptoLedger — Jenkins pipeline (multibranch)
//
// Every branch/PR : lint + unit tests + build image
// develop only    : push image, bump app/chart/values.yaml, ArgoCD syncs
//
// Runs on the Jenkins host as the `jenkins` user (same as OpsBoon).
// Needs: python3-venv, docker CLI (jenkins in `docker` group), git.
// Credentials used: github-ssh (write access to the repo) — nothing else.
// Tests need NO credentials: config.settings.test supplies dummy values.
// ============================================================

pipeline {
    agent any

    environment {
        REGISTRY     = '192.168.122.1:5000'
        IMAGE_NAME   = 'crypto'
        PROJECT_DIR  = 'app/source'
        VALUES_FILE  = 'app/chart/values.yaml'
        BRANCH       = 'develop'
        GITHUB_CREDS = 'github-ssh'
        GITHUB_REPO  = 'techie-guy92/CryptoLedger'
        // v1.4.x on purpose: old v1.3.x tags exist from main builds, and
        // develop's build counter would collide with them.
        IMAGE_TAG    = "v1.4.${BUILD_NUMBER}"
        // pip picks these up automatically (regional PyPI mirror + fallback)
        PIP_INDEX_URL       = 'https://mirror-pypi.runflare.com/simple/'
        PIP_EXTRA_INDEX_URL = 'https://pypi.org/simple/'
        PATH         = '/usr/local/bin:/usr/bin:/bin'
    }

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }

    // No triggers{}: set "Scan Multibranch Pipeline Triggers" or a webhook on the job.

    stages {

        // Skip the whole run when the latest commit is our own manifest bump
        // (checks only HEAD, so real commits pushed alongside a bump still build)
        stage('CI') {
            when {
                not {
                    expression {
                        return sh(script: 'git log -1 --pretty=%B', returnStdout: true).contains('[skip ci]')
                    }
                }
            }

            stages {

                stage('Lint') {
                    steps {
                        sh '''
                            python3 -m venv .venv-ci
                            . .venv-ci/bin/activate
                            pip install -q black isort
                            cd "$PROJECT_DIR"
                            black --check .
                            isort --profile black --check-only .
                        '''
                    }
                }

                stage('Unit Tests') {
                    steps {
                        sh '''
                            . .venv-ci/bin/activate
                            pip install -q -r "$PROJECT_DIR/requirements.txt"
                            cd "$PROJECT_DIR"
                            python manage.py test --settings=config.settings.test
                        '''
                    }
                }

                stage('Build Image') {
                    steps {
                        sh '''
                            docker build \
                                -t $REGISTRY/$IMAGE_NAME:$IMAGE_TAG \
                                -t $REGISTRY/$IMAGE_NAME:latest \
                                -f $PROJECT_DIR/Dockerfile $PROJECT_DIR
                        '''
                    }
                }

                stage('Push Image') {
                    when { branch 'develop' }
                    steps {
                        sh '''
                            docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                            docker push $REGISTRY/$IMAGE_NAME:latest
                        '''
                    }
                }

                stage('Update Manifests') {
                    when { branch 'develop' }
                    steps {
                        withCredentials([sshUserPrivateKey(
                            credentialsId: env.GITHUB_CREDS,
                            keyFileVariable: 'SSH_KEY'
                        )]) {
                            // single-quoted on purpose: the shell expands vars, Groovy never sees the key path
                            sh '''
                                set -e
                                export GIT_SSH_COMMAND='ssh -i "$SSH_KEY" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new'

                                # Fresh clone avoids workspace staleness
                                WORK=/tmp/bump-cryptoledger-$BUILD_NUMBER
                                rm -rf "$WORK"
                                git clone --branch "$BRANCH" "git@github.com:${GITHUB_REPO}.git" "$WORK"
                                cd "$WORK"
                                git config user.email "jenkins@ci.com"
                                git config user.name "Jenkins CI"

                                # only touches the `tag:` line(s); formatting and comments stay intact
                                sed -i -E "s/^( *tag: ).*/\\1${IMAGE_TAG}/" "$VALUES_FILE"

                                git add "$VALUES_FILE"
                                if git diff --cached --quiet; then
                                    echo "No manifest changes."
                                else
                                    git commit -m "ci: bump image tag to $IMAGE_TAG [skip ci]"
                                    git push origin "$BRANCH"
                                    echo "Pushed image tag $IMAGE_TAG to $BRANCH"
                                fi

                                cd /
                                rm -rf "$WORK"
                            '''
                        }
                    }
                }
            }
        }
    }

    // ===============================================================
    // POST-BUILD ACTIONS: cleanup and email notifications
    // ===============================================================
    post {
        always {
            sh '''
                docker rmi $REGISTRY/$IMAGE_NAME:$IMAGE_TAG 2>/dev/null || true
                docker rmi $REGISTRY/$IMAGE_NAME:latest     2>/dev/null || true
            '''
        }
        success {
            mail (
                to: 'soheil.dalirii@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} - #${env.BUILD_NUMBER}",
                body: """
                    Build Successful!
                    Job: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Branch: ${env.BRANCH_NAME}
                    URL: ${env.BUILD_URL}
                """
            )
        }
        failure {
            mail (
                to: 'soheil.dalirii@gmail.com',
                subject: "FAILED: ${env.JOB_NAME} - #${env.BUILD_NUMBER}",
                body: """
                    Build Failed!
                    Job: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Branch: ${env.BRANCH_NAME}
                    URL: ${env.BUILD_URL}
                    Please check the logs for details.
                """
            )
        }
    }
}
