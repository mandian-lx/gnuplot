%define	modeversion 0.6.0

Summary:	A program for plotting mathematical expressions and data
Name:		gnuplot
Version:	4.6.2
Release:	1
License:	Freeware-like
Group:		Sciences/Other
Url:		http://www.gnuplot.info/
Source0:	http://downloads.sourceforge.net/project/gnuplot/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:	http://cars9.uchicago.edu/~ravel/software/gnuplot-mode/gnuplot-mode.%{modeversion}.tar.bz2
Source2:	http://www.gnuplot.info/faq/faq.html
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		gnuplot-4.0.0-emacs-mode--disable-f9.patch
Patch2:		gnuplot-4.6.2-texinfo5.patch

BuildRequires:	emacs-bin
BuildRequires:  texinfo
BuildRequires:	texlive-epstopdf
BuildRequires:	tetex-latex
BuildRequires:  gd-devel
BuildRequires:	readline-devel
BuildRequires:	wxgtku-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:	pkgconfig(libpng15)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(x11)
Requires:	gnuplot-nox
Suggests:	gnuplot-mode
Suggests:	gnuplot-doc

%description
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

%package	nox
Summary:	A program for plotting mathematical expressions and data
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

%description	nox
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

This package provides GNUPlot without any X dependency.

%package	mode
Summary:	Yet another Gnuplot mode for Emacs
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

%description	mode
Gnuplot is a major mode for Emacs flavours with the following features:

 - Functions for plotting lines, regions, entire scripts, or entire files
 - Graphical interface to setting command arguments
 - Syntax colorization
 - Completion of common words in Gnuplot
 - Code indentation
 - On-line help using Info for Gnuplot functions and features
 - Interaction with Gnuplot using comint
 - Pull-down menus plus a toolbar in XEmacs
 - Distributed with a quick reference sheet in postscript.

%package	doc
Summary:	GNUPlot Documentation
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

%description	doc
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

This package provides the additional documentation.

%prep
%setup -q -a 1
%apply_patches

sed -i -e 's|(^\s*)mkinstalldirs\s|$1./mkinstalldirs |' gnuplot-mode.%{modeversion}/Makefile.in
# Non-free stuff. Ouch. -- Geoff
rm -f demo/prob.dem demo/prob2.dem

%build
export CFLAGS="%{optflags} -fno-fast-math"
export CONFIGURE_TOP=..

mkdir build-nox
pushd build-nox
%configure2_5x \
	--with-readline=gnu \
	--with-png \
	--without-linux-vga \
	--without-x \
	--disable-wxwidgets
%make -C src/
%make -C docs/ pdf
popd

mkdir build-x11
pushd build-x11
%configure2_5x 
	--with-readline=gnu 
	--with-png 
	--without-linux-vga
%make
popd

pushd gnuplot-mode.%{modeversion} && {
    ./configure --prefix=/usr
    %make
} && popd

cp -f %SOURCE2 .
chmod 644 faq.html

%install
pushd build-nox
%makeinstall_std
mv %{buildroot}%{_bindir}/gnuplot %{buildroot}%{_bindir}/gnuplot-nox
popd

pushd build-x11
%makeinstall_std
popd

pushd gnuplot-mode.%{modeversion} && {
    make install prefix=%{buildroot}/usr
    pdflatex gpelcard
    install -d %{buildroot}%{_sysconfdir}/emacs/site-start.d
    install -m 644 dotemacs %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el
} && popd

# Copy back from build dir to be able to package those files
pushd build-nox
mv docs/gnuplot.pdf ../docs/
#mv docs/gnuplot.ps ../docs/
#mv docs/gpcard.ps ../docs/
popd

# menu

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Version=1.0
Name=Gnuplot
Comment=The famous function plotting program
Exec=%{name}
Icon=%{name}
Terminal=true
Type=Application
StartupNotify=true
Categories=Education;Science;Math;DataVisualization;
EOF

# icon
install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

%files
%{_bindir}/gnuplot

%files nox
%doc Copyright faq.html
%doc README README.1ST
%doc NEWS PORTING
%{_bindir}/gnuplot-nox
%{_mandir}/*/*
%{_libdir}/gnuplot
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/texmf/tex/latex/gnuplot
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files doc
%doc demo docs/gnuplot.pdf
%{_datadir}/gnuplot
%{_infodir}/*

%files mode
%doc gnuplot-mode.%{modeversion}/gpelcard.pdf
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_datadir}/emacs/site-lisp/*

