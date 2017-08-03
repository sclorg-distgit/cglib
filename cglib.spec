%{?scl:%scl_package cglib}
%{!?scl:%global pkg_name %{name}}

%global tarball_name RELEASE_3_2_4

Name:           %{?scl_prefix}cglib
Version:        3.2.4
Release:        4.2%{?dist}
Summary:        Code Generation Library for Java
License:        ASL 2.0 and BSD
Url:            https://github.com/cglib/cglib
Source0:        https://github.com/cglib/cglib/archive/%{tarball_name}.tar.gz

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}maven-plugin-bundle
BuildRequires:  %{?scl_prefix}javapackages-local
BuildRequires:  %{?scl_prefix}mvn(org.apache.ant:ant)
BuildRequires:  %{?scl_prefix}mvn(org.ow2.asm:asm)
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.sonatype.oss:oss-parent:pom:)
BuildArch:      noarch

%description
cglib is a powerful, high performance and quality code generation library
for Java. It is used to extend Java classes and implements interfaces
at run-time.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Documentation for the cglib code generation library.

%prep
%setup -q -n %{pkg_name}-%{tarball_name}

%pom_disable_module cglib-nodep
%pom_disable_module cglib-integration-test
%pom_disable_module cglib-jmh
%pom_xpath_set pom:packaging 'bundle' cglib
%pom_xpath_inject pom:build/pom:plugins '<plugin>
                                           <groupId>org.apache.felix</groupId>
                                           <artifactId>maven-bundle-plugin</artifactId>
                                           <version>1.4.0</version>
                                           <extensions>true</extensions>
                                           <configuration>
                                             <instructions>
                                               <Bundle-SymbolicName>net.sf.cglib.core</Bundle-SymbolicName>
                                               <Export-Package>net.*</Export-Package>
                                               <Import-Package>org.apache.tools.*;resolution:=optional,*</Import-Package>
                                             </instructions>
                                           </configuration>
                                         </plugin>' cglib
%pom_remove_plugin org.apache.maven.plugins:maven-gpg-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-jarsigner-plugin cglib-sample
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_xpath_inject "pom:dependency[pom:artifactId='ant']" "<optional>true</optional>" cglib

%mvn_alias :cglib "net.sf.cglib:cglib" "cglib:cglib-full" "cglib:cglib-nodep" "org.sonatype.sisu.inject:cglib"

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 3.2.4-4.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 3.2.4-4.1
- Automated package import and SCL-ization

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.4-4
- Remove unneeded maven-javadoc-plugin invocation

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul  8 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.4-2
- Make ant dependency optional

* Thu Jul 07 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.2.4-1
- Upgrade to latest 3.2.4 release.
- Resolves RHBZ#1352315

* Mon Feb 22 2016 Mat Booth <mat.booth@redhat.com> - 3.1-10
- Make ant an optional dependency

* Thu Feb 18 2016 Mat Booth <mat.booth@redhat.com> - 3.1-9
- Modernise spec file

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 09 2015 Michael Simacek <msimacek@redhat.com> - 3.1-7
- Update bnd invocation

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-5
- Add alias for cglib:cglib-nodep

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-3
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Jan 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-1
- Update to upstream version 3.1
- Remove patch for upstream bug 44 (fixed upstream)

* Mon Nov 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0-1
- Update to upstream version 3.0
- Add alias for org.sonatype.sisu.inject:cglib

* Mon Aug 05 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.2-17
- Remove old call to %%add_to_maven_depmap macro.
- Fixes RHBZ#992051.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-14
- Add additional maven depmap

* Mon Sep 17 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.2-13
- Use aqute bnd in order to generate OSGi metadata.

* Fri Aug 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-12
- Add additional depmap

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-11
- Fix license tag
- Install LICENSE and NOTICE with javadoc package
- Convert versioned JARs to unversioned
- Preserve timestamp of POM file
- Update to current packaging guidelines

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-7
- Add missing pom file (Resolves rhbz#655793)

* Fri Nov 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2-6
- BR unzip to fix openSUSE build

* Tue Dec  9 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-5
- Add dist to version
- Fix BuildRoot to follow the latest guidelines

* Mon Nov 24 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-4
- Add a comment explaining the patch

* Thu Nov  6 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-3
- Flag Maven depmap as "config"

* Wed Nov  5 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-2
- Explicitly require Java > 1.6 because it won't compile with gcj
- Fix cosmetic issues in spec file

* Tue Nov  4 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-1
- Initial package (based on previous JPP version)
