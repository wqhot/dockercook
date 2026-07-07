Name:              qt5-qtsvg
Version:           5.15.2
Release:           2
Summary:           Qt GUI toolkit for rendering and displaying SVG
License:           LGPLv2 with exceptions or GPLv3 with exceptions
Url:               http://www.qt.io
Source0:           https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/qtsvg-everywhere-src-%{version}.tar.xz
Patch0:            qtsvg-5.15.2-clamp-parsed-doubles-to-float-representtable-values.patch
Patch1:            CVE-2021-45930.patch
# backport for CVE-2025-10729
Patch10: qtsvg-5.15.17-CVE-2025-10729.patch

BuildRequires:    qt5-qtbase-devel >= %{version} pkgconfig(zlib) qt5-qtbase-private-devel  make
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}

%description
The Qt SVG module provides functionality for displaying SVG images in
widget, and to create SVG files using drawing commands.

%package devel
Summary:          Library and header files of libdwarf for qt5-qtsvg
Requires:         %{name} = %{version}-%{release} qt5-qtbase-devel
Provides:         %{name}-examples = %{version}-%{release}
Obsoletes:        %{name}-examples < %{version}-%{release}

%description devel
qt5-qtsvg-devel provides libraries and header files for qt5-qtsvg.

%prep
%autosetup -n qtsvg-everywhere-src-%{version} -p1

%build
%{qmake_qt5}

%make_build

%install
make install INSTALL_ROOT=%{buildroot}

pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.*
%dir %{_qt5_libdir}/cmake/Qt5Svg/
%{_qt5_libdir}/{libQt5Svg.so.5*,cmake/Qt5Svg/Qt5Svg_*Plugin.cmake}
%{_qt5_plugindir}/{iconengines/libqsvgicon.so,imageformats/libqsvg.so}
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QSvg*Plugin.cmake

%files devel
%{_qt5_examplesdir}/
%{_qt5_headerdir}/QtSvg/
%{_qt5_libdir}/cmake/Qt5Svg/Qt5SvgConfig*.cmake
%{_qt5_libdir}/{libQt5Svg.so,libQt5Svg.prl,pkgconfig/Qt5Svg.pc}
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_svg*.pri

%changelog
* Sun Mar 08 2026 Funda Wang <fundawang@yeah.net> - 5.15.2-2
- fix CVE-2025-10729

* Tue Jan 18 2022 liyanan  <liyanan32@huawei.com> - 5.15.2-1
- update to upstream version 5.15.2

* Thu Jan 13 2022 wangkai <wangkai385@huawei.com> - 5.11.1-6
- Fix CVE-2021-45930

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0

* Fri Jan 10 2020 zhouyihang <zhouyihang1@huawei.com> - 5.11.1-4
- change the source to valid address

* Thu Nov 07 2019 yanzhihua <yanzhihua4@huawei.com> - 5.11.1-3
- Package init
