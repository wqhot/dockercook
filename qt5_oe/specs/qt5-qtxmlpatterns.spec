Name:                 qt5-qtxmlpatterns
Version:              5.15.2
Release:              1
Summary:              Provide support for XQuery, XPath, etc

License:              LGPLv2 with exceptions or GPLv3 with exceptions
Url:                  http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:              https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qtxmlpatterns-everywhere-src-%{version}.tar.xz

BuildRequires:        make qt5-qtdeclarative-devel
BuildRequires:        qt5-qtbase-devel >= %{version} qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

%description
This package is qt5-qtxmlpatterns component. It provides support for XQuery, XPath, etc.

%package              devel
Summary:              Programming examples and libraries for qt5-qtxmlpatterns development
Requires:             %{name} = %{version}-%{release} qt5-qtbase-devel

Provides:             qt5-qtxmlpatterns-examples = %{version}-%{release}
Obsoletes:            qt5-qtxmlpatterns-examples < %{version}-%{release}

%description          devel
This package contains the programming examples and libraries for qt5-qtxmlpatterns development.

%prep
%autosetup -n qtxmlpatterns-everywhere-src-%{version} -p1

%build
%{qmake_qt5}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

mkdir %{buildroot}%{_bindir}
cd %{buildroot}%{_qt5_bindir}

for i in *
do
  if [ ${i} = "xmlpatterns" ]
  then
    ln ${i} %{buildroot}%{_bindir}/${i}-qt5
    ln -s ${i} ${i}-qt5
  elif [ ${i} = "xmlpatternsvalidator" ]
  then
    ln ${i} %{buildroot}%{_bindir}/${i}-qt5
    ln -s ${i} ${i}-qt5
  else
    ln ${i} %{buildroot}%{_bindir}/${i}
fi
done
cd -

cd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl
do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]
  then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
cd -

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.LGPL*
%{_qt5_libdir}/libQt5*.*
%{_qt5_archdatadir}/qml/QtQuick/XmlListModel/


%files devel
%{_qt5_bindir}/xmlpatterns*
%{_bindir}/xmlpatterns*
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_qt5_examplesdir}/

%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0 

* Mon Oct 28 2019 dongjian <dongjian13@huawei.com> - 5.11.1-4
- Package init

