---
title: "MOOS-IvP : Help - OSX Mac Ports browse"
source: "https://oceanai.mit.edu/ivpman/pmwiki/pmwiki.php?n=Help.OSXMacPorts"
author:
published:
created: 2026-04-25
description:
---
## Help Topic: Installing and Using the MacPorts Package Manager

---

Maintained by: mikerb@mit.edu [Get PDF](https://oceanai.mit.edu/ivpman/pdfs/help_osx_macports.pdf)

---

## Installing and Using the MacPorts Package Manager

---

We will use MacPorts or Homebrew occasionally in this class to install open source software packages as needed. Both package managers work perfectly fine for the purposes of 2.680. You do not need both package managers. If you already have MacPorts installed, you can safely skip installing Homebrew, and vice-versa.

Arguably there is greater adoption of Homebrew than MacPorts, and Homebrew is generally faster to install packages, but both are very fast in practice. If you would like to use Homebrew, see:

[https://oceanai.mit.edu/ivpman/help/osx\_get\_homebrew](https://oceanai.mit.edu/ivpman/help/osx_get_homebrew)

Here we discuss how to obtain MacPorts and install needed packages for 2.680. If you're using a 2025 course-provided computer, Homebrew and most of the common packages are already installed.

\*Note: If you have a course computer, with MacPorts already installed, you still need to augment your shell path as described later in this section.

From the [http://www.macports.org](http://www.macports.org/) page: The MacPorts Project is an open-source community initiative to design an easy-to-use system for compiling, installing, and upgrading either command-line, X11 or Aqua based open-source software on the Mac OS X operating system.

Note: You need to have installed XCode before MacPorts may be installed. If you have not installed XCode yet, or if you are not sure, return to this topic an do so. A direct link is here:

[http://oceanai.mit.edu/ivpman/help/osx\_get\_xcode](http://oceanai.mit.edu/ivpman/help/osx_get_xcode).

## Getting the MacPorts base

---

MacPorts is a package manager that allows you to easily download software packages need in our labs. But package manager itself, the MacPorts base, first needs to downloaded and installed in the steps described here.

(In most Linux distributions, the analagous package manager (apt-get) is present with the out-of-the-box OS installation. Perhaps because many Mac users are not developers, the steps of installing XCode and a package manager are left as options for developers.)

Here's how to get MacPorts:

- Get the MacPorts base here: [http://www.macports.org](http://www.macports.org/). Click on the DOWNLOAD link and grab the.dmg disk image for whichever OS you may have.
- Confirm that MacPorts is installed by typing "which port" and verifying that it returns /opt/local/bin/port. If not, see below on adding the MacPorts bin to your shell path.

## Add the MacPorts bin directory to your shell path

---

MacPorts packages are installed in /opt/local/. The port command line tool should be installed in /opt/local/bin/. You need to add or ensure this latter directory to your shell path. If you're not sure how to augment your shell path, see

[http://oceanai.mit.edu/ivpman/help/cmdline\_augment\_shell\_path](http://oceanai.mit.edu/ivpman/help/cmdline_augment_shell_path).

## Download packages needed for our labs

---

Once the MacPorts base is installed, we need to use MacPorts package manager to download and install common open source software packages used in this course. This part is relatively easy and is all done from the command line in a terminal window. Again make sure the port command is in your shell path and then:

```
$ sudo port install cmake
$ sudo port install subversion
$ sudo port install wget
$ sudo port install libtiff
$ sudo port install fltk-devel
```
- Note: Not all of the above packages result in an executable, i.e., *program*, installed on your machine. Some do, like cmake, wget, and svn from the subversion package. The others install libraries that other programs need later in the course.
- Hint: The port install command accepts a list of packages on the command line like the last entry above. This obviates the need for re-typing your password each time.
- Hint: The port installed command, with no arguments, returns a list of already installed packages. You may notice a number of packages installed that you didn't request. The MacPorts package manager will also down dependency packages as-needed, to build the ones you did explicitly request.
- Hint: The port installed requested command, with no arguments, returns a list of installed packages that have been explicitly requested, as opposed to those that were installed because they were a dependency of a requested package.

---

Document Maintained by: mikerb@mit.edu  
Page built from LaTeX source using *texwiki*, developed at MIT. Errata to issues@moos-ivp.org. [Get PDF](https://oceanai.mit.edu/ivpman/pdfs/help_osx_macports.pdf)