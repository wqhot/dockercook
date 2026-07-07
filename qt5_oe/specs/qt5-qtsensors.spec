%global __provides_exclude_from ^(%{_qt5_archdatadir}/qml/.*\\.so|%{_qt5_plugindir}/.*\\.so)$
Name:          qt5-qtsensors	
Version:       5.15.2
Release:       2
Summary:       The Qt5 Sensors library
License:       LGPLv2 with exceptions or GPLv3 with exceptions
Url:           http://www.qt.io/
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtsensors-everywhere-src-%{version}.tar.xz
BuildRequires: make chrpath
BuildRequires: qt5-qtbase-devel >= %{version} qt5-qtbase-private-devel qt5-qtdeclarative-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

Provides:       %{name}-examples = %{version}-%{release}
Obsoletes:      %{name}-examples < %{version}-%{release}

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      qt5-qtbase-devel%{?_isa}
%description devel
Development files for qt5-qtsensors.

%prep
%autosetup -n qtsensors-everywhere-src-%{version} -p1


%build
%{qmake_qt5}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

pushd %{buildroot}%{_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -rf "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd
chrpath -d %{buildroot}%{_libdir}/qt5/examples/sensors/grue/sensors/libqtsensors_grue.so
chrpath -d %{buildroot}%{_libdir}/qt5/examples/sensors/grue/Grue/libdeclarative_grue.so

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE.*
%{_libdir}/libQt5Sensors.so.5*
%{_libdir}/qt5/plugins/sensors
%{_libdir}/qt5/plugins/sensorgestures
%{_libdir}/qt5/qml/QtSensors
%dir %{_libdir}/cmake/Qt5Sensors
%{_libdir}/cmake/Qt5Sensors/Qt5Sensors_*Plugin.cmake
%{_libdir}/qt5/examples

%files devel
%defattr(-,root,root)
%{_includedir}/qt5/QtSensors
%{_libdir}/libQt5Sensors.so
%{_libdir}/libQt5Sensors.prl
%{_libdir}/pkgconfig/Qt5Sensors.pc
%{_libdir}/cmake/Qt5Sensors/Qt5SensorsConfig*.cmake
%{_libdir}/qt5/mkspecs/modules/qt_lib_sensors*.pri

%changelog
* Mon Aug 22 2022 xu_ping <xuping33@h-partners.com> - 5.15.2-2
- del rpath in grue plugin

* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-6
- Fix Source0 

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-5
- Package init
