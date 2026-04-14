---
source: "https://mermaid.ai/open-source/syntax/mindmap.html"
author:
published:
created: 2026-04-13
---
## Mindmap

> Mindmap: This is an experimental diagram for now. The syntax and properties can change in future releases. The syntax is stable except for the icon integration which is the experimental part.

"A mind map is a diagram used to visually organize information into a hierarchy, showing relationships among pieces of the whole. It is often created around a single concept, drawn as an image in the center of a blank page, to which associated representations of ideas such as images, words and parts of words are added. Major ideas are connected directly to the central concept, and other ideas branch out from those major ideas." Wikipedia

### An example of a mindmap.

##### Code:

```
mermaidmindmap
  root((mindmap))
    Origins
      Long history
      ::icon(fa fa-book)
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectiveness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
    Tools
      Pen and paper
      Mermaid
```

## Syntax

The syntax for creating Mindmaps is simple and relies on indentation for setting the levels in the hierarchy.

In the following example you can see how there are 3 different levels. One with starting at the left of the text and another level with two rows starting at the same column, defining the node A. At the end there is one more level where the text is indented further than the previous lines defining the nodes B and C.

```
mindmap
    Root
        A
            B
            C
```

In summary is a simple text outline where there is one node at the root level called `Root` which has one child `A`. `A` in turn has two children `B` and `C`. In the diagram below we can see this rendered as a mindmap.

##### Code:

```
mermaidmindmap
Root
    A
      B
      C
```

<svg id="mermaid-28" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 242.63975524902344px;" viewBox="5 5 242.63975524902344 210.3272247314453" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-28_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-28_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-28_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-28_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g><path d="M192.311,176.507L188.892,172.131C185.473,167.755,178.635,159.003,171.796,150.251C164.958,141.499,158.12,132.747,154.701,128.371L151.282,123.995" id="mermaid-28-edge_0_1" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_1" data-points="W3sieCI6MTkyLjMxMDg3MjE3MTkyMzYyLCJ5IjoxNzYuNTA3MjMzODEwOTE4ODV9LHsieCI6MTcxLjc5NjQ5NTY4NjcwNTg0LCJ5IjoxNTAuMjUxMDAyOTMwNDgzODh9LHsieCI6MTUxLjI4MjExOTIwMTQ4ODA2LCJ5IjoxMjMuOTk0NzcyMDUwMDQ4OTF9XQ==" data-look="classic" fill="none" stroke="currentColor"></path><path d="M127.111,110.792L121.057,110.232C115.004,109.672,102.896,108.551,90.789,107.431C78.682,106.31,66.575,105.189,60.521,104.629L54.467,104.069" id="mermaid-28-edge_1_2" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_1_2" data-points="W3sieCI6MTI3LjExMDgyNDQzNTQ1NDQ4LCJ5IjoxMTAuNzkyMzQyNTQwODk5NTF9LHsieCI6OTAuNzg5MTE3MjEzMzMxMzQsInkiOjEwNy40MzA1NDMwMTkwMjU0NH0seyJ4Ijo1NC40Njc0MDk5OTEyMDgyLCJ5IjoxMDQuMDY4NzQzNDk3MTUxMzZ9XQ==" data-look="classic" fill="none" stroke="currentColor"></path><path d="M149.621,99.228L152.268,94.704C154.914,90.181,160.206,81.134,165.499,72.087C170.792,63.041,176.084,53.994,178.73,49.471L181.377,44.947" id="mermaid-28-edge_1_3" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_1_3" data-points="W3sieCI6MTQ5LjYyMTM2NTQ4MDA5MDg0LCJ5Ijo5OS4yMjc2MjQ2MjQ5MjkyOX0seyJ4IjoxNjUuNDk5MDI2MTg3ODE0MDIsInkiOjcyLjA4NzM4ODQ0MjczMTk5fSx7IngiOjE4MS4zNzY2ODY4OTU1MzcyLCJ5Ijo0NC45NDcxNTIyNjA1MzQ2OX1d" data-look="classic" fill="none" stroke="currentColor"></path></g><g><g><g data-id="edge_0_1" transform="translate(0, 0)"></g></g><g><g data-id="edge_1_2" transform="translate(0, 0)"></g></g><g><g data-id="edge_1_3" transform="translate(0, 0)"></g></g></g><g><g id="mermaid-28-node_0" data-look="classic" transform="translate(201.546006946749, 188.32722897550377)"><path id="mermaid-28-node_0" style="" d="
    M-36.09375 12
    v-24
    q0,-5 5,-5
    h62.1875
    q5,0 5,5
    v24
    q0,5 -5,5
    h-62.1875
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-36.09375" y1="17" x2="36.09375" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-16.09375, -12)"><rect></rect><foreignObject width="32.1875" height="24"><p>Root</p></foreignObject></g></g><g id="mermaid-28-node_1" data-look="classic" transform="translate(142.04698442666268, 112.17477688546398)"><path id="mermaid-28-node_1" style="" d="
    M-24.71875 12
    v-24
    q0,-5 5,-5
    h39.4375
    q5,0 5,5
    v24
    q0,5 -5,5
    h-39.4375
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-24.71875" y1="17" x2="24.71875" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-4.71875, -12)"><rect></rect><foreignObject width="9.4375" height="24"><p>A</p></foreignObject></g></g><g id="mermaid-28-node_2" data-look="classic" transform="translate(39.53125, 102.68630915258689)"><path id="mermaid-28-node_2" style="" d="
    M-24.53125 12
    v-24
    q0,-5 5,-5
    h39.0625
    q5,0 5,5
    v24
    q0,5 -5,5
    h-39.0625
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-24.53125" y1="17" x2="24.53125" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-4.53125, -12)"><rect></rect><foreignObject width="9.0625" height="24"><p>B</p></foreignObject></g></g><g id="mermaid-28-node_3" data-look="classic" transform="translate(188.95106794896537, 32)"><path id="mermaid-28-node_3" style="" d="
    M-24.78749990463257 12
    v-24
    q0,-5 5,-5
    h39.57499980926514
    q5,0 5,5
    v24
    q0,5 -5,5
    h-39.57499980926514
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-24.78749990463257" y1="17" x2="24.78749990463257" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-4.787499904632568, -12)"><rect></rect><foreignObject width="9.574999809265137" height="24"><p>C</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

