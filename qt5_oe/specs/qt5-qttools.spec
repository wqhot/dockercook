Name:          qt5-qttools
Version:       5.15.2
Release:       4
Summary:       Qt5 QtTool module
License:       LGPLv3 or LGPLv2
Url:           http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qttools-everywhere-src-%{version}.tar.xz
Source1:       assistant.desktop
Source2:       designer.desktop
Source3:       linguist.desktop
Source4:       qdbusviewer.desktop

Patch0:        qttools-opensource-src-5.13.2-runqttools-with-qt5-suffix.patch
Patch1:        qttools-opensource-src-5.7-add-libatomic.patch
Patch2:        0001-Link-against-libclang-cpp.so-instead-of-the-clang-co.patch
Patch3:        0001-modify-lupdate-qt5-run-error.patch

BuildRequires: make
BuildRequires: cmake desktop-file-utils /usr/bin/file qt5-rpm-macros >= %{version}
BuildRequires: qt5-qtbase-private-devel qt5-qtbase-devel >= %{version} qt5-qtbase-static >= %{version}
BuildRequires: clang-devel llvm-devel qt5-qtdeclarative-devel >= %{version} pkgconfig(Qt5Qml)
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}

Provides:      %{name}-common = %{version}-%{release} %{name}-libs-designer = %{version}-%{release}
Obsoletes:     %{name}-common < %{version}-%{release} %{name}-libs-designer < %{version}-%{release}
Provides:      %{name}-libs-designercomponents = %{version}-%{release} %{name}-libs-help = %{version}-%{release}
Obsoletes:     %{name}-libs-designercomponents < %{version}-%{release} %{name}-libs-help < %{version}-%{release}
Obsoletes:     qt5-qttools-libs-clucene < 5.9.0 qt5-designer-plugin-webkit < 5.9.0
Conflicts:     qt5-tools < 5.4.0-0.2
%description
This package contains Qt5 QtTool module core files.

%package devel
Summary:       %{name} development files
Requires:      %{name} = %{version}-%{release} %{name}-libs-designer = %{version}-%{release}
Requires:      %{name}-libs-designercomponents = %{version}-%{release} %{name}-libs-help = %{version}-%{release}
Requires:      qt5-doctools = %{version}-%{release} qt5-designer = %{version}-%{release}
Requires:      qt5-linguist = %{version}-%{release} qt5-qtbase-devel
Provides:      qt5-qttools-static = %{version}-%{release} qt5-qttools-examples = %{version}-%{release}
Obsoletes:     qt5-qttools-static < %{version}-%{release} qt5-qttools-examples < %{version}-%{release}
%description devel
The devel package contains libraries and header files for developing applications that use %{name}.

%package -n qt5-assistant
Summary:       Qt5 Documentation browser
Requires:      %{name} = %{version}-%{release}
%description -n qt5-assistant
This package contains Qt5 Documentation browser files.

%package -n qt5-designer
Summary:       Qt5 Design GUI
Requires:      %{name} = %{version}-%{release}
%description -n qt5-designer
This package contains Qt5 Design GUI files.

%package -n qt5-linguist
Summary:       Tools for Qt5 Linguist
Requires:      %{name} = %{version}-%{release}
%description -n qt5-linguist
This package contains tools to add translations to Qt5 applications.

%package -n qt5-qdbusviewer
Summary:       Qt5 D-Bus debugger and viewer
Requires:      %{name} = %{version}-%{release}
%{?_qt5:Requires: %{_qt5} >= %{_qt5_version}}
%description -n qt5-qdbusviewer
This package is created for debugging D-Bus objects.

%package -n qt5-doctools
Summary:       Tools for Qt5 doc
Provides:      qt5-qdoc = %{version} qt5-qhelpgenerator = %{version} qt5-qtattributionsscanner = %{version}
Obsoletes:     qt5-qdoc < 5.8.0 qt5-qhelpgenerator < 5.8.0 qt5-qtattributionsscanner < 5.8.0
Requires:      qt5-qtattributionsscanner = %{version}

%description -n qt5-doctools
This package contains tools for Qt5 doc.

%prep
%setup -q -n qttools-everywhere-src-%{version}
%patch0 -p1 -b ..runqttools-with-qt5-suffix.patch
%ifarch %{mips32}
%patch1 -p1 -b .libatomic
%endif
%patch2 -p1 -b .libclang-cpp
%patch3 -p1

%build
%{qmake_qt5}
%make_build


%install
%make_install INSTALL_ROOT=%{buildroot}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications --vendor="qt5" \
  %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4}

install -Dp -m 644 src/assistant/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant-qt5.png
install -Dp -m 644 src/assistant/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant-qt5.png
install -Dp -m 644 src/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/designer-qt5.png
install -Dp -m 644 src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer-qt5.png
install -Dp -m 644 src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer-qt5.png

for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m 644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist-qt5.png
done

mkdir %{buildroot}%{_bindir}
cd %{buildroot}%{_qt5_bindir}
for x in * ; do
  case "${x}" in
   assistant|designer|lconvert|linguist|lrelease|lupdate|lprodump|pixeltool|qcollectiongenerator|qdbus \
   |qdbusviewer|qhelpconverter|qhelpgenerator|qtplugininfo|qtattributionsscanner)
      ln -v  ${x} %{buildroot}%{_bindir}/${x}-qt5
      ln -sv ${x} ${x}-qt5
      ;;
    *)
      ln -v  ${x} %{buildroot}%{_bindir}/${x}
      ;;
  esac
done
cd -

cd  %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
cd -

