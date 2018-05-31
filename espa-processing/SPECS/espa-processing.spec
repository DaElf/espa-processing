Name:           espa-processing
Version:        1.0
Release:        1%{?dist}
Summary:	ESPA processing

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-processing
Source0:        espa-processing.tar.gz

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
Requires:       python-lxml
Requires:       python-espa
Requires:       python-requests
Requires:       python2-boto3
Requires:       python-gdal


%description
%summary

%prep
%setup -q


%build
export PREFIX=/usr
make %{?_smp_mflags} ENABLE_THREADING=yes

%install
export PREFIX=%{buildroot}/usr
export ENABLE_THREADI=yes
rm -rf $RPM_BUILD_ROOT
%make_install lib_link_path=%{buildroot}%{_libdir}  bin_link_path=%{buildroot}%{_bindir}


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-processing
%{_datadir}/espa


%doc
%changelog
