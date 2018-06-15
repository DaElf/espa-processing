Name:           espa-cloud-masking
Version:        1.0
Release:        1%{?dist}
Summary:	ESPA Product Formatting Software

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-cloud-masking
Source0:        espa-cloud-masking.tar.gz


BuildRequires: espa-product-formatter-devel
Requires: espa-product-formatter
BuildRequires: libxml2-devel
Requires: libxml2

%description
ESPA cloud masking

%prep
%setup -q -n espa-cloud-masking

%build
export PREFIX=%{_prefix}
export XML2INC=$(pkg-config libxml-2.0 --cflags-only-I | sed s/-I//)
export XML2LIB=%{_libdir}
export ESPAINC=%{_includedir}
export ESPALIB=%{_libdir}
export LZMALIB=%{_libdir}
export ZLIBLIB=%{_libdir}
make %{?_smp_mflags} ENABLE_THREADING=yes


%install
export PREFIX=%{buildroot}/usr
rm -rf $RPM_BUILD_ROOT
%make_install lib_link_path=%{buildroot}%{_libdir}  bin_link_path=%{buildroot}%{_bindir}


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-cloud-masking

%doc
%changelog
