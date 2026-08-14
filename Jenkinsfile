pipeline {
    agent any
    
    environment {
        REGISTRY = '192.168.122.1:5000'
        IMAGE_NAME = 'crypto'
        PROJECT_DIR = 'app/source'
        VALUES_FILE = 'app/chart/values.yaml'
        GITHUB_CREDS = 'github-token'
        HOME = '/tmp'
        PATH = '/tmp/.local/bin:/usr/local/bin:/usr/bin:/bin'
    }
    
    stages {
        // ============================================================
        // STAGE 1: Lint (Runs on ALL branches)
        // ============================================================
        stage('Lint') {
            agent {
                docker {
                    image "${env.REGISTRY}/python:3.12-slim"
                    args '--network host -u root'
                }
            }
            steps {
                dir('app/source') {
                    sh '''
                        export PATH="/tmp/.local/bin:$PATH"
                        pip install --break-system-packages black isort
                        black --check .
                        isort --profile black --check-only .
                    '''
                }
            }
        }
        
        // ============================================================
        // STAGE 2: Build & Push Docker (ONLY on main branch)
        // ============================================================
        stage('Build & Push Docker') {
            when {
                branch 'main'
            }
            agent {
                docker {
                    image "${env.REGISTRY}/docker:latest"
                    args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
                }
            }
            steps {
                script {
                    def imageTag = "v1.3.${env.BUILD_NUMBER}"
                    def fullImage = "${env.REGISTRY}/${env.IMAGE_NAME}:${imageTag}"
                    
                    sh """
                        docker build -t ${fullImage} -f ${env.PROJECT_DIR}/Dockerfile ${env.PROJECT_DIR}
                        docker tag ${fullImage} ${env.REGISTRY}/${env.IMAGE_NAME}:latest
                        docker push ${fullImage}
                        docker push ${env.REGISTRY}/${env.IMAGE_NAME}:latest
                    """
                    
                    writeFile file: 'image_tag.txt', text: imageTag
                    stash name: 'image-tag', includes: 'image_tag.txt'
                }
            }
        }
        
        // ============================================================
        // STAGE 3: Unit Tests (Runs on ALL branches)
        // ============================================================
        stage('Unit Tests') {
            agent {
                docker {
                    image "${env.REGISTRY}/python:3.12-slim"
                    args '--network host -u root'
                }
            }
            steps {
                withCredentials([
                    // Django Core
                    string(credentialsId: 'crypto-secret-key', variable: 'SECRET_KEY'),
                    string(credentialsId: 'DEBUG', variable: 'DEBUG'),
                    string(credentialsId: 'ALLOWED_HOSTS', variable: 'ALLOWED_HOSTS'),
                    string(credentialsId: 'FRONTEND_DOMAIN', variable: 'FRONTEND_DOMAIN'),
                    
                    // Security Settings
                    string(credentialsId: 'SECURE_SSL_REDIRECT', variable: 'SECURE_SSL_REDIRECT'),
                    string(credentialsId: 'SESSION_COOKIE_SECURE', variable: 'SESSION_COOKIE_SECURE'),
                    string(credentialsId: 'CSRF_COOKIE_SECURE', variable: 'CSRF_COOKIE_SECURE'),
                    string(credentialsId: 'SECURE_HSTS_SECONDS', variable: 'SECURE_HSTS_SECONDS'),
                    string(credentialsId: 'SECURE_HSTS_INCLUDE_SUBDOMAINS', variable: 'SECURE_HSTS_INCLUDE_SUBDOMAINS'),
                    string(credentialsId: 'SECURE_HSTS_PRELOAD', variable: 'SECURE_HSTS_PRELOAD'),
                    string(credentialsId: 'USE_X_FORWARDED_HOST', variable: 'USE_X_FORWARDED_HOST'),
                    string(credentialsId: 'USE_X_FORWARDED_PORT', variable: 'USE_X_FORWARDED_PORT'),
                    string(credentialsId: 'SECURE_PROXY_SSL_HEADER', variable: 'SECURE_PROXY_SSL_HEADER'),
                    
                    // Email Settings
                    string(credentialsId: 'EMAIL_HOST', variable: 'EMAIL_HOST'),
                    string(credentialsId: 'EMAIL_PORT', variable: 'EMAIL_PORT'),
                    string(credentialsId: 'EMAIL_HOST_USER', variable: 'EMAIL_HOST_USER'),
                    string(credentialsId: 'EMAIL_HOST_PASSWORD', variable: 'EMAIL_HOST_PASSWORD'),
                    string(credentialsId: 'EMAIL_USE_TLS', variable: 'EMAIL_USE_TLS'),
                    
                    // JWT Settings
                    string(credentialsId: 'ACCESS_TOKEN', variable: 'ACCESS_TOKEN'),
                    string(credentialsId: 'REFRESH_TOKEN', variable: 'REFRESH_TOKEN'),
                    string(credentialsId: 'ROTATE_REFRESH_TOKENS', variable: 'ROTATE_REFRESH_TOKENS'),
                    string(credentialsId: 'BLACKLIST_AFTER_ROTATION', variable: 'BLACKLIST_AFTER_ROTATION'),
                    
                    // Database Settings
                    string(credentialsId: 'ENGINE_NAME', variable: 'ENGINE_NAME'),
                    string(credentialsId: 'DB_NAME', variable: 'DB_NAME')
                ]) {
                    dir('app/source') {
                        sh '''
                            export PATH="/tmp/.local/bin:$PATH"
                            pip install --break-system-packages -r requirements.txt
                            python manage.py test --settings=config.test_settings
                        '''
                    }
                }
            }
        }
        
        // ============================================================
        // STAGE 4: Update Manifests (ONLY on main branch)
        // ============================================================
        stage('Update Manifests') {
            when {
                branch 'main'
            }
            agent {
                docker {
                    image "${env.REGISTRY}/alpine:latest"
                    args '-u root'
                }
            }
            steps {
                    script {
                        dir(env.WORKSPACE) {
                            checkout scm
                            unstash 'image-tag'
                            def imageTag = readFile('image_tag.txt').trim()

                            withCredentials([string(credentialsId: env.GITHUB_CREDS, variable: 'GIT_TOKEN')]) {

                            sh """
                                apk add --no-cache git sed openssh-client

                                git config --global --add safe.directory '*'
                                git config --global user.email "jenkins@ci.com"
                                git config --global user.name "Jenkins CI"

                                git remote set-url origin https://\${GIT_USER}:\${GIT_TOKEN}@github.com/techie-guy92/CryptoLedger.git

                                echo "PWD: \$(pwd)"
                                ls -la

                                echo "Updating values.yaml on MAIN branch..."
                                git pull origin main
                                sed -i "s/tag: .*/tag: ${imageTag}/" ${env.VALUES_FILE}
                                git add ${env.VALUES_FILE}
                                git commit -m "Update image tag to ${imageTag} [skip ci]"
                                git push origin HEAD:main
                                
                                echo "Updating values.yaml on DEVELOP branch..."
                                git checkout develop
                                git pull origin develop
                                sed -i "s/tag: .*/tag: ${imageTag}/" ${env.VALUES_FILE}
                                git add ${env.VALUES_FILE}
                                git commit -m "Sync image tag to ${imageTag} from main [skip ci]"
                                git push origin HEAD:develop
                                
                                git checkout main
                                echo "Both branches updated with image tag: ${imageTag}"
                            """
                        }
                    }
                }
            }
        }
    }
    // ============================================================
    // POST-BUILD ACTIONS: Email Notifications
    // ============================================================
    post {
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
