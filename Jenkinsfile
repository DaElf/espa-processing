
properties(
  [parameters(
      [string(defaultValue: 'master'
              , name: 'build_branch'
              , description: 'Build this branch if it exists'),
       string(defaultValue: '9000.1.0'
              , name: 'force_rpm_version'
              , description: 'Version to force built rpms to be, its over 9000.'),
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
	      env.my_dist = "${force_rpm_version}"
	      git branch: "JenkinsBuild", credentialsId: 'rcattelan-code-usgs-gov', url: 'https://code.usgs.gov/eros-lsds/espa-rpmbuild.git'
	      dir(name) {
		      sh "rpmbuild --define \"_topdir ${pwd()}\" --define \"dist $my_dist\" -bs SPECS/*.spec"
		      sh "sudo my_dist=Test0 mock --configdir=${WORKSPACE}/mock_config -r my-epel-7-x86_64 \
                        --rootdir=${pwd()}/root \
                        --define \"dist $my_dist\" -r my-epel-7-x86_64 --resultdir ${pwd()}/mock_result SRPMS/*.src.rpm"
	      }
      }
    }
    } catch(error) {
	    error("Fatal exception while building ${name}")
	    throw error
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

parallel par_tasks
