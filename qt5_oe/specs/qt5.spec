Name:          qt5
Version:       5.15.2
Release:       2
Summary:       Qt5 meta package
License:       GPLv3
URL:           https://getfedora.org/
Source0:       macros.qt5
Source1:       macros.qt5-srpm
Source2:       qmake-qt5.sh
BuildArch:     noarch

Requires:      qt5-qdbusviewer qt5-qt3d qt5-qtbase qt5-qtbase-gui qt5-qtbase-mysql
Requires:      qt5-qtbase-postgresql qt5-qtconnectivity qt5-qtdeclarative qt5-qtdoc
Requires:      qt5-qtgraphicaleffects qt5-qtimageformats qt5-qtlocation qt5-qtmultimedia
Requires:      qt5-qtquickcontrols qt5-qtquickcontrols2 qt5-qtscript qt5-qtsensors
Requires:      qt5-qtserialport qt5-qtsvg qt5-qttools qt5-qtwayland qt5-qtwebchannel
Requires:      qt5-qtwebsockets qt5-qtx11extras qt5-qtxmlpatterns

%description
Qt is a full development framework with tools designed to streamline the creation of applications
and user interfaces for desktop, embedded, and mobile platforms.

%package      devel
Summary:      Qt5 meta devel package
Requires:     qt5-rpm-macros qt5-qttools-static qt5-qtdeclarative-static qt5-qtbase-static
Requires:     qt5-designer qt5-qdoc qt5-qhelpgenerator qt5-linguist qt5-qtbase-devel
Requires:     qt5-qtconnectivity-devel qt5-qtdeclarative-devel qt5-qtlocation-devel
Requires:     qt5-qtmultimedia-devel qt5-qtscript-devel qt5-qtsensors-devel qt5-qtserialport-devel
Requires:     qt5-qtsvg-devel qt5-qttools-devel qt5-qtwayland-devel qt5-qtwebchannel-devel
#Requires:    qt5-qtwebengine-devel
Requires:     qt5-qtwebsockets-devel qt5-qtx11extras-devel qt5-qtxmlpatterns-devel
#Requires:    qt5-qtwebkit-devel qt5-qtenginio-devel qt5-qt3d-devel
%description  devel
Development files for %{name}

%package      rpm-macros
Summary:      RPM macros for building Qt5 and KDE Frameworks 5 packages
Requires:     gcc-c++
%if 0%{?epel}
Requires: cmake3
%endif

%description  rpm-macros
RPM provides a rich set of macros to make package maintenance simpler and consistent across packages.

%package     srpm-macros
Summary:     RPM macros for source Qt5 packages

%description srpm-macros
RPM RPM provides a rich set of macros for source Qt5 packages

%install
install -Dpm644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5
install -Dpm644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5-srpm
install -Dpm755 %{SOURCE2} %{buildroot}%{_bindir}/qmake-qt5.sh
mkdir -p %{buildroot}%{_datadir}/qt5/wrappers
ln -s %{_bindir}/qmake-qt5.sh %{buildroot}%{_datadir}/qt5/wrappers/qmake-qt5
ln -s %{_bindir}/qmake-qt5.sh %{buildroot}%{_datadir}/qt5/wrappers/qmake

sed -i \
  -e "s|@@QT5_CFLAGS@@|%{?qt5_cflags}|g" \
  -e "s|@@QT5_CXXFLAGS@@|%{?qt5_cxxflags}|g" \
  -e "s|@@QT5_RPM_LD_FLAGS@@|%{?qt5_rpm_ld_flags}|g" \
  -e "s|@@QT5_RPM_OPT_FLAGS@@|%{?qt5_rpm_opt_flags}|g" \
  -e "s|@@QMAKE@@|%{_prefix}/%%{_lib}/qt5/bin/qmake|g" \
  -e "s|@@QMAKE_QT5_WRAPPER@@|%{_bindir}/qmake-qt5.sh|g" \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5

mkdir -p %{buildroot}%{_docdir}/qt5
mkdir -p %{buildroot}%{_docdir}/qt5-devel
echo "- Qt5 meta package" > %{buildroot}%{_docdir}/qt5/README
echo "- Qt5 devel meta package" > %{buildroot}%{_docdir}/qt5-devel/README

%files
%defattr(-,root,root)
%{_docdir}/qt5/README

%files devel
%defattr(-,root,root)
%{_docdir}/qt5-devel/README

%files rpm-macros
%defattr(-,root,root)
%{_rpmconfigdir}/macros.d/macros.qt5
%{_bindir}/qmake-qt5.sh
%{_datadir}/qt5/wrappers/

%files srpm-macros
%defattr(-,root,root)
%{_rpmconfigdir}/macros.d/macros.qt5-srpm

%changelog
* Mon May 27 2024 laokz <zhangkai@iscas.ac.cn> - 5.15.2-2
- add riscv64 to %qt5-srpm-macros

* Tue Feb 2 2021 jinzhimin <jinzhimin2@huawei.com> - 5.15.2-1
- update to 5.15.2

* Tue Aug 18 2020 jinzhimin <jinzhimin2@huawei.com> - 5.14.2-1
- rollback package to 5.14.2

* Thu Jun 23 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.15.0-0
- update package to 5.15.0

* Sat Mar 14 2020 songnannan <songnannan2@huawei.com> - 5.11.1-7
- delete the unused requires

* Fri Nov 15 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.11.1-6
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:Delete the dependency include qt5-qt3d qt5-qtenginio-devel qt5-qtwebkit-devel

* Mon Sep 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.11.1-5
- Package init
