Name:           espa-surface-temperature
Version:        1.0
Release:        1%{?dist}
Summary:        ESPA surface temperature

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-surface-temperature
Source0:        espa-surface-temperature.tar.gz

BuildRequires: libxml2-devel
BuildRequires: pkgconfig
BuildRequires: HDF-EOS
BuildRequires: espa-product-formatter
BuildRequires: espa-product-formatter-devel

%description
ESPA surface temperature

%prep
%setup -q


%build
export PREFIX=%{_prefix}
export XML2INC=$(pkg-config libxml-2.0 --cflags-only-I | sed s/-I//)
export XML2LIB=%{_libdir}
export HDFEOS_GCTPLIB=%{_libdir}
export ESPAINC=%{_includedir}
export ESPALIB=%{_libdir}
export ZLIBLIB=%{_libdir}
export LZMALIB=%{_libdir}
make %{?_smp_mflags} ENABLE_THREADING=yes

%install
rm -rf $RPM_BUILD_ROOT
export PREFIX=%{buildroot}%{_prefix}
%make_install lib_link_path=%{buildroot}%{_libdir} bin_link_path=%{buildroot}%{_bindir}
%make_install


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-surface-temperature
%doc



%changelog
