Name:           qt5-qtquickcontrols2
Summary:        Qt5 - module for embedded QtQuick control set
Version:        5.15.2
Release:        1
License:        GPLv2+ or LGPLv3 and GFDL
Url:            http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtquickcontrols2-everywhere-src-%{version}.tar.xz
BuildRequires:  make
BuildRequires:  qt5-qtbase-devel >= %{version} qt5-qtbase-private-devel qt5-qtdeclarative-devel
Requires:       qt5-qtdeclarative >= %{version} qt5-qtgraphicaleffects >= %{version}
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}

%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

%description
This package provides a set of controls for building a complete interface in Qt Quick.
These controls are the first choice for hardware with limited resources as it is
optimized for embedded systems.

%package devel
Summary:        Development and Examples files for %{name}
Requires:       %{name} = %{version}-%{release} qt5-qtbase-devel qt5-qtdeclarative-devel
Provides:       %{name}-examples = %{version}-%{release}
Obsoletes:      %{name}-examples < %{version}-%{release}
%description devel
This package provides module for embedded QtQuick control set

%prep
%autosetup -n qtquickcontrols2-everywhere-src-%{version} -p1

%build
%{qmake_qt5}
%make_build


%install
make install INSTALL_ROOT=%{buildroot}

cd %{buildroot}%{_qt5_libdir}
for file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${file}
  if [ -f "$(basename ${file} .prl).so" ]; then
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${file}
    rm -f "$(basename ${file} .prl).la"
  fi
done
cd -

%delete_la

%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%files
%license LICENSE.LGPLv3 LICENSE.GPLv3
%{_qt5_libdir}/libQt5Quick*.so.5*
%{_qt5_qmldir}/Qt/labs/*
%{_qt5_archdatadir}/qml/QtQuick/*.2/


%files devel
%{_qt5_examplesdir}/quickcontrols2/
%{_qt5_headerdir}/
%{_qt5_libdir}/pkgconfig/*.pc
%{_qt5_libdir}/libQt5Quick*2.so
%{_qt5_libdir}/libQt5Quick*2.prl
%{_qt5_libdir}/qt5/mkspecs/modules/*
%{_libdir}/cmake/Qt5QuickControls2/
%{_libdir}/cmake/Qt5QuickTemplates2/


%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-4
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-4
- Fix Source0 

* Wed Nov 27 2019 likexin<likexin4@huawei.com> - 5.11.1-3
- Package init
