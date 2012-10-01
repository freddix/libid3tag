Summary:	Library for reading and writing ID3 tags
Name:		libid3tag
Version:	0.15.1b
Release:	13
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.mars.org/pub/mpeg/%{name}-%{version}.tar.gz
# Source0-md5:	e5808ad997ba32c498803822078748c3
Patch0:		%{name}-id3v23.patch
URL:		http://www.underbit.com/products/mad/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libid3tag is a library for reading and (eventually) writing ID3 tags,
both ID3v1 and the various versions of ID3v2.

%package devel
Summary:	Header files for libid3tag
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libid3tag.

%prep
%setup -q
%patch0 -p1

# Create an additional pkgconfig file
%{__cat} > id3tag.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: id3tag
Description: ID3 tag library
Requires:
Version: %{version}
Libs: -L%{_libdir} -lid3tag -lz
Cflags: -I%{_includedir}
EOF

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
install id3tag.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES COPYRIGHT CREDITS README TODO
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_pkgconfigdir}/id3tag.pc
