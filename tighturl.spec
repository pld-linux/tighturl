Summary:	TightURL - Tighten up long URLs to make short ones
Name:		tighturl
Version:	0.1.3.3
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/project/tighturl/tighturl/%{version}%20beta/%{name}-%{version}.tar.gz
# Source0-md5:	e16b2a2aa96583c869e4f1af042170d3
URL:		http://www.tighturl.com/project/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-bad-behavior
Requires:	webapps
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
TightURL is a PHP/MySQL-based Blind Redirection Service.

The primary purpose of TightURL is to allow people to shorten very
long URLs that would otherwise wrap when pasted into e-mail messages.
URL wrapping in e-mail messages usually results in broken links. The
e-mail program will convert everything up to the end of the first line
into a hyperlink, and the rest of the URL gets ignored.

%prep
%setup -q

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

# locale for glob, altho satisified by rpmmacros already
export LC_ALL=C
install -d docs
mv [A-Z]* docs

# we have rpm pkg
rm -rf bad-behavior

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a . $RPM_BUILD_ROOT%{_appdir}
rm -rf $RPM_BUILD_ROOT%{_appdir}/docs

mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/apache.conf
cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf
mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/lighttpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
#%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
