# spec file for qt5-qtwayland
%global qt_module qtwayland

Name:           qt5-%{qt_module}
Version:        5.15.2
Release:        1
Summary:        Qt5 - Wayland platform support and QtCompositor module
License:        LGPLv3
Url:            http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

Patch00:        0005-Scanner-Avoid-accessing-dangling-pointers-in-destroy.patch
Patch01:        0006-Make-setting-QT_SCALE_FACTOR-work-on-Wayland.patch
Patch02:        0007-Do-not-try-to-eglMakeCurrent-for-unintended-case.patch
Patch03:        0008-Make-setting-QT_SCALE_FACTOR-work-on-Wayland.patch
Patch04:        0009-Ensure-that-grabbing-is-performed-in-correct-context.patch
Patch05:        0010-Fix-leaked-subsurface-wayland-items.patch
Patch06:        0011-Use-qWarning-and-_exit-instead-of-qFatal-for-wayland.patch
Patch07:        0012-Fix-memory-leak-in-QWaylandGLContext.patch
Patch08:        0013-Client-Send-set_window_geometry-only-once-configured.patch
Patch09:        0014-Translate-opaque-area-with-frame-margins.patch
Patch10:        0015-Client-Send-exposeEvent-to-parent-on-subsurface-posi.patch
Patch11:        0016-Get-correct-decoration-margins-region.patch
Patch12:        0017-xdgshell-Tell-the-compositor-the-screen-we-re-expect.patch
Patch13:        0018-Fix-compilation.patch
Patch14:        0019-client-Allow-QWaylandInputContext-to-accept-composed.patch
Patch15:        0020-Client-Announce-an-output-after-receiving-more-compl.patch
Patch16:        0021-Fix-issue-with-repeated-window-size-changes.patch
Patch17:        0022-Include-locale.h-for-setlocale-LC_CTYPE.patch
Patch18:        0023-Client-Connect-drags-being-accepted-to-updating-the-.patch
Patch19:        0024-Client-Disconnect-registry-listener-on-destruction.patch
Patch20:        0025-Client-Set-XdgShell-size-hints-before-the-first-comm.patch
Patch21:        0026-Fix-build.patch
Patch22:        0027-Fix-remove-listener.patch
Patch23:        0028-Hook-up-queryKeyboardModifers.patch
Patch24:        0029-Do-not-update-the-mask-if-we-do-not-have-a-surface.patch
Patch25:        0030-Correctly-detect-if-image-format-is-supported-by-QIm.patch
Patch26:        qtwayland-client-expose-toplevel-window-state.patch
Patch27:        qtwayland-client-use-wl-keyboard-to-determine-active-state.patch
Patch28:        qtwayland-client-do-not-empty-clipboard-when-new-popup-or-window-is-opened.patch

%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

BuildRequires:  make
BuildRequires:  qt5-qtbase-devel >= %{version}
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  qt5-qtbase-static
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires:  qt5-qtdeclarative-devel libXext-devel
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-scanner) pkgconfig(wayland-server) pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor) pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(egl) pkgconfig(gl)
BuildRequires:  pkgconfig(xcomposite) pkgconfig(xrender)
BuildRequires:  pkgconfig(libudev) pkgconfig(libinput)
BuildRequires:  tree


%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      qt5-qtbase-devel%{?_isa}

%package help
Summary:       Programming example files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description
This package is a Qt 5 module that wraps the functionality of Wayland.

%description devel
This package provide development files for %{name}

%description help
This package provide programming example files for %{name}


%prep
%autosetup -n %{qt_module}-everywhere-src-%{version} -p1


%build
%{qmake_qt5}
%make_build


%install
make install INSTALL_ROOT=%{buildroot}

pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" "${prl_file}"
  if [[ -f "$(basename ${prl_file} .prl).so" ]]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" "${prl_file}"
  fi
done
popd


%ldconfig_scriptlets

%files
%doc README
%license LICENSE.*
%{_qt5_libdir}/libQt5WaylandCompositor.so.5*
%{_qt5_libdir}/libQt5WaylandClient.so.5*

%{_qt5_plugindir}/platforms/libqwayland-egl.so
%{_qt5_plugindir}/platforms/libqwayland-generic.so
%{_qt5_plugindir}/platforms/libqwayland-xcomposite*.so

%{_qt5_plugindir}/wayland-decoration-client/
%{_qt5_plugindir}/wayland-graphics-integration-server
%{_qt5_plugindir}/wayland-graphics-integration-client
%{_qt5_plugindir}/wayland-shell-integration

%{_qt5_qmldir}/QtWayland/

%files devel
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_qt5_bindir}/qtwaylandscanner

%{_qt5_headerdir}/QtWaylandCompositor/
%{_qt5_headerdir}/QtWaylandClient/

%{_qt5_libdir}/cmake/Qt5WaylandCompositor/Qt5WaylandCompositorConfig*.cmake
%{_qt5_libdir}/libQt5WaylandCompositor.prl
%{_qt5_libdir}/libQt5WaylandCompositor.so
%{_qt5_libdir}/libQt5WaylandClient.prl
%{_qt5_libdir}/libQt5WaylandClient.so
%{_qt5_libdir}/pkgconfig/*.pc

%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_*.cmake
%{_qt5_libdir}/cmake/Qt5WaylandClient/
%{_qt5_libdir}/cmake/Qt5WaylandCompositor/

%files help
%{_qt5_examplesdir}/wayland/


%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-6
- Fix Source0

* Thu Aug 06 2020 zhangjiapeng <zhangjiapeng9@huawei.com> - 5.11.1-5
- Add compilation dependency to solve compilation failure

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-4
- Package init
