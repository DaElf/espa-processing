properties(
	   [parameters(
		       [string(defaultValue: 'cloud-master'
			       , name: 'build_branch'
			       , description: 'This is not currently connected -- Build this branch if it exists'),
			string(defaultValue: '.eros'
			       , name: 'param_dist'
			       , description: 'A dist name for packages'),
			]
		       ),
	    pipelineTriggers([])
	    ]
	   )


def buildIt(String name, def unstash_list = []) {
    return {
	stage(name) {
	    node("mock-build") {

		checkout([$class: 'GitSCM',
			  branches: [[name: '*/*']],
			  extensions: [
				       [$class: 'GitLFSPull'],
				       [$class: 'CheckoutOption', timeout: 600],
				       [$class: 'CloneOption',
					depth: 0,
					noTags: false,
					reference: '',
					shallow: false,
					timeout: 120],
				       [$class: 'SubmoduleOption',
					disableSubmodules: false,
					parentCredentials: true,
					recursiveSubmodules: false,
					reference: '',
					trackingSubmodules: true,
					timeout: 120]
				       ],
			  submoduleCfg: [],
			  userRemoteConfigs: [[credentialsId: 'gitlab-code.usgs',
					       url: 'https://code.usgs.gov/eros-lsds/espa-all.git']
					      ]
			  ])
		dir('local-repo/RPMS') {
			copyArtifacts(projectName: 'eros-support-rpmbuild')
			if (!unstash_list.isEmpty()) {
				unstash_list.each { item ->
					unstash name: item
				}
			}
		}
		dir('local-repo') {
		    sh '''
			createrepo_c .
			ls -lR
			'''
		}
		env.my_dist = "${param_dist}.${BUILD_NUMBER}"
		dir(name) {
		    sh 'rm -f '  + env.WORKSPACE + '/espa-rpmbuild/'+ name + '/SOURCES/' + name + '.tar.gz'
		    sh 'mkdir -p ' + env.WORKSPACE + '/espa-rpmbuild/'+ name + '/SOURCES/'
		    sh 'git branch -a; git archive --format=tar.gz -o ' + env.WORKSPACE + '/espa-rpmbuild/'+ name + '/SOURCES/' + name + '.tar.gz --prefix=' + name +'/ HEAD'
		}
		dir('espa-rpmbuild/'+name) {
		    sh """
			cp ../mock_config/my-epel-7-x86_64.cfg local-mock.cfg
			sed -i -e 's#baseurl=http://127.0.0.1:9000.*#baseurl=file://${env.WORKSPACE}/local-repo#g' local-mock.cfg
			rpmbuild --define \"_topdir ${pwd()}\" --define \"dist $my_dist\" -bs SPECS/*.spec
			sudo mock			 \
			--verbose			 \
			--configdir=${pwd()}		 \
			--root local-mock		 \
			--rootdir=${pwd()}/root		 \
			--define \"dist $my_dist\"	 \
			--resultdir ${pwd()}/mock_result \
			SRPMS/*.src.rpm
			"""
		}
		dir('espa-rpmbuild/'+name+'/mock_result') {
		    stash name: name, includes: '*.rpm'
		    archiveArtifacts artifacts: "**/*.rpm", fingerprint: true
		}
	    }
	}
    }
}

par_tasks = [:]
par_tasks["espa-product-formatter"] = buildIt("espa-product-formatter")
par_tasks["espa-python-library"] = buildIt("espa-python-library")
par_tasks["espa-reprojection"] = buildIt("espa-reprojection")
par_tasks["espa-plotting"] = buildIt("espa-plotting")
par_tasks["espa-processing"] = buildIt("espa-processing")
par_tasks["eros-scene-processing-tools"]  = buildIt("eros-scene-processing-tools")
parallel par_tasks

par_tasks = [:]
par_tasks["espa-surface-temperature"] = buildIt("espa-surface-temperature", ['espa-product-formatter'])
par_tasks["espa-spectral-indices"] = buildIt("espa-spectral-indices", ['espa-product-formatter'])
par_tasks["espa-l2qa-tools"] = buildIt("espa-l2qa-tools", ['espa-product-formatter'])
par_tasks["espa-surface-water-extent"] = buildIt("espa-surface-water-extent", ['espa-product-formatter'])
par_tasks["espa-surface-reflectance"] = buildIt("espa-surface-reflectance", ['espa-product-formatter'])
par_tasks["espa-elevation"] = buildIt("espa-elevation", ['espa-python-library'])
par_tasks["espa-cloud-masking"]  = buildIt("espa-cloud-masking", ['espa-product-formatter'])
parallel par_tasks


stage("All done") {
    node {
	sh 'echo "All done"'
    }
}
