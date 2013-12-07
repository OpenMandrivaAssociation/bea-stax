# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support     1
%define section         free
%define api_version     1.0.1

Name:           bea-stax
Version:        1.2.0
Release:        1.3.13
Epoch:          0
Summary:        Streaming API for XML
License:        Apache License
Group:          Development/Java
URL:            http://dev2dev.bea.com/technologies/stax/index.jsp
Source0:        http://dist.codehaus.org/stax/distributions/stax-src-1.2.0.zip
Patch0:         %{name}-ecj-bootclasspath.patch
BuildRequires:  ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel >= 0:1.4.2
%endif
BuildRequires:  java-rpmbuild >= 0:1.6
Requires:       jpackage-utils >= 0:1.6
Requires:       %{name}-api = %{epoch}:%{version}-%{release}

%description
The Streaming API for XML (StAX) is a groundbreaking 
new Java API for parsing and writing XML easily and 
efficiently. 

%package api
Summary:        The StAX API
Group:          Development/Java

%description api
%{summary}

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}

%prep
%setup -q -c
%patch0 -p0
%{__perl} -pi -e 's/source="1\.2" target="1\.2"/source="1.3" target="1.3"/g' build.xml
%{__perl} -pi -e 's/<javac/<javac nowarn="true"/g' build.xml

%build
export OPT_JAR_LIST=:
export CLASSPATH=`pwd`/build/stax-api-1.0.1.jar
%{ant} all javadoc

%install
# jar
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 0644 build/stax-api-%{api_version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-api-%{version}.jar
install -p -m 0644 build/stax-%{version}-dev.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-ri-%{version}.jar
ln -s %{name}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-api.jar
ln -s %{name}-ri-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-ri.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%files
#%{_docdir}/%{name}-%{version}/BEA*.doc
#%{_docdir}/%{name}-%{version}/README.txt
#%{_datadir}/%{name}-%{version}
%{_javadir}/%{name}-ri-%{version}.jar
%{_javadir}/%{name}-ri.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif

%files api
%{_javadir}/%{name}-api-%{version}.jar
%{_javadir}/%{name}-api.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.2.0-1.3.6mdv2011.0
+ Revision: 663318
- mass rebuild
