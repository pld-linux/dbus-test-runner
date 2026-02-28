#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library to assist testing with a fresh DBus daemon
Summary(pl.UTF-8):	Biblioteka wspomagające testowanie z użyciem demona DBus
Name:		dbus-test-runner
Version:	12.10.1
Release:	2
License:	GPL v3+
Group:		Libraries
Source0:	https://launchpad.net/dbus-test-runner/12.10/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	810dc82f9e06401ad903156bacc7008f
URL:		https://launchpad.net/dbus-test-runner
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.30
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library to assist testing with a fresh DBus daemon.

%description -l pl.UTF-8
Biblioteka wspomagające testowanie z użyciem demona DBus.

%package devel
Summary:	Header files for dbustest library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dbustest
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.30

%description devel
Header files for dbustest library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dbustest.

%package static
Summary:	Static dbustest library
Summary(pl.UTF-8):	Statyczna biblioteka dbustest
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static dbustest library.

%description static -l pl.UTF-8
Statyczna biblioteka dbustest.

%prep
%setup -q

%{__sed} -i -e 's/-Werror //' libdbustest/Makefile.am src/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdbustest.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-test-runner
%attr(755,root,root) %{_libdir}/libdbustest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdbustest.so.1
%{_datadir}/dbus-test-runner

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbustest.so
%{_includedir}/libdbustest-1
%{_pkgconfigdir}/dbustest-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdbustest.a
%endif
