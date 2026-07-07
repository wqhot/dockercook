# spec file for qt5-qtconnectivity
%global qt_module qtconnectivity

Name:          qt5-%{qt_module}
Version:       5.15.2
Release:       2
Summary:       Qt5 - Connectivity components
License:       LGPLv2 with exceptions or GPLv3 with exceptions
Url:           https://qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
Patch0:        %{name}-gcc11.patch
Patch6001:     CVE-2025-23050-qtconnectivity-5.15.diff

%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

BuildRequires: make
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel >= %{version}
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
BuildRequires: pkgconfig(bluez)

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}

%package help
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description
This package provides features as Dial-up, (W)LAN, USB and VPN support.

%description devel
Development files for %{name}

%description help
Examples files for %{name}


%prep
%autosetup -p1 -n %{qt_module}-everywhere-src-%{version}


%build
%{qmake_qt5}
%make_build


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in *; do
  case "${i}" in
    *)
      ln -v  "${i}" %{buildroot}%{_bindir}/"${i}"
      ;;
  esac
done
popd

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
%license LICENSE.GPL* LICENSE.LGPL*
%{_bindir}/sdpscanner
%{_qt5_archdatadir}/qml/QtBluetooth/
%{_qt5_archdatadir}/qml/QtNfc/
%{_qt5_bindir}/sdpscanner
%{_qt5_libdir}/libQt5Bluetooth.so.5*
%{_qt5_libdir}/libQt5Nfc.so.5*

%files devel
%{_qt5_headerdir}/QtBluetooth/
%{_qt5_libdir}/libQt5Bluetooth.so
%{_qt5_libdir}/libQt5Bluetooth.prl

%dir %{_qt5_libdir}/cmake/Qt5Bluetooth/
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_bluetooth*.pri
%{_qt5_headerdir}/QtNfc/
%{_qt5_libdir}/cmake/Qt5Bluetooth/Qt5BluetoothConfig*.cmake
%{_qt5_libdir}/libQt5Nfc.so
%{_qt5_libdir}/libQt5Nfc.prl
%{_qt5_libdir}/pkgconfig/Qt5Bluetooth.pc

%dir %{_qt5_libdir}/cmake/Qt5Nfc/
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_nfc*.pri
%{_qt5_libdir}/cmake/Qt5Nfc/Qt5NfcConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Nfc.pc

%files help
%{_qt5_examplesdir}/


%changelog
* Wed Jan 22 2025 Funda Wang <fundawang@yeah.net> - 5.15.2-2
- fix CVE-2025-23050

* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-4
- Fix Source0

* Sat Nov 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.11.1-3
- refactor qt5-qtconnectivity.spec
