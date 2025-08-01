Summary:	A Probabilistic Routing Protocol
Name:		prophet
Version:	2.7
Release:	0.r83.3
License:	GPL
Group:		System/Servers
URL:		https://prophet.grasic.net/
Source0:	%{name}.tar.bz2
Source1:	prophet-16x16.png
Source2:	prophet-32x32.png
Source3:	prophet-48x48.png
Patch0:		prophet-fhs.diff
Patch1:		prophet-ini_file_in_etc.diff
Patch2:		prophet-helio.diff
Requires:	dtn
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	dos2unix

%description
PRoPHET is a Probabilistic Routing Protocol using a History Imageof Encounters
and Transitivity. PRoPHET is used for intermittently connected networks, where
there is no guarantee that a fully connected path between source and
destination exists at any time, rendering traditional routing protocols unable
to deliver messages between hosts. These networks are examples of networks
where the Delay-Tolerant Network architecture is  applicable. The protocol
specification was written by A. Lindgren and A. Doria. The PRoPHET draft is
available here:

http://www.dtnrg.org/docs/specs/draft-lindgren-dtnrg-prophet-02.txt

Severals demo PRoPHET implementations were done before on the Lulea University
of Technology in the previous years. One of them was presented using a "Lego
Mindstorms" robots as mobile nodes.

The lastest  PRoPHET implementation uses the DTN reference implementation
(version 2.2.0) software. It is written in C++ using the well known Trolltech
QT 4.1 framework. The code itself is now totally platform independable. 

%prep

%setup -q -n %{name}
%patch0 -p0
%patch1 -p0
%patch2 -p0

find . -type f |xargs dos2unix

# instead of a patch
perl -pi -e "s|^GUI =.*|GUI = true|g" %{name}.pro
perl -pi -e "s|^PDAGUI =.*|PDAGUI = false|g" %{name}.pro
perl -pi -e "s|^DTN_INTERFACE =.*|DTN_INTERFACE = true|g" %{name}.pro

# Quick and dirty way to port to Qt 5
echo 'QT+=widgets' >>%{name}.pro
find . -name "*.h" -o -name "*.cpp" |xargs sed -i -e 's,toAscii(),toLocal8Bit(),g;s,toAscii (),toLocal8Bit (),g;/#include <QtGui>/i#include <QtWidgets>'

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

qmake-qt5 %{name}.pro

%build
%make_build

%install
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_localstatedir}/lib/%{name}/storage
install -d %{buildroot}%{_localstatedir}/lib/%{name}/list
install -d %{buildroot}/var/log/%{name}

install -m0755 %{name} %{buildroot}%{_sbindir}/
install -m0644 %{name}.ini %{buildroot}%{_sysconfdir}/

# menu

# icon
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_liconsdir}

install -m0644 prophet-16x16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 prophet-32x32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 prophet-48x48.png %{buildroot}%{_liconsdir}/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=PRoPHET
Comment=A Probabilistic Routing Protocol
Exec=%{_sbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-RemoteAccess;Network;RemoteAccess;
EOF

%files
%defattr(0644,root,root,0755)
%doc dia/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.ini
%attr(0755,root,root) %{_sbindir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/lib/%{name}/storage
%dir %{_localstatedir}/lib/%{name}/list
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/applications/*.desktop
