%define _binaries_in_noarch_packages_terminate_build 0
%global _hardened_build 1
%global __provides_exclude ^lib.*plugin\\.so.*|libv8\\.so$
%global __requires_exclude ^libv8\\.so$
%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$

Name:           qt5-qtwebengine
Version:        5.11.1
Release:        10 
Summary:        Qt5 - QtWebEngine components
License:        (LGPLv2 with exceptions or GPLv3 with exceptions) and BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:            http://www.qt.io
Source0:        qtwebengine-everywhere-src-%{version}-clean.tar.xz
# some tweaks to linux.pri (system yasm, link libpci, run unbundling script)
# From: https://github.com/rpmfusion/qt5-qtwebengine-freeworld/blob/master/qtwebengine-everywhere-src-5.10.0-linux-pri.patch
Patch0000:      qtwebengine-everywhere-src-5.10.0-linux-pri.patch
# quick hack to avoid checking for the nonexistent icudtl.dat and silence the
# resulting warnings - not upstreamable as is because it removes the fallback
# mechanism for the ICU data directory (which is not used in our builds because
# we use the system ICU, which embeds the data statically) completely
# From: https://github.com/rpmfusion/qt5-qtwebengine-freeworld/blob/master/qtwebengine-everywhere-src-5.11.0-no-icudtl-dat.patch
Patch0001:      qtwebengine-everywhere-src-5.11.0-no-icudtl-dat.patch
# fix extractCFlag to also look in QMAKE_CFLAGS_RELEASE, needed to detect the
# ARM flags with our %%qmake_qt5 macro, including for the next patch
# From: https://gitlab.com/unity-mageia/qtwebengine5/-/blob/master/qtwebengine-opensource-src-5.9.0-fix-extractcflag.patch
Patch0002:      qtwebengine-opensource-src-5.9.0-fix-extractcflag.patch
# fix missing ARM -mfpu setting
# From: https://gitlab.com/unity-mageia/qtwebengine5/-/blob/master/qtwebengine-opensource-src-5.9.2-arm-fpu-fix.patch
Patch0003:      qtwebengine-opensource-src-5.9.2-arm-fpu-fix.patch
# remove Android dependencies from openmax_dl ARM NEON detection (detect.c)
# From: https://gitlab.com/unity-mageia/qtwebengine5/-/blob/master/qtwebengine-opensource-src-5.9.0-openmax-dl-neon.patch
Patch0004:      qtwebengine-opensource-src-5.9.0-openmax-dl-neon.patch
# webrtc: enable the CPU feature detection for ARM Linux also for Chromium
# From: https://gitlab.com/unity-mageia/qtwebengine5/-/blob/master/qtwebengine-opensource-src-5.9.0-webrtc-neon-detect.patch
Patch0005:      qtwebengine-opensource-src-5.9.0-webrtc-neon-detect.patch
# Force verbose output from the GN bootstrap process
# From: https://gitlab.com/unity-mageia/qtwebengine5/-/blob/master/qtwebengine-everywhere-src-5.10.0-gn-bootstrap-verbose.patch
Patch0006:      qtwebengine-everywhere-src-5.10.0-gn-bootstrap-verbose.patch
# Fix FTBFS with GCC 8 on i686: GCC8 has changed the alignof operator to return
# the minimal alignment required by the target ABI instead of the preferred
# alignment. This means int64_t is now 4 on i686 (instead of 8). Use __alignof__
# to get the value we expect (and chromium checks for). Patch by spot.
# From: https://gitlab.com/unity-mageia/qtwebengine5/-/blob/master/qtwebengine-everywhere-src-5.10.1-gcc8-alignof.patch
Patch0009:      qtwebengine-everywhere-src-5.10.1-gcc8-alignof.patch
Patch0010:      qtwebengine-everywhere-src-5.11.1-fix-U16_NEXT-calls.patch 
Patch6000:      qtwebengine-fix-pluse-stubs.patch

