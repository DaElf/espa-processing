properties(
	   [parameters(
		       [string(defaultValue: 'master'
			       , name: 'build_branch'
			       , description: 'Build this branch if it exists'),
			string(defaultValue: '.eros'
			       , name: 'param_dist'
			       , description: 'A dist name for packages'),
			]
		       ),
	    pipelineTriggers([])
	    ]
	   )


def buildIt(String name, Boolean do_unstash) {
    return {
	stage(name) {
	    node("mock-build") {
		dir('local-repo/x86_64/RPMS') {
		    copyArtifacts(projectName: 'cots-rpmbuild')
		    if (do_unstash) {
			unstash 'espa-product-formatter'
			unstash 'espa-python-library'
			unstash 'python-botocore'
			unstash 'python-jmespath'
			unstash 'python-dateutil'
		    }
		}
		dir('local-repo/x86_64') {
		    sh 'createrepo_c .; ls -lR; pwd'
		}
		checkout([$class: 'GitSCM',
			  branches: [[name: '*/master']],
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
			  userRemoteConfigs: [[credentialsId: 'rcattelan-code-usgs-gov',
					       url: 'https://code.usgs.gov/eros-lsds/espa-all.git']
					      ]
			  ])
		env.my_dist = "${param_dist}.${BUILD_NUMBER}"
		dir('espa-rpmbuild/'+name) {
		    sh 'cp ../mock_config/my-epel-7-x86_64.cfg local-mock.cfg'
		    sh "sed -i -e 's#baseurl=http://127.0.0.1:9000.*#baseurl=file://${WORKSPACE}/local-repo/x86_64#g' local-mock.cfg"
		    sh "rpmbuild --define \"_topdir ${pwd()}\" --define \"dist $my_dist\" -bs SPECS/*.spec; \
			      sudo mock					\
			      --verbose					\
			      --no-clean				\
			      --configdir=${pwd()}			\
			      --root local-mock				\
			      --rootdir=${pwd()}/root			\
			      --define \"dist $my_dist\"		\
			      --resultdir ${pwd()}/mock_result		\
			      SRPMS/*.src.rpm"
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
par_tasks["goofys"]  = buildIt("goofys", false)
par_tasks["watchtower"]  = buildIt("watchtower", false)
par_tasks["python-botocore"]  = buildIt("python-botocore", false)
par_tasks["python-jmespath"]  = buildIt("python-jmespath", false)
par_tasks["python-dateutil"]  = buildIt("python-dateutil", false)
par_tasks["python-s3transfer"]  = buildIt("python-s3transfer", false)
par_tasks["awscli"]  = buildIt("awscli", false)
parallel par_tasks

par_tasks = [:]
par_tasks["espa-product-formatter"] = buildIt("espa-product-formatter", false)
parallel par_tasks

par_tasks = [:]
par_tasks["espa-python-library"] = buildIt("espa-python-library", false)
parallel par_tasks

par_tasks = [:]
par_tasks["espa-spectral-indices"] = buildIt("espa-spectral-indices", true)
parallel par_tasks

par_tasks = [:]
par_tasks["python-boto3"]  = buildIt("python-boto3", true)
par_tasks["espa-surface-temperature"] = buildIt("espa-surface-temperature", true)
par_tasks["espa-l2qa-tools"] = buildIt("espa-l2qa-tools", true)
par_tasks["espa-surface-water-extent"] = buildIt("espa-surface-water-extent", true)
par_tasks["espa-surface-reflectance"] = buildIt("espa-surface-reflectance", true)
par_tasks["espa-elevation"] = buildIt("espa-elevation", true)
par_tasks["espa-reprojection"] = buildIt("espa-reprojection", false)
par_tasks["espa-plotting"] = buildIt("espa-plotting", false)
par_tasks["espa-processing"] = buildIt("espa-processing", false)
par_tasks["espa-cloud-masking"]  = buildIt("espa-cloud-masking", false)
parallel par_tasks


stage("All done") {
    node {
	sh 'echo "All done"'
    }
}
