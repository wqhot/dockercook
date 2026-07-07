%global qt_module qtwebsockets

Summary:       Qt5 - WebSockets component
Name:          qt5-%{qt_module}
Version:       5.15.2
Release:       1

License:       LGPLv2 with exceptions or GPLv3 with exceptions
Url:           http://qt-project.org/
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
Patch0:        %{name}-gcc11.patch

%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

BuildRequires: make
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel

%package       devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      qt5-qtbase-devel%{?_isa}

%package       help
Summary:       Programming examples for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description
This module implements the WebSocket protocol as specified in RFC
6455. It depends on Qt solely.

%description devel
This package include development files for %{name}

%description help
This package include examples for %{name}

%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}
%patch0 -p1


%build
%{qmake_qt5}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
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
%{_qt5_archdatadir}/qml/Qt/WebSockets/
%{_qt5_libdir}/libQt5WebSockets.so.5*

%files devel
%{_qt5_headerdir}/QtWebSockets/
%{_qt5_libdir}/libQt5WebSockets.so
%{_qt5_libdir}/libQt5WebSockets.prl
%dir %{_qt5_libdir}/cmake/Qt5WebSockets/
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_websockets*.pri
%{_qt5_libdir}/cmake/Qt5WebSockets/Qt5WebSocketsConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5WebSockets.pc
%{_qt5_libdir}/qt5/qml/QtWebSockets/

%files help
%{_qt5_examplesdir}/

%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-6
- Fix Source0 

* Fri Feb 14 2020 Ling Yang <lingyang2@huawei.com> - 5.11.1-5
- Package init
