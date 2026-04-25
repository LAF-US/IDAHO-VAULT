---
title: "Why and how to set up MacPorts package manager for macOS"
source: "https://brianreiter.org/2020/06/25/why-and-how-to-set-up-macports-package-manager-for-macos/"
author:
  - "[[Leave a comment]]"
published: 2020-06-25
created: 2026-04-25
description: "Package managers for macOS Do I need a package manager? If you never open Terminal.app the answer is definitely, no. macOS is fully functional out of the box with the software shipped by Apple. The base system of command line applications available in a default install are also good enough for poking around and getting…"
---
## Package managers for macOS

Do I need a package manager? If you never open Terminal.app the answer is definitely, no. macOS is fully functional out of the box with the software shipped by Apple. The base system of command line applications available in a default install are also good enough for poking around and getting started with learning the UNIX system. You need a package manager when you want to install UNIX tools that Apple doesn’t bundle or newer or different versions of tools that they do.

A package manager helps you to download, possibly compile, install, and update tools in the UNIX environment in macOS. Alternatively you can download and install things by hand, possibly configuring and compiling them by hand.

There are three main package managers for macOS:

- [Homebrew](https://brew.sh/)
- [pkgsrc](http://pkgsrc.joyent.com/)
- [MacPorts](https://www.macports.org/)

### Homebrew

Homebrew is currently the most popular of these, but it is “too clever by half”. My issue is primarily that it works by taking over `/usr/local/bin` and changing the permission on that directory. This is a security problem but also it is in conflict with the conceptual purpose of `/usr/local/bin` being the directory where I install programs myself. If Homebrew messes up or gets broken then it can be a big mess to clean it up without breaking anything that doesn’t belong to Homebrew.

Homebrew will also help you to install things that it doesn’t control and cannot update — which I don’t think it should do. I also find it’s beer metaphors of casks and cellars overly cute.

Homebrew is popular so it is probably the lowest friction option despite my criticism. You can also use it to automate installing apps from the App Store, commercial software, and UNIX utilities. This can be helpful if you [set up a new Mac frequently](https://www.caseyliss.com/2019/10/8/brew-bundle) or have a standard config to push out. I have heard that GitHub uses Homebrew for this.

### pkgsrc

Pkgsrc comes from NetBSD. It is the standard package manager for NetBSD and SmartOS. Packages for Red Hat Enterprise Linux / CentOS, macOS, and SmartOS are maintained by Joyent. The packages are mostly pre-built binaries and pkgsrc is fast and works well. All of the packages are installed into `/opt/pkg` which means they are safely isolated from your base system. If somehow you borked up pkgsrc, just `rm -fr /opt/pkg` and install it again. If you want to get rid of pkgsrc, just `rm -fr /opt/pkg` and go on with life.

On the downside, all of the GUI packages for macOS are built for X rather than Quartz and the repository is smaller than Homebrew and MacPorts.

If you work in an environment with some combination of RHEL, SmartOS, and macOS then you should consider strongly standardizing on pkgsrc. For example on RHEL, instead of adding EPEL and IUS you can just not install anything on top of the base system with yum/dnf and only use yum/dnf for updating the base system. Then use pkgsrc to install all of the additional software. Then you can enjoy a very similar configuration and maintenance stack across your server and workstation fleet.

### MacPorts

MacPorts (neé DarwinPorts) was originally created by engineers working in the Apple UNIX engineering team as part of the OpenDarwin project. It came out about around the same time as OS X 10.2 *Jaguar*. Darwin is the open source underpinning of macOS and consists of the xnu kernel plus the BSD subsystem. MacPorts was hosted by Apple on MacOS Forge but has subsequently moved to GitHub.

MacPorts used to be the *de facto* standard for installing open source packages on OS X for a long time until it was dethroned by Homebrew. At the time, MacPorts was criticized for wasting time and space by installing its own dependencies rather than linking to the ones from Apple. It also used to install everything by compiling from source and still does compile from source quite a bit, which can be slow. Like pkgsrc, MacPorts installs into its own sandbox: `/opt/local` where it can’t hurt anything and can be easily discarded. MacPorts has a variants system that lets you choose a lot of granular options when installing packages. For example, you can have GUI apps built against the native Quartz window manager whenever possible. It has a huge library of ports that are community maintained and reliable. There are problems occasionally, but they are sorted out quickly.

I’ve used all three of these systems, but have settled on MacPorts as my preference for a combination of practical and aesthetic reasons.

## Setting up MacPorts

### Prerequisites

Before installing MacPorts, you need to install Xcode from [developer.apple.com](https://developer.apple.com/) or the App Store and the Xcode command line tools. Once you have installed Xcode, open Terminal.app and run this command to install the command line tools:

`xcode-select --install`

### Installing macports from pkg or source

You can now probably head over to [www.macports.org](https://www.macports.org/) and download a.pkg installer for your version of macOS. If you are using a beta of a new release or the hot, fresh bits of a.0 release, the.pkg may not be available and you will have to build from source. Either download the tarball and unpack it or clone the git repo and checkout the current release tag.

```
# use actual latest tarball
curl -O https://distfiles.macports.org/MacPorts/MacPorts-2.6.2.tar.bz2
tar xf MacPorts-2.6.2.tar.bz2
```

**OR**

```
git clone https://github.com/macports/macports-base.git
git checkout 10.6.2 # or whatever is the highest version number without a -beta or -rc suffix
```

Whichever way you got the source code, enter the directory in your Terminal.app, configure, build, and install.

```
./configure
make
sudo make install
```

Now you have a `/opt/local` directory and a `port` command.

### Configure options

#### Variants

Set default variants options. I have not used X11 on macOS in years. I like to disable X and enable Quartz by default. I also like to add bash completion scripts whenever they are available.

`sudo vi /opt/local/etc/macports/variants.conf`

```
-x11 +no_x11 +quartz +bash_completion
```

If you live outside of the USA, it can be a significant speedup to change to a [local mirror](https://trac.macports.org/wiki/Mirrors). I am using one in South Africa.

#### Mirrors

In `macports.conf`, set the rsync\_server and rsync\_dir to match your alternate mirror.

`sudo vi /opt/local/etc/macports/macports.conf`

```
# The rsync server for fetching MacPorts base during selfupdate. This
# setting is NOT used when downloading the ports tree; the sources for
# the ports tree are set in sources.conf. See
# https://trac.macports.org/wiki/Mirrors#MacPortsSource for a list of
# available servers.
#rsync_server           rsync.macports.org
rsync_server            jnb.za.rsync.macports.org

# Location of MacPorts base sources on rsync_server. If this references
# a .tar file, a signed .rmd160 file must exist in the same directory
# and will be used to verify its integrity. See
# https://trac.macports.org/wiki/Mirrors#MacPortsSource to find the
# correct rsync_dir for a particular rsync_server.
#rsync_dir              release/tarballs/base.tar
rsync_dir               macports/release/tarballs/base.tar
```

In `sources.conf` change the path to your local mirror.

`sudo vi /opt/local/etc/macports/sources.conf`

#rsync://rsync.macports.org/release/tarballs/ports.tar \[default\]  
rsync://jnb.za.rsync.macports.org/macports/release/tarballs/ports.tar \[default\]

#### Paths

I like to have my path searched in this order:

1. stuff I installed manually
2. MacPorts
3. macOS base system

MacPorts will stick itself into your PATH in your shell profile, which is a good default to make it work, but I prefer to handle this more systematically in a central location.

Edit the system default path:

`sudo vi /etc/paths`

```
/usr/local/bin
/usr/local/sbin
/opt/local/libexec/gnubin
/opt/local/bin
/opt/local/sbin
/usr/bin
/bin
/usr/sbin
/sbin
```

Edit the system default manpath to resolve documentation in the same order as the binaries:

`sudo vi /etc/manpaths`

```
/usr/local/share/man
/usr/share/man
/opt/local/libexec/gnubin/man
/opt/local/share/man
```

The `gnubin` paths are for installing GNU utilities that override the BSD versions in macOS to conform to a *de facto* standard configuration in a world dominated by Linux + GNU servers.

If you want a contemporary `bash` from MacPorts, you need to have it in `/etc/shells` so that it can be set as a user shell with `chsh`.

`sudo vi /etc/shells`

```
/bin/bash
/bin/csh
/bin/ksh
/bin/sh
/bin/tcsh
/bin/zsh
/opt/local/bin/bash
```

### Basics

MacPorts works a lot like `apt` you need to update the local cache and then install or update your packages.

#### Update local cache and macports itself

`sudo port selfupdate`

#### Install a pacakge

`sudo port install`

#### Find package

`port search`

#### List packages

List installed packages

`port installed`

**OR**

`port list installed`

List outdated packages

`port outdated`

**OR**

`port list outdated`

#### Update outdated packages

`sudo port upgrade outdated`

#### Remove old packages

When `port` upgrades a package it doesn’t delete the old one, it moves it to an inactive state so that you can roll back if the new one does not work.

You can clean up old packages

`sudo port uninstall inactive`

## Install GNU flavor like Linux

At this point, if you primarily work with Linux servers, it makes sense to install a GNU base system to override the BSD flavor of a default macOS install.

`sudo port install bash bash-completion coreutils findutils grep gnutar gawk wget`

I also like to install a fully patched `git` to make sure that I have the current features and the bash completion scripts.

`sudo port install git git-lfs`

Also the latest vim.

`sudo port install vim +huge`

### Set up bash

Make sure you have a `~/.bashrc` and `~/.bash_profile`.

Edit `~/.bash_profile` to add

```
#flags to hint build systems to find things in macports
CFLAGS="$CFLAGS -I/opt/local/include" 
CXXFLAGS="$CXXFLAGS -I/opt/local/include" 
LDFLAGS="$LDFLAGS -L/opt/local/lib"
PKG_CONFIG_PATH=/opt/local/lib/pkgconfig
```

If MacPorts altered your `PATH` then comment that out:

```
# MacPorts Installer addition on 2016-09-22_at_13:35:36: adding an appropriate PATH variable for use with MacPorts.
# export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
```

At the very end of `~/.bash_profile` load `~/.bashrc`.

```
if [ -f ~/.bashrc ]; then
   source ~/.bashrc
fi
```

In `~/.bashrc` you can set up some preferences:

#### Prompt

I’m not into the fancy prompts. I like a classic `$`.

```
#classic, minimalist prompt + current git branch
PS1='\$ '
```

#### Prevent ssh from messing up the title

```
# force reset of the current directory name in terminal title
# to reset it after SSH sessions end.
PROMPT_COMMAND='echo -ne "\033]0;$(basename ${PWD})\007"'
```

#### Bash completion

```
if [ -f /opt/local/etc/profile.d/bash_completion.sh ]; then
  . /opt/local/etc/profile.d/bash_completion.sh
fi
```

#### Git prompt

Again, I like something simple. You can look up the fancy things.

```
if [ -f /opt/local/share/git/git-prompt.sh ]; then
  . /opt/local/share/git/git-prompt.sh
  PS1='\[\033[1;36m\]$(__git_ps1 "[%s] ")\[\033[0m\]\$ '
fi
```

#### Colors like Debian and Ubuntu

```
#colorful
export CLICOLOR=1

# The color designators are as follows:
#  
# a     black
# b     red
# c     green
# d     brown
# e     blue
# f     magenta
# g     cyan
# h     light grey
# A     bold black, usually shows up as dark grey
# B     bold red
# C     bold green
# D     bold brown, usually shows up as yellow
# E     bold blue
# F     bold magenta
# G     bold cyan
# H     bold light grey; looks like bright white
# x     default foreground or background
#  
# Note that the above are standard ANSI colors.  The actual display may differ depending on the color capabilities of the terminal in use.
#  
# The order of the attributes are as follows:
#  
# 1.   directory
# 2.   symbolic link
# 3.   socket
# 4.   pipe
# 5.   executable
# 6.   block special
# 7.   character special
# 8.   executable with setuid bit set
# 9.   executable with setgid bit set
# 10.  directory writable to others, with sticky bit
# 11.  directory writable to others, without sticky bit

if [[ $(which ls) = *gnubin* ]]; then
  # GNU ls colors
  eval "$(dircolors -b)"
  alias ls='ls --color=auto'
else
  #BSD ls colors
  #default colors
  #export LSCOLORS=exfxcxdxbxegedabagacad
  export LSCOLORS=xxfxcxdxbxegedabagacad
fi
if [[ $(which grep) = *gnubin* ]]; then
  alias grep='grep --color=auto'
  alias egrep='egrep --color=auto'
  alias fgrep='fgrep --color=auto'
else
  export GREP_OPTIONS='--color=auto'
fi
export GREP_COLOR='0;36' # regular;foreground-cyan
export MINICOM='--color on'
```

#### Prefered editor and pager

```
export EDITOR=vim
export PAGER=less
```

At this point if you open a new terminal, it should feel very much like a Linux install.

## Install some other stuff

### aws cli

`sudo port install python38 py38-awscli`  
`sudo port select --set python3 python38`

Create a file `~/.aws/config` that contains API key credentials like this:

```
[default]
aws_access_key_id = some-key-id
aws_secret_access_key = some-key-value
region = us-east-1

[profile some-name]
aws_access_key_id = some-key-id
aws_secret_access_key = some-key-value
region = us-east-1
```

### Network tools

nmap  
`sudo port install nmap`

wireshark  
`sudo port install GeoLiteCity wireshark3 +geoip +python38 +qt5`

whatmask  
`sudo port install whatmask`

sf-pwgen (password generator)  
`sudo port install sf-pwgen`

axel (download accelerator)  
`sudo port install axel`

curl  
`sudo port install +http2 +openldap +ssl`

tcping (ping tcp ports)  
`sudo port install tcping`

httping (ping http)  
`sudo port install http`

minicom (terminal emulator for connecting to serial devices)  
`sudo port install minicom`

openvpn2  
`sudo port install openvpn2`

### Programming languages

Go  
`sudo port install go`

Rust  
`sudo port install rust`

Java OpenJDK with IBM Eclipse OpenJ9 VM  
`sudo port install openjdk14-openj9`

**OR**

Java OpenJDK with Oracle HotSpot VM  
`sudo port install openjdk14`

Microsoft SQL Server client tools: `sqlcmd` and `bcp`  
`sudo port install mssql-tools`

```
msodbcsql17 has the following notes:
  To make this work with SSL you need to create a symbolic link as follows: 
   sudo mkdir -p /usr/local/opt/openssl/ 
   sudo ln -s /opt/local/lib /usr/local/opt/openssl/lib 

   This is because this port installs binaries meant to be used with Homebrew.
```

`sudo mkdir -p /usr/local/opt/openssl/`  
`sudo ln -s /opt/local/lib /usr/local/opt/openssl/lib`

### Additional

7zip  
`sudo port install p7zip`

youtube-dl (download video offline from youtube and other sites)  
`sudo port install youtube-dl`

dos2unix (convert line endings)  
`sudo port install dos2unix`

ghostscript  
`sudo port install ghostscript`

rsync  
`sudo port install rsync`