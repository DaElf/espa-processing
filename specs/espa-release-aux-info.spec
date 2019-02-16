
# This spec file can be used to build an RPM package for installation.
# **NOTE**
#     Version, Release, and tagname information should be updated for the
#     particular release to build an RPM for.


%define project espa-release-aux-info
%define build_timestamp %(date +"%%Y%%m%%d%%H%%M%%S")

# Change the default rpm name format for the rpm built by this spec file
%define _build_name_fmt %%{NAME}.%%{VERSION}.%%{RELEASE}%{?dist}.%{ARCH}.rpm


# ----------------------------------------------------------------------------
Name:		%{project}
Version:	2.30.0
Release:	1.%{build_timestamp}
Summary:	ESPA Aux Script Release Information

Group:		ESPA
License:	NASA Open Source Agreement
URL:		https://github.com/USGS-EROS/espa-rpms.git

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
Packager:	USGS EROS LSRD

# List of every RPM and what version they should be at
Requires: espa-surface-reflectance-ledaps-aux == 3.3.0
Requires: espa-surface-reflectance-lasrc-aux == 1.4.1
Requires: espa-surface-temperature-aux == 2.0.0

%description
Provides an ESPA aux script release information file to be stored in /etc/espa-release-aux.

# ----------------------------------------------------------------------------
%prep
# We don't need to perform anything here

%build
echo %{version} >espa-release-aux

%install
install -D -m 644 espa-release-aux %{buildroot}/etc/espa-release-aux

%clean
rm -rf %{buildroot}

# ----------------------------------------------------------------------------
%files
%defattr(-,root,root,-)
/etc/espa-release-aux

# ----------------------------------------------------------------------------
%changelog
* Thu Dec 20 2018 Sam Gould <sgould@contractor.usgs.gov>
- Initial Version for ESPA 2.30.0
* Mon Dec 10 2018 Sam Gould <sgould@contractor.usgs.gov>
- RPM restructure for ESPA 2.29.0
