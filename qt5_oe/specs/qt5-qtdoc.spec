# spec file for qt5-qtdoc

%global qt_module qtdoc

Name:          qt5-%{qt_module}
Version:       5.15.2
Release:       1
Summary:       Main Qt5 Reference Documentation
License:       GFDL
Url:           http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

BuildArch:     noarch
%global _qt5_qmake %{_bindir}/qmake-qt5

BuildRequires: make
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-doctools
BuildRequires: qt5-qtbase-doc

Obsoletes:     qt5-qtdoc-doc < 5.9.3
Provides:      qt5-qtdoc-doc = %{version}-%{release}

%description
This package contains the main Qt Reference Documentation about
overviews, Qt topics, and examples not specific to any Qt module.

%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}


%build
%{qmake_qt5}
%make_build docs


%install
make install_docs INSTALL_ROOT=%{buildroot}


%files
%doc LICENSE.FDL
%{_qt5_docdir}/qtdoc.qch
%{_qt5_docdir}/qtdoc/
%{_qt5_docdir}/qtcmake.qch
%{_qt5_docdir}/qtcmake/


%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-4
- Fix Source0

* Tue Nov 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.11.1-3
- refactor qt5-doc.spec
