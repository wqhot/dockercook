# spec file for qt5-qtserialbus

%global qt_module qtserialbus

Name:          qt5-%{qt_module}
Version:       5.15.2
Release:       1
Summary:       QtSerialbus component for qt5
License:       LGPLv2 with exceptions or GPLv3 with exceptions
Url:           http://www.qt.io

%global major_minor %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{major_minor}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
Patch0:        qtserialbus-everywhere-src-5.12.3-SIOCGSTAMP.patch
BuildRequires: make
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtserialport-devel >= %{version}

%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      qt5-qtbase-devel%{?_isa}

%package help
Summary:       Programming examples for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description
This package provides the functionalities for qt5 which includes configuring,
I/O operations, getting and setting the control signals of the RS-232 pinouts.

%description devel
Development files for %{name}

%description help
Examples files for %{name}

%prep
%autosetup -n %{qt_module}-everywhere-src-%{version} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} .. %{?_qt5_examplesdir:CONFIG+=qt_example_installs}
%make_build


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%ldconfig_scriptlets

%files
%license LICENSE.*
%{_qt5_bindir}/canbusutil
%{_qt5_libdir}/libQt5SerialBus.so.5*
%{_qt5_plugindir}/canbus

%files devel
%{_qt5_headerdir}/QtSerialBus/
%{_qt5_libdir}/libQt5SerialBus.prl
%{_qt5_libdir}/libQt5SerialBus.so

%dir %{_qt5_libdir}/cmake/Qt5SerialBus/
%{_qt5_archdatadir}/mkspecs/modules/*
%{_qt5_libdir}/cmake/Qt5SerialBus
%{_qt5_libdir}/pkgconfig/Qt5SerialBus.pc

%exclude %{_qt5_libdir}/libQt5SerialBus.la

%files help
%{_qt5_examplesdir}/


%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Nov 09 2020 huanghaitao <huanghaitao8@huawei.com> - 5.11.1-7
- Fix missing define

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-6
- Fix Source0 

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-5
- Package init
