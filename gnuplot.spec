%define	name	gnuplot
%define	version 4.2.0
%define release	%mkrel 1
%define	modeversion 0.6.0

Name:		%{name}
Summary:	A program for plotting mathematical expressions and data
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.gnuplot.info/pub/gnuplot/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnuplot.info/pub/gnuplot/gnuplot-mode.%{modeversion}.tar.bz2
Source2:	ftp://ftp.gnuplot.info/pub/gnuplot/faq/gnuplot-faq.html.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		gnuplot-4.0.0-emacs-mode--disable-f9.patch
License:	Freeware-like
Group:		Sciences/Other
URL:		http://www.gnuplot.info/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(post):		info-install
Requires(preun):		info-install
BuildRequires:	XFree86-devel
BuildRequires:	emacs-bin
BuildRequires:	ncurses-devel
BuildRequires:	png-devel
BuildRequires:	readline-devel
BuildRequires:	tetex-latex
BuildRequires:  texinfo
BuildRequires:  gd-devel

%description
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

%prep
%setup -q -a 1
%patch0 -p1

perl -pi -e 's|(^\s*)mkinstalldirs\s|$1./mkinstalldirs |' gnuplot-mode.%{modeversion}/Makefile.in
# Non-free stuff. Ouch. -- Geoff
rm -f demo/prob.dem demo/prob2.dem

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-fast-math"
%configure --with-readline=gnu --with-png --without-linux-vga
%make

pushd gnuplot-mode.%{modeversion} && {
    ./configure --prefix=/usr
    %make
} && popd

cp %{SOURCE2} .
bzip2 -d gnuplot-faq.html.bz2

cd docs
make ps
make pdf

%install
rm -rf $RPM_BUILD_ROOT

%{makeinstall_std}

pushd gnuplot-mode.%{modeversion} && {
    make install prefix=$RPM_BUILD_ROOT/usr
} && popd

cd gnuplot-mode.%{modeversion}
pdflatex gpelcard

install -d $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d
install -m 644 dotemacs $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d/%{name}.el

# menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}

cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << EOF
?package(%{name}):\
needs="text"\
section="More Applications/Sciences/Mathematics"\
title="Gnuplot"\
longtitle="The famous function plotting program"\
command="%_bindir/gnuplot"\
icon="gnuplot.png" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Gnuplot
Comment=The famous function plotting program
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=true
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Sciences-Mathematics;Sciences
EOF

# icon
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

%post
%{update_menus}
%_install_info %{name}.info

%postun
%{clean_menus}
%_remove_install_info %{name}.info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Copyright docs/psdoc docs/gnuplot.pdf gnuplot-faq.html
%doc demo gnuplot-mode.%{modeversion}/gpelcard.pdf README README.1ST README.exp
%doc TODO FAQ NEWS PORTING
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_bindir}/gnuplot
%{_mandir}/*/*
%{_datadir}/emacs/site-lisp/*
%{_libdir}/gnuplot
%{_datadir}/gnuplot
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_infodir}/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_libdir}/X11/app-defaults/Gnuplot.app-defaults
%{_datadir}/texmf/tex/latex/gnuplot/gnuplot.cfg



