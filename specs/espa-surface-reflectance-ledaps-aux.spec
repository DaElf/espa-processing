
# This spec file can be used to build an RPM package for installation.
# **NOTE**
#     Version, Release, and tagname information should be updated for the
#     particular release to build an RPM for.


%define project espa-surface-reflectance
%define bin_location ledaps
%define algorithm ledaps-aux
%define build_timestamp %(date +"%%Y%%m%%d%%H%%M%%S")
# Specify the repository tag/branch to clone and build from
%define tagname dev_lasrc_opt_minsu
# Specify the name of the directory to clone into
%define clonedname %{name}-%{tagname}
# Change the default rpm name format for the rpm built by this spec file
%define _build_name_fmt %%{NAME}.%%{VERSION}.%%{RELEASE}%{?dist}.%{ARCH}.rpm

# ----------------------------------------------------------------------------
Name:		%{project}-%{algorithm}
Version:	3.2.1
Release:	2.%{build_timestamp}
Summary:	ESPA Surface Reflectance Software - Ledaps - Auxiliary

Group:		ESPA
License:	NASA Open Source Agreement
URL:		https://github.com/USGS-EROS/espa-surface-reflectance.git

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	x86_64
Packager:	USGS EROS LSRD

BuildRequires:	espa-product-formatter >= 1.13.1
Requires:	espa-surface-reflectance >= 1.0.10

%description
Provides software to update and archive auxiliary input to LaSRC processing.


# ----------------------------------------------------------------------------
%prep
# We don't need to perform anything here

%build
# Start with a clean clone of the repo
rm -rf %{clonedname}
git clone --depth 1 --branch %{tagname} %{url} %{clonedname}
# Build the applications
cd %{clonedname}
make all-ledaps-aux BUILD_STATIC=yes ENABLE_THREADING=yes

%install
# Start with a clean installation location
rm -rf %{buildroot}
# Install the applications for a specific path
cd %{clonedname}
make install-ledaps-aux PREFIX=%{buildroot}/usr/local

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
/usr/local/%{project}/%{bin_location}/bin/*


# ----------------------------------------------------------------------------
%changelog
* Wed Sep 6 2017 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Rebuild Version for ESPA 2.23.0
* Wed Aug 2 2017 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Initial Version for ESPA 2.22.0