In this way we can use a text outline to generate a hierarchical mindmap.

## Different shapes

Mermaid mindmaps can show nodes using different shapes. When specifying a shape for a node the syntax is similar to flowchart nodes, with an id followed by the shape definition and with the text within the shape delimiters. Where possible we try/will try to keep the same shapes as for flowcharts, even though they are not all supported from the start.

Mindmap can show the following shapes:

### Square

##### Code:

```
mermaidmindmap
    id[I am a square]
```

<svg id="mermaid-44" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 156.5px;" viewBox="5 5 156.5 64" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-44_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-44_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-44_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-44_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g></g><g></g><g><g id="mermaid-44-node_0" data-look="classic" transform="translate(83.25, 37)"><rect style="" x="-68.25" y="-22" width="136.5" height="44" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-48.25, -12)"><rect></rect><foreignObject width="96.5" height="24"><p>I am a square</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

### Rounded square

##### Code:

```
mermaidmindmap
    id(I am a rounded square)
```

<svg id="mermaid-48" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 210.16250610351562px;" viewBox="5 5 210.16250610351562 74" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-48_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-48_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-48_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-48_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g></g><g></g><g><g id="mermaid-48-node_0" data-look="classic" transform="translate(110.08125305175781, 42)"><rect style="" rx="5" ry="5" x="-95.08125305175781" y="-27" width="190.16250610351562" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-80.08125305175781, -12)"><rect></rect><foreignObject width="160.16250610351562" height="24"><p>I am a rounded square</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

### Circle

##### Code:

```
mermaidmindmap
    id((I am a circle))
```

<svg id="mermaid-52" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 129.0875015258789px;" viewBox="5.000003814697266 5.000003814697266 129.0875015258789 129.0875015258789" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-52_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-52_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-52_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-52_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g></g><g></g><g><g id="mermaid-52-node_0" data-look="classic" transform="translate(69.54375076293945, 69.54375076293945)"><circle style="" r="54.54375076293945" cx="0" cy="0" fill="none" stroke="currentColor"></circle><g style="" transform="translate(-44.54375076293945, -12)"><rect></rect><foreignObject width="89.0875015258789" height="24"><p>I am a circle</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

