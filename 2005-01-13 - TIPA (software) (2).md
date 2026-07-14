---
title: "TIPA (software)"
source: "https://en.wikipedia.org/wiki/TIPA_(software)"
author:
  - "[[Wikipedia]]"
published: 2005-01-13
created: 2026-05-03
description:
date created: Sunday, May 3rd 2026, 9:04:24 pm
date modified: Sunday, May 3rd 2026, 11:07:26 pm
---

![](https://upload.wikimedia.org/wikipedia/en/thumb/0/05/TIPA_code_points.png/500px-TIPA_code_points.png)

The TIPA character set

**TIPA** is a [free software](https://en.wikipedia.org/wiki/Free_software "Free software") package providing [International Phonetic Alphabet](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet "International Phonetic Alphabet") and other [phonetic character](https://en.wikipedia.org/wiki/Phonetic_notation "Phonetic notation") capabilities for [TeX](https://en.wikipedia.org/wiki/TeX "TeX") and [LaTeX](https://en.wikipedia.org/wiki/LaTeX "LaTeX"). Written by Rei Fukui ([福井玲](https://ja.wikipedia.org/wiki/%E7%A6%8F%E4%BA%95%E7%8E%B2 "ja:福井玲"), *Fukui Rei*), TIPA is based upon the author's previous work in TSIPA. In 2018, the TeX TIPA Roman font was selected as best representing the IPA symbol set by the [International Phonetic Association](https://en.wikipedia.org/wiki/International_Phonetic_Association "International Phonetic Association") 's Alphabet, Charts and Fonts committee.[^1]

TIPA characters are placed within a LaTeX document using any of the following ways: `\textipa{...}`, `{\tipaencoding ...}`, or `\begin{IPA} ... \end{IPA}`.

TIPA supports many of the symbols in the *[Phonetic Symbol Guide](https://en.wikipedia.org/wiki/Phonetic_Symbol_Guide "Phonetic Symbol Guide")* (though macros are sometimes required) as well as a few idiosyncratic ones, such as a l–ɾ ligature 𝼑.

## Examples

![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Tipa_explanation.svg/250px-Tipa_explanation.svg.png)

```
\textipa{[""Ekspl@"neIS@n]}
```

![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Tipa_phonetics.svg/250px-Tipa_phonetics.svg.png)

```
\textipa{/f@"nEtIks/}
```

[^1]: International Phonetic Association (2018). ["IPA charts and sub-charts in four fonts"](https://www.internationalphoneticassociation.org/IPAcharts/IPA_charts_2018.html). Retrieved 19 May 2018.