BuildRequires:  qt5-qtbase-devel qt5-qtbase-private-devel qt5-qtdeclarative-devel qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qtlocation-devel qt5-qtsensors-devel qt5-qtwebchannel-devel qt5-qttools-static
BuildRequires:  qt5-qtquickcontrols2-devel ninja-build cmake bison flex git-core gperf libicu-devel
BuildRequires:  libjpeg-devel re2-devel snappy-devel pkgconfig(expat) pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(fontconfig) pkgconfig(freetype2) pkgconfig(gl) pkgconfig(egl) pkgconfig(libpng)
BuildRequires:  pkgconfig(libudev) pkgconfig(libwebp) >= 0.6.0 pkgconfig(harfbuzz) pkgconfig(libdrm)
BuildRequires:  pkgconfig(opus) pkgconfig(libevent) pkgconfig(zlib) pkgconfig(minizip) pkgconfig(x11)
BuildRequires:  pkgconfig(xi) pkgconfig(xcursor) pkgconfig(xext) pkgconfig(xfixes) pkgconfig(xrender)
BuildRequires:  pkgconfig(xdamage) pkgconfig(xcomposite) pkgconfig(xtst) pkgconfig(xrandr) pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(libcap) pkgconfig(libpulse) pkgconfig(alsa) pkgconfig(libpci) pkgconfig(dbus-1)
BuildRequires:  pkgconfig(nss) pkgconfig(lcms2) perl-interpreter python2 pkgconfig(glib-2.0)
Provides:       bundled(chromium) = 61.0.3163.140 bundled(angle) = 2422 bundled(boringssl) bundled(brotli)
Provides:       bundled(ffmpeg) = 3.3 bundled(hunspell) = 1.6.0 bundled(iccjpeg) bundled(khronos_headers)
Provides:       bundled(leveldb) = 1.20 bundled(libjingle) bundled(libsrtp) = 2.1.0 bundled(libvpx) = 1.6.1
Provides:       bundled(libxml2) = 2.9.4 bundled(libxslt) = 1.1.29 bundled(libXNVCtrl) = 302.17
Provides:       bundled(libyuv) = 1658 bundled(modp_b64) bundled(openmax_dl) = 1.0.2 bundled(ots)
Provides:       bundled(protobuf) = 3.0.0-0.1.beta3 bundled(qcms) = 4 bundled(sfntly) bundled(skia)
Provides:       bundled(SMHasher) = 0-0.1.svn147 bundled(sqlite) = 3.20 bundled(usrsctp) bundled(webrtc) = 90
Provides:       bundled(dmg_fp) bundled(dynamic_annotations) = 4384 bundled(superfasthash) = 0 bundled(symbolize)
Provides:       bundled(valgrind.h) bundled(xdg-mime) bundled(xdg-user-dirs) = 0.10 bundled(nsURLParsers)
Provides:       bundled(mozilla_security_manager) = 1.9.2 bundled(mojo) bundled(v8) = 6.1.534.44 bundled(fdlibm) = 5.3
%ifarch x86_64
BuildRequires:  yasm
Provides:       bundled(x86inc)
%endif
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}
%{?_qt5_version:Requires: qt5-qtbase = %{_qt5_version}}

%description
Qt5 - QtWebEngine components.

%package        devel
Summary:        Development files for qt5-qtwebengine
Requires:       qt5-qtwebengine = %{version}-%{release} qt5-qtbase-devel qt5-qtdeclarative-devel

%description    devel
Qt5 - QtWebEngine components.

%package        examples
Summary:        Example files for qt5-qtwebengine

%description    examples
Example files for qt5-qtwebengine.

%prep
%autosetup -n qtwebengine-everywhere-src-%{version}%{?prerelease:-%{prerelease}} -p1
sed -i -e 's!gpu//!gpu/!g' src/3rdparty/chromium/content/renderer/gpu/compositor_forwarding_message_filter.cc
sed -i -e 's!audio_processing//!audio_processing/!g' src/3rdparty/chromium/third_party/webrtc/modules/audio_processing/utility/ooura_fft.cc \
                                                     src/3rdparty/chromium/third_party/webrtc/modules/audio_processing/utility/ooura_fft_sse2.cc
sed -i -e 's!\./!!g' src/3rdparty/chromium/third_party/angle/src/compiler/preprocessor/Tokenizer.cpp \
                     src/3rdparty/chromium/third_party/angle/src/compiler/translator/glslang_lex.cpp
