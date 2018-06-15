Name:           espa-reprojection
Version:        1.0
Release:        1%{?dist}
Summary:        ESPA repojection

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-plotting
Source0:        espa-reprojection.tar.gz

%description
ESPA repojection

%prep
%setup -q -n espa-reprojection


%build
export PREFIX=%{_prefix}
make %{?_smp_mflags}
make %{?_smp_mflags} ENABLE_THREADING=yes



%install
rm -rf $RPM_BUILD_ROOT
export PREFIX=%{buildroot}/%{_prefix}
%make_install lib_link_path=%{buildroot}%{_libdir} bin_link_path=%{buildroot}%{_bindir}


%files
%exclude %dir %{_bindir}
%{_bindir}
%{_prefix}/espa-reprojection

%doc



%changelog
