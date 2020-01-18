%global nss_version 3.10
%global nspr_version 4.6
%global with_curl	1
%global with_ldap	1


Name:           pam_pkcs11
Version:        0.6.2
Release:        27%{?dist}
Summary:        PKCS #11/NSS PAM login module

Group:          System Environment/Base
License:        LGPLv2+
URL:            http://www.opensc-project.org/pam_pkcs11
Source0: 	http://www.opensc-project.org/files/pam_pkcs11/%{name}-%{version}.tar.gz
Source1:	rh_pam_pkcs11.conf
Source2:	rh_pkcs11_eventmgr.conf
patch1:		pam_pkcs11-0.6.2-login_required.patch
patch2:		pam_pkcs11-0.6.2-pcsc-lite.patch
patch3:		pam_pkcs11-0.6.2-ldap_fix.patch
patch4:		pam_pkcs11-0.6.2-nss_ldap_fix.patch
patch5:		pam_pkcs11-0.6.2-bad_token_fix.patch
Patch6:		pam_pkcs11-0.6.2-fix-arg-parsing.patch
Patch7:		pam_pkcs11-0.6.2-no_errors.patch
Patch8:		pam_pkcs11-0.6.2-no_remote_spew.patch
Patch9:		pam_pkcs11-default-ssl.patch
Patch10:	pam_pkcs11-0.6.2-coverity-fixes.patch
Patch11:	pam_pkcs11-0.6.2-mem-leak.patch
Patch12:	pam_pkcs11-0.6.2-drop_path.patch
Patch13:	pam_pkcs11-fix-conf-man.patch
Patch14:	pam_pkcs11-0.6.2-uid-attribute.patch
Patch15:	pam_pkcs11-0.6.2-fix-debug-output.patch
Patch16:	pam_pkcs11-0.6.2-generic-mapper-fix.patch
Patch17:	pam_pkcs11-0.6.2-add-ms-map-file.patch
Patch18:	pam_pkcs11-0.6.2-strip-email-domain.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pam-devel
%{?with_ldap:BuildRequires: openldap-devel}
%{?with_curl:BuildRequires: curl-devel}
BuildRequires: libxslt 
BuildRequires: docbook-style-xsl 
BuildRequires: nss-devel >= %{nss_version} 
BuildRequires: nspr-devel
BuildRequires: pcsc-lite-devel
BuildRequires: pkgconfig
BuildRequires: intltool
BuildRequires: gettext
Provides:       pam_pkcs11 = %{version}-%{release}

%description
This Linux-PAM login module allows a X.509 certificate based user
authentication. The certificate and its dedicated private key are thereby
accessed by means of an appropriate PKCS #11 module. For the
verification of the users' certificates, locally stored CA
certificates as well as either online or locally accessible CRLs and
OCSP are used. This version uses NSS to validate the Certificates and manage
the PKCS #11 smartCards.
Additional included pam_pkcs11 related tools
- pkcs11_eventmgr: Generate actions on card insert/removal/timeout events
- pklogin_finder: Get the loginname that maps to a certificate
- pkcs11_inspect: Inspect the contents of a certificate

%prep
%setup -q -n pam_pkcs11-%{version}
%patch1 -p1 -b .login-required
%patch2 -p1 -b .pcsc-lite
%patch3 -p1 -b .ldap-fix
%patch4 -p1 -b .nss-ldap-fix
%patch5 -p1 -b .bad-token-fix
%patch6 -p1 -b .fix-arg-parsing
%patch7 -p1 -b .no-errors
%patch8 -p1 -b .no-remote-spew
%patch9 -p1 -b .default-ssl
%patch10 -p1 -b .coverity
%patch11 -p1 -b .mem-leak
%patch12 -p1 -b .drop-path
%patch13 -p1 -b .fix-conf-man
%patch14 -p1 -b .uid-attribute
%patch15 -p1 -b .fix-debug-output
%patch16 -p1 -b .generic-mapper-fix
%patch17 -p1 -b .add-ms-map-file
%patch18 -p1 -b .strip-email-domain