sed -i -e '/toolprefix = /d' -e 's/\${toolprefix}//g' src/3rdparty/chromium/build/toolchain/linux/BUILD.gn
cp -bv /usr/include/re2/*.h src/3rdparty/chromium/third_party/re2/src/re2/
cd src/3rdparty
python2 chromium/tools/licenses.py --file-template ../../tools/about_credits.tmpl \
  --entry-template ../../tools/about_credits_entry.tmpl credits >../webengine/doc/src/qtwebengine-3rdparty.qdoc
cd -
cp -p src/3rdparty/chromium/LICENSE LICENSE.Chromium

%build
export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJA_PATH=%{__ninja}
%{qmake_qt5} CONFIG+="force_debug_info" QMAKE_EXTRA_ARGS+="-system-webengine-icu" .
%make_build

%install
make install INSTALL_ROOT=%{buildroot}
echo -e "%_qt5_qtwebengine @@NAME@@\n%_qt5_qtwebengine_epoch @@EPOCH@@\n%_qt5_qtwebengine_version @@VERSION@@\n%_qt5_qtwebengine_evr @@EVR@@" > macros.qt5-qtwebengine
install -p -m644 -D macros.qt5-qtwebengine %{buildroot}%(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)/macros.qt5-qtwebengine
rm -f macros.qt5-qtwebengine
sed -i -e "s|@@NAME@@|qt5-qtwebengine|g" -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" %{buildroot}%(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || \
  d=%{_sysconfdir}/rpm; echo $d)/macros.qt5-qtwebengine
install -d %{buildroot}%{_bindir}
cd %{buildroot}%{_qt5_bindir}
for i in * ; do ln -v  ${i} %{buildroot}%{_bindir}/${i}; done
cd -
cd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
    sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
    if [ -f "$(basename ${prl_file} .prl).so" ]; then
        rm -fv "$(basename ${prl_file} .prl).la"; sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
    fi
done
cd -
install -d %{buildroot}%{_qt5_datadir}/qtwebengine_dictionaries
%global lesser_version $(echo -e "%{version}\\n%{_qt5_version}" | sort -V | head -1)
sed -i -e "s|%{version} \${_Qt5WebEngine|%{lesser_version} \${_Qt5WebEngine|" %{buildroot}%{_qt5_libdir}/cmake/Qt5WebEngine*/Qt5WebEngine*Config.cmake

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%filetriggerin -- %{_datadir}/myspell
while read filename ; do
    case "$filename" in
        *.dic)
            bdicname=%{_qt5_datadir}/qtwebengine_dictionaries/`basename -s .dic "$filename"`.bdic
            %{_qt5_bindir}/qwebengine_convert_dict "$filename" "$bdicname" &> /dev/null || :
            ;;
    esac
done