### Bang

##### Code:

```
mermaidmindmap
    id))I am a bang((
```

<svg id="mermaid-56" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 186.390625px;" viewBox="8.32781982421875 6.599998474121094 186.390625 100" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-56_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-56_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-56_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-56_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g></g><g></g><g><g id="mermaid-56-node_0" data-look="classic" transform="translate(98.1953125, 55)"><path style="" d="M0 0 
    a19.96687545776367,19.96687545776367 1 0,0 33.27812576293945,-6.4
    a19.96687545776367,19.96687545776367 1 0,0 33.27812576293945,0
    a19.96687545776367,19.96687545776367 1 0,0 33.27812576293945,0
    a19.96687545776367,19.96687545776367 1 0,0 33.27812576293945,6.4

    a19.96687545776367,19.96687545776367 1 0,0 19.96687545776367,21.12
    a15.973500366210937,15.973500366210937 1 0,0 0,21.76
    a19.96687545776367,19.96687545776367 1 0,0 -19.96687545776367,21.12

    a19.96687545776367,19.96687545776367 1 0,0 -33.27812576293945,9.6
    a19.96687545776367,19.96687545776367 1 0,0 -33.27812576293945,0
    a19.96687545776367,19.96687545776367 1 0,0 -33.27812576293945,0
    a19.96687545776367,19.96687545776367 1 0,0 -33.27812576293945,-9.6

    a19.96687545776367,19.96687545776367 1 0,0 -13.311250305175783,-21.12
    a15.973500366210937,15.973500366210937 1 0,0 0,-21.76
    a19.96687545776367,19.96687545776367 1 0,0 13.311250305175783,-21.12
  H0 V0 Z" transform="translate(-66.5562515258789, -32)" fill="none"></path><g style="" transform="translate(-41.556251525878906, -12)"><rect></rect><foreignObject width="83.11250305175781" height="24"><p>I am a bang</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

### Cloud

##### Code:

```
mermaidmindmap
    id)I am a cloud(
```

<svg id="mermaid-60" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 143.21898651123047px;" viewBox="7.269340515136719 6.441516876220703 143.21898651123047 101.05596160888672" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-60_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-60_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-60_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-60_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g></g><g></g><g><g id="mermaid-60-node_0" data-look="classic" transform="translate(76.60949325561523, 55.52798080444336)"><path style="" d="M0 0 
    a14.685000228881835,14.685000228881835 0 0,1 24.475000381469727,-9.790000152587892
    a34.26500053405761,34.26500053405761 1 0,1 39.16000061035157,-9.790000152587892
    a24.475000381469727,24.475000381469727 1 0,1 34.26500053405761,19.580000305175783

    a14.685000228881835,14.685000228881835 1 0,1 14.685000228881835,11.899999999999999
    a19.580000305175783,19.580000305175783 1 0,1 -14.685000228881835,22.1

    a24.475000381469727,14.685000228881835 1 0,1 -24.475000381469727,14.685000228881835
    a34.26500053405761,34.26500053405761 1 0,1 -48.95000076293945,0
    a14.685000228881835,14.685000228881835 1 0,1 -24.475000381469727,-14.685000228881835

    a14.685000228881835,14.685000228881835 1 0,1 -9.790000152587892,-11.899999999999999
    a19.580000305175783,19.580000305175783 1 0,1 9.790000152587892,-22.1
  H0 V0 Z" transform="translate(-48.95000076293945, -17)" fill="none"></path><g style="" transform="translate(-43.95000076293945, -12)"><rect></rect><foreignObject width="87.9000015258789" height="24"><p>I am a cloud</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

### Hexagon

##### Code:

```
mermaidmindmap
    id{{I am a hexagon}}
```

