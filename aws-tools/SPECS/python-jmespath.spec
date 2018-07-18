%define _trivial .0
%define _buildid .1

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

%global pypi_name jmespath

Name:           python-%{pypi_name}
Version:        0.9.3
Release:        1%{?dist}%{?_trivial}%{?_buildid}
Summary:        JSON Matching Expressions

License:        MIT
URL:            https://github.com/jmespath/jmespath.py
Source0:        https://pypi.python.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.

%package -n     python2-%{pypi_name}
Summary:        JSON Matching Expressions
%{?el6:Provides: python-%{pypi_name}}
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-mock
BuildRequires:  python-nose
BuildRequires:  python-setuptools
%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires:  python-ordereddict
# tests specifically import simplejson as json if python version is 2.6
BuildRequires:  python-simplejson
BuildRequires:  python-unittest2
%endif # rhel < 7

%description -n python2-%{pypi_name}
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        JSON Matching Expressions
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-mock
BuildRequires:  python3-nose
BuildRequires:  python3-setuptools

%description -n python3-%{pypi_name}
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.
%endif # with python3

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if %{with python3}
%py3_build
%endif # with python3

%install
%if %{with python3}
%py3_install
mv %{buildroot}/%{_bindir}/jp.py %{buildroot}/%{_bindir}/jp.py-%{python3_version}
ln -sf %{_bindir}/jp.py-%{python3_version} %{buildroot}/%{_bindir}/jp.py-3
%endif # with python3

%py2_install
mv %{buildroot}/%{_bindir}/jp.py %{buildroot}/%{_bindir}/jp.py-%{python2_version}
ln -sf %{_bindir}/jp.py-%{python2_version} %{buildroot}/%{_bindir}/jp.py-2
ln -sf %{_bindir}/jp.py-%{python2_version} %{buildroot}/%{_bindir}/jp.py

%check
nosetests
%if %{with python3}
nosetests-%{python3_version}
%endif # with python3

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE.txt
%{_bindir}/jp.py
%{_bindir}/jp.py-2
%{_bindir}/jp.py-%{python2_version}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE.txt
%{_bindir}/jp.py-3
%{_bindir}/jp.py-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with python3

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 27 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.0-4
- Fix python2 subpackage requiring python3 (RHBZ#1342501)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.9.0-2
- Improve to set the Provides tag for EL6 too

* Tue Dec 29 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.9.0-1
- Upgrade to upstream current version
- Improve the spec file
- Make possible to build in EL6

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.5.0-1
- New version

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-2
- Add Python 3 support

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-1
- Initial packaging
