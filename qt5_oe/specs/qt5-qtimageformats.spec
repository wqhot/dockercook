%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$

Name:           qt5-qtimageformats
Version:        5.15.2
Release:        2
Summary:        Qtimageformats component of qt5
License:        LGPLv2 with exceptions or GPLv3 with exceptions
Url:            http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtimageformats-everywhere-src-%{version}.tar.xz
# https://download.qt.io/official_releases/qt/6.5/CVE-2025-5683-qtimageformats-6.5.patch
Patch0:         CVE-2025-5683.patch

BuildRequires:  make
BuildRequires:  qt5-qtbase-devel >= %{version} libmng-devel libtiff-devel libwebp-devel
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}
BuildRequires:  qt5-qtbase-private-devel
#BuildRequires:  jasper-devel

Obsoletes:      qt5-qtimageformats-devel < 5.4.0
Provides:       qt5-qtimageformats-devel = %{version}-%{release}

%description
The core Qt Gui library by default supports reading and writing image files of the most common file formats:
PNG, JPEG, BMP, GIF and a few more, ref. Reading and Writing Image Files. The Qt Image Formats add-on module
provides optional support for other image file formats.

%prep
%autosetup -n qtimageformats-everywhere-src-%{version} -p1
rm -rv src/3rdparty

%build
%{qmake_qt5}
%make_build

%install
make install INSTALL_ROOT=%{buildroot}

%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_qt5_plugindir}/*/*.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*Plugin.cmake

%changelog
* Thu Oct 16 2025 Funda Wang <fundawang@yeah.net> - 5.15.2-2
- fix CVE-2025-5683

* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Thu Mar 18 2021 maminjie <maminjie1@huawei.com> - 5.11.1-7
- Fix syntax error when macro is not defined

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-6
- Fix Source0

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-5
- Package init
