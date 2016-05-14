%{?scl:%scl_package cglib}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 3

Name:           %{?scl_prefix}cglib
Version:        3.1
Release:        5.%{baserelease}%{?dist}
Summary:        Code Generation Library for Java
License:        ASL 2.0 and BSD
Group:          Development/Tools
Url:            http://cglib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{pkg_name}/%{pkg_name}-src-%{version}.jar
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{pkg_name}/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
Source2:        bnd.properties


Requires: %{?scl_prefix_java_common}objectweb-asm5

BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}jpackage-utils >= 0:1.5

BuildRequires:  %{?scl_prefix_java_common}objectweb-asm5
BuildRequires:  unzip
BuildRequires:  %{?scl_prefix_maven}aqute-bnd
Requires:       %{?scl_prefix}runtime
BuildArch:      noarch

%description
cglib is a powerful, high performance and quality code generation library 
for Java. It is used to extend Java classes and implements interfaces 
at runtime.

%package javadoc
Summary:        Javadoc for %{pkg_name}
Group:          Documentation

%description javadoc
Documentation for the cglib code generation library.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q -c %{pkg_name}-%{version}
cp -p %{SOURCE1} pom.xml
rm lib/*.jar
# Remove the repackaging step that includes other jars into the final thing
sed -i "/<taskdef name=.jarjar/,/<.jarjar>/d" build.xml

%pom_xpath_remove "pom:dependency[pom:artifactId = 'asm-util']/pom:optional"
sed -i -e 's/4\.2/5.0.3/' -e 's/groupId>ant/groupId>org.apache.ant/' pom.xml

%mvn_file :cglib cglib
%mvn_alias :cglib "net.sf.cglib:cglib" "cglib:cglib-full" "cglib:cglib-nodep" "org.sonatype.sisu.inject:cglib"
%mvn_compat_version : 3 3.1
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
export OPT_JAR_LIST=objectweb-asm5
ant jar javadoc
# Convert to OSGi bundle
pushd dist
java -Dcglib.bundle.version="%{version}" \
  -jar $(build-classpath aqute-bnd) wrap -output %{pkg_name}-%{version}.bar -properties %{SOURCE2} %{pkg_name}-%{version}.jar
popd

mv dist/%{pkg_name}-%{version}.bar dist/%{pkg_name}-%{version}.jar
%mvn_artifact pom.xml dist/%{pkg_name}-%{version}.jar
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
install -d -m 755 %{buildroot}%{_javadocdir}/%{pkg_name}
cp -rp docs/* %{buildroot}%{_javadocdir}/%{pkg_name}
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{pkg_name}

%changelog
* Tue Feb 16 2016 Mat Booth <mat.booth@redhat.com> - 3.1-5.3
- Fix dep on ant

* Tue Feb 16 2016 Mat Booth <mat.booth@redhat.com> - 3.1-5.2
- Build as a compat package to avoid conflicts

* Fri Feb 12 2016 Mat Booth <mat.booth@redhat.com> - 3.1-5.1
- Import latest from Fedora

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
- Remove old call to %add_to_maven_depmap macro.
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
