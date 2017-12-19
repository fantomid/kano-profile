#!/usr/bin/env groovy

@Library('kanolib')
import build_deb_pkg


stage ('Build') {
    autobuild_repo_pkg 'kano-profile'
}


stage ('Test') {
    def dep_repos = [
        "kano-toolset",
        "kano-i18n"
    ]
	python_test_env(dep_repos) { python_path_var ->
    }
}
