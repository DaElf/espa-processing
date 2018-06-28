Name:           espa-processing
Version:        2.27.1
Release:        1%{?dist}
Summary:	ESPA processing

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-processing
Source0:        espa-processing.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires:       espa-elevation
Requires:       espa-l2qa-tools
Requires:       espa-plotting
Requires:       espa-processing
Requires:       espa-product-formatter
Requires:       espa-reprojection
Requires:       espa-spectral-indices
Requires:       espa-surface-reflectance
Requires:       espa-surface-temperature
Requires:       espa-surface-water-extent
Requires:       espa-cloud-masking
Requires:       python-lxml
Requires:       python-espa
Requires:       python-requests
Requires:       python2-boto3
Requires:       python-gdal
Requires:	python-watchtower


%description
%summary

%prep
%setup -q -n espa-processing


%build
%py2_build


%install
%py2_install

%files
%exclude %dir %{_bindir}
%{_bindir}
%{python2_sitelib}/*
%{_datadir}/espa


%doc
%changelog
