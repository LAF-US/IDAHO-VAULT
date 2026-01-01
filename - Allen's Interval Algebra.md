---
title: "Allen's Interval Algebra"
source: "https://ics.uci.edu/~alspaugh/cls/shr/allen.html"
author:
  - "[[Thomas A. Alspaugh]]"
published:
created: 2026-08-12
description: "Allen's interval algebra"
---
[Sets](https://ics.uci.edu/~alspaugh/cls/shr/set.html)  
[Relations](https://ics.uci.edu/~alspaugh/cls/shr/relation.html)  
[Correspondences](https://ics.uci.edu/~alspaugh/cls/shr/correspondence.html)  
[Ordered Sets](https://ics.uci.edu/~alspaugh/cls/shr/orderedSet.html)  
[Lattices](https://ics.uci.edu/~alspaugh/cls/shr/lattice.html)  
[Graphs](https://ics.uci.edu/~alspaugh/cls/shr/graph.html)  
[Powersets](https://ics.uci.edu/~alspaugh/cls/shr/powerset.html)  
[Binary Strings](https://ics.uci.edu/~alspaugh/cls/shr/binaryString.html)  
[Logic](https://ics.uci.edu/~alspaugh/cls/shr/logicConcepts.html)  
[AIA](https://ics.uci.edu/~alspaugh/cls/shr/allen.html)  
[Greek](https://ics.uci.edu/~alspaugh/cls/shr/greek.html)

[Glossary](https://ics.uci.edu/~alspaugh/cls/shr/glossaryExternal.html)  
[Abstracts](https://ics.uci.edu/~alspaugh/cls/shr/goodAbstract.html)  
[Argument](https://ics.uci.edu/~alspaugh/cls/shr/argument.html)  
[Inquiry Cycle](https://ics.uci.edu/~alspaugh/cls/shr/inquiryCycle.html)  
[Legal Relations](https://ics.uci.edu/~alspaugh/cls/shr/hohfeld.html)  
[Presentations](https://ics.uci.edu/~alspaugh/cls/shr/goodPresentation.html)

[Elicitation](https://ics.uci.edu/~alspaugh/cls/shr/quickStart.html)  
[Glossaries](https://ics.uci.edu/~alspaugh/cls/shr/ontology.html)  
[Goals](https://ics.uci.edu/~alspaugh/cls/shr/goal.html)  
[i\*](https://ics.uci.edu/~alspaugh/cls/shr/istar.html)  
[SCR](https://ics.uci.edu/~alspaugh/cls/shr/SCR.html)  
[Tracing](https://ics.uci.edu/~alspaugh/cls/shr/tracing.html)

[Alloy](https://ics.uci.edu/~alspaugh/cls/shr/alloy.html)  
[MSCs](https://ics.uci.edu/~alspaugh/cls/shr/msc.html)  
[Regular Exprs.](https://ics.uci.edu/~alspaugh/cls/shr/regularExpression.html)

[Design Patterns](https://ics.uci.edu/~alspaugh/cls/shr/java-designPattern.html)  
[Javadoc](https://ics.uci.edu/~alspaugh/cls/shr/javadoc.html)  
[Java Packages](https://ics.uci.edu/~alspaugh/cls/shr/java-package.html)  
[Java Types](https://ics.uci.edu/~alspaugh/cls/shr/java-type.html)

[(X)HTML](https://ics.uci.edu/~alspaugh/cls/shr/html.html)  
[XML Schemas](https://ics.uci.edu/~alspaugh/cls/shr/xmlSchema.html)  
[XSLT](https://ics.uci.edu/~alspaugh/cls/shr/xslt.html)

In 1983 James F. Allen published a paper \[[Allen1983-mkti](#Allen1983-mkti)\] in which he proposed thirteen basic relations between time intervals that are distinct, exhaustive, and qualitative.

- distinct because no pair of definite intervals can be related by more than one of the relationships
- exhaustive because any pair of definite intervals are described by one of the relations
- qualitative (rather than quantitative) because no numeric time spans are considered

These relations and the operations on them form *Allen's interval algebra*.

## Thirteen basic relations

Allen's thirteen basic relations are illustrated in Table 1. This table shows all the possible relations that two definite intervals can have. Each one is defined graphically by a diagram relating two definite intervals a and b, with time running → from left to right. For example, the first diagram shows that " *a* precedes *b* " means that *a* ends before *b* begins, with a gap separating them; the second shows that " *a* meets *b* " means that *b* begins when *a* ends.

| precedes | meets | overlaps | finished   by | contains | starts | equals | started   by | during | finishes | overlap-   ped by | met   by | preceded   by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |
| p | m | o | F | D | s | e | S | d | f | O | M | P |

The basic relations are listed in Table 1 sorted by the degree to which *a* begins before *b* and then within that by the degree to which *a* ends before *b*. We will commonly list them in this order (pmoFDseSdfOMP), as it makes the relations easier to remember and simplifies comparison of general relations.

Six pairs of the relations are converses. For example, the converse of " *a* precedes *b* " is " *b* preceded by *a* "; whenever the first relation is true, its converse is true also. Table 2 lists the relations with each one beside its converse. The thirteenth, "equals", is its own converse. Each pair of converse relation symbols consists of the lowercase and uppercase of the same letter (e.g. p and P; the uppercase letters represent the relations Allen defined as converses).

<table><caption>Table 2. Converses of Allen's basic temporal relations</caption><thead><tr><th colspan="2">Relation</th><th colspan="2">Converse</th></tr></thead><tbody><tr><td>precedes</td><td>(p)</td><td>(P)</td><td>preceded by</td></tr></tbody><tbody><tr><td>meets</td><td>(m)</td><td>(M)</td><td>met by</td></tr></tbody><tbody><tr><td>overlaps</td><td>(o)</td><td>(O)</td><td>overlapped by</td></tr></tbody><tbody><tr><td>finished by</td><td>(F)</td><td>(f)</td><td>finishes</td></tr></tbody><tbody><tr><td>contains</td><td>(D)</td><td>(d)</td><td>during</td></tr></tbody><tbody><tr><td>starts</td><td>(s)</td><td>(S)</td><td>started by</td></tr></tbody><tbody><tr><td colspan="4">equals (e)</td></tr></tbody></table>

## 8192 general relations

<table><caption>Table 3. Example "Turn on the light"</caption><tbody><tr><td><i>a</i></td><td colspan="2">(pmMP)</td><td><i>b</i></td></tr></tbody><tbody><tr><td rowspan="4">"John was<br>in the room"</td><td>p</td><td></td><td rowspan="4">"I touched the<br>light switch"</td></tr><tr><td>m</td><td></td></tr><tr><td>M</td><td></td></tr><tr><td>P</td><td></td></tr></tbody><tbody><tr><td><i>b</i></td><td colspan="2">(mo)</td><td><i>c</i></td></tr></tbody><tbody><tr><td rowspan="2">"I touched the<br>light switch"</td><td>m</td><td></td><td rowspan="2">"The light<br>was on"</td></tr><tr><td>o</td><td></td></tr></tbody></table>

The basic relations describe relations between definite intervals. Indefinite intervals whose exact relation may be uncertain are described by a set of all the basic relations that may apply. We call such a set of basic relations a general Allen relation, or just an Allen relation.

For example, "John was not in the room when I touched the switch to turn on the light" \[[Allen1983-mkti](#Allen1983-mkti) p.837\]. Let

- *a* be the time John was in the room,
- *b* be the time I touched the light switch, and
- *c* be the time the light was on.

Then we can say *a* (pmMP) *b*, that is, *a* precedes, meets, is met by, or is preceded by *b*; and *b* (mo) *c*, that is, *b* meets or overlaps *c*. Table 3 shows these relations.

There is a general relation for every combination of the thirteen basic relations: 2 <sup>13</sup> or 8192 of them. Each of the basic relations is a relation, of course, as are all their combinations. The full relation (pmoFDseSdfOMP) holds between two intervals about whom nothing is known. The empty relation () has no meaning in terms of relations between actual intervals, but is the result of some operations on interval relations and is needed for subalgebras of Allen's interval algebra (discussed below).

## Operations on relations

| Converse examples |
| --- |
| ~(p) = (moFDseSdfOMP) |
| ~(pmoFD) = (seSdfOMP) |
| ~() = (pmoFDseSdfOMP) |

## Complement

The complement *~r* of a relation *r* is the relation consisting of all basic relations not in *r*.

From the definition of complement, we see that the converse operation is its own inverse; for every relation *r*,

~(~ *r*) = *r*

| Composition examples |
| --- |
| (m).(m) = (p) |
| (pm).(pm) = (p) |
| (oFD).(oFDseS) = (pmoFD) |

## Composition

The composition (*r.s*) of two relations (*r*) and (*s*) is the relation that holds between *a* and *c* if there is a *b* such that *a* (*r*) *b* and *b* (*s*) *c*; we then write *a* (*r.s*) *c*.

Calculation of composition is not simple like the other operations in this section. It can be determined by going back to the definitions of the relations, and working from there; or by determining the composition of each basic relation from *r* with each basic relation from *s* (using a [table](#BasicCompositionsTable), perhaps), and taking the union of the results; or by using the " `allen` " command.

Composition is not commutative but is both left and right associative, and distributes over union (as seen in the procedure for calculating composition using a table of composition of basic relations).

Composition is discussed further [below](#CompositionMore).

| Converse examples |
| --- |
| !(p) = (P) |
| !(pmoFD) = (dfOMP) |
| !(mM) = (mM) |
| !() = () |

## Converse

The converse *!r* of a relation *r* is the relation consisting of the converses of all basic relations in *r*.

From the definition of converse, we see that the converse operation is its own inverse; for every relation *r*,

!(!*r*) = *r*

| Intersection examples |
| --- |
| (pmo)^(FDseS) = () |
| (pFsSf)^(pmoFD) = (pF) |
| (pmo)^(pmo) = (pmo) |

## Intersection

The intersection (*r^s*) of two relations (*r*) and (*s*) is the set-theoretic intersection of the two relations; it is the relation composed of all basic relations that are in both (*r*) and (*s*).

Intersection is commutative and associative.

| Union examples |
| --- |
| (pmo)+(FDseS) = (pmoFDseS) |
| (pFsSf)+(pmoFD) = (pmoFDsSf) |
| (pmo)+(pmo) = (pmo) |

## Union

The union (*r+s*) of two relations (*r*) and (*s*) is the set-theoretic union of the two relations; it is the relation composed of all basic relations that are in either (*r*) or (*s*).

Union is commutative and associative.

## The composition operation

Table 4a gives the composition of any two basic relations. Such a table can be used in calculating general compositions by hand, but is also interesting in its own right. There are striking patterns of partial symmetry in the distribution of the results, here highlighted by giving each result value its own background color. Out of the 8192 relations in the interval algebra, only 27 appear as compositions of basic relations, and each of those comprises either 1, 3, 5, 9 (*concur*) or all 13 (*full*) basic relations.

| . | p | m | o | F | D | s | e | S | d | f | O | M | P |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p | (p) | (p) | (p) | (p) | (p) | (p) | (p) | (p) | (pmosd) | (pmosd) | (pmosd) | (pmosd) | full |
| m | (p) | (p) | (p) | (p) | (p) | (m) | (m) | (m) | (osd) | (osd) | (osd) | (Fef) | (DSOMP) |
| o | (p) | (p) | (pmo) | (pmo) | (pmoFD) | (o) | (o) | (oFD) | (osd) | (osd) | concur | (DSO) | (DSOMP) |
| F | (p) | (m) | (o) | (F) | (D) | (o) | (F) | (D) | (osd) | (Fef) | (DSO) | (DSO) | (DSOMP) |
| D | (pmoFD) | (oFD) | (oFD) | (D) | (D) | (oFD) | (D) | (D) | concur | (DSO) | (DSO) | (DSO) | (DSOMP) |
| s | (p) | (p) | (pmo) | (pmo) | (pmoFD) | (s) | (s) | (seS) | (d) | (d) | (dfO) | (M) | (P) |
| e | (p) | (m) | (o) | (F) | (D) | (s) | (e) | (S) | (d) | (f) | (O) | (M) | (P) |
| S | (pmoFD) | (oFD) | (oFD) | (D) | (D) | (seS) | (S) | (S) | (dfO) | (O) | (O) | (M) | (P) |
| d | (p) | (p) | (pmosd) | (pmosd) | full | (d) | (d) | (dfOMP) | (d) | (d) | (dfOMP) | (P) | (P) |
| f | (p) | (m) | (osd) | (Fef) | (DSOMP) | (d) | (f) | (OMP) | (d) | (f) | (OMP) | (P) | (P) |
| O | (pmoFD) | (oFD) | concur | (DSO) | (DSOMP) | (dfO) | (O) | (OMP) | (dfO) | (O) | (OMP) | (P) | (P) |
| M | (pmoFD) | (seS) | (dfO) | (M) | (P) | (dfO) | (M) | (P) | (dfO) | (M) | (P) | (P) | (P) |
| P | full | (dfOMP) | (dfOMP) | (P) | (P) | (dfOMP) | (P) | (P) | (dfOMP) | (P) | (P) | (P) | (P) |

In the tables, *full* =(pmoFDseSdfOMP) and *concur* =(oFDseSdfO) in order to conserve space.

<table><caption>Table 4b. Frequency distribution of<br>compositions of basic relations.</caption><tbody><tr><td>22</td><td>(p)</td><td>(P)</td><td colspan="6"></td></tr><tr><td>9</td><td>(d)</td><td>(D)</td><td colspan="6"></td></tr><tr><td>7</td><td>(oFD)</td><td>(osd)</td><td>(DSO)</td><td>(dfO)</td><td colspan="4"></td></tr><tr><td>6</td><td>(pmoFD)</td><td>(pmosd)</td><td>(m)</td><td>(DSOMP)</td><td>(dfOMP)</td><td>(M)</td><td colspan="2"></td></tr><tr><td>5</td><td>(o)</td><td>(O)</td><td colspan="6"></td></tr><tr><td>4</td><td>(pmo)</td><td>(OMP)</td><td colspan="6"></td></tr><tr><td>3</td><td>full</td><td>concur</td><td>(F)</td><td>(Fef)</td><td>(seS)</td><td>(s)</td><td>(S)</td><td>(f)</td></tr><tr><td>1</td><td>(e)</td><td colspan="7"></td></tr></tbody></table>

| n | Relation | Diagrams |
| --- | --- | --- |
| 22 | (p) |  |
| 22 | (P) |  |
| 9 | (d) |  |
| 9 | (D) |  |
| 7 | (oFD) |  |
| 7 | (osd) |  |
| 7 | (dfO) |  |
| 7 | (DSO) |  |
| 6 | (pmoFD) |  |
| 6 | (pmosd) |  |
| 6 | (dfOMP) |  |
| 6 | (DSOMP) |  |
| 6 | (m) |  |
| 6 | (M) |  |
| 5 | (o) |  |
| 5 | (O) |  |
| 4 | (pmo) |  |
| 4 | (OMP) |  |
| 4 | (s) |  |
| 3 | (S) |  |
| 3 | full |  |
| 3 | concur |  |
| 3 | (F) |  |
| 3 | (f) |  |
| 3 | (Fef) |  |
| 3 | (seS) |  |
| 1 | (e) |  |

<table><caption>Table 5. Inference of relation</caption><tbody><tr><td><i>a</i></td><td colspan="2">(pseSdfOMP)</td><td><i>c</i></td></tr></tbody><tbody><tr><td rowspan="9">"John was<br>in the room"</td><td>p</td><td></td><td rowspan="9">"The light<br>was on"</td></tr><tr><td>s</td><td></td></tr><tr><td>e</td><td></td></tr><tr><td>S</td><td></td></tr><tr><td>d</td><td></td></tr><tr><td>f</td><td></td></tr><tr><td>O</td><td></td></tr><tr><td>M</td><td></td></tr><tr><td>P</td><td></td></tr></tbody></table>

## Composition and inference

The composition operation is the basis for inference among interval relations.

Let *a <sub>0</sub>* (*r <sub>1</sub>*) *a <sub>1</sub>*, *a <sub>1</sub>* (*r <sub>2</sub>*) *a <sub>2</sub>*,..., *a <sub>(n-1)</sub>* (*r <sub>n</sub>*) *a <sub>n</sub>* be a chain of relations among intervals *a <sub>0</sub>* through *a <sub>n</sub>*. Then this chain of relations may be used to infer that

*a <sub>0</sub>* (*r <sub>1</sub>*.*r <sub>2</sub>*.....*r <sub>n</sub>*) *a <sub>n</sub>*

For a collection of relations on intervals, we can derive the *strongest implied relation* between *a <sub>0</sub>* and *a <sub>n</sub>* by examining all possible chains of inference between *a <sub>0</sub>* and *a <sub>n</sub>*, and taking the intersection of all the resulting compositions of chained relations. Each chain of inference places a constraint on the relation, so the inferences are combined by taking their intersection.

The number of possible chains rises very quickly as the number of relations in the collection is increased.

A related problem is determining, for a particular collection of relations on indefinite intervals, whether there is any set of specific time values for the intervals such that all the relations in the collection are true. This is the *satisfaction* problem for Allen's interval algebra, and it has been shown to be NP-complete \[[Vilain+Kautz+Beek1989-cpat](#Vilain_Kautz_Beek1989-cpat)\].

![Unsatisfiable graph](https://ics.uci.edu/~alspaugh/cls/shr/img/Unsatisfiable.png)

Figure 1. Unsatisfiable relations

A simple example of a collection of relations and intervals that is not satisfiable is three intervals *a*, *b*, and *c* such that *a* (p) *b*, *b* (p) *c*, and *c* (p) *a* (each precedes the next, and the last precedes the first). There are no definite intervals for which all these relations can hold. We can calculate that this collection is unsatisfiable by inferring the relation that is implied between *a* and *c* by the other relations. The inferred relation through *b* is

(*a* to *b*).(*b* to *c*) = (p).(p) = (p)

We already know that the relation between as the relation between *c* and *a* is (P) (the converse of the relation (p) between *a* and *c*). The strongest inferred relation between *c* and *a* is the intersection of these two relations

(p)∩ (P) = ∅

∅ means that *c* and *a* have no relation at all, which is not possible; so this collection of intervals and relations is unsatisfiable.

## Relationships between Allen relations

The relationships between Allen relations are defined in terms of the corresponding sets of basic relations.

Two Allen relations are equal if they contain the same basic relations, and not equal otherwise.

<table><thead><tr><th colspan="2">Weaker/stronger examples</th></tr></thead><tbody><tr><td>(pmoFD)<(oDF)</td><td>(pmoFD) is weaker than (oDF)</td></tr><tr><td>(pmo)>(pmoFD)</td><td>(pmo) is stronger than (pmoFD)</td></tr><tr><td>(oDF)#(pmo)</td><td>(oDF) and (pmo) are incomparable</td></tr></tbody></table>

The Allen relations form a [partial order](https://ics.uci.edu/~alspaugh/cls/shr/relation.html#order); we say that one relation can be *weaker* than another, (or conversely, *stronger*). This partial order is the same as the partial order on the sets of basic Allen relations defined by ⊃. Relation *A* is weaker than relation *B* if *A* ⊃ *B*. If the sets *A* and *B* are not comparable by ⊃, then the general relations *A* and *B* are incomparable also.

Because we naturally think of "stronger" as bigger than "weaker", we write *A* < *B* to indicate *A* is weaker. Note that *A* < *B* is equivalent to *A* ⊃ *B*; the < and ⊃ point in opposite directions.

## Eighteen maximal tractable subalgebras

<table><thead><tr><th colspan="2">A <sub>≡</sub> examples</th></tr></thead><tbody><tr><th>in</th><th>not in</th></tr></tbody><tbody><tr><td>()</td><td>(pmo)</td></tr><tr><td>(e)</td><td>(s)</td></tr><tr><td>(seS)</td><td>(sS)</td></tr></tbody></table>

Although satisfaction in interval algebra is NP-complete, there are subsets of the 8192 relations for which satisfaction is tractable (a polynomial-time algorithm exists). Once such subsets have been found, a natural course of action is to maximize their size by adding more relations, stopping just before an intractable subset results; the result is a tractable subset that cannot accept another relation without becoming intractable, and is thus maximal. It turns out that there are eighteen maximal tractable subsets of Allen's interval algebra; every tractable subset of the full algebra is a subset of one or more of these eighteen \[[Krokhin+Jeavons+Jonsson2003-rtrt](#Krokhin_Jeavons_Jonsson2003-rtrt)\]. The maximal tractable subsets are all *algebras*, that is, each is closed under composition, converse, and intersection (a set is *closed* under an operation if the result of applying the operation to any element(s) of the set is another member of the set). Thus they are usually described as maximal tractable subalgebras.

The eighteen maximal tractable subalgebras are listed in Table 6, along with rules defining which relations belong to them and links to the sets of elements in each one. The most important one is the H or Horn subalgebra; it is the only one of the eighteen that contains all 13 of the basic relations, and inference in it can be done using the path consistency algorithm rather than a more complex one.

<table><thead><tr><th colspan="2">A <sub>1</sub> examples</th></tr></thead><tbody><tr><th>in</th><th>not in</th></tr></tbody><tbody><tr><td>()</td><td>(p)</td></tr><tr><td>(pS)</td><td>(ps)</td></tr><tr><td>(sOMP)</td><td>(SOP)</td></tr></tbody></table>

The rules give properties that each member of the subalgebra must have. For example, for a relation *r* to be a member of the A <sub>≡</sub> subalgebra, if *r* is not the empty relation, it must contain e. Thus (), (e), and (Fef) are members, but not (m) or (pmoFD).

The rules appear in pairs, labelled + and −. The relations named in each pair are converses. The rules that appear as singletons are those whose relations are their own converses (like () and (e) in the A <sub>≡</sub> rule). For example, for a relation *r* to be a member of A <sub>1</sub>, if *r* has any basic relations in common with (pmoFD), then *r* must contain S. The converses of (pmoFD) and (S) are (dfOMP) and (s), respectively, and the − rule says that if *r* has any basic relations in common with (dfOMP), then *r* must contain s. In the literature, this pair of rules is often expressed as

A <sub>1</sub> = { *r* | *r* ∩ (pmoFD) <sup>±1</sup> ≠ ∅ ⇒ (p) <sup>±1</sup> ⊆ *r* }

where the superscript ±1 indicates the relation and its converse respectively in the two rules of the pair.

<table><caption>Table 6. Tractable subalgebras (from Krokhin <i>et al.</i>)</caption><thead><tr><th>Name</th><th colspan="7">Rules</th><th>Size</th></tr></thead><tbody><tr><th rowspan="1">A <sub>≡</sub></th><th></th><td colspan="2"><i>r</i> ≠ ()</td><td>⇒</td><td>(e) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="1">4097 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/Ae.txt">elements</a></td></tr></tbody><tbody><tr><th rowspan="2">A <sub>1</sub></th><th>+)</th><td><i>r</i> ∩ (pmoFD)</td><td>≠ ()</td><td>⇒</td><td>(S) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2178 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/A1.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (dfOMP)</td><td>≠ ()</td><td>⇒</td><td>(s) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">A <sub>2</sub></th><th>+)</th><td><i>r</i> ∩ (pmoFD)</td><td>≠ ()</td><td>⇒</td><td>(s) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2178 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/A2.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (dfOMP)</td><td>≠ ()</td><td>⇒</td><td>(S) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">A <sub>3</sub></th><th>+)</th><td><i>r</i> ∩ (pmodf)</td><td>≠ ()</td><td>⇒</td><td>(s) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2178 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/A3.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (FDOMP)</td><td>≠ ()</td><td>⇒</td><td>(S) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">A <sub>4</sub></th><th>+)</th><td><i>r</i> ∩ (pmoFd)</td><td>≠ ()</td><td>⇒</td><td>(s) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2178 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/A4.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (DfOMP)</td><td>≠ ()</td><td>⇒</td><td>(S) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">B <sub>1</sub></th><th>+)</th><td><i>r</i> ∩ (pmosd)</td><td>≠ ()</td><td>⇒</td><td>(F) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2178 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/B1.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (DSOMP)</td><td>≠ ()</td><td>⇒</td><td>(f) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">B <sub>2</sub></th><th>+)</th><td><i>r</i> ∩ (pmosd)</td><td>≠ ()</td><td>⇒</td><td>(f) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2178 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/B2.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (DSOMP)</td><td>≠ ()</td><td>⇒</td><td>(F) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">B <sub>3</sub></th><th>+)</th><td><i>r</i> ∩ (pmoDS)</td><td>≠ ()</td><td>⇒</td><td>(F) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2178 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/B3.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (sdOMP)</td><td>≠ ()</td><td>⇒</td><td>(f) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">B <sub>4</sub></th><th>+)</th><td><i>r</i> ∩ (pmoDs)</td><td>≠ ()</td><td>⇒</td><td>(F) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2178 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/B4.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (SdOMP)</td><td>≠ ()</td><td>⇒</td><td>(f) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">E <sub>d</sub></th><th>+)</th><td><i>r</i> ∩ (pmosd)</td><td>≠ ()</td><td>⇒</td><td>(d) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2312 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/Ed.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (DSOMP)</td><td>≠ ()</td><td>⇒</td><td>(D) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">E <sub>o</sub></th><th>+)</th><td><i>r</i> ∩ (pmosd)</td><td>≠ ()</td><td>⇒</td><td>(o) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2312 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/Eo.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (DSOMP)</td><td>≠ ()</td><td>⇒</td><td>(O) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">E <sub>p</sub></th><th>+)</th><td><i>r</i> ∩ (pmosd)</td><td>≠ ()</td><td>⇒</td><td>(p) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2312 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/Ep.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (DSOMP)</td><td>≠ ()</td><td>⇒</td><td>(P) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="3">E <sup>*</sup></th><th>1+)</th><td><i>r</i> ∩ (pmosd)</td><td>≠ ()</td><td>⇒</td><td>(s) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="3">1445 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/Estar.txt">elements</a></td></tr><tr><th>1−)</th><td><i>r</i> ∩ (DSOMP)</td><td>≠ ()</td><td>⇒</td><td>(S) ⊆ <i>r</i></td><td colspan="2"></td></tr><tr><th>2)</th><td><i>r</i> ∩ (Ff)</td><td>≠ ()</td><td>⇒</td><td>(e) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="6">H</th><th>1+)</th><td><i>r</i> ∩ (os)</td><td>≠ ()</td><td>&</td><td><i>r</i> ∩ (Of) ≠ ()</td><td>⇒</td><td>(d) ⊆ <i>r</i></td><td rowspan="6">868 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/H.txt">elements</a></td></tr><tr><th>1−)</th><td><i>r</i> ∩ (SO)</td><td>≠ ()</td><td>&</td><td><i>r</i> ∩ (oF) ≠ ()</td><td>⇒</td><td>(D) ⊆ <i>r</i></td></tr><tr><th>2+)</th><td><i>r</i> ∩ (sd)</td><td>≠ ()</td><td>&</td><td><i>r</i> ∩ (FD) ≠ ()</td><td>⇒</td><td>(o) ⊆ <i>r</i></td></tr><tr><th>2−)</th><td><i>r</i> ∩ (DS)</td><td>≠ ()</td><td>&</td><td><i>r</i> ∩ (df) ≠ ()</td><td>⇒</td><td>(O) ⊆ <i>r</i></td></tr><tr><th>3+)</th><td><i>r</i> ∩ (pm)</td><td>≠ ()</td><td>&</td><td>¬(r ⊆ (pm))</td><td>⇒</td><td>(o) ⊆ <i>r</i></td></tr><tr><th>3−)</th><td><i>r</i> ∩ (MP)</td><td>≠ ()</td><td>&</td><td>¬(r ⊆ (MP))</td><td>⇒</td><td>(O) ⊆ <i>r</i></td></tr></tbody><tbody><tr><th rowspan="2">S <sub>d</sub></th><th>+)</th><td><i>r</i> ∩ (pmoFD)</td><td>≠ ()</td><td>⇒</td><td>(D) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2312 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/Sd.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (dfOMP)</td><td>≠ ()</td><td>⇒</td><td>(d) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">S <sub>o</sub></th><th>+)</th><td><i>r</i> ∩ (pmoFD)</td><td>≠ ()</td><td>⇒</td><td>(o) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2312 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/So.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (dfOMP)</td><td>≠ ()</td><td>⇒</td><td>(O) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="2">S <sub>p</sub></th><th>+)</th><td><i>r</i> ∩ (pmoFD)</td><td>≠ ()</td><td>⇒</td><td>(p) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="2">2312 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/Sp.txt">elements</a></td></tr><tr><th>−)</th><td><i>r</i> ∩ (dfOMP)</td><td>≠ ()</td><td>⇒</td><td>(P) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody><tbody><tr><th rowspan="4">S <sup>*</sup></th><th>1+)</th><td><i>r</i> ∩ (pmoFD)</td><td>≠ ()</td><td>⇒</td><td>(F) ⊆ <i>r</i></td><td colspan="2"></td><td rowspan="4">1445 <a href="https://ics.uci.edu/~alspaugh/cls/shr/allen-subalgebras/Sstar.txt">elements</a></td></tr><tr><th>1−)</th><td><i>r</i> ∩ (dfOMP)</td><td>≠ ()</td><td>⇒</td><td>(f) ⊆ <i>r</i></td><td colspan="2"></td></tr><tr><th>2+)</th><td><i>r</i> ∩ (pmoFD)</td><td>≠ ()</td><td>⇒</td><td>(F) ⊆ <i>r</i></td><td colspan="2"></td></tr><tr><th>2−)</th><td><i>r</i> ∩ (dfOMP)</td><td>≠ ()</td><td>⇒</td><td>(f) ⊆ <i>r</i></td><td colspan="2"></td></tr></tbody></table>

## Networks of relations

![Example as graph](https://ics.uci.edu/~alspaugh/cls/shr/img/TurnOnTheLight2.png)

Figure 2. Example as graph

The Allen relations among three or more intervals form a graph whose nodes are the intervals and whose edges are the relations. The light switch example from [Table 3](#TurnOnTheLight) can be presented as a graph as in Figure 2. This graph is not complete — there is no edge from node *a* to node *c*. Instead, only the known relations are presented.

![Example as graph](https://ics.uci.edu/~alspaugh/cls/shr/img/TurnOnTheLight3.png)

Figure 3. Complete graph

The graph may be completed by inferring the relations corresponding to each missing edge (Figure 3). In this case, the missing edge is (pmMP).(mo) = (pseSdfOMP). Inference of missing edges is equivalent to solving for satisfaction, which in the general case is NP-complete. For the H subclass, the path-consistency algorithm may be used for complete inference and determining satisfiability \[[Gennari1998-trcp](#Gennari1998-trcp) p.194ff\].

## Equivalence of two networks

Two complete networks are equivalent if they contain the same intervals, and the relations between corresponding intervals are the same.

If one or both the networks are not complete, then they are equivalent if the corresponding completed networks are equivalent.

## Specialization of a network

A complete network α is a *specialization* of another complete network β if

1. *Nodes* (α) ⊇ *Nodes* (β)  
	(every interval in β is present in α)
2. For all corresponding edges *a* of α and *b* of β, *a* ≥ *b*  
	(every relation in α is the same or stronger than the corresponding relation in β)

If one or both the networks are not complete, then α specializes β if the completion of α specialized the completion of β.

Informally, a network can be specialized into another network that meets all the first one's constraints. This can't happen if the specialization doesn't have all the intervals, nor if the specialization has a weaker edge. A mnemonic is "specialization means bigger and stronger".

![Partial order of the basic relations](https://ics.uci.edu/~alspaugh/cls/shr/img/AllenBasicRelationsPO-vertical.png)

Figure 4. Partial order of the basic relations

## Ordering the basic relations

The standard order I selected isn't the only plausible one. Figure 4 shows a partial order of the basic relations, in which each relation is obtained from the one(s) immediately above it by nudging one end of *a* to or beyond the next end of *b*.

## Other names and symbols for the basic relations

<table><caption>Table 7. Names and symbols for the basic relations</caption><thead><tr><th></th><th colspan="2">Here</th><th colspan="2">Allen</th><th colspan="2">Krokhin et al.</th></tr></thead><tbody><tr><td></td><td>precedes</td><td>p</td><td>before</td><td><</td><td>precedes</td><td>p</td></tr><tr><td></td><td>meets</td><td>m</td><td>meets</td><td>m</td><td>meets</td><td>m</td></tr><tr><td></td><td>overlaps</td><td>o</td><td>overlaps</td><td>o</td><td>overlaps</td><td>o</td></tr><tr><td></td><td>finished-by</td><td>F</td><td>finished-by</td><td>fi</td><td>finished-by</td><td>f <sup>-1</sup></td></tr><tr><td></td><td>contains</td><td>d</td><td>contains</td><td>di</td><td>contains</td><td>d <sup>-1</sup></td></tr><tr><td></td><td>starts</td><td>s</td><td>starts</td><td>s</td><td>starts</td><td>s</td></tr><tr><td></td><td>equals</td><td>e</td><td>equals</td><td>=</td><td>equals</td><td>≡</td></tr><tr><td></td><td>started-by</td><td>S</td><td>started-by</td><td>si</td><td>started-by</td><td>s <sup>-1</sup></td></tr><tr><td></td><td>during</td><td>d</td><td>during</td><td>d</td><td>during</td><td>d</td></tr><tr><td></td><td>finishes</td><td>f</td><td>finishes</td><td>f</td><td>finishes</td><td>f</td></tr><tr><td></td><td>overlapped-by</td><td>O</td><td>overlapped-by</td><td>oi</td><td>overlapped-by</td><td>o <sup>-1</sup></td></tr><tr><td></td><td>met-by</td><td>M</td><td>met-by</td><td>mi</td><td>met-by</td><td>m <sup>-1</sup></td></tr><tr><td></td><td>preceded-by</td><td>P</td><td>after</td><td>></td><td>preceded-by</td><td>p <sup>-1</sup></td></tr></tbody></table>

## Acknowledgments

I thank Philippus Baalman, Tassilo Karge, Richard Allen (no relation), and Thomas S. Dye for pointing out errors in earlier versions of this page.

## References

Allen, James F. "Maintaining knowledge about temporal intervals". *Communications of the ACM* **26** (11) pp.832-843, Nov. 1983.

Gennari, Rosella. Temporal Reasoning and Constraint Programming: A survey. *CWI Quarterly*, **11** (2-3):163-214. 1998.

Andrei Krokhin, Peter Jeavons, and Peter Jonsson. "Reasoning about temporal relations: The tractable subalgebras of Allen's interval algebra". *Journal of the ACM* **50** (5), pp. 591-640, 2003.

Marc Vilain, Henry Kautz, and Peter van Beek. "Constraint propagation algorithms for temporal reasoning: a revised report". In *Readings in qualitative reasoning about physical systems*, edited by D. S. Weld and J. de Kleer, pp. 373-381, 1989.

<iframe allow="clipboard-write; web-share" src="chrome-extension://cnjifjpddelmedmihgijeibhnjfabmlf/side-panel.html?context=iframe"></iframe>