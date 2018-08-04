
properties(
  [parameters(
      [string(defaultValue: 'master'
	      , name: 'build_branch'
	      , description: 'Build this branch if it exists'),
       string(defaultValue: '.eros'
	      , name: 'my_dist'
	      , description: 'A dist name for packages'),
      ]
    ),
   pipelineTriggers([])
  ]
)

def buildIt(String name) {
    return {
	try {
	    stage(name) {
		node("mock-build") {
		    checkout([$class: 'GitSCM',
			      branches: [[name: '*/master']],
			      doGenerateSubmoduleConfigurations: false,
			      extensions: [
					   [$class: 'GitLFSPull'],
					   [$class: 'CheckoutOption', timeout: 600],
					   [$class: 'CloneOption',
					    depth: 0,
					    noTags: false,
					    reference: '/devel/git_reference_repos/espa-all',
					    shallow: false,
					    timeout: 120],
					   [$class: 'SubmoduleOption',
					    disableSubmodules: false,
					    parentCredentials: true,
					    recursiveSubmodules: true,
					    reference: '/devel/git_reference_repos/espa-all',
					    trackingSubmodules: true]
					   ],
			      submoduleCfg: [],
			      userRemoteConfigs: [[credentialsId: 'rcattelan-code-usgs-gov',
						   url: 'https://code.usgs.gov/eros-lsds/espa-all.git']
						  ]
			      ])
		    env.my_dist = "${my_dist}.${BUILD_NUMBER}"
		    checkout scm
		    dir('espa-rpmbuild/'+name) {
			sh "rpmbuild --define \"_topdir ${pwd()}\" --define \"dist $my_dist\" -bs SPECS/*.spec"
			sh """sudo mock \
			--verbose \
			--configdir=${WORKSPACE}/mock_config \
			--root my-epel-7-x86_64 \
			--rootdir=${pwd()}/root \
			--define \"dist $my_dist\" \
			--resultdir ${pwd()}/mock_result \
			SRPMS/*.src.rpm"""
		    }
		    dir('espa-rpmbuild/'+name+'/mock_result') {
			//stash name: name, includes: '*.rpm'
			archiveRpms()
		    }
		}
	    }
	} catch(error) {
	    error("Fatal exception while building ${name}")
	    throw error
	}
    }
}

def archiveRpms() {
    try {
	archiveArtifacts artifacts: "**/*.rpm", fingerprint: true
    } catch(e) {
	echo("archiving stuff failed apparently")
	echo(e)
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

parallel par_tasks
