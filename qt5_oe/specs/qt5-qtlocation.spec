%global __provides_exclude_from ^(%{_qt5_archdatadir}/qml/.*\\.so|%{_qt5_plugindir}/.*\\.so)$

Name:             qt5-qtlocation
Version:          5.15.2
Release:          1
Summary:          Qt5 module for Location framework
License:          LGPLv2 with exceptions or GPLv3 with exceptions
Url:              http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:          https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtlocation-everywhere-src-%{version}.tar.xz

Patch0:           qtlocation-gcc10.patch

BuildRequires: make
BuildRequires:    qt5-qtbase-devel >= 5.9.0 qt5-qtbase-private-devel pkgconfig(zlib)
BuildRequires:    pkgconfig(icu-i18n) pkgconfig(libssl) pkgconfig(libcrypto) qt5-qtdeclarative-devel >= 5.9.0
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}

%description
The Qt Location API helps you create viable mapping solutions using the
data available from some of the popular location services.

%package devel
Summary:          Development files provided for qt5-qtlocation
Requires:         %{name} = %{version}-%{release} qt5-qtbase-devel
Provides:         %{name}-examples = %{version}-%{release}
Obsoletes:        %{name}-examples < %{version}-%{release}
%description devel
This package is a developing files for t5-qtlocation.

%prep
%autosetup -n qtlocation-everywhere-src-%{version} -p1

%build
%{qmake_qt5}

%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

cd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
cd -

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/{libQt5Location.so.5*,libQt5Positioning.so.5*,libQt5PositioningQuick.so.5*}

%{_qt5_archdatadir}/qml/QtLocation/
%{_qt5_archdatadir}/qml/QtPositioning/*
%{_qt5_archdatadir}/qml/Qt/labs/location

%{_qt5_plugindir}/position/
%{_qt5_plugindir}/geoservices/

%dir %{_qt5_archdatadir}/qml/Qt
%dir %{_qt5_archdatadir}/qml/Qt/labs
%dir %{_qt5_archdatadir}/qml/QtPositioning

%files devel
%{_qt5_headerdir}/{QtLocation/,QtPositioning/,QtPositioningQuick/}

%{_qt5_libdir}/{libQt5Location.so,libQt5Location.prl,libQt5Positioning.so}
%{_qt5_libdir}/{libQt5Positioning.prl,libQt5PositioningQuick.so,libQt5PositioningQuick.prl}
%{_qt5_libdir}/pkgconfig/{Qt5Location.pc,Qt5Positioning.pc,Qt5PositioningQuick.pc}

%dir %{_qt5_libdir}/cmake/{Qt5Location,Qt5Positioning,Qt5PositioningQuick/}

%{_qt5_libdir}/cmake/Qt5Location/Qt5Location*.cmake
%{_qt5_libdir}/cmake/Qt5Positioning/Qt5Positioning*.cmake
%{_qt5_libdir}/cmake/Qt5PositioningQuick/Qt5PositioningQuick*.cmake

%{_qt5_archdatadir}/mkspecs/modules/{qt_lib_location*.pri,qt_lib_positioning*.pri,qt_lib_positioning*.pri}

%{_qt5_examplesdir}/

%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Sat Jul 31 2021 wangyong<wangyong187@huawei.com> - 5.11.1-7
- Patch for GCC-10

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-6
- Fix Source0

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-5
- Package init
