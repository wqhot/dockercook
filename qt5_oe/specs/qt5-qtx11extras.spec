%global majmin %(echo %{version} | cut -d. -f1-2)

Name:		qt5-qtx11extras
Version:	5.15.2
Release:        1
Summary:	Qt GUI toolkit
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
Url:            http://www.qt.io
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtx11extras-everywhere-src-%{version}.tar.xz

BuildRequires:  make
BuildRequires:	qt5-qtbase-devel >= %{version} qt5-qtbase-private-devel
Requires:       qt5-qtbase = %{version}

%description
Provides specific APIs for X11.

%package        devel
Summary:        Header files for qt5-qtx11extras
Requires:       qt5-qtbase-devel  %{name} = %{version}-%{release}

%description    devel
Header files for qt5-qtx11extras

%prep
%autosetup -n qtx11extras-everywhere-src-%{version}

%build
%{qmake_qt5}

%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}
%delete_la

pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
    sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
    if [ -f "$(basename ${prl_file} .prl).so" ]; then
        rm -fv "$(basename ${prl_file} .prl).la"
	sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
    fi
done
popd

%ldconfig_scriptlets

%files
%license LICENSE.LGPL* LICENSE.GPL*
%{_libdir}/*.so.5*

%files          devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libQt5X11Extras.so
%{_libdir}/libQt5X11Extras.prl
%{_libdir}/cmake/Qt5X11Extras/*.cmake
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_includedir}/qt5/QtX11Extras

%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-6
- Fix Source0 

* Fri Feb 14 2020 Ling Yang <lingyang2@huawei.com> - 5.11.1-5
- Package init
