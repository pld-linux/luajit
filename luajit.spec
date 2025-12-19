# TODO
# - x32 not supported by upstream: http://www.freelists.org/post/luajit/Building-luajit202-on-x32,1
#
# Conditional build:
%bcond_without	lua51		# LuaJIT without Lua 5.2 extensions
%bcond_without	lua52		# LuaJIT with Lua 5.2 extensions

%define		snap		20251208
%define		rel		2
# git show -s --format=%ct
%define		rolling_ver	1765228720
Summary:	Just-in-Time compiler for Lua
Summary(pl.UTF-8):	Kompilator JIT dla języka Lua
Name:		luajit
Version:	2.1.0
Release:	0.%{snap}.%{rel}
License:	MIT
Group:		Libraries
# Source0Download: http://luajit.org/download.html
Source0:	%{name}-%{version}-%{snap}.tar.xz
# Source0-md5:	0b581f57990134db706b41360a4b54ff
Patch0:		config.patch
Patch1:		abi-5.2.patch
URL:		http://luajit.org/
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 mips mips64 mipsel ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		luajit_abi	2.1

%description
LuaJIT is a Just-In-Time (JIT) compiler for the Lua programming
language.

%description -l pl.UTF-8
LuaJIT to działający w locie (Just-In-Time) kompilator języka Lua.

%package common
Summary:	Common files for LuaJIT libraries
Summary(pl.UTF-8):	Pliki wspólne dla bibliotek LuaJIT
Group:		Libraries
Conflicts:	luajit-libs < 2.1.0-0.20240704.5

%description common
Common files for LuaJIT libraries.

%description common -l pl.UTF-8
Pliki wspólne dla bibliotek LuaJIT.

%package libs
Summary:	LuaJIT libraries
Summary(pl.UTF-8):	Biblioteki LuaJIT
Group:		Libraries
Requires:	%{name}-common = %{version}-%{release}

%description libs
LuaJIT libraries.

%description libs -l pl.UTF-8
Biblioteki LuaJIT.

%package common-devel
Summary:	Common header files for LuaJIT library
Summary(pl.UTF-8):	Wspólne pliki nagłówkowe biblioteki LuaJIT
Group:		Development/Libraries
Conflicts:	luajit-devel < 2.1.0-0.20240704.5

%description common-devel
Common header files for LuaJIT library.

%description common-devel -l pl.UTF-8
Wspólne pliki nagłówkowe biblioteki LuaJIT.

%package devel
Summary:	Header files for LuaJIT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LuaJIT
Group:		Development/Libraries
Requires:	%{name}-common-devel = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for LuaJIT library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LuaJIT.

%package static
Summary:	Static LuaJIT library
Summary(pl.UTF-8):	Statyczna biblioteka LuaJIT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LuaJIT library.

%description static -l pl.UTF-8
Statyczna biblioteka LuaJIT.

%package -n luajit52
Summary:	Just-in-Time compiler for Lua (with Lua 5.2 extensions)
Summary(pl.UTF-8):	Kompilator JIT dla języka Lua (z rozszerzeniami Lua 5.2)
Group:		Libraries
Requires:	luajit52-libs = %{version}-%{release}

%description -n luajit52
LuaJIT is a Just-In-Time (JIT) compiler for the Lua programming
language (with Lua 5.2 extensions).

%description -n luajit52 -l pl.UTF-8
LuaJIT to działający w locie (Just-In-Time) kompilator języka Lua (z
rozszerzeniami Lua 5.2).

%package -n luajit52-libs
Summary:	LuaJIT libraries (with Lua 5.2 extensions)
Summary(pl.UTF-8):	Biblioteki LuaJIT (z rozszerzeniami Lua 5.2)
Group:		Libraries
Requires:	%{name}-common = %{version}-%{release}

%description -n luajit52-libs
LuaJIT libraries (with Lua 5.2 extensions).

%description -n luajit52-libs -l pl.UTF-8
Biblioteki LuaJIT (z rozszerzeniami Lua 5.2).

%package -n luajit52-devel
Summary:	Header files for LuaJIT library (with Lua 5.2 extensions)
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LuaJIT (z rozszerzeniami Lua 5.2)
Group:		Development/Libraries
Requires:	%{name}-common-devel = %{version}-%{release}
Requires:	luajit52-libs = %{version}-%{release}

%description -n luajit52-devel
Header files for LuaJIT library (with Lua 5.2 extensions).

%description -n luajit52-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LuaJIT (z rozszerzeniami Lua 5.2).

%package -n luajit52-static
Summary:	Static LuaJIT library (with Lua 5.2 extensions)
Summary(pl.UTF-8):	Statyczna biblioteka LuaJIT (z rozszerzeniami Lua 5.2)
Group:		Development/Libraries
Requires:	luajit52-devel = %{version}-%{release}

%description -n luajit52-static
Static LuaJIT library (with Lua 5.2 extensions).

