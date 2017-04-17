Summary:	Intel LLDP Agent
Name:		lldpad
Version:	1.0.1
Release:	1
License:	GPL v2
Group:		Daemons
# git://www.open-lldp.org/open-lldp.git
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	602088dcb826d0b7966eafe2c082fe46
Patch0:		systemd-in-roor.patch
URL:		http://open-lldp.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex >= 2.5.33
BuildRequires:	kernel-headers >= 2.6.32
BuildRequires:	libconfig-devel >= 1.3.2
BuildRequires:	libnl-devel
BuildRequires:	libtool
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	systemd
Requires:	readline
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux user space daemon and configuration
tool for Intel LLDP Agent with Enhanced Ethernet support for the Data
Center.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains header files for developing
applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
export CFLAGS="%{rpmcflags} -Wno-error"
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_post %{name}.service %{name}.socket

%preun
%systemd_preun %{name}.service %{name}.socket

%postun
/sbin/ldconfig
%systemd_reload

%files
%defattr(644,root,root,755)
%doc COPYING README ChangeLog
%{_sysconfdir}/bash_completion.d/*
%attr(755,root,root) %{_sbindir}/dcbtool
%attr(755,root,root) %{_sbindir}/lldpad
%attr(755,root,root) %{_sbindir}/lldptool
%attr(755,root,root) %{_libdir}/liblldp_clif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblldp_clif.so.1
%{systemdunitdir}/%{name}.service
%{systemdunitdir}/%{name}.socket
%dir %{_sharedstatedir}/%{name}
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
l%{_mandir}/man8/ldptool-vdp.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblldp_clif.so
%{_includedir}/lldpad
%{_pkgconfigdir}/liblldp_clif.pc
%{_pkgconfigdir}/liblldp.pc
