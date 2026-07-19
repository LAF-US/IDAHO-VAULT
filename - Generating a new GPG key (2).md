---
title: "man page"
source: "https://en.wikipedia.org/wiki/Man_page"
author:
  - "[[Wikipedia]]"
published: 2002-09-14
created: 2026-04-20
description:
date created: Monday, April 20th 2026, 12:49:21 pm
date modified: Monday, April 20th 2026, 12:53:45 pm
---

![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Sed_stream_editor_%28cropped%29.jpg/250px-Sed_stream_editor_%28cropped%29.jpg)

The man page for the sed utility, as seen in various Linux distributions

A **man page**, short for **manual page**, is a form of [software documentation](https://en.wikipedia.org/wiki/Software_documentation "Software documentation") found on [Unix](https://en.wikipedia.org/wiki/Unix "Unix") and [Unix-like](https://en.wikipedia.org/wiki/Unix-like "Unix-like") [operating systems](https://en.wikipedia.org/wiki/Operating_systems "Operating systems"). Topics covered include programs, [system libraries](https://en.wikipedia.org/wiki/System_libraries "System libraries"), [system calls](https://en.wikipedia.org/wiki/System_call "System call"), and sometimes local system details. The local host administrators can create and install manual pages associated with the specific host. A manual end user may invoke a documentation page by issuing the `man` [command](https://en.wikipedia.org/wiki/Command_\(computing\) "Command (computing)") followed by the name of the item for which they want the documentation. These manual pages are typically requested by end users, programmers and administrators doing real time work but can also be formatted for printing.

By default, `man` typically uses a formatting program such as `nroff` with a macro package or [mandoc](https://en.wikipedia.org/wiki/Mandoc "Mandoc"), and also a [terminal pager](https://en.wikipedia.org/wiki/Terminal_pager "Terminal pager") program such as `more` or `less` to display its output on the user's screen.

Man pages are often referred to as an *[online](https://en.wikipedia.org/wiki/Online "Online")* form of software documentation,[^1] even though the `man` command does not require Internet access, because man pages are available from a [command-line interface](https://en.wikipedia.org/wiki/Command-line_interface "Command-line interface") with the `man` command or from a [graphical user interface](https://en.wikipedia.org/wiki/Graphical_user_interface "Graphical user interface") with a man-page viewer, rather than only being readable in printed form. The environment variable MANPATH often specifies a list of directory paths to search for the various documentation pages. Manual pages date back to when printed documentation was the norm.

## History

![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Screenshot_of_%22Xman%22_program.png/250px-Screenshot_of_%22Xman%22_program.png)

xman, an early X11 application for viewing manual pages

![](https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/OpenBSD_Manpages_Section_8_Intro.png/250px-OpenBSD_Manpages_Section_8_Intro.png)

OpenBSD section 8 intro man page, displaying in a text console

With some software, as of 1987, documentation was printed pages, available on the premises to users.[^2] At some sites, they were organized into steel binders, locked together in one monolithic steel reading rack, bolted to a table or counter, with pages organized for modular information updates, replacement, errata, and addenda. Popular manuals about microcomputers were advertised as being for sale in loose-leaf binders with regular updates.[^3]

In the first two years of the [history of Unix](https://en.wikipedia.org/wiki/History_of_Unix "History of Unix"), no documentation existed.[^4] The *[Unix Programmer's Manual](http://man.cat-v.org/unix-1st/)* was first published on November 3, 1971. The first actual man pages were written by [Dennis Ritchie](https://en.wikipedia.org/wiki/Dennis_Ritchie "Dennis Ritchie") and [Ken Thompson](https://en.wikipedia.org/wiki/Ken_Thompson "Ken Thompson") at the insistence of their manager [Doug McIlroy](https://en.wikipedia.org/wiki/Douglas_McIlroy "Douglas McIlroy") in 1971. Aside from the man pages, the *Programmer's Manual* also accumulated a set of short papers, some of them [tutorials](https://en.wikipedia.org/wiki/Tutorial "Tutorial") (e.g. for general Unix usage, the [C](https://en.wikipedia.org/wiki/C_\(programming_language\) "C (programming language)") programming language, and tools such as [Yacc](https://en.wikipedia.org/wiki/Yacc "Yacc")), and others more detailed descriptions of operating system features. The printed version of the manual initially fit into a single binder, but as of [PWB/UNIX](https://en.wikipedia.org/wiki/PWB/UNIX "PWB/UNIX") and the [7th Edition](https://en.wikipedia.org/wiki/Version_7_Unix "Version 7 Unix") of [Research Unix](https://en.wikipedia.org/wiki/Research_Unix "Research Unix"), it was split into two volumes with the printed man pages forming Volume 1.[^5]

Later versions of the documentation imitated the first man pages' terseness. Ritchie added a "How to get started" section to the [Third Edition](https://en.wikipedia.org/wiki/Version_3_Unix "Version 3 Unix") introduction, and [Lorinda Cherry](https://en.wikipedia.org/wiki/Lorinda_Cherry "Lorinda Cherry") provided the "Purple Card" pocket reference for the [Sixth](https://en.wikipedia.org/wiki/Version_6_Unix "Version 6 Unix") and [Seventh](https://en.wikipedia.org/wiki/Version_7_Unix "Version 7 Unix") Editions.[^4] Versions of the software were named after the revision of the manual; the seventh edition of the *Unix Programmer's Manual*, for example, came with the 7th Edition or Version 7 of Unix.[^6]

For the [Fourth](https://en.wikipedia.org/wiki/Version_4_Unix "Version 4 Unix") Edition the man pages were formatted using the [troff](https://en.wikipedia.org/wiki/Troff "Troff") typesetting package [^4] and its set of `-man` macros (which were completely revised between the Sixth and Seventh Editions of the *Manual*,[^5] but have since not drastically changed). At the time, the availability of online documentation through the manual page system was regarded as a great advance. To this day, virtually every Unix command line application comes with a man page, and many Unix users perceive a program's lack of man pages as a sign of low quality or incompleteness. Indeed, some projects, such as [Debian](https://en.wikipedia.org/wiki/Debian "Debian"), go out of their way to write man pages for programs lacking one. The modern descendants of [4.4BSD](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution "Berkeley Software Distribution") also distribute man pages as one of the primary forms of system documentation (having replaced the old `-man` macros with the newer `-mdoc`).

There was a hidden [Easter egg](https://en.wikipedia.org/wiki/Easter_egg_\(media\) "Easter egg (media)") in the man-db version of the man command that would cause the command to return "gimme gimme gimme" when run at 00:30 (a reference to the [ABBA](https://en.wikipedia.org/wiki/ABBA "ABBA") song [Gimme! Gimme! Gimme! (A Man After Midnight)](https://en.wikipedia.org/wiki/Gimme!_Gimme!_Gimme!_\(A_Man_After_Midnight\) "Gimme! Gimme! Gimme! (A Man After Midnight)")). It was introduced in 2011 [^7] but first restricted [^8] and then removed in 2017 [^9] after finally being found.[^10]

## Formatting

![](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/FreeBSD_typeset_man_page.png/250px-FreeBSD_typeset_man_page.png)

Part of the FreeBSD man(1) manual page, typeset into PDF format

The default format of man pages is [troff](https://en.wikipedia.org/wiki/Troff "Troff"), with either the [macro package](https://en.wikipedia.org/wiki/Troff_macros "Troff macros") man (appearance oriented) or mdoc (semantic oriented). This makes it possible to typeset a man page into [PostScript](https://en.wikipedia.org/wiki/PostScript "PostScript"), [PDF](https://en.wikipedia.org/wiki/Portable_document_format "Portable document format"), and various other formats for viewing or printing.

Some [Unix](https://en.wikipedia.org/wiki/Unix "Unix") systems have a package for the man2html command, which enables users to browse their man pages using an HTML browser. Systems with groff and man-db should use the higher-quality native HTML output (man --html) instead. The [GNU Emacs](https://en.wikipedia.org/wiki/GNU_Emacs "GNU Emacs") program *WoMan* (from "WithOut man") allows for browsing man pages from the editor.[^11]

In 2010, [OpenBSD](https://en.wikipedia.org/wiki/OpenBSD "OpenBSD") deprecated [troff](https://en.wikipedia.org/wiki/Troff "Troff") for formatting man pages in favour of [mandoc](https://en.wikipedia.org/wiki/Mandoc "Mandoc"), a specialised compiler/formatter for man pages with native support for output in [PostScript](https://en.wikipedia.org/wiki/PostScript "PostScript"), [HTML](https://en.wikipedia.org/wiki/HTML "HTML"), [XHTML](https://en.wikipedia.org/wiki/XHTML "XHTML"), and the terminal. It is meant to only support a subset of troff used in manual pages, specifically those using mdoc macros.

### Online services

Quite a few websites offer online access to manual pages from various Unix-like systems.

In February 2013, the [BSD](https://en.wikipedia.org/wiki/BSD "BSD") community saw a new open source [mdoc.su](http://mdoc.su/) service launched, which unified and shortened access to the man.cgi scripts of the major modern BSD projects through a unique [nginx](https://en.wikipedia.org/wiki/Nginx "Nginx") -based deterministic [URL shortening](https://en.wikipedia.org/wiki/URL_shortening "URL shortening") service for the \*BSD man pages.[^12] [^13] [^14]

For Linux, a man7.org service has been set up to serve manuals specific to the system.[^15] A ManKier service provides a wider selection, and integrates the TLDR pages too.[^16]

## Command usage

To read a manual page for a Unix command, a user can type:

```
man <command_name>
```

Pages are traditionally referred to using the notation "name(section)": for example, `ftp(1)`. The section refers to different ways the topic might be referenced - for example, as a system call, or a shell (command line) command or package, or a package's configuration file, or as a coding construct / header.

The same page name may appear in more than one section of the manual, such as when the names of [system calls](https://en.wikipedia.org/wiki/System_call "System call"), user [commands](https://en.wikipedia.org/wiki/Command_\(computing\) "Command (computing)"), or [macro packages](https://en.wikipedia.org/wiki/Troff_macro "Troff macro") coincide. Examples are `man(1)` and `man(7)`, or `exit(2)` and `exit(3)`. The syntax for accessing the non-default manual section varies between different man implementations.

On Solaris and illumos, for example, the syntax for reading `printf(3C)` is:

```
man -s 3c printf
```

On Linux and BSD derivatives the same invocation would be:

```
man 3 printf
```

which searches for *[printf](https://en.wikipedia.org/wiki/Printf "Printf")* in section 3 of the man pages. The actual file name likely includes the section. Continuing this example, printf.3.gz would be a compressed manual page file in section 3 for *[printf](https://en.wikipedia.org/wiki/Printf "Printf")*.

## Manual sections

The manual is generally split into eight numbered sections. Most systems today (e.g. [BSD](https://en.wikipedia.org/wiki/BSD "BSD"),[^17] [macOS](https://en.wikipedia.org/wiki/MacOS "MacOS"), [Linux](https://en.wikipedia.org/wiki/Linux "Linux"),[^18] and [Solaris](https://en.wikipedia.org/wiki/Oracle_Solaris "Oracle Solaris") 11.4) inherit the numbering scheme used by [Research Unix](https://en.wikipedia.org/wiki/Research_Unix "Research Unix"),[^19] [^20] while [System V](https://en.wikipedia.org/wiki/UNIX_System_V "UNIX System V") uses a different order:[^21]

| Common | System V | Description |
| --- | --- | --- |
| 1 | 1 | General [commands](https://en.wikipedia.org/wiki/Command_\(computing\) "Command (computing)") |
| 2 | 2 | [System calls](https://en.wikipedia.org/wiki/System_call "System call") |
| 3 | 3 | [Library](https://en.wikipedia.org/wiki/Library_\(computing\) "Library (computing)") functions, covering in particular the [C standard library](https://en.wikipedia.org/wiki/C_standard_library "C standard library") |
| 4 | 7 | [Special files](https://en.wikipedia.org/wiki/Special_file "Special file") (usually devices, those found in /dev) and [drivers](https://en.wikipedia.org/wiki/Device_driver "Device driver") |
| 5 | 4 | [File formats](https://en.wikipedia.org/wiki/File_format "File format") and conventions |
| 6 | 6 | [Games](https://en.wikipedia.org/wiki/Video_game "Video game") and [screensavers](https://en.wikipedia.org/wiki/Screensaver "Screensaver") |
| 7 | 5 | Miscellaneous |
| 8 | 1M | System administration [commands](https://en.wikipedia.org/wiki/Command_\(computing\) "Command (computing)") and [daemons](https://en.wikipedia.org/wiki/Daemon_\(computer_software\) "Daemon (computer software)") |

[POSIX](https://en.wikipedia.org/wiki/POSIX "POSIX") APIs are present in both sections 2 and 3, where section 2 contains APIs that are implemented as system calls and section 3 contains APIs that are implemented as library routines.

On some systems, additional sections may be included, such as:

| Section | Description |
| --- | --- |
| 0 | [C library](https://en.wikipedia.org/wiki/C_library "C library") [header files](https://en.wikipedia.org/wiki/Header_file "Header file") (Unix v6) |
| 9 | [Kernel](https://en.wikipedia.org/wiki/Kernel_\(operating_system\) "Kernel (operating system)") routines (FreeBSD, SVR4, Linux) [^20] [^17] |
| l | [LAPACK](https://en.wikipedia.org/wiki/LAPACK "LAPACK") library functions [^22] |
| n | [Tcl](https://en.wikipedia.org/wiki/Tcl_\(programming_language\) "Tcl (programming language)") / [Tk](https://en.wikipedia.org/wiki/Tk_\(computing\) "Tk (computing)") commands |
| x | The [X Window System](https://en.wikipedia.org/wiki/X_Window_System "X Window System") |

Some sections are further subdivided by means of a suffix; for example, in some systems, section 3C is for C library calls, 3M is for the math library, and so on. A consequence of this is that section 8 (system administration commands) is sometimes relegated to the 1M subsection of the main commands section. Some subsection suffixes have a general meaning across sections:

| Subsection | Description |
| --- | --- |
| p | [POSIX](https://en.wikipedia.org/wiki/POSIX "POSIX") specifications |
| x | [X Window System](https://en.wikipedia.org/wiki/X_Window_System "X Window System") documentation |

(Section 3 tends to be the exception, with many suffixes for different languages.)

Some versions of `man` cache the formatted versions of the last several pages viewed. One form is the *cat page*, simply piped to the pager for display.

## Layout

All man pages follow a common layout that is optimized for presentation on a simple [ASCII](https://en.wikipedia.org/wiki/ASCII "ASCII") text display, possibly without any form of highlighting or font control. Sections present may include:[^23]<sup><span title="Location: MANUAL STRUCTURE">: MANUAL STRUCTURE</span></sup>

NAME

The name of the command or function, followed by a one-line description of what it does.

SYNOPSIS

In the case of a command, a formal description of how to run it and what command line options it takes. For program functions, a list of the parameters the function takes and which header file contains its declaration.

DESCRIPTION

A textual description of the functioning of the command or function. For programs, this section often includes explanations of available command line options.

EXAMPLES

Some examples of common usage.

SEE ALSO

A list of related commands or functions.

Other sections may be present, but these are not well standardized across man pages. Common examples include: OPTIONS, EXIT STATUS, RETURN VALUE, ENVIRONMENT, BUGS, FILES, AUTHOR, REPORTING BUGS, HISTORY and COPYRIGHT.

## Authoring

Manual pages can be written either in the old `man` macros or the new `doc` macros.[^24] The `man` macro set provides minimal [rich text](https://en.wikipedia.org/wiki/Rich_text "Rich text") functions, with directives for the title line, section headers, (bold, small or italic) fonts, paragraphs and adding/reducing indentation.[^25] The newer `mdoc` language is more semantic in nature, and contains specialized macros for most standard sections such as program name, synopsis, function names, and the name of the authors. This information can be used to implement a [semantic search](https://en.wikipedia.org/wiki/Semantic_search "Semantic search") for manuals by programs such as [mandoc](https://en.wikipedia.org/wiki/Mandoc "Mandoc"). Although it also includes directives to directly control the styling, it is expected that the specialized macros will cover most of the use-cases.[^23] Both the mandoc and the groff projects consider `mdoc` the preferred format for new documents.[^26]

Although man pages are, to troff, text laid out using 10-point [Roman type](https://en.wikipedia.org/wiki/Roman_type "Roman type"), this distinction is usually moot because man pages are viewed in the terminal (TTY) instead of laid out on paper. As a result, the "small font" macro is seldom used.[^27] On the other hand, bold and italic text is supported by the terminal via [ECMA-48](https://en.wikipedia.org/wiki/ECMA-48 "ECMA-48"), and groff's `grotty` does emit them as requested when it detects a supporting terminal. The BSD mandoc however only supports bold and underlined (as a replacement for italics) text via the typewriter backspace-then-overstrike sequence, which needs to be translated into ECMA-48 by `less`.[^28] [^29]

Some tools have been used to convert documents in a less contrived format to manual pages. Examples include GNU's `help2man`, which takes a `--help` output and some additional content to generate a manual page.[^30] The manual would be barely more useful than the said output, but for GNU programs this is not an issue as texinfo is the main documentation system.[^31] A number of tools, including [pandoc](https://en.wikipedia.org/wiki/Pandoc "Pandoc"), ronn, and md2man support conversion from [Markdown](https://en.wikipedia.org/wiki/Markdown "Markdown") to manual pages. All these tools emit the `man` format, as Markdown is not expressive enough to match the semantic content of `mdoc`. [DocBook](https://en.wikipedia.org/wiki/DocBook "DocBook") has an inbuilt man(7) converter – of appalling quality, according to mandoc's author [^32] who wrote a separate mdoc(7) converter.

Man pages are usually written in English, but translations into other languages may be available on the system. The GNU `man-db` and the mandoc `man` is known to search for localized manual pages under subdirectories.[^33] [^18]<sup><span title="Location: Overview">: Overview</span> </sup> [^17]

### Alternatives

Few alternatives to `man` have enjoyed much popularity, with the possible exception of [GNU Project's](https://en.wikipedia.org/wiki/GNU_Project "GNU Project") " `info` " system, an early and simple [hypertext](https://en.wikipedia.org/wiki/Hypertext "Hypertext") system. There is also a third-party effort known as [TLDR pages](https://en.wikipedia.org/wiki/TLDR_pages "TLDR pages") (`tldr`) that provides simple examples for common use cases, similar to a [cheatsheet](https://en.wikipedia.org/wiki/Cheatsheet "Cheatsheet").[^34]

In addition, some Unix [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface "Graphical user interface") applications (particularly those built using the [GNOME](https://en.wikipedia.org/wiki/GNOME "GNOME") and [KDE](https://en.wikipedia.org/wiki/KDE "KDE") development environments) now provide end-user documentation in [HTML](https://en.wikipedia.org/wiki/HTML "HTML") and include embedded HTML viewers such as `yelp` for reading the help within the application. An HTML system in [Emacs](https://en.wikipedia.org/wiki/Emacs "Emacs") is also slated to replace texinfo.[^35]

[^1]: ["man(1)"](https://man.freebsd.org/cgi/man.cgi?query=man&sektion=1). *FreeBSD General Commands Manual*. [Archived](https://web.archive.org/web/20230130060434/https://man.freebsd.org/cgi/man.cgi?query=man&sektion=1) from the original on 2023-01-30. Retrieved 2023-07-15.

[^2]: [*ASTM Standards on Computerized Systems*](https://archive.org/details/annualbookofastm00amer/page/136/mode/2up?q=binders) (second ed.). American Society for Testing and Materials. 1987. p. 136. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0-8031-1580-4](https://en.wikipedia.org/wiki/Special:BookSources/978-0-8031-1580-4 "Special:BookSources/978-0-8031-1580-4"). Order forms, paper, ribbons, magnetic storage media, and other supplies that will be needed to operate the system. Also order file and storage cabinets, racks and binders, and other miscellaneous office hardware for documentation, printout, magnetic tape reels, disk packs, and other such items.

[^3]: [Adam Osborne](https://en.wikipedia.org/wiki/Adam_Osborne "Adam Osborne") (June 1969). ["OSBORNE/McGraw-Hill presents An Introduction to Microcomputers"](https://archive.org/details/InterfaceAge198005/page/n137/mode/2up?q=binders). *Software Age*.

[^4]: [McIlroy, M. D.](https://en.wikipedia.org/wiki/Doug_McIlroy "Doug McIlroy") (1987). [*A Research Unix reader: annotated excerpts from the Programmer's Manual, 1971–1986*](http://www.cs.dartmouth.edu/~doug/reader.pdf) (PDF) (Technical report). CSTR. Bell Labs. 139. [Archived](https://web.archive.org/web/20171111151817/http://www.cs.dartmouth.edu/~doug/reader.pdf) (PDF) from the original on 2017-11-11. Retrieved 2015-02-01.

[^5]: Darwin, Ian; Collyer, Geoffrey. ["UNIX Evolution: 1975-1984 Part I - Diversity"](http://www.collyer.net/who/geoff/history.html). [Archived](https://web.archive.org/web/20120717002523/http://www.collyer.net/who/geoff/history.html) from the original on 17 July 2012. Retrieved 22 December 2012. Originally published in *Microsystems* **5** (11), November 1984.

[^6]: Fiedler, Ryan (October 1983). ["The Unix Tutorial / Part 3: Unix in the Microcomputer Marketplace"](https://archive.org/stream/byte-magazine-1983-10/1983_10_BYTE_08-10_UNIX#page/n133/mode/2up). *BYTE*. p. 132. Retrieved 30 January 2015.

[^7]: ["GIT commit 002a6339b1fe8f83f4808022a17e1aa379756d99"](https://git.savannah.nongnu.org/cgit/man-db.git/commit/src/man.c?id=002a6339b1fe8f83f4808022a17e1aa379756d99). [Archived](https://web.archive.org/web/20171204003014/http://git.savannah.nongnu.org/cgit/man-db.git/commit/src/man.c?id=002a6339b1fe8f83f4808022a17e1aa379756d99) from the original on 4 December 2017. Retrieved 22 November 2017.

[^8]: ["GIT commit 84bde8d8a9a357bd372793d25746ac6b49480525"](https://git.savannah.gnu.org/cgit/man-db.git/commit/?id=84bde8d8a9a357bd372793d25746ac6b49480525). [Archived](https://web.archive.org/web/20180905095817/https://git.savannah.gnu.org/cgit/man-db.git/commit/?id=84bde8d8a9a357bd372793d25746ac6b49480525) from the original on 5 September 2018. Retrieved 22 November 2017.

[^9]: ["GIT commit b225d9e76fbb0a6a4539c0992fba88c83f0bd37e"](https://git.savannah.gnu.org/cgit/man-db.git/commit/?id=b225d9e76fbb0a6a4539c0992fba88c83f0bd37e). [Archived](https://web.archive.org/web/20201109034103/https://git.savannah.gnu.org/cgit/man-db.git/commit/?id=b225d9e76fbb0a6a4539c0992fba88c83f0bd37e) from the original on 9 November 2020. Retrieved 25 September 2018.

[^10]: [""Why does man print "gimme gimme gimme" at 00:30?""](https://unix.stackexchange.com/questions/405783/why-does-man-print-gimme-gimme-gimme-at-0030). [Archived](https://web.archive.org/web/20171121230223/https://unix.stackexchange.com/questions/405783/why-does-man-print-gimme-gimme-gimme-at-0030) from the original on 21 November 2017. Retrieved 22 November 2017.

[^11]: Wright, Francis J. ["WoMan: Browse Unix Manual Pages "W.O. (without) Man""](https://www.gnu.org/software/emacs/manual/html_mono/woman.html). GNU. [Archived](https://web.archive.org/web/20201111204938/https://www.gnu.org/software/emacs/manual/html_mono/woman.html) from the original on 11 November 2020. Retrieved 3 August 2020.

[^12]: Pali, Gabor, ed. (12 May 2013). ["FreeBSD Quarterly Status Report, January-March 2013"](http://www.freebsd.org/news/status/report-2013-01-2013-03.html#mdoc.su-%E2%80%94-Short-Manual-Page-URLs). [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD "FreeBSD"). [Archived](https://web.archive.org/web/20141222022258/http://www.freebsd.org/news/status/report-2013-01-2013-03.html#mdoc.su-%E2%80%94-Short-Manual-Page-URLs) from the original on 22 December 2014. Retrieved 25 December 2014.

[^13]: Murenin, Constantine A. (19 February 2013). ["announcing mdoc.su, short manual page URLs"](http://lists.freebsd.org/pipermail/freebsd-doc/2013-February/021465.html). *freebsd-doc@freebsd.org* (Mailing list). [Archived](https://web.archive.org/web/20140807051219/http://lists.freebsd.org/pipermail/freebsd-doc/2013-February/021465.html) from the original on 7 August 2014. Retrieved 25 December 2014.

[^14]: Murenin, Constantine A. (23 February 2013). ["mdoc.su — Short manual page URLs for FreeBSD, OpenBSD, NetBSD and DragonFly BSD"](http://mdoc.su/). [Archived](https://web.archive.org/web/20141217170726/http://mdoc.su/) from the original on 17 December 2014. Retrieved 25 December 2014.

[^15]: ["Linux man pages online"](http://man7.org/linux/man-pages/index.html). *man7.org*. [Archived](https://web.archive.org/web/20200507122101/http://www.man7.org/linux/man-pages/index.html) from the original on 2020-05-07. Retrieved 2020-05-05.

[^16]: ["About"](https://www.mankier.com/about). *ManKier*. [Archived](https://web.archive.org/web/20200425112006/https://www.mankier.com/about) from the original on 2020-04-25. Retrieved 2020-05-05.

[^17]: `man(1)` – [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD "FreeBSD") General Commands Manual

[^18]: `man(1)` – [Linux](https://en.wikipedia.org/wiki/Linux "Linux") General Commands Manual from ManKier.com

[^19]: ["Manual Pages for Research Unix Eighth Edition"](http://man.cat-v.org/unix_8th/). *man.cat-v.org*. [Archived](https://web.archive.org/web/20200630215702/http://man.cat-v.org/unix_8th/) from the original on 2020-06-30. Retrieved 2020-05-06.

[^20]: ["Unix Programmer's Manual - Introduction"](https://www.bell-labs.com/usr/dmr/www/manintro.html). *www.bell-labs.com*. November 3, 1971. [Archived](https://web.archive.org/web/20200601064923/https://www.bell-labs.com/usr/dmr/www/manintro.html) from the original on June 1, 2020. Retrieved May 6, 2020.

[^21]: ["System V release 4 manuals"](http://bitsavers.trailing-edge.com/pdf/att/unix/System_V_Release_4/). *bitsavers.trailing-edge.com*. [Archived](https://web.archive.org/web/20200803205815/http://bitsavers.trailing-edge.com/pdf/att/unix/System_V_Release_4/) from the original on 2020-08-03. Retrieved 2020-05-06.

[^22]: ["lapack (l) - Linux Man Pages"](https://www.systutorials.com/docs/linux/man/l-lapack/). *www.systutorials.com*. [Archived](https://web.archive.org/web/20230311130845/https://www.systutorials.com/docs/linux/man/l-lapack/) from the original on 2023-03-11. Retrieved 2021-05-29.

[^23]: `mdoc(7)` – [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD "FreeBSD") Miscellaneous Information Manual

[^24]: `groff_tmac(5)` – [Linux](https://en.wikipedia.org/wiki/Linux "Linux") File Formats Manual from ManKier.com

[^25]: `man(7)` – [Linux](https://en.wikipedia.org/wiki/Linux "Linux") Miscellanea Manual from ManKier.com

[^26]: ["Groff Mission Statement - 2014"](https://www.gnu.org/software/groff/groff-mission-statement.html). *www.gnu.org*. [Archived](https://web.archive.org/web/20201203121306/https://www.gnu.org/software/groff/groff-mission-statement.html) from the original on 2020-12-03. Retrieved 2021-01-02. Concurrent with work on man(7), mdoc(7) will be actively supported and its use promoted.

[^27]: ["man"](https://www.gnu.org/software/groff/manual/html_node/man.html). *The GNU Troff Manual*. [Archived](https://web.archive.org/web/20191224124039/https://www.gnu.org/software/groff/manual/html_node/man.html) from the original on 24 December 2019. Retrieved 31 December 2019.

[^28]: ["Italics and colour in manual pages on a nosh user-space virtual terminal"](https://jdebp.uk/Softwares/nosh/italics-in-manuals.html). *jdebp.eu*. [Archived](https://web.archive.org/web/20210128033617/https://jdebp.uk/Softwares/nosh/italics-in-manuals.html) from the original on 2021-01-28. Retrieved 2021-01-21.

[^29]: `mandoc(1)` – [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD "FreeBSD") General Commands Manual. "Font styles are applied by using back-spaced encoding..."

[^30]: ["help2man Reference Manual"](https://www.gnu.org/software/help2man). [Archived](https://web.archive.org/web/20230306093151/https://www.gnu.org/software/help2man/) from the original on 6 March 2023. Retrieved 5 March 2023.

[^31]: ["Man Pages (GNU Coding Standards)"](https://www.gnu.org/prep/standards/html_node/Man-Pages.html). *www.gnu.org*. [Archived](https://web.archive.org/web/20230305170922/https://www.gnu.org/prep/standards/html_node/Man-Pages.html) from the original on 2023-03-05. Retrieved 2023-03-05.

[^32]: Ingo Schwarze. ["New mandoc -mdoc -T markdown converter"](https://undeadly.org/cgi?action=article&sid=20170304230520). *undeadly.org*. [Archived](https://web.archive.org/web/20230305170920/https://undeadly.org/cgi?action=article&sid=20170304230520) from the original on 2023-03-05. Retrieved 2023-03-05. – for specific complaints by the author, see Ingo Schwarze (28 February 2014). ["Re: Groff man pages (tangential to Future Redux)"](https://lists.gnu.org/archive/html/groff/2014-02/msg00109.html). *Groff* (Mailing list). [Archived](https://web.archive.org/web/20230305171936/https://lists.gnu.org/archive/html/groff/2014-02/msg00109.html) from the original on 2023-03-05.

[^33]: ["command line - Linux man pages in different languages"](https://askubuntu.com/a/1113662). *Ask Ubuntu*. [Archived](https://web.archive.org/web/20230311130846/https://askubuntu.com/questions/1113648/linux-man-pages-in-different-languages/1113662) from the original on 2023-03-11. Retrieved 2020-05-05.

[^34]: ["TLDR pages"](https://tldr.sh/). *tldr.sh*. [Archived](https://web.archive.org/web/20200427081953/https://tldr.sh/) from the original on 2020-04-27. Retrieved 2020-05-05.

[^35]: [Raymond, Eric S.](https://en.wikipedia.org/wiki/Eric_S._Raymond "Eric S. Raymond") ["Re: \[Groff\] man pages (tangential to Future Redux)"](https://lists.gnu.org/archive/html/groff/2014-02/msg00104.html). *groff* (Mailing list). [Archived](https://web.archive.org/web/20230305171106/https://lists.gnu.org/archive/html/groff/2014-02/msg00104.html) from the original on 2023-03-05. Retrieved 2023-03-05 – via lists.gnu.org.