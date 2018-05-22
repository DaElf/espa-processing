Name:           espa-product-formatter
Version:        1.0
Release:        1%{?dist}
Summary:	ESPA Product Formatting Software

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-product-formatter
Source0:        espa-product-formatter.tar.gz
Patch0:         build.patch

BuildRequires: libxml2-devel
BuildRequires: netcdf-devel pkgconfig
BuildRequires: libgeotiff-devel
BuildRequires: jbigkit-devel
BuildRequires: hdf-devel
BuildRequires: HDF-EOS
#Requires:       

%description
Provides executables for converting from input formats to our internal format,
as well as, converting from the internal format to the output formats.
This application also provided for generating the land water mask.
These applications are implementated in C.

%package devel
Summary: ESPA Product Formatting Software -- development headers / libs
Group: Development/Libraries

%description devel
Provides executables for converting from input formats to our internal format,
as well as, converting from the internal format to the output formats.
This application also provided for generating the land water mask.
These applications are implementated in C.

%prep
%setup -q
%patch0 -p1 -b .build

%build
export lib_link_path=%{_libdir}
export bin_link_path=%{_bindir}
export PREFIX=/usr
export XML2INC=$(pkg-config libxml-2.0 --cflags-only-I | sed s/-I//)
export GEOTIFF_INC=$(pkg-config libgeotiff --cflags-only-I | sed s/-I//)
export HDFINC=%{_includedir}/hdf
# These are all std and such should not be defined but the build requires something
# to be set otherwise the build will have a stray -I
export TIFFINC=%{_includedir}
export HDFEOS_INC=%{_includedir}
export HDFEOS_GCTPINC=%{_includedir}
export CURLLIB=%{_libdir}
export NCDF4LIB=%{_libdir}
export XML2LIB=%{_libdir}
export TIFFLIB=%{_libdir}
export GEOTIFF_LIB=%{_libdir}
export HDFEOS_LIB=%{_libdir}
export HDFEOS_GCTPLIB=%{_libdir}
export JPEGLIB=%{_libdir}
export JBIGLIB=%{_libdir}
export ZLIBLIB=%{_libdir}
export LZMALIB=%{_libdir}
export SZIPLIB=%{_libdir}
export HDFLIB=%{_libdir}/hdf
make %{?_smp_mflags} ENABLE_THREADING=yes


%install
export PREFIX=%{buildroot}/usr
rm -rf $RPM_BUILD_ROOT
%make_install lib_link_path=%{buildroot}%{_libdir}  bin_link_path=%{buildroot}%{_bindir}


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-product-formatter/raw_binary/bin
%{_prefix}/espa-product-formatter/python
%{_prefix}/espa-product-formatter/schema
%{_prefix}/schema
%{_prefix}/python

%files devel
%exclude %dir %{_includedir}
%{_includedir}
%{_libdir}/*.a
%{_prefix}/espa-product-formatter/raw_binary/lib
%{_prefix}/espa-product-formatter/raw_binary/include


%doc
%changelog
