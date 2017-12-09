#!/usr/bin/env groovy

@Library('kanolib')
import build_deb_pkg


stage ('Build') {
    autobuild_repo_pkg 'kano-profile'
}


stage ('Test') {
    node ('os') {
        docker.image('python:2.7-jessie').inside('--user root') {
            sh 'apt-get install -y make'

            // Install pip dependencies
            checkout scm
            sh 'pip install --requirement requirements.txt'
            sh 'pip install --requirement requirements-dev.txt'

            // Download repo dependencies
            repo_path = '/repos'

            def dep_repos = [
                "kano-toolset",
                "kano-i18n"
            ]
            def python_path_var = 'PYTHONPATH=\$PYTHONPATH'

            dep_repos.each { repo ->
                def repo_path = "$repo_path/$repo"
                sh "git clone https://www.github.com/KanoComputing/${repo}.git $repo_path"
                python_path_var = "$python_path_var:$repo_path"
            }

            // Run tests
            sh "$python_path_var make check OMITTED_TAGS=gtk"

            // Publish tests report
            junit(
                allowEmptyResults: true,
                healthScaleFactor: 0.0,
                testResults: 'reports/tests/*.xml'
            )

            // Publish coverage report
            cobertura(
                coberturaReportFile: 'reports/coverage/*.xml',
                conditionalCoverageTargets: '70, 0, 0',
                lineCoverageTargets: '80, 0, 0',
                methodCoverageTargets: '80, 0, 0',
                failUnhealthy: false,
                failUnstable: false,
                autoUpdateHealth: false,
                autoUpdateStability: false,
                maxNumberOfBuilds: 0,
                onlyStable: false,
                sourceEncoding: 'ASCII',
                zoomCoverageChart: false
            )
            archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/coverage/html/*'
        }
    }
}
