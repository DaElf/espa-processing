
# This spec file can be used to build an RPM package for installation.
# **NOTE**
#     Version, Release, and tagname information should be updated for the
#     particular release to build an RPM for.


%define project espa-surface-temperature
%define installed_dirname espa-surface-temperature
%define algorithm aux
%define build_timestamp %(date +"%%Y%%m%%d%%H%%M%%S")
# Specify the repository tag/branch to clone and build from
%define tagname dev_1.4
# Specify the name of the directory to clone into
%define clonedname %{name}-%{tagname}
# Change the default rpm name format for the rpm built by this spec file
%define _build_name_fmt %%{NAME}.%%{VERSION}.%%{RELEASE}%{?dist}.%{ARCH}.rpm


# ----------------------------------------------------------------------------
Name:		%{project}-%{algorithm}
Version:	2.0.0
Release:	1.%{build_timestamp}
Summary:	ESPA Surface Temperature Software - Auxiliary

Group:		ESPA
License:	NASA Open Source Agreement
URL:		https://github.com/USGS-EROS/espa-surface-temperature.git

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	x86_64
Packager:	USGS EROS LSRD

# XXX: A little confusing here
Requires:	espa-surface-temperature >= 1.0.9

%description
Provides auxiliary data ingest required for generating surface temperature products for Landsat 4, 5, 7, and 8.  Implemented in Python.


# ----------------------------------------------------------------------------
%prep
# We don't need to perform anything here

%build
# Start with a clean clone of the repo
rm -rf %{clonedname}
git clone --depth 1 --branch %{tagname} %{url} %{clonedname}
# Build the applications
cd %{clonedname}
make all-rit-aux BUILD_STATIC=yes

%install
# Start with a clean installation location
rm -rf %{buildroot}
# Install the applications for a specific path
cd %{clonedname}
make install-rit-aux PREFIX=%{buildroot}/usr/local

%clean
# Cleanup our cloned repository
rm -rf %{clonedname}
# Cleanup our installation location
rm -rf %{buildroot}


# ----------------------------------------------------------------------------
%files
%defattr(-,root,root,-)
# All sub-directories are automatically included
/usr/local/bin/*
/usr/local/%{installed_dirname}/auxiliary


# ----------------------------------------------------------------------------
%changelog
* Fri Feb 15 2019 Sam Gould <sgould@contractor.usgs.gov>
- Version fix for ESPA 2.30.0
* Thu Dec 20 2018 Sam Gould <sgould@contractor.usgs.gov>
- Initial Version for ESPA 2.30.0
* Wed Sep 19 2018 Sam Gould <sgould@contractor.usgs.gov>
- Initial Version for ESPA 2.28.0
* Thu Feb 22 2018 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Initial Version for ESPA 2.27.0
