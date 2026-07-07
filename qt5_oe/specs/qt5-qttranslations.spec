%global _qt5_qmake %{_bindir}/qmake-qt5

Name:          qt5-qttranslations
Version:       5.15.2
Release:       3
Summary:       Qt5 - QtTranslations module

License:       LGPLv2 with exceptions or GPLv3 with exceptions and GFDL-1.1-or-later
Url:           http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/qttranslations-everywhere-src-%{version}.tar.xz
Patch01: 0001-add-translation-about-QPlatformTheme.patch
BuildArch:     noarch
BuildRequires: make
BuildRequires: qt5-qtbase-devel qt5-linguist

%if 0%{?_qt5:1}
Provides:      %{_qt5}-ar = %{version}-%{release} %{_qt5}-ca = %{version}-%{release}
Provides:      %{_qt5}-cs = %{version}-%{release} %{_qt5}-da = %{version}-%{release}
Provides:      %{_qt5}-de = %{version}-%{release} %{_qt5}-es = %{version}-%{release}
Provides:      %{_qt5}-fa = %{version}-%{release} %{_qt5}-fi = %{version}-%{release}
Provides:      %{_qt5}-fr = %{version}-%{release} %{_qt5}-gl = %{version}-%{release}
Provides:      %{_qt5}-gd = %{version}-%{release} %{_qt5}-he = %{version}-%{release}
Provides:      %{_qt5}-hu = %{version}-%{release} %{_qt5}-it = %{version}-%{release}
Provides:      %{_qt5}-ja = %{version}-%{release} %{_qt5}-ko = %{version}-%{release}
Provides:      %{_qt5}-lt = %{version}-%{release} %{_qt5}-lv = %{version}-%{release}
Provides:      %{_qt5}-pl = %{version}-%{release} %{_qt5}-pt = %{version}-%{release}
Provides:      %{_qt5}-ru = %{version}-%{release} %{_qt5}-sk = %{version}-%{release}
Provides:      %{_qt5}-sl = %{version}-%{release} %{_qt5}-sv = %{version}-%{release}
Provides:      %{_qt5}-uk = %{version}-%{release} %{_qt5}-zh_CN = %{version}-%{release}
Provides:      %{_qt5}-zh_TW = %{version}-%{release}
%endif

%description
Translation module for Qt Project apps.

%prep
%autosetup -n qttranslations-everywhere-src-%{version} -p1

%build
%{qmake_qt5}
%make_build

%install
make install INSTALL_ROOT=%{buildroot}

%files
%license LICENSE.*
%lang(ar) %{_qt5_translationdir}/*_ar.qm
%lang(bg) %{_qt5_translationdir}/*_bg.qm
%lang(ca) %{_qt5_translationdir}/*_ca.qm
%lang(cs) %{_qt5_translationdir}/*_cs.qm
%lang(da) %{_qt5_translationdir}/*_da.qm
%lang(de) %{_qt5_translationdir}/*_de.qm
%lang(es) %{_qt5_translationdir}/*_es.qm
%lang(en) %{_qt5_translationdir}/*_en.qm
%lang(fa) %{_qt5_translationdir}/*_fa.qm
%lang(fi) %{_qt5_translationdir}/*_fi.qm
%lang(fr) %{_qt5_translationdir}/*_fr.qm
%lang(gl) %{_qt5_translationdir}/*_gd.qm
%lang(gl) %{_qt5_translationdir}/*_gl.qm
%lang(he) %{_qt5_translationdir}/*_he.qm
%lang(hu) %{_qt5_translationdir}/*_hu.qm
%lang(it) %{_qt5_translationdir}/*_it.qm
%lang(ja) %{_qt5_translationdir}/*_ja.qm
%lang(ko) %{_qt5_translationdir}/*_ko.qm
%lang(lt) %{_qt5_translationdir}/*_lt.qm
%lang(lt) %{_qt5_translationdir}/*_lv.qm
%lang(pl) %{_qt5_translationdir}/*_pl.qm
%lang(pt) %{_qt5_translationdir}/*_pt.qm
%lang(ru) %{_qt5_translationdir}/*_ru.qm
%lang(sk) %{_qt5_translationdir}/*_sk.qm
%lang(sl) %{_qt5_translationdir}/*_sl.qm
%lang(sv) %{_qt5_translationdir}/*_sv.qm
%lang(sv) %{_qt5_translationdir}/*_tr.qm
%lang(uk) %{_qt5_translationdir}/*_uk.qm
%lang(zh_CN) %{_qt5_translationdir}/*_zh_CN.qm
%lang(zh_TW) %{_qt5_translationdir}/*_zh_TW.qm


%changelog
* Wed May 31 2023 peijiankang <peijiankang@kylinos.cn> - 5.15.2-3
- add translation about QPlatformTheme

* Wed Jul 13 2022 Chenyx <chenyixiong3@huawei.com> - 5.15.2-2
- License compliance rectification

* Wed Oct 13 2021 peijiankang <peijiankang@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-5
- Fix Source0 

* Fri Feb 14 2020 lingsheng <lingsheng@huawei.com> - 5.11.1-4
- Package init
