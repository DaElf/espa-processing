Name:           espa-spectral-indices
Version:        1.0
Release:        1%{?dist}
Summary:        ESPA spectral indices

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-spectral-indices
Source0:        espa-spectral-indices.tar.gz

BuildRequires: espa-product-formatter-devel
BuildRequires: espa-product-formatter
BuildRequires: libxml2-devel

%description
ESPA spectral indices

%prep
%setup -q -n espa-spectral-indices


%build
export PREFIX=%{_prefix}
export XML2INC=$(pkg-config libxml-2.0 --cflags-only-I | sed s/-I//)
export ESPAINC=%{_includedir}
export ESPALIB=%{_libdir}
export XML2LIB=%{_libdir}
export LZMALIB=%{_libdir}
export ZLIBLIB=%{_libdir}
make %{?_smp_mflags} ENABLE_THREADING=yes


%install
rm -rf $RPM_BUILD_ROOT
export PREFIX=%{buildroot}%{_prefix}
%make_install lib_link_path=%{buildroot}%{_libdir}  bin_link_path=%{buildroot}%{_bindir}


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-spectral-indices

%doc

%changelog
