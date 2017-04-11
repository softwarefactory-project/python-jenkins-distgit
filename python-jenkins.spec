%if 0%{?fedora} > 12
%global with_python3 1
%endif

Name:           python-jenkins
Version:        0.4.8
Release:        1%{?dist}
Summary:        Python bindings for the remote Jenkins API

Group:          Development/Libraries
License:        BSD
URL:            http://python-jenkins.readthedocs.org/en/latest
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Patch0:         %{name}-0.4.8-six-1.3.patch

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-mock
BuildRequires:  python-nose
BuildRequires:  python-pbr
BuildRequires:  python-six
BuildRequires:  python-sphinx
Requires:       python-pbr
Requires:       python-six

%description
Python Jenkins is a library for the remote API of the Jenkins continuous
integration server. It is useful for creating and managing jobs as well as
build nodes.

%if 0%{?with_python3}
%package -n python3-jenkins
Summary:        Python bindings for the remote Jenkins API

BuildRequires:  python3-devel
BuildRequires:  python3-mock
BuildRequires:  python3-nose
BuildRequires:  python3-pbr
BuildRequires:  python3-six
BuildRequires:  python3-sphinx
Requires:       python3-pbr
Requires:       python3-six
%endif

%if 0%{?with_python3}
%description -n python3-jenkins
Python Jenkins is a library for the remote API of the Jenkins continuous
integration server. It is useful for creating and managing jobs as well as
build nodes.
%endif

%prep
%setup -qc

mv %{name}-%{version} python2
pushd python2
%if 0%{?epel}
%patch0 -p1
%endif

# Remove env from __init__.py
sed -i '/^#!\/usr\/bin\/env python$/d' jenkins/__init__.py

# Loosen python-pbr requirement
sed -i 's/pbr>=0.8.2/pbr>=0.8.0/' requirements.txt

# copy common doc files to top dir
cp -pr AUTHORS ChangeLog COPYING README.rst ../
popd

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif

find python2 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
export PBR_VERSION=%{version}

pushd python2
%{__python2} setup.py build
make -C doc html man
rm -f doc/build/html/.buildinfo
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
SPHINXBUILD=sphinx-build-%{python3_version} make -C doc html man
rm -f doc/build/html/.buildinfo
popd
%endif

%install
pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
install -p -D -m0644 doc/build/man/pythonjenkins.1 %{buildroot}%{_mandir}/man1/pythonjenkins.1
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
install -p -D -m0644 doc/build/man/pythonjenkins.1 %{buildroot}%{_mandir}/man1/python3jenkins.1
popd
%endif

%check
pushd python2
PYTHONPATH=%{buildroot}%{python2_sitelib} nosetests -w tests
popd

%if 0%{?with_python3}
pushd python3
PYTHONPATH=%{buildroot}%{python3_sitelib} nosetests-%{python3_version} -w tests
popd
%endif

%files
%doc AUTHORS ChangeLog README.rst python2/doc/build/html
%license COPYING
%{python2_sitelib}/jenkins
%{python2_sitelib}/python_jenkins-%{version}-py?.?.egg-info
%{_mandir}/man1/pythonjenkins.1.gz

%if 0%{?with_python3}
%files -n python3-jenkins
%doc AUTHORS ChangeLog README.rst python3/doc/build/html
%license COPYING
%{python3_sitelib}/jenkins
%{python3_sitelib}/python_jenkins-%{version}-py?.?.egg-info
%{_mandir}/man1/python3jenkins.1.gz
%endif

%changelog
* Tue Aug 25 2015 Scott K Logan <logans@cottsay.net> - 0.4.8-1
- Update to 0.4.8

* Tue Jun 30 2015 Scott K Logan <logans@cottsay.net> - 0.4.7-1
- Update to 0.4.7

* Sun Apr 12 2015 Scott K Logan <logans@cottsay.net> - 0.4.5-1
- Update to 0.4.5
- Update to latest python packaging guidelines

* Wed Nov 12 2014 Scott K Logan <logans@cottsay.net> - 0.4.1-1
- Update to 0.4.1 (RHBZ #1162743)
- Switch to PyPI upstream
- Add python3 package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Scott K Logan <logans@cottsay.net> - 0.2.1-1
- Initial package