<svg id="mermaid-64" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 170.2624969482422px;" viewBox="5 5 170.2624969482422 64" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-64_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-64_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-64_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-64_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g></g><g></g><g><g id="mermaid-64-node_0" data-look="classic" transform="translate(90.1312484741211, 37)"><polygon points="11,0 139.26250457763672,0 150.26250457763672,-22 139.26250457763672,-44 11,-44 0,-22" transform="translate(-75.13125228881836,22)" fill="none" stroke="currentColor"></polygon><g style="" transform="translate(-54.13125228881836, -12)"><rect></rect><foreignObject width="108.26250457763672" height="24"><p>I am a hexagon</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

### Default

##### Code:

```
mermaidmindmap
    I am the default shape
```

<svg id="mermaid-68" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 222.27500915527344px;" viewBox="5 5 222.27500915527344 54" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-68_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-68_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-68_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-68_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g></g><g></g><g><g id="mermaid-68-node_0" data-look="classic" transform="translate(116.13750457763672, 32)"><path id="mermaid-68-node_0" style="" d="
    M-101.13750457763672 12
    v-24
    q0,-5 5,-5
    h192.27500915527344
    q5,0 5,5
    v24
    q0,5 -5,5
    h-192.27500915527344
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-101.13750457763672" y1="17" x2="101.13750457763672" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-81.13750457763672, -12)"><rect></rect><foreignObject width="162.27500915527344" height="24"><p>I am the default shape</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

More shapes will be added, beginning with the shapes available in flowcharts.

## Icons and classes

## Icons

As with flowcharts you can add icons to your nodes but with an updated syntax. The styling for the font based icons are added during the integration so that they are available for the web page. *This is not something a diagram author can do but has to be done with the site administrator or the integrator*. Once the icon fonts are in place you add them to the mind map nodes using the `::icon()` syntax. You place the classes for the icon within the parenthesis like in the following example where icons for material design and [Font Awesome 5](https://fontawesome.com/v5/search?o=r&m=free) are displayed. The intention is that this approach should be used for all diagrams supporting icons. **Experimental feature:** This wider scope is also the reason Mindmaps are experimental as this syntax and approach could change.

##### Code:

```
mermaidmindmap
    Root
        A
        ::icon(fa fa-book)
        B(B)
        ::icon(mdi mdi-skull-outline)
```

<svg id="mermaid-81" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 287.6764831542969px;" viewBox="5 5 287.6764831542969 74" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-81_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-81_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-81_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-81_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g><path d="M158.651,42L165.676,42C172.702,42,186.753,42,200.804,42C214.855,42,228.907,42,235.932,42L242.958,42" id="mermaid-81-edge_0_1" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_1" data-points="W3sieCI6MTU4LjY1MDcyNjQ0MzYwNzk0LCJ5Ijo0Mn0seyJ4IjoyMDAuODA0MjE0NjY1NDEyMjUsInkiOjQyfSx7IngiOjI0Mi45NTc3MDI4ODcyMTY1NiwieSI6NDJ9XQ==" data-look="classic" fill="none" stroke="currentColor"></path><path d="M128.651,42L122.057,42C115.464,42,102.278,42,89.091,42C75.904,42,62.718,42,56.125,42L49.531,42" id="mermaid-81-edge_0_2" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_2" data-points="W3sieCI6MTI4LjY1MDcyNjQ0MzYwNzk0LCJ5Ijo0Mn0seyJ4Ijo4OS4wOTA5ODgyMjE4MDM5NywieSI6NDJ9LHsieCI6NDkuNTMxMjUsInkiOjQyfV0=" data-look="classic" fill="none" stroke="currentColor"></path></g><g><g><g data-id="edge_0_1" transform="translate(0, 0)"></g></g><g><g data-id="edge_0_2" transform="translate(0, 0)"></g></g></g><g><g id="mermaid-81-node_0" data-look="classic" transform="translate(143.65072644360794, 42)"><path id="mermaid-81-node_0" style="" d="
    M-36.09375 12
    v-24
    q0,-5 5,-5
    h62.1875
    q5,0 5,5
    v24
    q0,5 -5,5
    h-62.1875
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-36.09375" y1="17" x2="36.09375" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-16.09375, -12)"><rect></rect><foreignObject width="32.1875" height="24"><p>Root</p></foreignObject></g></g><g id="mermaid-81-node_1" data-look="classic" transform="translate(257.95770288721656, 42)"><path id="mermaid-81-node_1" style="" d="
    M-24.71875 12
    v-24
    q0,-5 5,-5
    h39.4375
    q5,0 5,5
    v24
    q0,5 -5,5
    h-39.4375
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-24.71875" y1="17" x2="24.71875" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-4.71875, -12)"><rect></rect><foreignObject width="9.4375" height="24"><p>A</p></foreignObject></g></g><g id="mermaid-81-node_2" data-look="classic" transform="translate(34.53125, 42)"><rect style="" rx="5" ry="5" x="-19.53125" y="-27" width="39.0625" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-4.53125, -12)"><rect></rect><foreignObject width="9.0625" height="24"><p>B</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

