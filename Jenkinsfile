pipeline {
    agent any

    stages {
        stage('启动数据库和后端') {
            steps {
                sh 'docker compose up -d'
                sh 'sleep 35'
            }
        }

        stage('安装 Laravel 依赖') {
            steps {
                sh 'docker compose exec -T laravel-api composer install --no-interaction --prefer-dist --optimize-autoloader --ignore-platform-reqs'
            }
        }

        stage('执行数据库迁移') {
            steps {
                sh 'docker compose exec -T laravel-api php artisan migrate:fresh --force'
                sh 'docker compose exec -T laravel-api php artisan db:seed --force'
            }
        }

        stage('运行接口自动化测试') {
            steps {
                sh 'python -m pytest tests/ -v --alluredir=allure-results'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }
    }
}