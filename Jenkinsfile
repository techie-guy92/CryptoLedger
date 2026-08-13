pipeline {
    agent any
    
    environment {
        REGISTRY = '192.168.122.1:5000'
        IMAGE_NAME = 'crypto'
        PROJECT_DIR = 'app/source'
        VALUES_FILE = 'app/chart/values.yaml'
        GITHUB_CREDS = 'github-token'
    }
    
    stages {
        // ============================================================
        // STAGE 1: Lint (Runs on ALL branches)
        // ============================================================
        stage('Lint') {
            agent {
                docker {
                    image "${env.REGISTRY}/python:3.12-slim"
                }
            }
            steps {
                dir('app/source') {
                    sh '''
                        pip install --user black isort
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
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
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
                }
            }
            steps {
                dir('app/source') {
                    sh '''
                        pip install --user -r requirements.txt
                        python manage.py test --settings=config.test_settings
                    '''
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
                }
            }
            steps {
                script {
                    unstash 'image-tag'
                    def imageTag = readFile('image_tag.txt').trim()
                    
                    withCredentials([string(credentialsId: env.GITHUB_CREDS, variable: 'GITHUB_TOKEN')]) {
                        sh """
                            apk add --no-cache git sed openssh-client
                            
                            git config user.email "jenkins@ci.com"
                            git config user.name "Jenkins CI"
                            
                            # ============================================
                            # 1. Update values.yaml on MAIN
                            # ============================================
                            echo "📝 Updating values.yaml on MAIN branch..."
                            sed -i "s/tag: .*/tag: ${imageTag}/" ${env.VALUES_FILE}
                            git add ${env.VALUES_FILE}
                            git commit -m "Update image tag to ${imageTag} [skip ci]"
                            git push origin HEAD:main
                            
                            # ============================================
                            # 2. Update values.yaml on DEVELOP
                            # ============================================
                            echo "📝 Updating values.yaml on DEVELOP branch..."
                            git checkout develop
                            git pull origin develop
                            sed -i "s/tag: .*/tag: ${imageTag}/" ${env.VALUES_FILE}
                            git add ${env.VALUES_FILE}
                            git commit -m "Sync image tag to ${imageTag} from main [skip ci]"
                            git push origin HEAD:develop
                            
                            git checkout main
                            echo "✅ Both branches updated with image tag: ${imageTag}"
                        """
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
                subject: "✅ SUCCESS: ${env.JOB_NAME} - #${env.BUILD_NUMBER}",
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
                subject: "❌ FAILED: ${env.JOB_NAME} - #${env.BUILD_NUMBER}",
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