## Classes

Again the syntax for adding classes is similar to flowcharts. You can add classes using a triple colon following a number of css classes separated by space. In the following example one of the nodes has two custom classes attached urgent turning the background red and the text white and large increasing the font size:

##### Code:

```
mermaidmindmap
    Root
        A[A]
        :::urgent large
        B(B)
        C
```

<svg id="mermaid-88" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 217.68896484375px;" viewBox="5.000001907348633 5 217.68896484375 243.042724609375" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-88_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-88_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-88_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-88_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g><path d="M88.456,117.394L95.504,118.06C102.553,118.727,116.65,120.059,130.746,121.392C144.843,122.725,158.94,124.058,165.988,124.724L173.037,125.391" id="mermaid-88-edge_0_1" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_1" data-points="W3sieCI6ODguNDU2MDIwNjgwMzU5MjksInkiOjExNy4zOTM4MzMzNjkwNTM5NX0seyJ4IjoxMzAuNzQ2NDE2ODQ2Mjc2NiwieSI6MTIxLjM5MjI5ODY3OTEwNzUxfSx7IngiOjE3My4wMzY4MTMwMTIxOTM4NywieSI6MTI1LjM5MDc2Mzk4OTE2MTA3fV0=" data-look="classic" fill="none" stroke="currentColor"></path><path d="M68.904,130.253L67.11,135.796C65.316,141.339,61.727,152.426,58.139,163.512C54.551,174.599,50.963,185.685,49.169,191.228L47.375,196.772" id="mermaid-88-edge_0_2" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_2" data-points="W3sieCI6NjguOTAzNjgzNjQyOTQ5MjgsInkiOjEzMC4yNTMwNTI1MzEwNjA5N30seyJ4Ijo1OC4xMzkxMzc3MDY2NzcxNiwieSI6MTYzLjUxMjMwNDQyMDgxNDY0fSx7IngiOjQ3LjM3NDU5MTc3MDQwNTA1LCJ5IjoxOTYuNzcxNTU2MzEwNTY4MzF9XQ==" data-look="classic" fill="none" stroke="currentColor"></path><path d="M67.931,102.063L66.052,97.384C64.173,92.706,60.414,83.348,56.655,73.991C52.896,64.634,49.137,55.276,47.258,50.598L45.379,45.919" id="mermaid-88-edge_0_3" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_3" data-points="W3sieCI6NjcuOTMxNDI1ODIzMjg5MTYsInkiOjEwMi4wNjI5MTI3Nzc5NTIzOH0seyJ4Ijo1Ni42NTUwNTk3OTAyNjU3OTYsInkiOjczLjk5MDk1NjMxMDU3MTA1fSx7IngiOjQ1LjM3ODY5Mzc1NzI0MjQzLCJ5Ijo0NS45MTg5OTk4NDMxODk3MjR9XQ==" data-look="classic" fill="none" stroke="currentColor"></path></g><g><g><g data-id="edge_0_1" transform="translate(0, 0)"></g></g><g><g data-id="edge_0_2" transform="translate(0, 0)"></g></g><g><g data-id="edge_0_3" transform="translate(0, 0)"></g></g></g><g><g id="mermaid-88-node_0" data-look="classic" transform="translate(73.52261919906186, 115.9819126211421)"><path id="mermaid-88-node_0" style="" d="
    M-36.09375 12
    v-24
    q0,-5 5,-5
    h62.1875
    q5,0 5,5
    v24
    q0,5 -5,5
    h-62.1875
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-36.09375" y1="17" x2="36.09375" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-16.09375, -12)"><rect></rect><foreignObject width="32.1875" height="24"><p>Root</p></foreignObject></g></g><g id="mermaid-88-node_1" data-look="classic" transform="translate(187.9702144934913, 126.80268473707292)"><rect style="" x="-24.71875" y="-22" width="49.4375" height="44" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-4.71875, -12)"><rect></rect><foreignObject width="9.4375" height="24"><p>A</p></foreignObject></g></g><g id="mermaid-88-node_2" data-look="classic" transform="translate(42.75565621429246, 211.0426962204872)"><rect style="" rx="5" ry="5" x="-19.53125" y="-27" width="39.0625" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-4.53125, -12)"><rect></rect><foreignObject width="9.0625" height="24"><p>B</p></foreignObject></g></g><g id="mermaid-88-node_3" data-look="classic" transform="translate(39.78750038146973, 32)"><path id="mermaid-88-node_3" style="" d="
    M-24.78749990463257 12
    v-24
    q0,-5 5,-5
    h39.57499980926514
    q5,0 5,5
    v24
    q0,5 -5,5
    h-39.57499980926514
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-24.78749990463257" y1="17" x2="24.78749990463257" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-4.787499904632568, -12)"><rect></rect><foreignObject width="9.574999809265137" height="24"><p>C</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

