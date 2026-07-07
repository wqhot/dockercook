%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

Name:           qt5-qtquickcontrols
Version:        5.15.2
Release:        1
Summary:        Qt5 Quick controls module
License:        LGPLv2 or LGPLv3 and GFDL
Url:            http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtquickcontrols-everywhere-src-%{version}.tar.xz

BuildRequires:  make
BuildRequires:  qt5-qtbase-devel >= %{version} qt5-qtbase-static >= %{version} qt5-qtbase-private-devel qt5-qtdeclarative-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

%description
This qt module provides a set of quick controls using for building complete interfaces in Qt Quick.

%package devel
Summary:        %{name} programming demos
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-examples  = %{version}-%{release}
Obsoletes:      %{name}-examples < %{version}-%{release}

%description devel
Qt Quick controls module's programming demos.

%prep
%autosetup -n qtquickcontrols-everywhere-src-%{version} -p1

%build
%{qmake_qt5}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%license LICENSE.*
%{_qt5_archdatadir}/qml/QtQuick/

%files devel
%if 0%{?_qt5_examplesdir:1}
%{_qt5_examplesdir}/
%endif

%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0 

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-4
- Package init
