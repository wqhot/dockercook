Name:           qt5-qtserialport
Version:        5.15.2
Release:        1
Summary:        Serialport component of qt5
License:        LGPLv2 with exceptions or GPLv3 with exceptions
Url:            http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtserialport-everywhere-src-%{version}.tar.xz

BuildRequires:  make
BuildRequires:  qt5-qtbase-devel >= %{version} pkgconfig(libudev)
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}

%description
Qt Serial Port provides the basic functionality, which includes configuring, I/O operations,
getting and setting the control signals of the RS-232 pinouts.

%package devel
Summary:        Development files for qt5-qtserialport
Requires:       qt5-qtbase-devel  %{name} = %{version}-%{release}

Obsoletes:      %{name}-examples = %{version}-%{release} 
Provides:       %{name}-examples < %{version}-%{release}

%description devel
This package contains the development files and examples for %{name}.

%prep
%autosetup -n qtserialport-everywhere-src-%{version} -p1

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

%ldconfig_scriptlets

%files
%license LICENSE.*
%{_qt5_libdir}/libQt5*.so.5*

%files devel
%{_qt5_libdir}/libQt5*.{so,prl}
%dir %{_qt5_libdir}/cmake/Qt5SerialPort/
%{_qt5_libdir}/cmake/*/*.cmake
%{_qt5_archdatadir}/*/*/*.pri
%{_qt5_headerdir}/*/
%{_qt5_libdir}/*/*.pc
%{_qt5_examplesdir}/

%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Thu Mar 18 2021 maminjie <maminjie1@huawei.com> - 5.11.1-6
- Fix syntax error when macro is not defined

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0 

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-4
- Package init