*These classes need to be supplied by the site administrator.*

## Unclear indentation

The actual indentation does not really matter only compared with the previous rows. If we take the previous example and disrupt it a little we can see how the calculations are performed. Let us start with placing C with a smaller indentation than `B` but larger then `A`.

```
mindmap
    Root
        A
            B
          C
```

This outline is unclear as `B` clearly is a child of `A` but when we move on to `C` the clarity is lost. `C` is neither a child of `B` with a higher indentation nor does it have the same indentation as `B`. The only thing that is clear is that the first node with smaller indentation, indicating a parent, is A. Then Mermaid relies on this known truth and compensates for the unclear indentation and selects `A` as a parent of `C` leading till the same diagram with `B` and `C` as siblings.

##### Code:

```
mermaidmindmap
Root
    A
        B
      C
```

<svg id="mermaid-102" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 242.63975524902344px;" viewBox="5 5 242.63975524902344 210.3272247314453" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-102_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-102_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-102_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-102_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g><path d="M192.311,176.507L188.892,172.131C185.473,167.755,178.635,159.003,171.796,150.251C164.958,141.499,158.12,132.747,154.701,128.371L151.282,123.995" id="mermaid-102-edge_0_1" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_1" data-points="W3sieCI6MTkyLjMxMDg3MjE3MTkyMzYyLCJ5IjoxNzYuNTA3MjMzODEwOTE4ODV9LHsieCI6MTcxLjc5NjQ5NTY4NjcwNTg0LCJ5IjoxNTAuMjUxMDAyOTMwNDgzODh9LHsieCI6MTUxLjI4MjExOTIwMTQ4ODA2LCJ5IjoxMjMuOTk0NzcyMDUwMDQ4OTF9XQ==" data-look="classic" fill="none" stroke="currentColor"></path><path d="M127.111,110.792L121.057,110.232C115.004,109.672,102.896,108.551,90.789,107.431C78.682,106.31,66.575,105.189,60.521,104.629L54.467,104.069" id="mermaid-102-edge_1_2" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_1_2" data-points="W3sieCI6MTI3LjExMDgyNDQzNTQ1NDQ4LCJ5IjoxMTAuNzkyMzQyNTQwODk5NTF9LHsieCI6OTAuNzg5MTE3MjEzMzMxMzQsInkiOjEwNy40MzA1NDMwMTkwMjU0NH0seyJ4Ijo1NC40Njc0MDk5OTEyMDgyLCJ5IjoxMDQuMDY4NzQzNDk3MTUxMzZ9XQ==" data-look="classic" fill="none" stroke="currentColor"></path><path d="M149.621,99.228L152.268,94.704C154.914,90.181,160.206,81.134,165.499,72.087C170.792,63.041,176.084,53.994,178.73,49.471L181.377,44.947" id="mermaid-102-edge_1_3" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_1_3" data-points="W3sieCI6MTQ5LjYyMTM2NTQ4MDA5MDg0LCJ5Ijo5OS4yMjc2MjQ2MjQ5MjkyOX0seyJ4IjoxNjUuNDk5MDI2MTg3ODE0MDIsInkiOjcyLjA4NzM4ODQ0MjczMTk5fSx7IngiOjE4MS4zNzY2ODY4OTU1MzcyLCJ5Ijo0NC45NDcxNTIyNjA1MzQ2OX1d" data-look="classic" fill="none" stroke="currentColor"></path></g><g><g><g data-id="edge_0_1" transform="translate(0, 0)"></g></g><g><g data-id="edge_1_2" transform="translate(0, 0)"></g></g><g><g data-id="edge_1_3" transform="translate(0, 0)"></g></g></g><g><g id="mermaid-102-node_0" data-look="classic" transform="translate(201.546006946749, 188.32722897550377)"><path id="mermaid-102-node_0" style="" d="
    M-36.09375 12
    v-24
    q0,-5 5,-5
    h62.1875
    q5,0 5,5
    v24
    q0,5 -5,5
    h-62.1875
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-36.09375" y1="17" x2="36.09375" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-16.09375, -12)"><rect></rect><foreignObject width="32.1875" height="24"><p>Root</p></foreignObject></g></g><g id="mermaid-102-node_1" data-look="classic" transform="translate(142.04698442666268, 112.17477688546398)"><path id="mermaid-102-node_1" style="" d="
    M-24.71875 12
    v-24
    q0,-5 5,-5
    h39.4375
    q5,0 5,5
    v24
    q0,5 -5,5
    h-39.4375
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-24.71875" y1="17" x2="24.71875" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-4.71875, -12)"><rect></rect><foreignObject width="9.4375" height="24"><p>A</p></foreignObject></g></g><g id="mermaid-102-node_2" data-look="classic" transform="translate(39.53125, 102.68630915258689)"><path id="mermaid-102-node_2" style="" d="
    M-24.53125 12
    v-24
    q0,-5 5,-5
    h39.0625
    q5,0 5,5
    v24
    q0,5 -5,5
    h-39.0625
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-24.53125" y1="17" x2="24.53125" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-4.53125, -12)"><rect></rect><foreignObject width="9.0625" height="24"><p>B</p></foreignObject></g></g><g id="mermaid-102-node_3" data-look="classic" transform="translate(188.95106794896537, 32)"><path id="mermaid-102-node_3" style="" d="
    M-24.78749990463257 12
    v-24
    q0,-5 5,-5
    h39.57499980926514
    q5,0 5,5
    v24
    q0,5 -5,5
    h-39.57499980926514
    q-5,0 -5,-5
    Z
  " fill="none"></path><line x1="-24.78749990463257" y1="17" x2="24.78749990463257" y2="17" stroke="currentColor" stroke-opacity="0.2"></line><g style="" transform="translate(-4.787499904632568, -12)"><rect></rect><foreignObject width="9.574999809265137" height="24"><p>C</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

