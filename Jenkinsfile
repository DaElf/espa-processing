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

def buildIt(String name) {
    return {
	stage(name) {
	    node("mock-build") {
		cleanWs()
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
		    sh "rpmbuild --define \"_topdir ${pwd()}\" --define \"dist $my_dist\" -bs SPECS/*.spec"
		    sh """sudo mock \
			--verbose			    \
			--configdir=${pwd()}/../mock_config \
			--root my-epel-7-x86_64		    \
			--rootdir=${pwd()}/root		    \
			--define \"dist $my_dist\"	    \
			--resultdir ${pwd()}/mock_result    \
			SRPMS/*.src.rpm"""
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
par_tasks["espa-l2qa-tools"] = buildIt("espa-l2qa-tools")
par_tasks["espa-spectral-indices"] = buildIt("espa-spectral-indices")
par_tasks["espa-surface-water-extent"] = buildIt("espa-surface-water-extent")
par_tasks["espa-surface-reflectance"] = buildIt("espa-surface-reflectance")
par_tasks["espa-surface-temperature"] = buildIt("espa-surface-temperature")
par_tasks["espa-elevation"] = buildIt("espa-elevation")
par_tasks["espa-reprojection"] = buildIt("espa-reprojection")
par_tasks["espa-plotting"] = buildIt("espa-plotting")
par_tasks["espa-processing"] = buildIt("espa-processing")
par_tasks["espa-cloud-masking"]  = buildIt("espa-cloud-masking")
par_tasks["watchtower"]  = buildIt("watchtower")

par_tasks["awscli"]  = buildIt("awscli")
par_tasks["python-boto3"]  = buildIt("python-boto3")
par_tasks["python-botocore"]  = buildIt("python-botocore")
par_tasks["python-dateutil"]  = buildIt("python-dateutil")
par_tasks["python-jmespath"]  = buildIt("python-jmespath")
par_tasks["python-s3transfer"]  = buildIt("python-s3transfer")


parallel par_tasks

stage("All done") {
    node {
	sh 'echo "All done"'
    }
}