%files
%doc LICENSE.* src/webengine/doc/src/qtwebengine-3rdparty.qdoc
%{_bindir}/qwebengine_convert_dict
%{_qt5_bindir}/qwebengine_convert_dict
%{_qt5_libdir}/{libQt5*.so.*,qt5/qml/*,qt5/libexec/QtWebEngineProcess}
%{_qt5_plugindir}/designer/libqwebengineview.so
%{_qt5_datadir}/resources/
%dir %{_qt5_datadir}/qtwebengine_dictionaries
%dir %{_qt5_translationdir}/qtwebengine_locales
%lang(am) %{_qt5_translationdir}/qtwebengine_locales/am.pak
%lang(ar) %{_qt5_translationdir}/qtwebengine_locales/ar.pak
%lang(bg) %{_qt5_translationdir}/qtwebengine_locales/bg.pak
%lang(bn) %{_qt5_translationdir}/qtwebengine_locales/bn.pak
%lang(ca) %{_qt5_translationdir}/qtwebengine_locales/ca.pak
%lang(cs) %{_qt5_translationdir}/qtwebengine_locales/cs.pak
%lang(da) %{_qt5_translationdir}/qtwebengine_locales/da.pak
%lang(de) %{_qt5_translationdir}/qtwebengine_locales/de.pak
%lang(el) %{_qt5_translationdir}/qtwebengine_locales/el.pak
%lang(en) %{_qt5_translationdir}/qtwebengine_locales/en-GB.pak
%lang(en) %{_qt5_translationdir}/qtwebengine_locales/en-US.pak
%lang(es) %{_qt5_translationdir}/qtwebengine_locales/es-419.pak
%lang(es) %{_qt5_translationdir}/qtwebengine_locales/es.pak
%lang(et) %{_qt5_translationdir}/qtwebengine_locales/et.pak
%lang(fa) %{_qt5_translationdir}/qtwebengine_locales/fa.pak
%lang(fi) %{_qt5_translationdir}/qtwebengine_locales/fi.pak
%lang(fil) %{_qt5_translationdir}/qtwebengine_locales/fil.pak
%lang(fr) %{_qt5_translationdir}/qtwebengine_locales/fr.pak
%lang(gu) %{_qt5_translationdir}/qtwebengine_locales/gu.pak
%lang(he) %{_qt5_translationdir}/qtwebengine_locales/he.pak
%lang(hi) %{_qt5_translationdir}/qtwebengine_locales/hi.pak
%lang(hr) %{_qt5_translationdir}/qtwebengine_locales/hr.pak
%lang(hu) %{_qt5_translationdir}/qtwebengine_locales/hu.pak
%lang(id) %{_qt5_translationdir}/qtwebengine_locales/id.pak
%lang(it) %{_qt5_translationdir}/qtwebengine_locales/it.pak
%lang(ja) %{_qt5_translationdir}/qtwebengine_locales/ja.pak
%lang(kn) %{_qt5_translationdir}/qtwebengine_locales/kn.pak
%lang(ko) %{_qt5_translationdir}/qtwebengine_locales/ko.pak
%lang(lt) %{_qt5_translationdir}/qtwebengine_locales/lt.pak
%lang(lv) %{_qt5_translationdir}/qtwebengine_locales/lv.pak
%lang(ml) %{_qt5_translationdir}/qtwebengine_locales/ml.pak
%lang(mr) %{_qt5_translationdir}/qtwebengine_locales/mr.pak
%lang(ms) %{_qt5_translationdir}/qtwebengine_locales/ms.pak
%lang(nb) %{_qt5_translationdir}/qtwebengine_locales/nb.pak
%lang(nl) %{_qt5_translationdir}/qtwebengine_locales/nl.pak
%lang(pl) %{_qt5_translationdir}/qtwebengine_locales/pl.pak
%lang(pt_BR) %{_qt5_translationdir}/qtwebengine_locales/pt-BR.pak
%lang(pt_PT) %{_qt5_translationdir}/qtwebengine_locales/pt-PT.pak
%lang(ro) %{_qt5_translationdir}/qtwebengine_locales/ro.pak
%lang(ru) %{_qt5_translationdir}/qtwebengine_locales/ru.pak
%lang(sk) %{_qt5_translationdir}/qtwebengine_locales/sk.pak
%lang(sl) %{_qt5_translationdir}/qtwebengine_locales/sl.pak
%lang(sr) %{_qt5_translationdir}/qtwebengine_locales/sr.pak
%lang(sv) %{_qt5_translationdir}/qtwebengine_locales/sv.pak
%lang(sw) %{_qt5_translationdir}/qtwebengine_locales/sw.pak
%lang(ta) %{_qt5_translationdir}/qtwebengine_locales/ta.pak
%lang(te) %{_qt5_translationdir}/qtwebengine_locales/te.pak
%lang(th) %{_qt5_translationdir}/qtwebengine_locales/th.pak
%lang(tr) %{_qt5_translationdir}/qtwebengine_locales/tr.pak
%lang(uk) %{_qt5_translationdir}/qtwebengine_locales/uk.pak
%lang(vi) %{_qt5_translationdir}/qtwebengine_locales/vi.pak
%lang(zh_CN) %{_qt5_translationdir}/qtwebengine_locales/zh-CN.pak
%lang(zh_TW) %{_qt5_translationdir}/qtwebengine_locales/zh-TW.pak

%files devel
%(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)/macros.qt5-qtwebengine
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/{libQt5*.so,libQt5*.prl,cmake/Qt5*/,pkgconfig/Qt5*.pc}
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files examples
%{_qt5_examplesdir}/

%changelog
* Fri Jul 24 2020 maminjie <maminjie1@huawei.com> -5.11.1-10
- Fix the build error for U16_NEXT calls

* Sun Jun 28 2020 huanghaitao <huanghaitao8@huawei.com> -5.11.1-9
- Fix the build errors with conflicting declaration of C

* Sat Jun 20 2020 huanghaitao <huanghaitao8@huawei.com> -5.11.1-8
- Solved the unresolved problem

* Wed Mar 18 2020 gulining <gulining1@huawei.com> - 5.11.1-7
- Fix build error

* Wed Mar 18 2020 yanglijin <yanglijin@huawei.com> - 5.11.1-6
- Remove help package

* Fri Mar 6 2020 Ling Yang <lingyang2@huawei.com> - 5.11.1-5
- Package Init