sed -i -e 's| Qt5UiPlugin||g' %{buildroot}%{_qt5_libdir}/pkgconfig/Qt5Designer.pc


%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
pkg-config --print-requires --print-requires-private Qt5Designer
export CMAKE_PREFIX_PATH=%{buildroot}%{_qt5_prefix}:%{buildroot}%{_prefix}
export PATH=%{buildroot}%{_qt5_bindir}:%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
mkdir tests/auto/cmake/%{_target_platform}
cd tests/auto/cmake/%{_target_platform}
cmake ..
ctest --output-on-failure ||:
cd -

cd  %{buildroot}%{_datadir}/icons
for RES in $(ls hicolor); do
  for APP in designer assistant linguist qdbusviewer; do
    if [ -e hicolor/$RES/apps/${APP}*.* ]; then
      file hicolor/$RES/apps/${APP}*.* | grep "$(echo $RES | sed 's/x/ x /')"
    fi
  done
done
cd -

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%{_bindir}/qdbus-qt5
%{_bindir}/qtpaths
%{_qt5_bindir}/qdbus
%{_qt5_bindir}/qdbus-qt5
%{_qt5_bindir}/qtpaths
%{_qt5_libdir}/libQt5Designer.so.5*
%dir %{_qt5_libdir}/cmake/Qt5Designer/
%{_qt5_libdir}/libQt5DesignerComponents.so.5*
%{_qt5_libdir}/libQt5Help.so.5*
%license LICENSE.LGPL*



%files -n qt5-assistant
%{_bindir}/assistant-qt5
%{_qt5_bindir}/assistant*
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*.*

%files -n qt5-doctools
%{_bindir}/qdoc*
%{_qt5_bindir}/qdoc*
%{_bindir}/qdistancefieldgenerator*
%{_bindir}/qhelpgenerator*
%{_qt5_bindir}/qdistancefieldgenerator*
%{_qt5_bindir}/qhelpgenerator*
%{_bindir}/qtattributionsscanner-qt5
%{_qt5_bindir}/qtattributionsscanner*

%files -n qt5-designer
%{_bindir}/designer*
%{_qt5_bindir}/designer*
%{_datadir}/applications/*designer.desktop
%{_datadir}/icons/hicolor/*/apps/designer*.*
%{_qt5_libdir}/cmake/Qt5DesignerComponents/Qt5DesignerComponentsConfig*.cmake

%files -n qt5-linguist
%{_bindir}/linguist*
%{_qt5_bindir}/linguist*
%{_qt5_datadir}/phrasebooks/
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/linguist*.*
%{_bindir}/lconvert*
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/lprodump*
%{_qt5_bindir}/lconvert*
%{_qt5_bindir}/lrelease*
%{_qt5_bindir}/lupdate*
%{_qt5_bindir}/lprodump*
%dir %{_qt5_libdir}/cmake/Qt5LinguistTools/
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsMacros.cmake


%files -n qt5-qdbusviewer
%{_bindir}/qdbusviewer*
%{_qt5_bindir}/qdbusviewer*
%{_datadir}/applications/*qdbusviewer.desktop
%{_datadir}/icons/hicolor/*/apps/qdbusviewer*.*

%files devel
%{_bindir}/pixeltool*
%{_bindir}/qcollectiongenerator*
#{_bindir}/qhelpconverter*
%{_bindir}/qtdiag*
%{_bindir}/qtplugininfo*
%{_qt5_bindir}/pixeltool*
%{_qt5_bindir}/qtdiag*
%{_qt5_bindir}/qcollectiongenerator*
#{_qt5_bindir}/qhelpconverter*
%{_qt5_bindir}/qtplugininfo*
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_headerdir}/Qt*/
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_*.pri
%{_qt5_libdir}/libQt5Designer*.prl
%{_qt5_libdir}/libQt5Designer*.so
%{_qt5_libdir}/libQt5Help.prl
%{_qt5_libdir}/libQt5Help.so
%{_qt5_libdir}/libQt5UiTools.*a
%{_qt5_libdir}/libQt5UiTools.prl
%{_qt5_libdir}/Qt5UiPlugin.la
%{_qt5_libdir}/libQt5UiPlugin.prl
%{_qt5_libdir}/cmake/Qt5Designer/Qt5DesignerConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5Help/
%{_qt5_libdir}/cmake/Qt5Help/Qt5HelpConfig*.cmake
%{_qt5_libdir}/cmake/Qt5UiPlugin/
%{_qt5_libdir}/cmake/Qt5AttributionsScannerTools/
%{_qt5_libdir}/cmake/Qt5DocTools/
%{_qt5_libdir}/cmake/Qt5UiTools/
%dir %{_qt5_libdir}/cmake/Qt5Designer
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_*
%{_qt5_examplesdir}/
%{_qt5_plugindir}/designer/*


%changelog
* Wed Mar 30 2022 ouyangminxiang <ouyangminxiang@kylinsec.com.cn> - 5.15.2-4
- Add Chinese translation

* Fri Mar 11 2022 pei-jiankang <peijiankang@kylinos.cn> - 5.15.2-3
- modify lupdate-qt5 run error

* Tue Feb 22 2022 pei-jiankang <peijiankang@kylinos.cn> - 5.15.2-2
- modify lupdate-qt5 run error

* Wed Oct 13 2021 pei-jiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0 

* Fri Jan 10 2020 zhujunhao <zhujunhao5@huawei.com> - 5.11.1-4
- change the url to valid address

* Wed Nov 27 2019 Shuaishuai Song <songshuaishuai2@huawei.com> - 5.11.1-3
- package init
