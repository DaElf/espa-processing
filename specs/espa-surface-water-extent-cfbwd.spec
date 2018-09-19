
# This spec file can be used to build an RPM package for installation.
# **NOTE**
#     Version, Release, and tagname information should be updated for the
#     particular release to build an RPM for.


%define project espa-surface-water-extent
%define algorithm cfbwd
%define build_timestamp %(date +"%%Y%%m%%d%%H%%M%%S")
# Specify the repository tag/branch to clone and build from
%define tagname cfbwd-v1.1.1
# Specify the name of the directory to clone into
%define clonedname %{name}-%{tagname}
# Change the default rpm name format for the rpm built by this spec file
%define _build_name_fmt %%{NAME}.%%{VERSION}.%%{RELEASE}%{?dist}.%{ARCH}.rpm


# ----------------------------------------------------------------------------
Name:		%{project}-%{algorithm}
Version:	1.1.0
Release:	8.%{build_timestamp}
Summary:	ESPA Surface Water Extent Software - CFBWD

Group:		ESPA
License:	NASA Open Source Agreement
URL:		https://github.com/USGS-EROS/espa-surface-water-extent.git

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	x86_64
Packager:	USGS EROS LSRD

BuildRequires:	espa-product-formatter >= 1.15.0
Requires:	espa-surface-water-extent >= 1.0.7

%description
Provides science application executables for generating surface water extent products based on CFmask water detection for Landsat 4, 5, 7, and 8.  This application is implementated in C.


# ----------------------------------------------------------------------------
%prep
# We don't need to perform anything here

%build
# Start with a clean clone of the repo
rm -rf %{clonedname}
git clone --depth 1 --branch %{tagname} %{url} %{clonedname}
# Build the applications
cd %{clonedname}
make all-cfbwd BUILD_STATIC=yes ENABLE_THREADING=yes

%install
# Start with a clean installation location
rm -rf %{buildroot}
# Install the applications for a specific path
cd %{clonedname}
make install-cfbwd PREFIX=%{buildroot}/usr/local

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
/usr/local/%{project}/cfmask-based-water-detection


# ----------------------------------------------------------------------------
%changelog
* Wed Sep 19 2018 Sam Gould <sgould@contractor.usgs.gov>
- Initial Version for ESPA 2.28.0
* Thu Feb 22 2018 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Rebuild Version for ESPA 2.27.0
* Mon Nov 6 2017 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Rebuild Version for ESPA 2.25.0
* Thu Sep 21 2017 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Rebuild Version for ESPA 2.24.0
* Wed Aug 2 2017 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Rebuild Version for ESPA 2.22.0
* Wed May 24 2017 Ronald D Dilley <ronald.dilley.ctr@usgs.gov>
- Initial Version for ESPA 2.19.0
