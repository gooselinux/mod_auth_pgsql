%define contentdir /var/www

Summary: Basic authentication for the Apache HTTP Server using a PostgreSQL database
Name: mod_auth_pgsql
Version: 2.0.3
Release: 10.1%{?dist}
Group: System Environment/Daemons
URL: http://www.giuseppetanzilli.it/mod_auth_pgsql2/
Source: http://www.giuseppetanzilli.it/mod_auth_pgsql2/dist/mod_auth_pgsql-%{version}.tar.gz
Source1: auth_pgsql.conf
Patch0: mod_auth_pgsql-2.0.1-nonpgsql.patch
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: httpd-devel >= 2.0.40-6, postgresql-devel
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing)

%description
mod_auth_pgsql can be used to authenticate remote users of the
Apache HTTP Server based on queries against in a PostgresQL
database.

%prep
%setup -q
%patch0 -p1 -b .nonpgsql

%build
%{_sbindir}/apxs -Wc,-Wformat-security -c %{name}.c -lpq

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m755 .libs/%{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

# Extract the licensing conditions
sed -n '1,/^ \*\/$/p' mod_auth_pgsql.c > LICENSE

# Install the manual
mkdir -p $RPM_BUILD_ROOT%{contentdir}/manual/mod
cp *.html $RPM_BUILD_ROOT%{contentdir}/manual/mod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README INSTALL LICENSE
%{contentdir}/manual/mod/*.html
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.0.3-10.1
- Rebuilt for RHEL 6

* Fri Aug 07 2009 Parag <paragn@fedoraproject.org> 2.0.3-10
- Spec cleanup as suggested in review bug #226153

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.3-7
- Autorebuild for GCC 4.3

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 2.0.3-6
- rebuild for fixed APR

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 2.0.3-5
- fix License, and package the license text

* Wed Jun 20 2007 Joe Orton <jorton@redhat.com> 2.0.3-4
- convert %%changelog file to UTF-8; use standard BuildRoot;
  tweak %%summary and %%description

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 2.0.3-3
- rebuild for new libpq

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.3-2.3.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.3-2.3
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.3-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan  6 2006 Joe Orton <jorton@redhat.com> 2.0.3-2
- update to 2.0.3 (includes fix for CVE-2005-3656)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Joe Orton <jorton@redhat.com> 2.0.1-9
- rebuild for httpd-2.2
- don't strip DSO so debuginfo works

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 2.0.1-8
- rebuild for new libpq

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 2.0.1-7
- fix possible crashes (Mirko Streckenbach, #150087)

* Thu Sep 23 2004 Joe Orton <jorton@redhat.com> 2.0.1-5
- merge from Taroon:
 * don't re-use database connections (#115496)
 * make functions static
 * downgrade "not configured" log message from warning to debug

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 13 2003 Joe Orton <jorton@redhat.com> 2.0.1-2
- rebuild for httpd-2.0.45

* Tue May 13 2003 Gary Benson <gbenson@redhat.com> 2.0.1-1
- upgrade to 2.0.1.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.9.12-14
- rebuilt

* Mon Jan 13 2003 Joe Orton <jorton@redhat.com> 0.9.12-13
- rebuild for new libpq

* Wed Nov  6 2002 Joe Orton <jorton@redhat.com> 0.9.12-12
- rebuild in new environment

* Mon Sep  2 2002 Joe Orton <jorton@redhat.com> 0.9.12-11
- require httpd-mmn to enforce module ABI compatibility

* Fri Aug 29 2002 Gary Benson <gbenson@redhat.com> 0.9.12-10
- add some examples to /etc/httpd/conf.d/auth_pgsql.conf (#71318)

* Mon Aug 12 2002 Gary Benson <gbenson@redhat.com> 0.9.12-9
- rebuild against httpd-2.0.40

* Fri Jun 21 2002 Gary Benson <gbenson@redhat.com> 0.9.12-8
- move /etc/httpd2 back to /etc/httpd

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.9.12-7
- automated rebuild

* Fri May 31 2002 Gary Benson <gbenson@redhat.com> 0.9.12-6
- port to httpd-2.0
- add the config file
- put the manual in with the Apache manual
- license is Apache Software License

* Sun May 26 2002 Tim Powers <timp@redhat.com> 0.9.12-5
- automated rebuild

* Mon May 20 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.9.12-4
- Rebuild 

* Wed Feb 27 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.12-2
- rebuild

* Fri Jan 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.9.12-1
- 0.9.12

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 20 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.9.11-1
- 0.9.11

* Wed Oct 10 2001 Tim Powers <timp@redhat.com> 0.9.9-3
- rebuilt against posgress for ia64

* Wed Oct 10 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.9.9-2
- Fix MD5 password authentication

* Wed Sep 26 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.9-1
- update to 0.9.9

* Wed Sep 19 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.8-2
- add patch from Andreas Hasenack to close more string injection problems

* Wed Sep  5 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.8-1
- update to 0.9.8, fixing problems detailed at
  http://cert.uni-stuttgart.de/advisories/apache_auth.php

* Fri May 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
