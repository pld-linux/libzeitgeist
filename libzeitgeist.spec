#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	Zeitgeist client library
Summary(pl.UTF-8):	Biblioteka kliencka Zeitgeist
Name:		libzeitgeist
Version:	0.3.18
Release:	6
License:	LGPL v2+
Group:		Libraries
Source0:	http://launchpad.net/libzeitgeist/0.3/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	d63a37295d01a58086d0d4ae26e604c2
Patch0:		%{name}-am.patch
URL:		http://zeitgeist-project.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	glib2 >= 1:2.26.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a client library for applications that want to
interact with the Zeitgeist daemon.

%description -l pl.UTF-8
Ten pakiet dostarcza bibliotekę kliencką dla aplikacji chcących
współdziałać z demonem Zeitgeist.

%package devel
Summary:	Header files for zeitgeist library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki zeitgeist
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26.0

%description devel
Header files for zeitgeist library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki zeitgeist.

%package static
Summary:	Static zeitgeist library
Summary(pl.UTF-8):	Statyczna biblioteka zeitgeist
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static zeitgeist library.

%description static -l pl.UTF-8
Statyczna biblioteka zeitgeist.

%package apidocs
Summary:	zeitgeist library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki zeitgeist
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API documentation for zeitgeist library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki zeitgeist.

%package -n vala-zeitgeist1
Summary:	Vala API for zeitgeist library
Summary(pl.UTF-8):	API języka Vala dla biblioteki zeitgeist
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
Conflicts:	vala-zeitgeist < 0.3.18-3
BuildArch:	noarch

%description -n vala-zeitgeist1
Vala API for zeitgeist library.

%description -n vala-zeitgeist1 -l pl.UTF-8
API języka Vala dla biblioteki zeitgeist.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
	%{__enable_disable apidocs gtk-doc} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libzeitgeist

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libzeitgeist-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzeitgeist-1.0.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzeitgeist-1.0.so
%{_includedir}/zeitgeist-1.0
%{_pkgconfigdir}/zeitgeist-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzeitgeist-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/zeitgeist-1.0
%endif

%files -n vala-zeitgeist1
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/zeitgeist-1.0.deps
%{_datadir}/vala/vapi/zeitgeist-1.0.vapi
