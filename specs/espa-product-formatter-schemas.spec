
# This spec file can be used to build an RPM package for installation.
# **NOTE**
#     Version, Release, and tagname information should be updated for the
#     particular release to build an RPM for.

%define project espa-product-formatter
%define algorithm schemas
%define build_timestamp %(date +"%%Y%%m%%d%%H%%M%%S")
# Specify the repository tag/branch to clone and build from
%define tagname product_formatter_v1.16.0
# Specify the name of the directory to clone into
%define clonedname %{name}-%{tagname}
# Change the default rpm name format for the rpm built by this spec file
%define _build_name_fmt %%{NAME}.%%{VERSION}.%%{RELEASE}%{?dist}.%{ARCH}.rpm

# ----------------------------------------------------------------------------
Name:		%{project}-%{algorithm}
# This version represents the schema version, and not the
# espa-product-formatter version.
Version:	2.0.0
Release:	7.%{build_timestamp}
Summary:	ESPA Metadata Schemas

Group:		ESPA
License:	NASA Open Source Agreement
URL:		https://github.com/USGS-EROS/espa-product-formatter.git

BuildRoot:	%(mktemp -ud %{_tmppath}/${name}-%{version}-%{release}-XXXXXX)
BuildArch:	x86_64
Packager:	USGS EROS LSRD

%description
Provides the schemas used by ESPA processing.


# ----------------------------------------------------------------------------
%prep
# We don't need to perform anything here

%build
# Start with a clean clone of the repo
rm -rf %{clonedname}
git clone --depth 1 --branch %{tagname} %{url} %{clonedname}
# Nothing to build for the schemas

%install
# Start with a clean installation location
rm -rf %{buildroot}
# Install the applications for a specific path
cd %{clonedname}
make install-schema PREFIX=%{buildroot}/usr/local

%clean
# Cleanup our cloned repository
rm -rf %{clonedname}
# Cleanup our installation location
rm -rf %{buildroot}


# ----------------------------------------------------------------------------
%files
%defattr(-,root,root,-)
# All sub-directories are automatically included
/usr/local/schema/*
/usr/local/espa-product-formatter/schema


# ----------------------------------------------------------------------------
%changelog
* Wed Sep 19 2018 Sam Gould <sgould@contractor.usgs.gov>
- Rebuild Version for ESPA 2.28.0
* Thu Feb 22 2018 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Rebuild Version for ESPA 2.27.0
* Mon Nov 6 2017 Jake Brinkmann <jacob.brinkmann.ctr@usgs.gov>
- Rebuild Version for ESPA 2.25.0
* Wed May 24 2017 Ronald D Dilley <ronald.dilley.ctr@usgs.gov>
- Initial Version for ESPA 2.19.0
