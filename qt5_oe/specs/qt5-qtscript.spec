%if !0%{?bootstrap}
%ifnarch %{arm}
%global tests 1
%endif
%endif

%ifarch loongarch64
%define debug_package %{nil}
%endif
%global qt_module qtscript

Name:          qt5-%{qt_module}
Version:       5.15.2
Release:       2
Summary:       QtScript component for qt5
License:       LGPLv2 with exceptions or GPLv3 with exceptions
Url:           http://www.qt.io

%global  major_minor %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{major_minor}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

Patch0:        qtscript-everywhere-src-5.12.1-s390.patch
Patch3001:     3001-add-sw_64-support.patch

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: qt5-qtbase-devel qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

%if ! 0%{?bootstrap}
BuildRequires: pkgconfig(Qt5UiTools)
%endif

%if 0%{?tests}
BuildRequires: dbus-x11 mesa-dri-drivers time xorg-x11-server-Xvfb
%endif

%package devel
Summary:       Development files for %{name}
Provides:      %{name}-private-devel = %{version}-%{release}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      qt5-qtbase-devel%{?_isa}

%package help
Summary:       Programming examples for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}


%description
This package provides support for qt5 application scripting with ECMAScript

%description devel
Development files for qt5-qtscript

%description help
Examples files for %{name}


%prep
%autosetup -n %{qt_module}-everywhere-src-%{version} -p1


%build
%ifarch loongarch64
export CXXFLAGS="${CXXFLAGS} -fpermissive"
%endif
%qmake_qt5
%make_build


%install
%make_install INSTALL_ROOT=%{buildroot}
sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" -e "/^QMAKE_PRL_LIBS/d" %{buildroot}%{_qt5_libdir}/*.prl
rm -fv %{buildroot}%{_qt5_libdir}/lib*.la

%check
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
%make_build -k sub-tests-all ||:
timeout 180 \
xvfb-run -a \
time \
%make_build check -k -C tests ||:
if [ "$?" -eq "124" ]; then
echo 'make check timeout reached!'
exit 1
fi
%endif


%ldconfig_scriptlets

%files
%license LICENSE.LGPL*
%{_qt5_libdir}/libQt5Script.so.5*
%{_qt5_libdir}/libQt5ScriptTools.so.5*

%files devel
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5Script.so
%{_qt5_libdir}/libQt5Script.prl
%{_qt5_libdir}/libQt5ScriptTools.so
%{_qt5_libdir}/libQt5ScriptTools.prl

%dir %{_qt5_libdir}/cmake/Qt5Script/
%{_qt5_libdir}/cmake/Qt5Script/Qt5ScriptConfig*.cmake

%dir %{_qt5_libdir}/cmake/Qt5ScriptTools/
%{_qt5_libdir}/cmake/Qt5ScriptTools/Qt5ScriptToolsConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files help
%{_qt5_examplesdir}/


%changelog
* Sat Aug 12 2023 panchenbo <panchenbo@kylinsec.com.cn> - 5.15.2-2
- add loongarch64 and sw_64 support

* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0 

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-4
- Package init