#
# don't rebuilds pam_pkcs11.html it creates a bunch of unique ids, which 
# creates unnecessary differences between 32 bit and 64 bit versions of the 
# file
#
touch doc/pam_pkcs11.html

%build

%if %{with_curl}
%global curl_flags --with-curl=yes
%else
%global curl_flags --with-curl=no
%endif

%if %{with_ldap}
%global ldap_flags --with-ldap=yes
%else
%global ldap_flags --with-ldap=no
%endif
%configure  \
    --with-nss \
    --with-debug  \
    --disable-dependency-tracking  \
    %{curl_flags} %{ldap_flags} 
make CFLAGS="$RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/security/%{name}.*a

#
# set up config files
#
install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}.conf
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/pkcs11_eventmgr.conf
#
# clean up those files that aren't part of this package
# (makefile should install them if --without-pcsclite is supplied
#
#rm -f $RPM_BUILD_ROOT/%{_bindir}/card_eventmgr
#rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/card_eventmgr.1
#rm -f $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}/card_eventmgr.conf.example

# nss version does not need this script
rm -f $RPM_BUILD_ROOT/%{_bindir}/make_hash_link.sh
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/pkcs11_make_hash_link.1

# package the examples in the doc directory directly.
rm -rf $RPM_BUILD_ROOT/%{_docdir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO ChangeLog NEWS 
%doc doc/pam_pkcs11.html
%doc doc/mappers_api.html
%doc doc/README.autologin
%doc doc/README.mappers
%doc etc/*.example
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/pkcs11_eventmgr.conf
%{_bindir}/pkcs11_eventmgr
%{_bindir}/pklogin_finder
%{_bindir}/pkcs11_inspect
%{_bindir}/pkcs11_setup
%{_bindir}/card_eventmgr
%{_bindir}/pkcs11_listcerts
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_libdir}/security/%{name}.so
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man1/pkcs11_eventmgr.1.gz
%{_mandir}/man1/pkcs11_inspect.1.gz
%{_mandir}/man1/pkcs11_listcerts.1.gz
%{_mandir}/man1/pkcs11_setup.1.gz
%{_mandir}/man1/pklogin_finder.1.gz
%{_mandir}/man1/card_eventmgr.1.gz

%changelog
* Thu Mar 23 2017 Bob Relyea <rrelyea@redhat.com> 0.6.2.27
- Too aggressive on fixing date log, restore old date for 0.6.2-25

* Mon Mar 13 2017 Bob Relyea <rrelyea@redhat.com> 0.6.2-26.1
- Fix bad dates in change log

* Fri Mar 10 2017 Bob Relyea <rrelyea@redhat.com> 0.6.2-26
- strip the domain value off of the email address (@example.net)

* Tue Jun 28 2016 Bob Relyea <rrelyea@redhat.com> 0.6.2-25
- fix the generic mapper
- update the pam_pkcs11 to show certs come from the cert database

* Fri Sep 11 2015 Bob Relyea <rrelyea@redhat.com> 0.6.2-24
- fix incorrect debug output in uid_attribute patch

* Mon Aug 31 2015 Bob Relyea <rrelyea@redhat.com> 0.6.2-23
- really fix dangling reference in the source man page file, not just the target

* Tue Aug 25 2015 Bob Relyea <rrelyea@redhat.com> 0.6.2-22
- Don't rebuild documentation for each platform. Doing so creates unique 
document files which are shared and conflict on multilib installations.

* Mon Jul 6 2015 Bob Relyea <rrelyea@redhat.com> 0.6.2-21
- fix clang issue in upstream patch

* Mon Jul 6 2015 Bob Relyea <rrelyea@redhat.com> 0.6.2-20
- backport upstream uid_attribute patch

* Mon Jul 6 2015 Bob Relyea <rrelyea@redhat.com> 0.6.2-19
- Fix dangling reference to non-existant pam_pkcs11.conf man page.

* Wed Sep 24 2014 Bob Relyea <rrelyea@redhat.com> 0.6.2-18
- Handle PKCS #11 modules when NSS or pam_pkcs11 only specify a partial path

* Wed Feb 26 2014  Bob Relyea <rrelyea@redhat.com> - 0.6.2-17
- Add spaces around the '=' on the cert_policy lines.

* Mon Feb 24 2014  Bob Relyea <rrelyea@redhat.com> - 0.6.2-16
- Fix memory leak in error path.
- Fix sprintf buffer overflow in prompt.

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.6.2-15
- Mass rebuild 2014-01-24

* Tue Jan 21 2014 Bob Relyea <rrelyea@redhat.com> - 0.6.2-14
- Install into %{_libdir}/system rather then /%{_lib}/system (rpmdiff error)
- Fix coverity issues
- Silence coverity warnings

* Thu Jan 16 2014 Bob Relyea <rrelyea@redhat.com> - 0.6.2-13
- Pick up RHEL 6 patches.

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.6.2-11
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Feb 10 2011 Bob Relyea <rrelyea@redhat.com> - 0.6.2-7
- Update code to accept new pcsc-lite defines

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 3 2010 Bob Relyea <rrelyea@redhat.com> - 0.6.2-5
- Sigh, ocsp should be off by default

* Mon May 3 2010 Bob Relyea <rrelyea@redhat.com> - 0.6.2-4
- update config file

* Fri Mar 19 2010 Bob Relyea <rrelyea@redhat.com> - 0.6.2-3
- fix missing function

* Wed Jan 13 2010 Bob Relyea <rrelyea@redhat.com> - 0.6.2-2
- Pick up the latest pam_pkcs11 from upstream

* Tue Jan 12 2010 Bob Relyea <rrelyea@redhat.com> - 0.6.2-1
- Pick up the latest pam_pkcs11 from upstream

- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov  8 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.5.3-27
- Include missing directory entries (#233895).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.3-26
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Bob Relyea <rrelyea@redhat.com> - 0.5.3-25
- Update License description to the new Fedora standard

* Thu Mar 08 2007 Florian La Roche <laroche@redhat.com> - 0.5.3-24
- remove empty rpm scripts

* Fri Oct 6 2006 Robert Relyea <rrelyea@redhat.com> - 0.5.3-23
- turn OCSP off by default

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.5.3-22
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-21
- update password supported patch.
- fix bug where the user and smart card prompt was coming up in login after
  the username had been entered.
- use pam_ignore for the case where we always want to drop to the other
  pam_modules.
- add environment variables for the certificate used to authenticate.

* Mon Sep 18 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-20
- Use pam_syslog rather than syslog (patch by Tmraz).
- Signal to the user that change password is not supported by pam_pkcs11.

* Thu Sep 14 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-19
- Fix problem where pin was not being passed in the pam password variable
  correctly. Needed for Kerberos PKInit

* Wed Sep 13 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-18
- define those apps that we shouldn't login initially with (screen-savers)

* Tue Sep 12 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-17
- restrict reauthentication to the token used in the inital login.
- don't require reauthentication apps to log into a token if the user
  didn't initally log into the token.
- handle the case where we have more than one token.

* Thu Sep 7 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-16
- make sure we have l10n tools for the build itself

* Fri Sep 1 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-15
- add l10n support
- correct mapper order.
- login should allow SSL Client Auth certs rather than restricting to Email
  Signing certs.

* Mon Aug 28 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-14
- use implicit paths to load the PKCS #11 module

* Mon Aug 28 2006 Tomas Mraz <tmraz@redhat.com>
- pkcs11_setup should respect $LIB in module paths (#204252)

* Mon Aug 28 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-13
- Fix the default mapping order.
- Make ocsp support controlled by a config entry.
- Fix login crash
- revert to explicit paths until we can fix 'login' and 'authconfig'

* Mon Aug 28 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-12
- use $LIB so the config file works for multi archs on the
- same machine

* Mon Aug 21 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-11
- Handle library paths in config file

* Wed Aug 16 2006 Robert Relyea <rrelyea@redhat.com> 0.5.3-10
- remove sceventd

* Mon Jul 24 2006 Ray Strode <rstrode@redhat.com> 0.5.3-9
- compile with better debugging flags

* Sun Jul 23 2006 Ray Strode <rstrode@redhat.com> 0.5.3-8
- fix bug where it was ignoring first argument of module
  command line

* Sun Jul 23 2006 Ray Strode <rstrode@redhat.com> 0.5.3-7
- add new wait_for_card option that stalls auth process
  until a card is inserted
- if the user is reauthenticating (already logged in, but
  say unlocking the screen) then only treat the token the
  user logged in with as a valid authentication token
- clean up "smart card" word.  Before we had a mix of 
  "smartcard", "Smart Card", "SmartCard", and "smart card" 
  i think.
- only say "Please insert your smart card." instead of
  "Please insert your Smart Card or enter username" if 
  username based login isn't allowed.

* Thu Jul 20 2006 Robert Relyea  <rrelyea at redhat.com> 0.5.3-6
- Include the login token in the environment
- Conditionally turn on OCSP
- Treat uninitialized tokens as not present.

* Tue Jul 18 2006 Tomas Mraz <tmraz at redhat.com> 0.5.3-5
- added a simple pkcs11_setup tool

* Tue Jul 18 2006 Robert Relyea  <rrelyea at redhat.com>
- Fix memory error in card_only.
- Use the TEXT_INFO field for smart card prompting

* Mon Jul 17 2006 Jesse Keating  <jkeating@redhat.com>  0.5.3-4
- rebuild

* Mon Jun 12 2006 Robert Relyea  <rrelyea at redhat.com>  0.5.3-3
- Updated to 0.5.3 with card_only and NSS support

* Thu Apr 20 2006 Robert Relyea < rrelyea at redhat.com > 0:0.5.1.-2.exp
- Added screenlocking helper support

* Thu Mar 30 2006 Robert Relyea < rrelyea at redhat.com > 0:0.5.1.-1.exp
- Added NSS support.

* Mon Jan 30 2006 Robert Relyea < rrelyea at redhat.com > 0:0.5.1.-0.demo
- include coolkey support
- added card_only option.

* Wed Sep 7 2005 Juan Antonio Martinez <jonsito at teleline.es 0:0.5.3-2
- Add ldap_mapper.so as separate package, as it depends on external library
- Changes from FC4 team

* Thu Sep 1 2005 Juan Antonio Martinez <jonsito at teleline.es 0:0.5.3-0
- Update to 0.5.3
- Remove tools package, and create pcsc one with pcsc-lite dependent files

* Mon Apr 11 2005 Juan Antonio Martinez <jonsito at teleline.es 0:0.5.2-1
- Changed package name to pam_pkcs11

* Fri Apr 8 2005 Juan Antonio Martinez <jonsito at teleline.es 0:0.5.2-0
- Updated to 0.5.2 release
- Changed /etc/pkcs11 for /etc/pam_pkcs11
- Changed /usr/share/pkcs11_login for /usr/share/pam_pkcs11
- Next item is change package name to pam_pkcs11

* Thu Apr 7 2005 Juan Antonio Martinez <jonsito at teleline.es 0:0.5.1-0
- patches to avoid autotools in compile from tgz

* Tue Mar 29 2005 Juan Antonio Martinez <jonsito at teleline.es 0:0.5-1
- upgrade to 0.5beta1 version
- BuildRequires now complains compilation of html manual from xml file

* Mon Feb 28 2005 Juan Antonio Martinez <jonsito at teleline.es> 0:0.4.4-2
- New pkcs11_eventmgr app in "tools" package

* Thu Feb 24 2005 Juan Antonio Martinez <jonsito at teleline.es> 0:0.4.4-1
- Fix pcsc-lite dependencies

* Tue Feb 15 2005 Juan Antonio Martinez <jonsito at teleline.es> 0:0.4.4-0
- Update to 0.4.4b2

* Sun Sep 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3b-0.fdr.1
- Update to 0.3b.
- Disable dependency tracking to speed up the build.

* Tue May  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3-0.fdr.1
- Update to 0.3.
- Do not use libcurl by default; rebuild using "--with curl" to use it.

* Mon Mar 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2-0.fdr.1
- Update to 0.2.
- Use libcurl by default; rebuild using "--without curl" to disable.

* Wed Jan 21 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1-0.fdr.0.2.beta5
- Add the user_mapping config file.

* Mon Jan 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1-0.fdr.0.1.beta5
- First build.
