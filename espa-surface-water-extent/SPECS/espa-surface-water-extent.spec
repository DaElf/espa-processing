Name:           espa-surface-water-extent
Version:        1.0
Release:        1%{?dist}
Summary:        ESPA surface water extent

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-surface-water-extent
Source0:        espa-surface-water-extent.tar.gz

BuildRequires: libxml2-devel
BuildRequires: pkgconfig
BuildRequires: espa-product-formatter
BuildRequires: espa-product-formatter-devel

%description
ESPA surface water extent


%prep
%setup -q -n espa-surface-water-extent


%build
export PREFIX=%{_prefix}
export XML2INC=$(pkg-config libxml-2.0 --cflags-only-I | sed s/-I//)
export XML2LIB=%{_libdir}
export ESPAINC=%{_includedir}
export ESPALIB=%{_libdir}
make %{?_smp_mflags} ENABLE_THREADING=yes

%install
rm -rf $RPM_BUILD_ROOT
export PREFIX=%{buildroot}%{_prefix}
%make_install lib_link_path=%{buildroot}%{_libdir} bin_link_path=%{buildroot}%{_bindir}
%make_install


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-surface-water-extent
%doc



%changelog
