%global pkg_name cglib
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.2
Release:        18.12%{?dist}
Summary:        Code Generation Library for Java
License:        ASL 2.0 and BSD
Url:            http://cglib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{pkg_name}/%{pkg_name}-src-%{version}.jar
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{pkg_name}/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
Source2:        bnd.properties
# Remove the repackaging step that includes other jars into the final thing
Patch0:         %{pkg_name}-build_xml.patch

Requires: %{?scl_prefix_java_common}objectweb-asm

BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}objectweb-asm
BuildRequires:  unzip
BuildRequires:  %{?scl_prefix}aqute-bnd
BuildArch:      noarch

%description
cglib is a powerful, high performance and quality code generation library 
for Java. It is used to extend Java classes and implements interfaces 
at runtime.

%package javadoc
Summary:        Javadoc for %{pkg_name}
%description javadoc
Documentation for the cglib code generation library.

%prep
%setup -q -c -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
rm lib/*.jar
%patch0 -p1
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=`build-classpath objectweb-asm`
ant jar javadoc
# Convert to OSGi bundle
pushd dist
java -Dcglib.bundle.version="%{version}" \
  -jar $(build-classpath aqute-bnd) wrap -output %{pkg_name}-%{version}.bar -properties %{SOURCE2} %{pkg_name}-%{version}.jar
popd
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
mkdir -p %{buildroot}%{_mavenpomdir}
cp %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom
# yes, this is really *.bar - aqute bnd created it
install -p -m 644 dist/%{pkg_name}-%{version}.bar %{buildroot}%{_javadir}/%{pkg_name}.jar
install -p -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap -a "net.sf.cglib:cglib,cglib:cglib-full"

cp -rp docs/* %{buildroot}%{_javadocdir}/%{name}
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.2-18.12
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 2.2-18.11
- BR/R on packages from rh-java-common

* Fri Jan 09 2015 Michal Srb <msrb@redhat.com> - 2.2-18.10
- Do not call %%add_maven_depmap twice on the same artifact

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 2.2-18.9
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.2-18.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-18.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-18.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-18.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-18.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-18.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-18.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-18.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.2-18
- Mass rebuild 2013-12-27

* Thu Nov 07 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-17
- Remove old macro invocation
- Resolves: rhbz#1027717

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-16
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

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
