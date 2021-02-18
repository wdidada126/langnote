Name:           libpng
Epoch:          2
Version:        1.6.36
Release:        3
Summary:        A library of functions for manipulating PNG image format files
License:        zlib
URL:            http://www.libpng.org/pub/png/libpng.html
Source0:        https://github.com/glennrp/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        pngusr.dfa

Patch0:         libpng-multilib.patch
Patch1:         libpng-fix-arm-neon.patch
Patch2:         libpng-CVE-2019-7317.patch
Patch3:		libpng-CVE-2018-14550.patch

BuildRequires:  zlib-devel autoconf automake libtool
Provides:       libpng-tools
Obsoletes:      libpng-tools

%description
The libpng package contains libraries used by other programs for reading and writing PNG format files.
The PNG format was designed as a replacement for GIF and, to a lesser extent, TIFF,
with many improvements and extensions and lack of patent problems.

%package        devel
Summary:        Development files for libpng
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release} zlib-devel%{?_isa} pkgconfig%{?_isa}

Provides:       libpng-static
Obsoletes:      libpng-static

%description    devel
The libpng-devel package contains libraries and header files for developing
applications that using the PNG library.

%package        help
Summary:        Help documents for libpng

%description    help
This package contain the license files and help documents for libpng.

%prep
%autosetup -n %{name}-%{version} -p1
cp -p %{SOURCE1} .

%build
autoreconf -vif
%configure
%make_build DFA_XTRA=pngusr.dfa

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%if %{?_with_check:1}%{!?_with_check:0}
make check
%endif

%ldconfig_post
%ldconfig_postun

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libpng16.so.*

%files devel
%{_bindir}/*
%{_includedir}/*
%{_libdir}/libpng*.so
%{_libdir}/libpng*.a
%{_libdir}/pkgconfig/libpng*.pc

%files help
%doc libpng-manual.txt example.c TODO CHANGES
%{_mandir}/man*/*

%changelog
* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.6.36-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:optimization the spec

* Wed Sep 18 2019 chenzhenyu <chenzhenyu13@huawei.com> - 1.6.36-2
- Package init
