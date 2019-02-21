
# This spec file can be used to build an RPM package for installation.
# **NOTE**
#     Version, Release, and tagname information should be updated for the
#     particular release to build an RPM for.


%define project espa-release-info
%define build_timestamp %(date +"%%Y%%m%%d%%H%%M%%S")

# Change the default rpm name format for the rpm built by this spec file
%define _build_name_fmt %%{NAME}.%%{VERSION}.%%{RELEASE}%{?dist}.%{ARCH}.rpm


# ----------------------------------------------------------------------------
Name:		%{project}
Version:	2.30.0
Release:	2.%{build_timestamp}
Summary:	ESPA Release Information

Group:		ESPA
License:	NASA Open Source Agreement
URL:		https://github.com/USGS-EROS/espa-rpms.git

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
Packager:	USGS EROS LSRD

# List of every RPM and what version they should be at
Requires: espa-product-formatter == 1.16.1
Requires: espa-l2qa-tools == 1.7.1
Requires: espa-surface-reflectance == 1.0.13
Requires: espa-surface-reflectance-ledaps == 3.3.1
Requires: espa-surface-reflectance-lasrc == 1.4.0
Requires: espa-surface-temperature == 1.4.0
Requires: espa-surface-temperature-rit == 1.3.0
Requires: espa-spectral-indices == 2.7.0
Requires: espa-surface-water-extent == 1.0.7
Requires: espa-surface-water-extent-cfbwd == 1.1.0
Requires: espa-surface-water-extent-dswe == 2.3.0
Requires: espa-elevation == 2.3.1
Requires: espa-reprojection == 1.0.3
Requires: espa-plotting == 0.1.0

%description
Provides an ESPA release information file to be stored in /etc/espa-release.

# ----------------------------------------------------------------------------
%prep
# We don't need to perform anything here

%build
echo %{version} >espa-release

%install
install -D -m 644 espa-release %{buildroot}/etc/espa-release

%clean
rm -rf %{buildroot}

# ----------------------------------------------------------------------------
%files
%defattr(-,root,root,-)
/etc/espa-release

# ----------------------------------------------------------------------------
%changelog
* Tue Feb 19 2019 Bill Howe <whowe@contractor.usgs.gov>
- Updated espa-surface-temperature requirement to 1.4.0
* Thu Dec 20 2018 Sam Gould <sgould@contractor.usgs.gov>
- Initial Version for ESPA 2.30.0
* Mon Dec 10 2018 Sam Gould <sgould@contractor.usgs.gov>
- RPM restructure for ESPA 2.29.0
* Mon Nov 26 2018 Sam Gould <sgould@contractor.usgs.gov>
- Initial Version for ESPA 2.29.0
