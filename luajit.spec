# TODO
# - x32 not supported by upstream: http://www.freelists.org/post/luajit/Building-luajit202-on-x32,1

%define		snap		20221222
Summary:	Just-in-Time compiler for Lua
Summary(pl.UTF-8):	Kompilator JIT dla języka Lua
Name:		luajit
Version:	2.1.0
Release:	0.%{snap}.1
License:	MIT
Group:		Libraries
# Source0Download: http://luajit.org/download.html
Source0:	%{name}-%{version}-%{snap}.tar.xz
# Source0-md5:	1b06e2bcacc09537f9d67dc3d636bd84
Patch0:		config.patch
URL:		http://luajit.org/
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 mips mips64 mipsel ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		lua_abi		5.1
%define		luajit_abi		2.1

%description
LuaJIT is a Just-In-Time (JIT) compiler for the Lua programming
language.

%description -l pl.UTF-8
LuaJIT to działający w locie (Just-In-Time) kompilator języka Lua.

%package libs
Summary:	LuaJIT libraries
Summary(pl.UTF-8):	Biblioteki LuaJIT
Group:		Libraries

%description libs
LuaJIT libraries.

%description libs -l pl.UTF-8
Biblioteki LuaJIT.

%package devel
Summary:	Header files for LuaJIT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LuaJIT
Group:		Development/Libraries
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

%prep
%setup -q -n luajit
%patch0 -p1

# preserve timestamps
sed -i -e '/install -m/s/-m/-p -m/' Makefile

%build
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
%{__make} \
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

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/luajit/%{luajit_abi}

%{__make} install \
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

ln -s luajit-%{version} $RPM_BUILD_ROOT%{_bindir}/luajit

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README
%attr(755,root,root) %{_bindir}/luajit
%attr(755,root,root) %{_bindir}/luajit-%{version}
%{_mandir}/man1/luajit.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libluajit-%{lua_abi}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libluajit-%{lua_abi}.so.2
%dir %{_libdir}/luajit
%dir %{_libdir}/luajit/%{luajit_abi}
%dir %{_datadir}/luajit
%{_datadir}/luajit/%{luajit_abi}
# lua module dirs (shared with lua interpreters)
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{lua_abi}
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{lua_abi}

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/libluajit-%{lua_abi}.so
%{_includedir}/luajit-%{luajit_abi}
%{_pkgconfigdir}/luajit.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libluajit-%{lua_abi}.a
