Summary:	Intel LLDP Agent
Summary(pl.UTF-8):	Agent LLDP firmy Intel
Name:		lldpad
Version:	1.1.1
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	https://github.com/intel/openlldp/archive/v%{version}/openlldp-%{version}.tar.gz
# Source0-md5:	7d5ff2233cd8ee26c8124f4b741d6acb
Patch0:		systemd-in-roor.patch
URL:		https://github.com/intel/openlldp
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	flex >= 2.5.33
BuildRequires:	linux-libc-headers >= 2.6.32
BuildRequires:	libconfig-devel >= 1.3.2
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	systemd-devel
Requires(post,preun,postun):	systemd-units >= 38
Requires:	iproute2-tc >= 2.6.29
Requires:	systemd-units >= 38
Requires:	uname(release) >= 2.6.29
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux user space daemon and configuration
tool for Intel LLDP Agent with Enhanced Ethernet support for the Data
Center.

%description -l pl.UTF-8
Ten pakiet zawiera demona przestrzeni użytkownika dla Linuksa oraz
narzędzie konfiguracyjne agenta LLDP firmy Intel z obsługą Enhanced
Ethernet dla DC.

%package devel
Summary:	Development files for LLDP Agent and its communication library
Summary(pl.UTF-8):	Pliki programistyczne agenta LLDP i jego biblioteki komunikacyjnej
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains header files for developing applications that
use LLDP Agent.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe to tworzenia aplikacji
wykorzystujących agenta LLDP.

%prep
%setup -q -n openlldp-%{version}
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/lldpad

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	bashcompletiondir=%{bash_compdir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_post lldpad.service lldpad.socket

%preun
%systemd_preun lldpad.service lldpad.socket

%postun
/sbin/ldconfig
%systemd_reload

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_sbindir}/dcbtool
%attr(755,root,root) %{_sbindir}/lldpad
%attr(755,root,root) %{_sbindir}/lldptool
%attr(755,root,root) %{_sbindir}/vdptool
%attr(755,root,root) %{_libdir}/liblldp_clif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblldp_clif.so.1
%{systemdunitdir}/lldpad.service
%{systemdunitdir}/lldpad.socket
%dir /var/lib/lldpad
%{bash_compdir}/lldpad
%{bash_compdir}/lldptool
%{_mandir}/man8/dcbtool.8*
%{_mandir}/man8/lldpad.8*
%{_mandir}/man8/lldptool.8*
%{_mandir}/man8/lldptool-app.8*
%{_mandir}/man8/lldptool-dcbx.8*
%{_mandir}/man8/lldptool-ets.8*
%{_mandir}/man8/lldptool-evb22.8*
%{_mandir}/man8/lldptool-evb.8*
%{_mandir}/man8/lldptool-med.8*
%{_mandir}/man8/lldptool-pfc.8*
%{_mandir}/man8/lldptool-vdp.8*
%{_mandir}/man8/vdptool.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblldp_clif.so
%{_includedir}/lldpad
%{_pkgconfigdir}/liblldp_clif.pc
%{_pkgconfigdir}/lldpad.pc
%{_mandir}/man3/liblldp_clif-vdp22.3*