## Markdown Strings

The "Markdown Strings" feature enhances mind maps by offering a more versatile string type, which supports text formatting options such as bold and italics, and automatically wraps text within labels.

##### Code:

```
mermaidmindmap
    id1["\`**Root** with
a second line
Unicode works too: 🤓\`"]
      id2["\`The dog in **the** hog... a *very long text* that wraps to a new line\`"]
      id3[Regular labels still works]
```

<svg id="mermaid-109" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 789.574951171875px;" viewBox="5 5 789.574951171875 132.83367156982422" role="graphics-document document" aria-roledescription="mindmap"><g><marker id="mermaid-109_mindmap-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-109_mindmap-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-109_mindmap-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-109_mindmap-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><g></g><g><path d="M403.746,62.13L424.235,63.678C444.724,65.226,485.703,68.321,526.682,71.417C567.66,74.512,608.639,77.608,629.128,79.156L649.618,80.704" id="mermaid-109-edge_0_1" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_1" data-points="W3sieCI6NDAzLjc0NTczNTY4NTA4NzIsInkiOjYyLjEyOTkyMTExODEzMDM3fSx7IngiOjUyNi42ODE2NDQzNjAzMTAzLCJ5Ijo3MS40MTY4MzIzNDIwNDcwOX0seyJ4Ijo2NDkuNjE3NTUzMDM1NTMzNCwieSI6ODAuNzAzNzQzNTY1OTYzOH1d" data-look="classic" fill="none" stroke="currentColor"></path><path d="M373.835,62.177L354.262,63.718C334.689,65.258,295.543,68.34,256.397,71.421C217.252,74.502,178.106,77.583,158.533,79.124L138.96,80.665" id="mermaid-109-edge_0_2" style="undefined;;;undefined" data-edge="true" data-et="edge" data-id="edge_0_2" data-points="W3sieCI6MzczLjgzNDYwNjQyMjYzNTYsInkiOjYyLjE3NzA0OTE4NDY2NTA4fSx7IngiOjI1Ni4zOTczMDEwNDY2MjkxNCwieSI6NzEuNDIwODUxNjA1OTM1ODF9LHsieCI6MTM4Ljk1OTk5NTY3MDYyMjY3LCJ5Ijo4MC42NjQ2NTQwMjcyMDY1NH1d" data-look="classic" fill="none" stroke="currentColor"></path></g><g><g><g data-id="edge_0_1" transform="translate(0, 0)"></g></g><g><g data-id="edge_0_2" transform="translate(0, 0)"></g></g></g><g><g id="mermaid-109-node_0" data-look="classic" transform="translate(388.7883536191372, 61)"><rect style="" x="-102.45625305175781" y="-46" width="204.91250610351562" height="92" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-82.45625305175781, -36)"><rect></rect><foreignObject width="164.91250610351562" height="72"><p><strong>Root</strong> with<br>a second line<br>Unicode works too: 🤓</p></foreignObject></g></g><g id="mermaid-109-node_1" data-look="classic" transform="translate(664.5749351014834, 81.83366468409417)"><rect style="" x="-120" y="-46" width="240" height="92" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-100, -36)"><rect></rect><foreignObject width="200" height="72"><p>The dog in <strong>the</strong> hog... a <em>very long text</em> that wraps to a new line</p></foreignObject></g></g><g id="mermaid-109-node_2" data-look="classic" transform="translate(124.0062484741211, 81.84170321187162)"><rect style="" x="-109.0062484741211" y="-22" width="218.0124969482422" height="44" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-89.0062484741211, -12)"><rect></rect><foreignObject width="178.0124969482422" height="24"><p>Regular labels still works</p></foreignObject></g></g></g></g><defs></defs><defs></defs></svg>

