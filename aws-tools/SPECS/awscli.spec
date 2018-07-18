%define _trivial .0
%define _buildid .3

%if 0%{?rhel}
%global with_python3 0
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%else
%global with_python3 1
%endif

Name:           awscli
Version:        1.14.8
Release:        1%{?dist}%{?_trivial}%{?_buildid}
Summary:        Universal Command Line Environment for AWS

License:        ASL 2.0 and MIT
URL:            http://aws.amazon.com/cli
Source0:        https://pypi.python.org/packages/source/a/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-botocore = 1.3.26
Requires:       python3-colorama
Requires:       python3-docutils
Requires:       python3-rsa
%else
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2-botocore = 1.8.12
Requires:       python-colorama
Requires:       python-docutils
Requires:       python-rsa
Requires:       python2-s3transfer
Requires:       PyYAML
%endif # with_python3
%if 0%{?fedora}
Recommends: bash-completion
Recommends: zsh
%endif # Fedora
Provides:	aws-cli = %{version}-%{release}

%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{name}}
%else
%{?python_provide:%python_provide python2-%{name}}
%endif # with_python3

%description
This package provides a unified
command line interface to Amazon Web Services.

%prep
%setup -q -n %{name}-%{version}
rm -rf %{name}.egg-info

%build
%if 0%{?with_python3}
%py3_build
%else
CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"
%endif # with_python3

%install
%if 0%{?with_python3}
%py3_install
%else
CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}
%endif # with_python3
# Fix path and permissions for bash completition
%global bash_completion_dir /etc/bash_completion.d
mkdir -p %{buildroot}%{bash_completion_dir}
mv %{buildroot}%{_bindir}/aws_bash_completer %{buildroot}%{bash_completion_dir}
chmod 644 %{buildroot}%{bash_completion_dir}/aws_bash_completer
# Fix path and permissions for zsh completition
%global zsh_completion_dir /usr/share/zsh/site-functions
mkdir -p %{buildroot}%{zsh_completion_dir}
mv %{buildroot}%{_bindir}/aws_zsh_completer.sh %{buildroot}%{zsh_completion_dir}
chmod 644 %{buildroot}%{zsh_completion_dir}/aws_zsh_completer.sh
ls -alh %{buildroot}%{zsh_completion_dir}/aws_zsh_completer.sh
# We don't need the Windows CMD script
rm %{buildroot}%{_bindir}/aws.cmd

%files
%{!?_licensedir:%global license %doc} 
%doc README.rst
%license LICENSE.txt
%{_bindir}/aws
%{_bindir}/aws_completer
%dir %{bash_completion_dir}
%{bash_completion_dir}/aws_bash_completer
%dir %{zsh_completion_dir}
%{zsh_completion_dir}/aws_zsh_completer.sh
%if 0%{?with_python3}
%{python3_sitelib}/awscli
%{python3_sitelib}/%{name}-%{version}-py?.?.egg-info
%else
%{python2_sitelib}/awscli
%{python2_sitelib}/%{name}-%{version}-py?.?.egg-info
%endif # with_python3

%changelog
* Fri Feb 12 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.10.4-1
- Update to current upstream version

* Wed Feb 10 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.10.3-1
- Update to current upstream version

* Tue Feb 09 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.10.2-1
- Update to current upstream version

* Tue Feb 02 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.10.1-1
- Update to current upstream version

* Fri Jan 22 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.10.0-1
- Update to current upstream version

* Wed Jan 20 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.9.21-1
- Update to current upstream version
- Don't fix documentation permissions any more (pull request merged)

* Fri Jan 15 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.920-1
- Update to current upstream version

* Fri Jan 15 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.9.19-1
- Update to current upstream version
- Don't substitue the text of bin/aws_bash_completer anymore (pull request merged)
- Don't remove the shabang from awscli/paramfile.py anymore (pull request merged)

* Wed Jan 13 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.9.18-1
- Update to current upstream version
- Fix completion for bash
- Remove bcdoc dependency that is not used anymore

* Sun Jan 10 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.9.17-1
- Update to current upstream version
- Lock the botocore dependency version

* Sat Jan 09 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.9.16-1
- Update to current upstream version
- Add dir /usr/share/zsh
- Add dir /usr/share/zsh/site-functions
- Add MIT license (topictags.py is MIT licensed)
- Move dependency from python-devel to python2-devel
- Add Recommends lines for zsh and bsah-completion for Fedora
- Remove BuildReuires: bash-completion
- Remove the macros py2_build and py2_install to prefer the extended form
- Force non-executable bit for documentation
- Remove shabang from awscli/paramfile.py
- Fix bash completion
- Fix zsh completion
- Remove aws.cmd

* Tue Dec 29 2015 Fabio Alessandro Locati <fabio@locati.cc> - 1.9.15-1
- Initial package.
