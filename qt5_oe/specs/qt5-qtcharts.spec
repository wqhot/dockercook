%global qt_module qtcharts

Summary:       Qt5 - Charts component
Name:          qt5-%{qt_module}
Version:       5.15.2
Release:       1

License:       GPLv3
Url:           http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

BuildRequires: make
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}

%description
Qt Charts module provides a set of easy to use chart components. It uses the Qt Graphics View Framework, therefore charts can be easily
integrated to modern user interfaces. Qt Charts can be used as QWidgets, QGraphicsWidget, or QML types.
Users can easily create impressive graphs by selecting one of the charts themes.

%package devel
Summary:       Development files for %{name}
Requires:      qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary:       Programming examples for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}


%build
%{qmake_qt5} \
  %{?_qt5_examplesdir:CONFIG+=qt_example_installs}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
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
%license LICENSE.GPL3
%{_qt5_libdir}/libQt5Charts.so.5*
%{_qt5_qmldir}/QtCharts/

%files devel
%{_qt5_headerdir}/QtCharts/
%{_qt5_libdir}/libQt5Charts.so
%{_qt5_libdir}/libQt5Charts.prl
%{_qt5_libdir}/cmake/Qt5Charts/
%{_qt5_libdir}/pkgconfig/Qt5Charts.pc
%{_qt5_archdatadir}/mkspecs/modules/*

%files examples
%{_qt5_examplesdir}/


%changelog
* Mon Jan 10 2022 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Dec 13 2021 huayadong <huayadong@kylinos.cn> - 5.11.1-5
- remove %{?dist}

* Thu Jul 23 2020 Zhao Yang <yangzhao1@kylinos.cn> - 5.11.1-4
- Initial release for OpenEuler
