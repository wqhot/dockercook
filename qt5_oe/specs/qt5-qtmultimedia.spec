%global __provides_exclude_from ^(%{_qt5_archdatadir}/qml/.*\\.so|%{_qt5_plugindir}/.*\\.so)$

%global openal 0

Name:          qt5-qtmultimedia
Version:       5.15.2
Release:       1
Summary:       Qt5 multimedia support
License:       LGPLv2 with exceptions or GPLv3 with exceptions
Url:           http://www.qt.io
Source0:       https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/qtmultimedia-everywhere-src-%{version}.tar.xz
BuildRequires: qt5-qtbase-devel >= %{version} qt5-qtbase-private-devel
BuildRequires: qt5-qtdeclarative-devel >= %{version} pkgconfig(alsa) pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-app-1.0) pkgconfig(gstreamer-audio-1.0)
BuildRequires: pkgconfig(gstreamer-base-1.0) pkgconfig(gstreamer-pbutils-1.0)
BuildRequires: pkgconfig(gstreamer-plugins-bad-1.0) pkgconfig(gstreamer-video-1.0) make
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib) pkgconfig(xv) chrpath wayland-devel
%if 0%{?openal}
BuildRequires: pkgconfig(openal)
%endif

%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}

%description
The Qt Multimedia module provides a set of QML types and C++ classes
to handle multimedia content. It also provides APIs to access the
camera and radio functionality. The included Qt Audio Engine provides
types for 3D positional audio playback and content management.

%package devel
Summary:       Development files for qt5-qtmultimedia
Requires:      %{name} = %{version}-%{release} qt5-qtbase-devel
Requires:      qt5-qtdeclarative-devel pkgconfig(libpulse-mainloop-glib)
Provides:      qt5-qtmultimedia-examples = %{version}-%{release}
Obsoletes:     qt5-qtmultimedia-examples < %{version}-%{release}

%description devel
This package provides Libraries and header files for qt5-qtmultimedia.

%prep
%autosetup -n qtmultimedia-everywhere-src-%{version} -p1

%build
%{qmake_qt5} CONFIG+=git_build GST_VERSION=1.0
%make_build

%install
make install INSTALL_ROOT=%{buildroot}

pushd %{buildroot}%{_qt5_libdir}
for prl_file in *.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

chrpath -d %{buildroot}/%{_qt5_examplesdir}/multimedia/spectrum/spectrum

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.*
%{_qt5_libdir}/libQt5Multimedia*.so.5*
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5Multimedia_*Plugin.cmake
%{_qt5_archdatadir}/qml/{QtAudioEngine/,QtMultimedia/}
%{_qt5_plugindir}/{audio/,mediaservice/,playlistformats/}
%dir %{_qt5_libdir}/cmake/Qt5Multimedia/
%dir %{_qt5_libdir}/cmake/Qt5MultimediaWidgets/

%files devel
%{_qt5_libdir}/libQt5Multimedia*.{so,prl}
%{_qt5_libdir}/pkgconfig/Qt5Multimedia*.pc
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5MultimediaConfig*.cmake
%{_qt5_libdir}/cmake/Qt5MultimediaWidgets/Qt5MultimediaWidgetsConfig*.cmake
%{_qt5_headerdir}/{QtMultimedia/,QtMultimediaQuick/,QtMultimediaWidgets/,QtMultimediaGstTools/}
%{_qt5_libdir}/cmake/Qt5MultimediaGstTools/Qt5MultimediaGstToolsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5MultimediaQuick/Qt5MultimediaQuickConfig*.cmake
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%if 0%{?_qt5_examplesdir:1}
%license LICENSE.FDL
%{_qt5_examplesdir}/
%endif

%changelog
* Mon Jan 17 2022 liyanan <liyanan32@huawei.com> - 5.15.2-1
- update to upstream version 5.15.2

* Thu Sep 09 2021 wangyue <wangyue92@huawei.com> - 5.11.1-8
- fix rpath problem

* Wed Jul 14 2021 zhaoshuang <zhaoshuang@uniontech.com> - 5.11.1-7
- Add patch Fix-gst_mini_object_unref to fix gstreamer related issue

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-6
- Fix Source0

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.11.1-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify self build err

* Sat Nov 30 2019 yanzhihua <yanzhihua4@huawei.com> - 5.11.1-3
- Package init
