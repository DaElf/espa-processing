# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-watchtower
Version:      	0.5.3  
Release:        1%{?dist}
Summary:        Watchtower is a log handler for Amazon Web Services CloudWatch Logs.

License:       Apache
URL:           https://github.com/kislyuk/watchtower 
Source0:        watchtower.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python2-setuptools

%description
Watchtower is a log handler for Amazon Web Services CloudWatch Logs.

CloudWatch Logs is a log management service built into AWS.
It is conceptually similar to services like Splunk and Loggly,
but is more lightweight, cheaper, and tightly integrated with the rest of AWS.

Watchtower, in turn, is a lightweight adapter between the Python logging system
and CloudWatch Logs. It uses the boto3 AWS SDK, and lets you plug your application
logging directly into CloudWatch without the need to install a system-wide log
collector like awscli-cwlogs and round-trip your logs through the instance's syslog.
It aggregates logs into batches to avoid sending an API request per each log message,
while guaranteeing a delivery deadline (60 seconds by default).


%prep
%setup -q -n watchtower


%build
%{py2_build}


%install
rm -rf $RPM_BUILD_ROOT
%{py2_install}

 
%files
%doc
# For noarch packages: sitelib
%{python2_sitelib}/*


%changelog
