%global qt_module qtwebchannel

Name:          qt5-%{qt_module}
Version:       5.15.10
Release:       1
Summary:       Qt5 - WebChannel component
License:       LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:           http://qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-opensource-src-%{version}.tar.xz

BuildRequires: make
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtwebsockets-devel

%description
The Qt WebChannel module provides a library for seamless integration of C++
and QML applications with HTML/JavaScript clients. Any QObject can be
published to remote clients, where its public API becomes available.

%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary:       Programming examples for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.

%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}

%build
%{qmake_qt5}
%make_build


%install
make install INSTALL_ROOT=%{buildroot}

pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" "${prl_file}"
  if [[ -f "$(basename ${prl_file} .prl).so" ]]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" "${prl_file}"
  fi
done
popd

%ldconfig_scriptlets

%files
%license LICENSE.*
%{_qt5_libdir}/libQt5WebChannel.so.5*
%{_qt5_archdatadir}/qml/QtWebChannel/

%files devel
%{_qt5_headerdir}/QtWebChannel/
%{_qt5_libdir}/libQt5WebChannel.prl
%{_qt5_libdir}/libQt5WebChannel.so

%dir %{_qt5_libdir}/cmake/Qt5WebChannel/
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_webchannel*.pri
%{_qt5_libdir}/cmake/Qt5WebChannel/Qt5WebChannelConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5WebChannel.pc

%files examples
%{_qt5_examplesdir}/


%changelog
* Wed Aug 23 2023 peijiankang <peijiankang@kylinos.cn> - 5.15.10-1
- update to upstream version 5.15.10

* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0 

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-4
- Package init
