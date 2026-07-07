%global qt_module qtvirtualkeyboard

Summary: 	Qt5 - VirtualKeyboard component
Name:    	qt5-%{qt_module}
Version:        5.15.2
Release: 	1

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: 	LGPLv2 with exceptions or GPLv3 with exceptions
Url:     	http://qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

BuildRequires:  make
BuildRequires: 	qt5-qtbase-devel qt5-qtbase-private-devel qt5-qtdeclarative-devel qt5-qtsvg-devel

%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
Provides: 	bundled(libpinyin)

%description
The Qt Virtual Keyboard project provides an input framework and reference keyboard frontend

%package devel
Summary: 	Development files for %{name}
Requires: 	%{name}%{?_isa} = %{version}-%{release}
Requires: 	qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary: 	Programming examples for %{name}
Requires: 	%{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%autosetup -n %{qt_module}-everywhere-src-%{version} -p1


%build
%{qmake_qt5} \
  CONFIG+=lang-all

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
%license LICENSE.*
%{_qt5_libdir}/libQt5VirtualKeyboard.so.5*
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QVirtualKeyboardPlugin.cmake
%{_qt5_plugindir}/platforminputcontexts/libqtvirtualkeyboardplugin.so
%{_qt5_plugindir}/virtualkeyboard/
%{_qt5_qmldir}/QtQuick/VirtualKeyboard/

%files devel
%{_qt5_headerdir}/QtVirtualKeyboard/
%{_qt5_libdir}/libQt5VirtualKeyboard.prl
%{_qt5_libdir}/libQt5VirtualKeyboard.so
%{_qt5_libdir}/cmake/Qt5VirtualKeyboard/
%{_qt5_libdir}/pkgconfig/Qt5VirtualKeyboard.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_virtualkeyboard*.pri

%files examples
%{_qt5_examplesdir}/


%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Fri Aug 7 2020 weidong <weidong@uniontech.com> - 5.12.5-1
- Initial release for OpenEuler
