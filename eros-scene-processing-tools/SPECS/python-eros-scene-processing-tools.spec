# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-eros-scene-processing-tools
Version:        0.1
Release:        1%{?dist}
Summary:        Tools for submitting AWS batch jobs for the EROS image processing system

License:	NASA Open Source Agreement
URL:            https://code.usgs.gov/eros-level1/eros-scene-processing-tools
Source0:        eros-scene-processing-tools.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:	python2-boto3 >= 1.7
Requires:	espa-processing

%description
%summary


%prep
%setup -q -n eros-scene-processing-tools


%build
%py2_build

%install
rm -rf $RPM_BUILD_ROOT
%py2_install


%files
%doc
%{_bindir}/*
%{python_sitelib}/*


%changelog
