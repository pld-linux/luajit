Summary:	Just-in-Time compiler for Lua
Summary(pl.UTF-8):	Kompilator JIT dla języka Lua
Name:		luajit
Version:	2.0.3
Release:	2
License:	MIT
Group:		Libraries
# Source0Download: http://luajit.org/download.html
Source0:	http://luajit.org/download/LuaJIT-%{version}.tar.gz
# Source0-md5:	f14e9104be513913810cd59c8c658dc0
URL:		http://luajit.org/
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664} arm mips ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		lua_abi		5.1

%description
LuaJIT is a Just-In-Time (JIT) compiler for the Lua programming
language.

%description -l pl.UTF-8
LuaJIT to działający w locie (Just-In-Time) kompilator języka Lua.

%package devel
Summary:	Header files for LuaJIT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LuaJIT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
%setup -q -n LuaJIT-%{version}

# preserve timestamps
sed -i -e '/install -m/s/-m/-p -m/' Makefile

%build
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
%{__make} \
	PREFIX=%{_prefix} \
	MULTILIB=%{_lib} \
	CC="%{__cc}" \
	CCOPT="%{rpmcflags} -fomit-frame-pointer" \
	CCOPT_x86= \
	MULTILIB=%{_lib} \
	E="@:" \
	Q= \
	amalg

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	MULTILIB=%{_lib} \
	LDCONFIG="/sbin/ldconfig -n"

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README
%attr(755,root,root) %{_bindir}/luajit
%attr(755,root,root) %{_bindir}/luajit-%{version}
%attr(755,root,root) %{_libdir}/libluajit-%{lua_abi}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libluajit-%{lua_abi}.so.2
%{_datadir}/luajit-%{version}
%{_mandir}/man1/luajit.1*
# lua module dirs (shared with lua interpreters)
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{lua_abi}
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{lua_abi}

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/libluajit-%{lua_abi}.so
%{_includedir}/luajit-2.0
%{_pkgconfigdir}/luajit.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libluajit-%{lua_abi}.a