Formatting:

- For bold text, use double asterisks \*\* before and after the text.
- For italics, use single asterisks \* before and after the text.
- With traditional strings, you needed to add  
	tags for text to wrap in nodes. However, markdown strings automatically wrap text when it becomes too long and allows you to start a new line by simply using a newline character instead of a  
	tag.

## Integrating with your library/website.

Mindmap uses the experimental lazy loading & async rendering features which could change in the future. From version 9.4.0 this diagram is included in mermaid but use lazy loading in order to keep the size of mermaid down. This is important in order to be able to add additional diagrams going forward.

You can still use the pre 9.4.0 method to add mermaid with mindmaps to a web page:

```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@9.3.0/dist/mermaid.esm.min.mjs';
  import mindmap from 'https://cdn.jsdelivr.net/npm/@mermaid-js/mermaid-mindmap@9.3.0/dist/mermaid-mindmap.esm.min.mjs';
  await mermaid.registerExternalDiagrams([mindmap]);
</script>
```

From version 9.4.0 you can simplify this code to:

```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
</script>
```

You can also refer the [implementation in the live editor](https://github.com/mermaid-js/mermaid-live-editor/blob/develop/src/lib/util/mermaid.ts) to see how the async loading is done.

## Layouts

Mermaid also supports a Tidy Tree layout for mindmaps.

```
---
config:
  layout: tidy-tree
---
mindmap
root((mindmap is a long thing))
  A
  B
  C
  D
```

Instructions to add and register tidy-tree layout are present in [Tidy Tree Configuration](https://mermaid.ai/open-source/config/tidy-tree.html)