%description -n luajit52-static -l pl.UTF-8
Statyczna biblioteka LuaJIT (z rozszerzeniami Lua 5.2).

%prep
%setup -qcT
%if %{with lua51}
tar --one-top-level=luajit-51 --strip-components=1 -xf %{SOURCE0}
cd luajit-51
%patch -P 0 -p1

# preserve timestamps
sed -i -e '/install -m/s/-m/-p -m/' Makefile

echo %{rolling_ver} > .relver
cd ..
%endif
%if %{with lua52}
tar --one-top-level=luajit-52 --strip-components=1 -xf %{SOURCE0}
cd luajit-52
%patch -P 0 -p1
%patch -P 1 -p1

# preserve timestamps
sed -i -e '/install -m/s/-m/-p -m/' Makefile

echo %{rolling_ver} > .relver
cd ..
%endif

%build
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
for v in %{?with_lua51:51} %{?with_lua52:52}; do
%{__make} -C luajit-$v \
	VERSION="%{version}" \
	PREFIX=%{_prefix} \
	MULTILIB=%{_lib} \
	LMULTILIB=%{_lib} \
	CC="%{__cc}" \
	CCOPT="%{rpmcflags} -fomit-frame-pointer" \
	CCOPT_x86= \
	LDFLAGS="%{rpmldflags}" \
	TARGET_STRIP=: \
	E="@:" \
	Q= \
	amalg
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/luajit/%{luajit_abi}

%if %{with lua52}
%{__make} -C luajit-52 install \
	DESTDIR=$RPM_BUILD_ROOT \
	VERSION="%{version}" \
	PREFIX=%{_prefix} \
	MULTILIB=%{_lib} \
	LMULTILIB=%{_lib} \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_SHARE=$RPM_BUILD_ROOT%{_datadir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTALL_PKGCONFIG=$RPM_BUILD_ROOT%{_pkgconfigdir} \
	LDCONFIG="/sbin/ldconfig -n"
%{__mv} $RPM_BUILD_ROOT%{_bindir}/luajit{,52}-%{version}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/luajit
%{__ln_s} luajit52-%{version} $RPM_BUILD_ROOT%{_bindir}/luajit52
%{__mv} $RPM_BUILD_ROOT%{_pkgconfigdir}/luajit{,52}.pc
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/luajit{,52}.1
%endif

%if %{with lua51}
%{__make} -C luajit-51 install \
	DESTDIR=$RPM_BUILD_ROOT \
	VERSION="%{version}" \
	PREFIX=%{_prefix} \
	MULTILIB=%{_lib} \
	LMULTILIB=%{_lib} \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_SHARE=$RPM_BUILD_ROOT%{_datadir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTALL_PKGCONFIG=$RPM_BUILD_ROOT%{_pkgconfigdir} \
	LDCONFIG="/sbin/ldconfig -n"
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n luajit52-libs -p /sbin/ldconfig
%postun	-n luajit52-libs -p /sbin/ldconfig

%if %{with lua51}
%files
%defattr(644,root,root,755)
%doc luajit-51/{COPYRIGHT,README}
%attr(755,root,root) %{_bindir}/luajit
%attr(755,root,root) %{_bindir}/luajit-%{version}
%{_mandir}/man1/luajit.1*
%endif

%files common
%defattr(644,root,root,755)
%dir %{_libdir}/luajit
%dir %{_libdir}/luajit/%{luajit_abi}
%dir %{_datadir}/luajit
%{_datadir}/luajit/%{luajit_abi}
%dir %{_libdir}/lua

%if %{with lua51}
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libluajit-5.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libluajit-5.1.so.2
# lua module dirs (shared with lua interpreters)
%dir %{_libdir}/lua/5.1
%dir %{_datadir}/lua/5.1
%endif

%files common-devel
%defattr(644,root,root,755)
%doc luajit-%{?with_lua51:51}%{!?with_lua51:52}/doc/*
%{_includedir}/luajit-%{luajit_abi}

%if %{with lua51}
%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libluajit-5.1.so
%{_pkgconfigdir}/luajit.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libluajit-5.1.a
%endif

%if %{with lua52}
%files -n luajit52
%defattr(644,root,root,755)
%doc luajit-52/{COPYRIGHT,README}
%attr(755,root,root) %{_bindir}/luajit52
%attr(755,root,root) %{_bindir}/luajit52-%{version}
%{_mandir}/man1/luajit52.1*

%files -n luajit52-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libluajit-5.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libluajit-5.2.so.2
# lua module dirs (shared with lua interpreters)
%dir %{_libdir}/lua/5.2
%dir %{_datadir}/lua/5.2

%files -n luajit52-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libluajit-5.2.so
%{_pkgconfigdir}/luajit52.pc

%files -n luajit52-static
%defattr(644,root,root,755)
%{_libdir}/libluajit-5.2.a
%endif
