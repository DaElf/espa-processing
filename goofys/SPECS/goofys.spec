%global commit      63fe64c471e7d76be96a625350468dfc65c06c31
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           goofys
Version:        master
Release:        1%{?dist}
Summary:        This application is an example for the golang binary RPM spec
License:        ASL 2.0 
URL:            http://www.example-app.io
#Source0:        https://github.com/kahing/goofys/archive/master.tar.gz

BuildRequires:  gcc

BuildRequires:  golang >= 1.2-7

%description
goofys

%prep

# many golang binaries are "vendoring" (bundling) sources, so remove them. Those dependencies need to be packaged independently.
rm -rf vendor

%build
# set up temporary build gopath, and put our directory there
#mkdir -p ./_build/src/github.com/example
#ln -s $(pwd) ./_build/src/github.com/example/app

export GOPATH=$(pwd)/_build:%{gopath}
go get -v github.com/kahing/goofys
go install -v github.com/kahing/goofys
#go build -o example-app .

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 _build/bin/goofys %{buildroot}%{_bindir}/goofys

%files
%defattr(-,root,root,-)
%{_bindir}/goofys

%changelog
* Tue Jul 01 2014 Jill User <jill.user@fedoraproject.org> - 1.0.0-6
- package the goofys

