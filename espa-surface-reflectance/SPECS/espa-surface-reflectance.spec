%{!?build_num:%define build_num 0}
Name:           espa-surface-reflectance
Version:        1.0.b_%{build_num}
Release:        1%{?dist}
Summary:        ESPA surface reflectance

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-spectral-indices
Source0:        espa-surface-reflectance.tar.gz

BuildRequires: libxml2-devel
BuildRequires: pkgconfig
BuildRequires: hdf-devel
BuildRequires: HDF-EOS
BuildRequires: espa-product-formatter
BuildRequires: espa-product-formatter-devel
BuildRequires: gcc-gfortran
BuildRequires: libaec-devel

%description
ESPA surface reflectance

%prep
%setup -q -n espa-surface-reflectance


%build
export PREFIX=/usr
export XML2INC=$(pkg-config libxml-2.0 --cflags-only-I | sed s/-I//)
export XML2LIB=%{_libdir}
export HDFEOS_LIB=%{_libdir}
export HDFEOS_GCTPLIB=%{_libdir}
export HDFEOS_GCTPINC=%{_includedir}
export HDFINC=%{_includedir}/hdf
export ESPAINC=%{_includedir}
export JPEGINC=%{_includedir}
export ESPALIB=%{_libdir}
export ZLIBLIB=%{_libdir}
export LZMALIB=%{_libdir}
export SZIPLIB=%{_libdir}
export HDFLIB=%{_libdir}/hdf
export JPEGLIB=%{_libdir}
make %{?_smp_mflags} ENABLE_THREADING=yes

%install
rm -rf $RPM_BUILD_ROOT
export PREFIX=%{buildroot}/usr
%make_install lib_link_path=%{buildroot}%{_libdir}  bin_link_path=%{buildroot}%{_bindir}
%make_install


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-surface-reflectance
%doc



%changelog
