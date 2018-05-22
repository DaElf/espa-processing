Name:           espa-l2qa-tools
Version:        1.0
Release:        1%{?dist}
Summary:	ESPA Product Formatting Software

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-l2qa-tools
Source0:        espa-l2qa-tools.tar.gz

BuildRequires: espa-product-formatter-devel
BuildRequires: espa-product-formatter
BuildRequires: libxml2-devel

%description
ESPA l2qa tools

%package devel
Summary: ESPA l2qa tools -- devel
Group: Development/Libraries

%description devel
ESPA l2qa tools

%prep
%setup -q

%build
export PREFIX=/usr
export ESPAINC=%{_includedir}
export ESPALIB=%{_libdir}
export XML2INC=$(pkg-config libxml-2.0 --cflags-only-I | sed s/-I//)
export XML2LIB=%{_libdir}
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
%{_prefix}/espa-l2qa-tools

%files devel
%exclude %dir %{_libdir}
%exclude %dir %{_includedir}
%{_libdir}
%{_includedir}

%doc
%changelog
