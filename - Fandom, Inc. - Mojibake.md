---
source: "https://worldlanguages.fandom.com/wiki/Mojibake"
author:
  - "[[Contributors to Languages Wiki]]"
published:
created: 2026-04-19
---
![Mojibake shown on a website in .](https://worldlanguages.fandom.com/wiki/Mojibake_text.png)

Mojibake shown on a website in Japanese script.

**Mojibake** (Japanese: 文字化け Pronunciation: \[modʑibake\] "unintelligible sequence of characters"), from Japanese 文字 (moji), meaning "character" and 化け (bake), meaning change, is an occurence of incorrect unreadable characters displayed when [computer software](https://en.wikipedia.org/wiki/en:Computer_software "wikipedia:en:Computer software") fails to render text correctly to its associated character encoding.

## Causes

![The  's article on mojibake, rendered using  encoding.](https://worldlanguages.fandom.com/wiki/Mojibake.png)

The Japanese Wikipedia 's article on mojibake, rendered using Windows-1252 encoding.

Mojibake often occurs when a character coding is incorrectly tagged in a document, or when a document is moved to a system with a different default coding than its preceding location. Such incorrect displays occur when writing systems or character encodings are mistagged or "foreign" to the computer system of the user: if a computer does not have a software required to process the characters of a foreign language, it attempts to process them in its default language encoding, which usually results in gibberish. Messages transferred between different encodings of the same language can also cause some mojibake problems. Users of the Japanese language, which has had several different encodings historically applied, would encounter this problem often. For example, the intended word in Japanese script, "文字化け", encoded in UTF-8, is incorrectly shown as "æ–‡å—åŒ–ã" in software configured to expect text in [Windows-1252](https://en.wikipedia.org/wiki/en:Windows-1252 "wikipedia:en:Windows-1252") and ISO/IEC 8859-1 encodings, usually labelled as Western.

A [web browser](https://en.wikipedia.org/wiki/en:Web_browser "wikipedia:en:Web browser") may not be able to display characters on a page coded in EUC-JP and another in Shift JIS if the coding scheme is not clearly assigned using [HTTP headers](https://en.wikipedia.org/wiki/en:HTTP_headers "wikipedia:en:HTTP headers") sent with the documents, or using the [HTML](https://en.wikipedia.org/wiki/en:HTML "wikipedia:en:HTML") document's [metatags](https://en.wikipedia.org/wiki/en:Metatag "wikipedia:en:Metatag") that are used as substitutes for missing HTTP headers if the server cannot be configured to send proper HTTP headers. Heuristics can be applied to guess at the set of characters, but are not always successful.

In the mid 1990s, due to commonness of this problem, several websites actually featured mojibake not as a problem to be solved, but as a method of amusement. Words and sentences were "deciphered" with meanings that delivered funny messages.

Mojibake also appears in what appear to be two same encodings. For example, some software created by [Microsoft](https://en.wikipedia.org/wiki/en:Microsoft "wikipedia:en:Microsoft") and [Eudora](https://en.wikipedia.org/wiki/en:Eudora_\(e-mail_client\) "wikipedia:en:Eudora (e-mail client)") for [Microsoft Windows](https://en.wikipedia.org/wiki/en:Microsoft_Windows "wikipedia:en:Microsoft Windows") supposedly encoded their output using ISO 8859-1 encoding, while they really used Windows-1252 that contains extra printable characters in the C1 range. These were not displayed correctly in software complying with the ISO standard, especially affecting software running under different operating systems, an example being [Unix](https://en.wikipedia.org/wiki/en:Unix "wikipedia:en:Unix").

## Solutions

Applications that use UTF-8 as a default encoding may achieve a greater degree of interoperability because it has been used widespread, and has backwards compatibility with ASCII.

The difficulty of resolving mojibake varies depending on the application in which mojibake occurs and what causes it. Two common applications that have problems with mojibake are web browsers and [word processors](https://en.wikipedia.org/wiki/en:Word_processor "wikipedia:en:Word processor"). Modern browsers and word processors usually support a wide array of character encodings. Browsers often allow users to change their [rendering engine](https://en.wikipedia.org/wiki/en:Rendering_engine "wikipedia:en:Rendering engine") 's encoding set on the go, while word processors allow users to select the appropriate encoding when opening files. It may take [trial and error](https://en.wikipedia.org/wiki/en:Trial_and_error "wikipedia:en:Trial and error") for users in order to determine the correct encoding.

This problem is more complicated when it occurs in an application that usually does not support a wide range of encodings, such as in non-Unicode computer games. If this is the case, the user must change the encoding settings of the operating system to match that of the game. However, changing system-wide encoding settings can also cause mojibake in already existing applications. In [Windows XP](https://en.wikipedia.org/wiki/en:Windows_XP "wikipedia:en:Windows XP") or later, a user is given the option to use [Microsoft AppLocale](https://en.wikipedia.org/wiki/en:Microsoft_AppLocale "wikipedia:en:Microsoft AppLocale"), an application allowing the change of per-application locale settings. Even so, changing the encoding settings of the operating system is impossible with earlier operating systems such as [Windows 98](https://en.wikipedia.org/wiki/en:Windows_98 "wikipedia:en:Windows 98"). To resolve this issue with earlier operating systems, users must use a third-party font for rendering the applications.

## Problems with specific languages

[Commodore International](https://en.wikipedia.org/wiki/en:Commodore_International "wikipedia:en:Commodore International") 's [8-bit](https://en.wikipedia.org/wiki/en:8-bit "wikipedia:en:8-bit") computers used [PETSCII](https://en.wikipedia.org/wiki/en:PETSCII "wikipedia:en:PETSCII") encoding, which is notable for *inverting* the upper and lower case compared to ASCII. Printers using the PETSCII encoding work rather fine on other computers of the era, with the only problem being that it flipped the case of all the letters.

In German, common terms of this phenomenon are *Buchstabensalat* (letter salad) and *Krähenfüße* (crow's feet).

Another affected language is Arabic (see the [example](#Example)).

### French

Fran軋is=Français

### English

Mojibake in [English](https://worldlanguages.fandom.com/wiki/English_language "English language") texts usually occurs with punctuation, such as em dashes (—), en dashes (–), and curly quotes (“, ”), but rarely in character texts, due to the fact that most encodings agree with ASCII on encoding the English alphabet. For example, the pound sign " £ " will appear as "Â£" if it was encoded by the sender as UTF-8 but interpreted by the recipient as CP1252 or ISO 8859-1. If this was repeated on each item, this can lead to "Ã‚Â£", "Ãƒâ€šÃ‚Â£", etc.

### Japanese

In Japanese, as mentioned before, this phenomenon is called *mojibake* 文字化け. It is often encountered by non-Japanese users attempting to run software that is written solely for the Japanese market.

### Central Europe

Users of [Central](https://en.wikipedia.org/wiki/en:Central_Europe "wikipedia:en:Central Europe") and [Eastern](https://en.wikipedia.org/wiki/en:Eastern_Europe "wikipedia:en:Eastern Europe") European languages are also affected by mojibake. Because most computers were unconnected to any network during the 1980s, there were different character encodings for *every* language with diacritical characters.

### Cyrillic-based scripts

![A sender's handwritten krakozyabry corrected by a postal employee before it was delivered to its destination.](https://worldlanguages.fandom.com/wiki/Letter_to_Russia_with_krokozyabry.jpg)

A sender's handwritten krakozyabry corrected by a postal employee before it was delivered to its destination.

Mojibake may also be called *krakozyabry* (кракозя́бры) in [Russian](https://worldlanguages.fandom.com/wiki/Russian_language "Russian language"), which was and still remains complicated by a number of systems for encoding [Cyrillic scripts](https://worldlanguages.fandom.com/wiki/Cyrillic_script "Cyrillic script").[^1] The [Soviet Union](https://en.wikipedia.org/wiki/en:Soviet_Union "wikipedia:en:Soviet Union") and early [Russian Federation](https://en.wikipedia.org/wiki/en:Russian_Federation "wikipedia:en:Russian Federation") created KOI character encodings (*Kod Obmena Informatsiey*, Код Обмена Информацией; literally translates into "Code for Information Exchange"). This was started with the Cyrillic-only 7-bit KOI-7, which was based on ASCII, but with the Latin and some other characters being replaced with Cyrillic characters. After this came the 8-bit KOI-8 encoding, which is an ASCII extension which encodes Cyrillic characters only with high-bit set octets corresponding to the 7-bit codes from the preceding KOI-7. That is the reason why KOI-8 text, even Russian, remains only partially readable after removing the eighth bit, which was considered a major advantage during the age of [8BITMIME](https://en.wikipedia.org/wiki/en:8BITMIME "wikipedia:en:8BITMIME") -unaware e-mail systems. Eventually, KOI-8 gained different flavors for Russian/ Bulgarian (KOI8-R), Ukrainian (KOI8-U), Belarusian (KOI8-RU), and even Tajik (KOI8-T).

Meanwhile, in the West, [Ukrainian](https://worldlanguages.fandom.com/wiki/Ukrainian_language "Ukrainian language") and Belarusian, as well as Bulgarian and Russian were supported by code page 866 in [MS-DOS](https://en.wikipedia.org/wiki/en:MS-DOS "wikipedia:en:MS-DOS"). For users of [Microsoft Windows](https://en.wikipedia.org/wiki/en:Microsoft_Windows "wikipedia:en:Microsoft Windows"), code page 1251 added support for the Serbian Cyrillic alphabet and other Slavic variants of Cyrillic. More recently, Unicode includes characters from the Early Cyrillic alphabet and non-Slavic minority languages in the Russian Federation. Currently, Unicode attempts to replace confusion with a system whereby any written languages of the world is either displayed correctly or informs you of which font the user needs to install, however, Unicode still remains unreactive to the legacy KOI and Code page encodings.

Before Unicode was developed, it was necessary to match text encodings with a font using the same coding system. Failure to do this displayed unreadable gibberish with appearances varying, depending on the exact combination of text encoding and font encoding. Vowels containing accents were symptomatic in the process of trying to view Cyrillic encoding with a font designed limitedly to the Latin alphabet. In general, Cyrillic gibberish was caused by using the wrong Cyrillic font. Unicode text in a location where it is not accomodated merely displays several question marks.

In the Bulgarian language, this phenomenon is known as *maymunitsa* (маймуница), literally translating into "monkey's alphabet". In the Serbian language, it is known as ђубре (*đubre*), translating into " [trash](https://en.wikipedia.org/wiki/en:Trash "wikipedia:en:Trash") ". Unlike the former Russian Federation, South Slavs never used a system like KO18, and Code Page 1251 was the dominant Cyrillic encoding in these areas before the development of Unicode. Therefore, the South Slavic languages experienced less encoding incompatibility issues with the Russian alphabet. During the 1980s, Bulgarian computers used its exclusive MIK encoding, which was a bit similar, but incompatible with, CP866.

### Polish

In Poland, all of the comapnies that sold early [DOS](https://en.wikipedia.org/wiki/en:DOS "wikipedia:en:DOS") computers developed their own encoding, simply reprogramming the [EPROMs](https://en.wikipedia.org/wiki/en:EPROM "wikipedia:en:EPROM") of the video cards (usually [CGA](https://en.wikipedia.org/wiki/en:Color_Graphics_Adapter "wikipedia:en:Color Graphics Adapter"), [EGA](https://en.wikipedia.org/wiki/en:Enhanced_Graphics_Adapter "wikipedia:en:Enhanced Graphics Adapter"), or [Hercules](https://en.wikipedia.org/wiki/en:Hercules_Graphic_Card "wikipedia:en:Hercules Graphic Card")) with needed glyphs for [Polish](https://worldlanguages.fandom.com/wiki/Polish_language "Polish language"), and in an arbitrary manner located without reference to where other computer sellers had placed them. Additionally, users of the then-popular home computers (such as [Atari ST](https://en.wikipedia.org/wiki/en:Atari_ST "wikipedia:en:Atari ST")) created their own encodings, incompatible with the international standards (ISO 8859-2), vendor standards (IBM CP852, Windows-1250), and locally agreed-upon PC/MS DOS standards (Mazovia). This situation started improving when, after pressure from groups of academics and users, ISO 8859-2 succeeded as "Internet standard" with a small amount of support from the dominant vendors' software, which is today largely replaced by Unicode. With several problems by the variety of encodings, even today some users refer to Polish diacritical characters as *krzaczki* ("bushes").

### Nordic languages and German

Among Nordic languages, mojibake is not an uncommon occurence, but is considered more of an annoyance than it is a problem. The Finnish and Swedish languages use the letters of the English alphabet with three additions: å, ä and ö, and it is typically these characters that are misinterpreted. This is similar with the situation in Danish and Norwegian, except the three affected letters are æ, ø and å, and in German the affected letters are ä, ö, ü and ß. In Swedish, Danish, Norwegian, and German, vowels are rarely ever repeated, and it is often obvious when a character is misinterpreted, such as the second letter in "kÃ⁠¤rlek" (*kärlek*, "love"). This way, even though the reader has to guess among the å, ä and ö, all texts usually remain perfectly readable. However, Finnish does have repeating vowels in words such as in the word "HÃ⁠¤Ã⁠¤yÃ⁠¶" (*hääyö*, "wedding night"), which can sometimes render text hard to read. Icelandic is worse, with ten possibly misinterpreted characters: á, ð, é, í, ó, ú, ý, þ, æ and ö.

### Asian encodings

![A  article on Wikipedia, incorrectly displayed as boxes.](https://static.wikia.nocookie.net/worldlanguages/images/c/cc/Mojibake-my.jpg/revision/latest/scale-to-width-down/250?cb=20110317151437)

A Burmese article on Wikipedia, incorrectly displayed as boxes.

Another variation of mojibake occurs when text is incorrectly parsed in a multi-byte encoding, such as one of the east Asian encodings. With this kind of mojibake, more than one (usually two) characters are incorrectly displayed at once, e.g. "k舐lek" (*kärlek*) in Swedish, where "är" is displayed as "舐". Compared to mojibake shown above, this is harder to read, as letters unrelated to the problematic å, ä or ö are missing. This is a major problem when displaying short words starting with these characters, such as "än" (which is displayed as "舅"). Since two letters are combined, this form of mojibake seems to be more random, with over 50 variants in comparison to the original three, not including the rarer capital letters. In rare cases, an entire string of text which happens to include a pattern of particular word lengths like in " Bush hid the facts " (displayed as "畢桳栠摩琠敨映捡獴"), may be misinterpreted.

Due to computer software issues like in most languages, writing from Asian languages may be replaced with other special characters, such as marks or boxes, due to the computer's inability to read Asian encodings.

### Countries of former Yugoslavia

The Slavic languages spoken in former Yugoslavia (Croatian, Bosnian, Serbian, Slovene) add to the original alphabet five letters: š, đ, č, ć, ž, along with their capital counterparts: Š, Đ, Č, Ć, Ž. All of these letters are defined as ISO 8859-2 and Windows-1250, while some of the characters (š, Š, ž, Ž, Đ) are present in the usual OS-default Western, and are only there because of some other languages.

Although those characters added in Windows-1252 (Western) are not immune from errors, the ones that are excluded are much more prone to errors. Even in present day, "šđčćž ŠĐČĆŽ" is often misinterpreted as "šðèæž ŠÐÈÆŽ", making users wonder where the ð, è, æ, È, Æ characters are used.

When confined to the basic ASCII (in most usernames), common replacements for characters are: š→s, đ→dj, č→c, ć→c, ž→z (capital forms, with Đ→Dj or Đ→DJ depending on word case). All of these replacements show ambiguities, so reconstructing what the original looked like is usually done manually if it is required.

The importance of Windows-1252 encoding is very high, because English versions of operating systems are found in more locations, and not the localized versions. The reasons for this are:

- A relatively small and fragmented market, increasing the price of high quality localization.
- A large degree of software piracy, caused by the high price of software in comparison to income, thus discouraging efforts of getting localized version.
- People prefer the English version of OS and other softwares.

The drive of differentiating Croatian from Serbian, Bosnian from Croatian and Serbian, and now even the Montenegrin alphabet from the other three shows to have many problems. There are numerous different localizations, using different standards and sometimes higher quality than others. There are no common translations for vast computer terminology created exclusively for the English language. In the end, people used adopted English words, such as kompjuter–computer and kompajlirati–compile. When this occurs, the people are completely unaccustomed to these translated terms, and often don't understand what some option is in menu supposed to do based upon the original phrase. Therefore, people who understand English and those who are accustomed to English terminology (which are most, because English terminology is taught at most schools due to the mentioned problems) will usually choose the original English version of the non-specialist software.

When Cyrillic script is used in these languages (for Macedonian and partially Serbian), this problem is relatively similar to [other Cyrillic-based scripts](#Cyrillic-based_scripts).

### Hungarian

The Hungarian language is also affected, using the 26 basic English characters as well as the accented forms á, é, í, ó, ú, ö, ü (all of which are present in Latin-1) and ő and ű, which are not included in Latin-1. However, these two characters can be correctly encoded with Latin-2, Windows-1250, and Unicode. Before Unicode was common in e-mail clients, e-mails containing Hungarian script often had the letters ő and ű displayed incorrectly, often to the point of unrecognizability. It is common to respond to an e-mail rendered unreadable with character mangling (referred to "betűszemét", meaning "garbage lettering" in English) with the phrase "Árvíztűrő tükörfúrógép" a nonsense phrase, literally meaning "Flood-resistant mirror-drilling machine", which includes all the accented characters used in the Hungarian alphabet.

### Indic text

![The erroneous Wikipedia logo, containing two errors, of which the Indic error is circled on the left.](https://static.wikia.nocookie.net/worldlanguages/images/f/f3/Erroneous_Wikipedia_logo.png/revision/latest/scale-to-width-down/200?cb=20110320030837)

The erroneous Wikipedia logo, containing two errors, of which the Indic error is circled on the left.

A similar effect is known to occur with Indic text, even if the character set used is recognized properly by the application. This is due to that, in many Indic scripts, the rules by which individual letter symbols combine to create symbols for syllables may be misunderstood by a computer without appropriate software, even if glyphs for the individual letter forms are available.

A notable example of this is the former Wikipedia logo, which attempts to show the character analogous to "w" or "wi" on each of the many puzzle pieces. Instead, the puzzle piece intended to bear the Devanagari character for "wi" formerly showed a somewhat nonsensical scribble with a line dangling at the end, which was easily recognizable as mojibake generated by a computer incompatible with correct displayment of Indic text. The fact that this occured on the front-page logo and has not been corrected over many years has been seen humorously emblematic of Wikipedia's questioned accuracy and reliability problems.[^2] The recently redesigned logo has fixed the error with the Devangari character, as well as a character of the Japanese script.

Some Indic and Indic-derived scripts, most notably the Lao script, were not officially supported by [Windows XP](https://en.wikipedia.org/wiki/en:Windows_XP "wikipedia:en:Windows XP") until the release of [Vista](https://en.wikipedia.org/wiki/en:Windows_Vista "wikipedia:en:Windows Vista").[^3] However, some websites have made free-to-download fonts.

### Spanish

[Spanish](https://worldlanguages.fandom.com/wiki/Spanish_language "Spanish language") is also affected by mojibake, which is known by the term *deformación* (literally meaning deformation). Its problems with mojibake are similar to those of the [Nordic languages](#Nordic_languages_and_German). Spanish uses all 26 of the standard Latin letters, but also includes ñ, acute accents with the five vowels (á, é, í, ó, ú), and sometimes ü. Ñ and the accent vowels are usually incorrectly displayed, as they are not available in ASCII.

## Example

| ![Wikipedia-logo](https://static.wikia.nocookie.net/worldlanguages/images/6/63/Wikipedia-logo.png/revision/latest/scale-to-width-down/50?cb=20110206214754)  Wikipedia-logo | This page or section incorporates [Creative Commons Licensed](https://community.fandom.com/wiki/Wikia:Licensing "w:Wikia:Licensing") content from [Wikipedia](https://en.wikipedia.org/wiki/Mojibake "wikipedia:Mojibake") ([view authors](http://en.wikipedia.org/w/index.php?title=Mojibake&action=history)). |
| --- | --- |

<table><tbody><tr><th>Output encoding</th><th>Setting in browser</th><th>Result</th></tr><tr><td colspan="2">Arabic example:</td><td>منتدى عرب شير مشاهدة الملف الشخصي</td></tr><tr><td rowspan="8"><span>UTF-8</span></td><td><span>ISO 8859-1</span></td><td>Ù…Ù†ØªØ¯Ù‰ Ø¹Ø±Ø¨ Ø´ÙŠØ± - Ù…Ø´Ø§Ù‡Ø¯Ø© Ø§Ù„Ù…Ù„Ù Ø§Ù„Ø´Ø®ØµÙŠ</td></tr><tr><td><span>KOI8-R</span></td><td>ы┘ы├ь╙ь╞ы┴ ь╧ь╠ь╗ ь╢ы┼ь╠ - ы┘ь╢ь╖ы┤ь╞ь╘ ь╖ы└ы┘ы└ы│ ь╖ы└ь╢ь╝ь╣ы┼</td></tr><tr><td><span>ISO 8859-5</span></td><td>ййиЊиЏй иЙиБиЈ иДйиБ - йиДиЇйиЏиЉ иЇйййй иЇйиДиЎиЕй</td></tr><tr><td><span>CP 866</span></td><td>Е┘Ж╪к╪п┘Й ╪╣╪▒╪и ╪┤┘К╪▒ - ┘Е╪┤╪з┘З╪п╪й ╪з┘Д┘Е┘Д┘Б ╪з┘Д╪┤╪о╪╡┘К</td></tr><tr><td><a href="https://worldlanguages.fandom.com/wiki/ISO_8859-6">ISO 8859-6</a></td><td>ظ…ظ†طھط¯ظ‰ ط¹ط±ط¨ ط´ظٹط± - ظ…ط´ط§ظ‡ط¯ط© ط§ظ„ظ…ظ„ظپ ط§ظ„ط´ط®طµظٹ</td></tr><tr><td><span>CP 852</span></td><td>┘ů┘ćě¬ě»┘ë ě╣ě▒ěĘ ě┤┘Őě▒ - ┘ůě┤ěž┘çě»ěę ěž┘ä┘ů┘ä┘ü ěž┘äě┤ě«ěÁ┘Ő</td></tr><tr><td><span>ISO 8859-2</span></td><td>ŮŮŘŞŘŻŮ ŘšŘąŘ¨ Ř´ŮŘą - ŮŘ´Ř§ŮŘŻŘŠ Ř§ŮŮŮŮ Ř§ŮŘ´ŘŽŘľŮ</td></tr><tr><td><a href="https://worldlanguages.fandom.com/wiki/ASMO_708">ASMO 708</a></td><td>عàع╢ظ╔ظ»عë ظ╥ظ▒ظ╟ ظ═عèظ▒ - عàظ═ظ╞عçظ»ظ╚ ظ╞ع╡عàع╡ع┤ ظ╞ع╡ظ═ظ«ظ╬عè</td></tr></tbody></table>

## References

## External links

- [Reprinted article from the Japan Times](http://www.denbushi.net/2003/02/28/avoiding-mojibake/)
- [Coldfusion Developers Guide article](http://coldfusion.sys-con.com/read/44480.htm)
- [Online decoder of Hebrew text](http://www.gibberish.co.il/) – Online decoder converts input into readable Hebrew text
- [Translators guide](http://www.fumizuki.com/mojibake.html)
- [Recovery tool](http://www.kanzaki.com/docs/jis-recover.html) – Recovery of Japanese text (In Japanese)
- [Chinese E-mail Fixer](http://www.mandarintools.com/email.html) – Recovery of Chinese text
- [Decodr.ru](http://decodr.ru/) - Fast Cyrillic decoder of e-mail and charsets
- [Universal Cyrillic decoder](http://2cyr.com/decode/) – Recovery of Cyrillic text
- [Multilingual online text decoder](http://www.online-decoder.com/) – Online decoder converts scrambled input into readable text. Supported languages are Russian, Bulgarian, Greek, Hebrew and Thai.
- [*Noto pri ĉapeloj: Resuma tabelo*](http://esperanto.pt/cx_tab.htm) – Covers most cases of Esperanto mojibake.
- [Encoding Repair Kit](http://www.cbootle.com/erk/erk.html) – Fixes mojibake, originally intended for Japanese. Windows freeware, 1998. Not compatible with Windows Vista or 7.

[^1]: p. 141, *Control + Alt + Delete: A Dictionary of Cyberslang*, Jonathon Keats, Globe Pequot, 2007, [ISBN 1599210398](https://worldlanguages.fandom.com/wiki/Special:BookSources/1599210398).

[^2]: Template:Cite news

[^3]: [http://msdn.microsoft.com/en-us/library/ms776260(VS.85).aspx](http://msdn.microsoft.com/en-us/library/ms776260\(VS.85\).aspx)