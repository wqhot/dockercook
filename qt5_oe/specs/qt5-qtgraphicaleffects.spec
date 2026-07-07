%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

Name:           qt5-qtgraphicaleffects
Version:        5.15.2
Release:        1
Summary:        Qtgraphicaleffects component of qt5
License:        LGPLv2 with exceptions or GPLv3 with exceptions
Url:            http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtgraphicaleffects-everywhere-src-%{version}.tar.xz

BuildRequires:  make qt5-qtbase-private-devel
BuildRequires:  qt5-qtbase-devel >= %{version} qt5-qtdeclarative-devel
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}
BuildRequires:  libmng-devel libtiff-devel

%description
The Qt Graphical Effects module provides a set of QML types for adding visually impressive and
configurable effects to user interfaces. Effects are visual items that can be added to Qt Quick
user interface as UI components.

%prep
%autosetup -n qtgraphicaleffects-everywhere-src-%{version} -p1

%build
%{qmake_qt5}
%make_build

%install
make install INSTALL_ROOT=%{buildroot}

%files
%license LICENSE*
%{_qt5_qmldir}/*/

%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Thu Mar 18 2021 maminjie <maminjie1@huawei.com> - 5.11.1-6
- Fix syntax error when macro is not defined

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-4
- Package init
