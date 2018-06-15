Name:           espa-elevation
Version:        1.0
Release:        1%{?dist}
Summary:	ESPA Product Formatting Software

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-elevation
Source0:        espa-elevation.tar.gz

BuildRequires: python-espa
Requires:      python-espa
Requires:      numpy
Requires:      gdal
Requires:      python-lxml


%description
ESPA elevation

%prep
%setup -q -n espa-elevation

%build
export PREFIX=/usr
make %{?_smp_mflags} ENABLE_THREADING=yes


%install
export PREFIX=%{buildroot}/usr
rm -rf $RPM_BUILD_ROOT
%make_install lib_link_path=%{buildroot}%{_libdir}  bin_link_path=%{buildroot}%{_bindir}


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-elevation

%doc
%changelog
