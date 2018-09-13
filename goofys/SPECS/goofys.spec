# This is seriously the very *wrong* way to do an rpm.spec
# This does not package any source but rather just downloads
# the pieces and packages the goofys binary.
# RMC

Name:           goofys
Version:        master
Release:        1%{?dist}
Summary:        This application is an example for the golang binary RPM spec
License:        ASL 2.0 
URL:            http://github.com/kahing/goofys
#Source0:        https://github.com/kahing/goofys/archive/master.tar.gz

BuildRequires:  gcc

BuildRequires:  golang >= 1.2-7
BuildRequires:  git

%description
goofys

%prep

# many golang binaries are "vendoring" (bundling) sources, so remove them. Those dependencies need to be packaged independently.
rm -rf vendor

%build
export GOPATH=$(pwd)/_build:%{gopath}
go get -v github.com/kahing/goofys
go install -v github.com/kahing/goofys

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 _build/bin/goofys %{buildroot}%{_bindir}/goofys

%files
%defattr(-,root,root,-)
%{_bindir}/goofys

%changelog
* Tue Jul 01 2014 Jill User <jill.user@fedoraproject.org> - 1.0.0-6
- package the goofys

