%global srcname espa

Name:           python-espa
Version:        1.0
Release:        1%{?dist}
Summary:        espa python library 

Group:		ESPA
License:	NASA Open Source Agreement
URL:            https://github.com/USGS-EROS/espa-python-library
Source0:        espa-python-library.tar.gz

BuildRequires: python34-devel
BuildRequires: python34-setuptools
BuildRequires: python-setuptools
Requires:      python-lxml

%description
ESPA python library


%package -n python3-%{srcname}
Summary:        %{summary}
#{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
ESPA python library


%prep
%setup -q -n espa-python-library


%build
%py_build
%py3_build


%install
%py_install
%py3_install


%files
%doc README.md
%{python_sitelib}/*

%files -n python3-%{srcname}
%doc README.md
%{python3_sitelib}/*


%changelog
