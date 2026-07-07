%global qt_module qtspeech

Summary:        Qt5 - Speech component
Name:           qt5-%{qt_module}
Version:        5.15.2
Release:        1
License:        LGPLv2 with exceptions or GPLv3 with exceptions
Url:            http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0:        https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz


BuildRequires:  make
BuildRequires: 	qt5-qtbase-devel speech-dispatcher-devel >= 0.8 qt5-qtbase-private-devel
BuildRequires: 	pulseaudio pulseaudio-libs
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
Recommends:     %{name}-speechd%{?_isa} = %{version}-%{release}

%description
The module enables a Qt application to support accessibility features such as text-to-speech, which is useful for end-users who are
visually challenged or cannot access the application for whatever reason. The most common use case where text-to-speech comes in handy
is when the end-user is driving and cannot attend the incoming messages on the phone. In such a scenario, the messaging application
can read out the incoming message. Qt Serial Port provides the basic functionality, which includes configuring, I/O operations,
getting and setting the control signals of the RS-232 pinouts.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary:        Programming examples for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.

%package speechd
Summary:        %{name} speech-dispatcher plugin
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description speechd
%{summary}.


%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}



%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} .. \
  %{?_qt5_examplesdir:CONFIG+=qt_example_installs}

%make_build


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

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
%{_qt5_libdir}/libQt5TextToSpeech.so.5*
%dir %{_qt5_plugindir}/texttospeech/
%dir %{_qt5_libdir}/cmake/Qt5TextToSpeech/

%files speechd
%{_qt5_plugindir}/texttospeech/libqtexttospeech_speechd.so
%{_qt5_libdir}/cmake/Qt5TextToSpeech/Qt5TextToSpeech_QTextToSpeechPluginSpeechd.cmake

%files devel
%{_qt5_headerdir}/QtTextToSpeech/
%{_qt5_libdir}/libQt5TextToSpeech.so
%{_qt5_libdir}/libQt5TextToSpeech.prl
%{_qt5_libdir}/cmake/Qt5TextToSpeech/Qt5TextToSpeechConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5TextToSpeech.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_texttospeech*.pri

%files examples
%license LICENSE.FDL
%{_qt5_examplesdir}/


%changelog
* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Fri Aug 7 2020 weidong <weidong@uniontech.com> - 5.12.5-1
- Initial release for OpenEuler
