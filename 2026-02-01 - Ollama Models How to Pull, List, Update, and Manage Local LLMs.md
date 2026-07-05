---
title: "Ollama Models: How to Pull, List, Update, and Manage Local LLMs"
source: "https://oneuptime.com/blog/post/2026-02-02-ollama-model-management/view"
author:
  - "[[Nawaz Dhandala]]"
published: 2026-02-01
created: 2026-07-03
description: "Complete guide to managing Ollama models. Pull new models, list installed ones, update to latest versions, customize with Modelfiles, and clean up disk space."
---
---

> Getting [[models]] into [[Ollama]] is straightforward, but managing them effectively requires understanding how Ollama [[stores]], [[versions]], and [[updates]] models. Knowing these [[details]] helps you keep your [[model library]] [[organized]] and your [[disk space]] [[under control]].

Whether you are [[experimenting]] with different models or [[building]] production applications, mastering [[model management in Ollama]] will save you [[time]] and [[frustration]] [[down the road]].

---

## Understanding Ollama's Model System

Before diving into commands, let us look at how Ollama organizes models internally.

<svg id="mermaid-1783135952257" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="max-width: 612.9453125px;" viewBox="-8 -8 612.9453125 611" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-1783135952257_flowchart-pointEnd" viewBox="0 0 10 10" refX="6" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135952257_flowchart-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135952257_flowchart-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1783135952257_flowchart-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1783135952257_flowchart-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135952257_flowchart-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><g><g><g id="Cache"><rect style="" rx="0" ry="0" x="115.1796875" y="417" width="354.23046875" height="178"></rect><g transform="translate(261.669921875, 417)"><foreignObject width="61.25" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Runtime</div></foreignObject></g></g><g id="Local"><rect style="" rx="0" ry="0" x="32.787109375" y="139" width="501.001953125" height="228"></rect><g transform="translate(194.8740234375, 139)"><foreignObject width="176.828125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Local Storage ~/.ollama</div></foreignObject></g></g><g id="Registry"><rect style="" rx="0" ry="0" x="0" y="0" width="596.9453125" height="89"></rect><g transform="translate(214.1796875, 0)"><foreignObject width="168.5859375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Ollama Model Registry</div></foreignObject></g></g><g id="Models"><rect style="" rx="0" ry="0" x="52.787109375" y="164" width="461.001953125" height="178"></rect><g transform="translate(253.1474609375, 164)"><foreignObject width="60.28125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">models/</div></foreignObject></g></g></g><g><path d="M98.527,64L98.527,68.167C98.527,72.333,98.527,80.667,98.527,89C98.527,97.333,98.527,105.667,98.527,114C98.527,122.333,98.527,130.667,98.527,139C98.527,147.333,98.527,155.667,122.205,165.27C145.882,174.874,193.237,185.747,216.915,191.184L240.592,196.621" id="L-R1-M1-0" style="fill:none;" marker-end="url(#mermaid-1783135952257_flowchart-pointEnd)" stroke="currentColor"></path><path d="M292.324,64L292.324,68.167C292.324,72.333,292.324,80.667,292.324,89C292.324,97.333,292.324,105.667,292.324,114C292.324,122.333,292.324,130.667,292.324,139C292.324,147.333,292.324,155.667,292.324,163.117C292.324,170.567,292.324,177.133,292.324,180.417L292.324,183.7" id="L-R2-M1-0" style="fill:none;" marker-end="url(#mermaid-1783135952257_flowchart-pointEnd)" stroke="currentColor"></path><path d="M492.27,64L492.27,68.167C492.27,72.333,492.27,80.667,492.27,89C492.27,97.333,492.27,105.667,492.27,114C492.27,122.333,492.27,130.667,492.27,139C492.27,147.333,492.27,155.667,467.569,165.331C442.868,174.995,393.466,185.99,368.765,191.487L344.064,196.985" id="L-R3-M1-0" style="fill:none;" marker-end="url(#mermaid-1783135952257_flowchart-pointEnd)" stroke="currentColor"></path><path d="M292.324,228L292.324,232.167C292.324,236.333,292.324,244.667,292.324,252.117C292.324,259.567,292.324,266.133,292.324,269.417L292.324,272.7" id="L-M1-M2-0" style="fill:none;" marker-end="url(#mermaid-1783135952257_flowchart-pointEnd)" stroke="currentColor"></path><path d="M292.324,317L292.324,321.167C292.324,325.333,292.324,333.667,292.324,342C292.324,350.333,292.324,358.667,292.324,367C292.324,375.333,292.324,383.667,292.324,392C292.324,400.333,292.324,408.667,292.324,416.117C292.324,423.567,292.324,430.133,292.324,433.417L292.324,436.7" id="L-M2-C1-0" style="fill:none;" marker-end="url(#mermaid-1783135952257_flowchart-pointEnd)" stroke="currentColor"></path><path d="M256.089,481L248.346,485.167C240.603,489.333,225.118,497.667,217.375,505.117C209.633,512.567,209.633,519.133,209.633,522.417L209.633,525.7" id="L-C1-C2-0" style="fill:none;" marker-end="url(#mermaid-1783135952257_flowchart-pointEnd)" stroke="currentColor"></path><path d="M328.56,481L336.302,485.167C344.045,489.333,359.53,497.667,367.273,505.117C375.016,512.567,375.016,519.133,375.016,522.417L375.016,525.7" id="L-C1-C3-0" style="fill:none;" marker-end="url(#mermaid-1783135952257_flowchart-pointEnd)" stroke="currentColor"></path></g><g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g></g><g><g id="flowchart-C1-5" data-node="true" data-id="C1" transform="translate(292.32421875, 461.5)"><rect style="" rx="0" ry="0" x="-61.15625" y="-19.5" width="122.3125" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-53.65625, -12)"><rect></rect><foreignObject width="107.3125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Loaded Model</div></foreignObject></g></g><g id="flowchart-C2-6" data-node="true" data-id="C2" transform="translate(209.6328125, 550.5)"><rect style="" rx="0" ry="0" x="-57.75" y="-19.5" width="115.5" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-50.25, -12)"><rect></rect><foreignObject width="100.5" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">GPU Memory</div></foreignObject></g></g><g id="flowchart-C3-7" data-node="true" data-id="C3" transform="translate(375.015625, 550.5)"><rect style="" rx="0" ry="0" x="-57.6328125" y="-19.5" width="115.265625" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-50.1328125, -12)"><rect></rect><foreignObject width="100.265625" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">CPU Memory</div></foreignObject></g></g><g id="flowchart-M1-3" data-node="true" data-id="M1" transform="translate(292.32421875, 208.5)"><rect style="" rx="0" ry="0" x="-46.56640625" y="-19.5" width="93.1328125" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-39.06640625, -12)"><rect></rect><foreignObject width="78.1328125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">manifests/</div></foreignObject></g></g><g id="flowchart-M2-4" data-node="true" data-id="M2" transform="translate(292.32421875, 297.5)"><rect style="" rx="0" ry="0" x="-30.8984375" y="-19.5" width="61.796875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-23.3984375, -12)"><rect></rect><foreignObject width="46.796875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">blobs/</div></foreignObject></g></g><g id="flowchart-R1-0" data-node="true" data-id="R1" transform="translate(98.52734375, 44.5)"><rect style="" rx="0" ry="0" x="-63.52734375" y="-19.5" width="127.0546875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-56.02734375, -12)"><rect></rect><foreignObject width="112.0546875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Official Models</div></foreignObject></g></g><g id="flowchart-R2-1" data-node="true" data-id="R2" transform="translate(292.32421875, 44.5)"><rect style="" rx="0" ry="0" x="-80.26953125" y="-19.5" width="160.5390625" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-72.76953125, -12)"><rect></rect><foreignObject width="145.5390625" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Community Models</div></foreignObject></g></g><g id="flowchart-R3-2" data-node="true" data-id="R3" transform="translate(492.26953125, 44.5)"><rect style="" rx="0" ry="0" x="-69.67578125" y="-19.5" width="139.3515625" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-62.17578125, -12)"><rect></rect><foreignObject width="124.3515625" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Custom Uploads</div></foreignObject></g></g></g></g></g></svg>

Ollama stores models in two parts:

- **Manifests**: Metadata files containing model information, configuration, and references to blobs
- **Blobs**: The actual model weights stored as content-addressed files

Multiple models can share blobs if they use the same base weights, which saves significant disk space when working with model variants.

---

## Pulling Models from the Registry

The `ollama pull` command downloads models from the Ollama model registry.

### Basic Pull Operations

Download a model using its name from the registry.

```bash
# Pull the latest version of Llama 3.2

# Ollama automatically selects an appropriate size based on your hardware
ollama pull llama3.2
```

You will see download progress with layer information:

```
pulling manifest
pulling 8934d96d3f08... 100% |████████████████████| 2.0 GB
pulling 8c17c2ebb0ea... 100% |████████████████████| 7.0 KB
pulling 7c23fb36d801... 100% |████████████████████| 4.8 KB
pulling 2e0493f67d0c... 100% |████████████████████| 59 B
pulling fa304d675061... 100% |████████████████████| 91 B
pulling 42ba7f8a01dd... 100% |████████████████████| 557 B
verifying sha256 digest
writing manifest
removing any unused layers
success
```

### Pulling Specific Model Variants

Models come in different sizes and quantization levels. Specify the exact variant using tags.

```bash
# Pull a specific size variant of Llama 3.2
# The :1b suffix indicates the 1 billion parameter version
ollama pull llama3.2:1b

# Pull the 3 billion parameter version
ollama pull llama3.2:3b

# Pull a specific quantization level
# Q4_K_M offers good balance between size and quality
ollama pull llama3.2:3b-instruct-q4_K_M

# Pull the full precision version (larger but higher quality)
ollama pull llama3.2:3b-instruct-fp16
```

### Understanding Model Tags

Model tags follow a consistent naming pattern.

<svg id="mermaid-1783135955713" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="max-width: 745.765625px;" viewBox="-8 -8 745.765625 322" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-1783135955713_flowchart-pointEnd" viewBox="0 0 10 10" refX="6" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135955713_flowchart-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135955713_flowchart-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1783135955713_flowchart-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1783135955713_flowchart-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135955713_flowchart-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><g><g></g><g><path d="M137.352,133.5L157.513,114.5C177.675,95.5,217.998,57.5,241.442,38.5C264.887,19.5,271.454,19.5,274.737,19.5L278.02,19.5" id="L-A-B-0" style="fill:none;" marker-end="url(#mermaid-1783135955713_flowchart-pointEnd)" stroke="currentColor"></path><path d="M178.736,133.5L192,129.333C205.264,125.167,231.792,116.833,249.136,112.667C266.481,108.5,274.641,108.5,278.721,108.5L282.802,108.5" id="L-A-C-0" style="fill:none;" marker-end="url(#mermaid-1783135955713_flowchart-pointEnd)" stroke="currentColor"></path><path d="M178.736,172.5L192,176.667C205.264,180.833,231.792,189.167,251.903,193.333C272.013,197.5,285.706,197.5,292.553,197.5L299.399,197.5" id="L-A-D-0" style="fill:none;" marker-end="url(#mermaid-1783135955713_flowchart-pointEnd)" stroke="currentColor"></path><path d="M137.352,172.5L157.513,191.5C177.675,210.5,217.998,248.5,241.507,267.5C265.016,286.5,271.711,286.5,275.059,286.5L278.407,286.5" id="L-A-E-0" style="fill:none;" marker-end="url(#mermaid-1783135955713_flowchart-pointEnd)" stroke="currentColor"></path><path d="M393.492,19.5L397.659,19.5C401.826,19.5,410.159,19.5,434.961,19.5C459.763,19.5,501.034,19.5,521.67,19.5L542.305,19.5" id="L-B-F-0" style="fill:none;" marker-end="url(#mermaid-1783135955713_flowchart-pointEnd)" stroke="currentColor"></path><path d="M388.711,108.5L393.674,108.5C398.638,108.5,408.565,108.5,431.326,108.5C454.086,108.5,489.68,108.5,507.477,108.5L525.274,108.5" id="L-C-G-0" style="fill:none;" marker-end="url(#mermaid-1783135955713_flowchart-pointEnd)" stroke="currentColor"></path><path d="M372.113,197.5L379.843,197.5C387.573,197.5,403.033,197.5,414.046,197.5C425.059,197.5,431.626,197.5,434.909,197.5L438.192,197.5" id="L-D-H-0" style="fill:none;" marker-end="url(#mermaid-1783135955713_flowchart-pointEnd)" stroke="currentColor"></path><path d="M393.105,286.5L397.337,286.5C401.568,286.5,410.03,286.5,422.426,286.5C434.822,286.5,451.152,286.5,459.316,286.5L467.481,286.5" id="L-E-I-0" style="fill:none;" marker-end="url(#mermaid-1783135955713_flowchart-pointEnd)" stroke="currentColor"></path></g><g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g></g><g><g id="flowchart-A-26" data-node="true" data-id="A" transform="translate(116.66015625, 153)"><rect style="" rx="0" ry="0" x="-116.66015625" y="-19.5" width="233.3203125" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-109.16015625, -12)"><rect></rect><foreignObject width="218.3203125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">llama3.2:3b-instruct-q4_K_M</div></foreignObject></g></g><g id="flowchart-B-27" data-node="true" data-id="B" transform="translate(338.40625, 19.5)"><rect style="" rx="0" ry="0" x="-55.0859375" y="-19.5" width="110.171875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-47.5859375, -12)"><rect></rect><foreignObject width="95.171875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Model Name</div></foreignObject></g></g><g id="flowchart-C-29" data-node="true" data-id="C" transform="translate(338.40625, 108.5)"><rect style="" rx="0" ry="0" x="-50.3046875" y="-19.5" width="100.609375" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-42.8046875, -12)"><rect></rect><foreignObject width="85.609375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Parameters</div></foreignObject></g></g><g id="flowchart-D-31" data-node="true" data-id="D" transform="translate(338.40625, 197.5)"><rect style="" rx="0" ry="0" x="-33.70703125" y="-19.5" width="67.4140625" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-26.20703125, -12)"><rect></rect><foreignObject width="52.4140625" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Variant</div></foreignObject></g></g><g id="flowchart-E-33" data-node="true" data-id="E" transform="translate(338.40625, 286.5)"><rect style="" rx="0" ry="0" x="-54.69921875" y="-19.5" width="109.3984375" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-47.19921875, -12)"><rect></rect><foreignObject width="94.3984375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Quantization</div></foreignObject></g></g><g id="flowchart-F-35" data-node="true" data-id="F" transform="translate(586.62890625, 19.5)"><rect style="" rx="0" ry="0" x="-39.0234375" y="-19.5" width="78.046875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-31.5234375, -12)"><rect></rect><foreignObject width="63.046875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">llama3.2</div></foreignObject></g></g><g id="flowchart-G-37" data-node="true" data-id="G" transform="translate(586.62890625, 108.5)"><rect style="" rx="0" ry="0" x="-56.0546875" y="-19.5" width="112.109375" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-48.5546875, -12)"><rect></rect><foreignObject width="97.109375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">3b = 3 billion</div></foreignObject></g></g><g id="flowchart-H-39" data-node="true" data-id="H" transform="translate(586.62890625, 197.5)"><rect style="" rx="0" ry="0" x="-143.13671875" y="-19.5" width="286.2734375" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-135.63671875, -12)"><rect></rect><foreignObject width="271.2734375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">instruct = fine-tuned for instructions</div></foreignObject></g></g><g id="flowchart-I-41" data-node="true" data-id="I" transform="translate(586.62890625, 286.5)"><rect style="" rx="0" ry="0" x="-113.84765625" y="-19.5" width="227.6953125" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-106.34765625, -12)"><rect></rect><foreignObject width="212.6953125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">q4_K_M = 4-bit quantization</div></foreignObject></g></g></g></g></g></svg>

Common tag components:

- **Parameter count**: 1b, 3b, 7b, 8b, 13b, 70b
- **Variants**: instruct, chat, code, text
- **Quantization**: q2\_K, q3\_K\_S, q4\_0, q4\_K\_M, q5\_K\_M, q8\_0, fp16

Lower quantization (q2, q3, q4) means smaller files but slightly reduced quality. Higher quantization (q8, fp16) preserves more quality but requires more memory.

---

## Listing and Inspecting Models

### View Downloaded Models

See all models stored locally using the list command.

```bash
# List all downloaded models with sizes and modification dates
ollama list
```

Example output:

```
NAME                    ID              SIZE      MODIFIED
llama3.2:latest         a80c4f17acd5    2.0 GB    2 hours ago
llama3.2:1b             baf6a787fdff    1.3 GB    3 hours ago
codellama:13b           8fdf8f752f6e    7.4 GB    1 day ago
mistral:latest          61e88e884507    4.1 GB    2 days ago
nomic-embed-text:latest 0a109f422b47    274 MB    3 days ago
```

### Check Running Models

See which models are currently loaded in memory.

```bash
# Display models loaded in GPU/CPU memory
ollama ps
```

Example output:

```
NAME              ID              SIZE      PROCESSOR    UNTIL
llama3.2:latest   a80c4f17acd5    3.3 GB    100% GPU     4 minutes from now
```

The UNTIL column shows when the model will be unloaded from memory if not used.

### Inspect Model Details

Get detailed information about a specific model.

```bash
# Show comprehensive model information including parameters and template
ollama show llama3.2
```

Output includes:

```
Model
  architecture     llama
  parameters       3.2B
  quantization     Q4_K_M
  context length   131072
  embedding length 3072

Parameters
  stop    "<|start_header_id|>"
  stop    "<|end_header_id|>"
  stop    "<|eot_id|>"

License
  Llama 3.2 Community License Agreement
  ...
```

For more specific information, use these variants:

```bash
# Show only the license information
ollama show llama3.2 --license

# Show the modelfile (template and parameters)
ollama show llama3.2 --modelfile

# Show the system prompt if defined
ollama show llama3.2 --system

# Show the prompt template
ollama show llama3.2 --template
```

---

## Updating Models

Ollama does not have a dedicated update command, but pulling a model again will download any newer version.

### Check for Updates

Pull the model again to check for and download updates.

```bash
# Re-pulling fetches the latest version if available
# Existing layers that match are not re-downloaded
ollama pull llama3.2
```

If the model is already up to date, you will see:

```
pulling manifest
pulling 8934d96d3f08... 100% |████████████████████| (already exists)
pulling 8c17c2ebb0ea... 100% |████████████████████| (already exists)
...
verifying sha256 digest
writing manifest
success
```

### Update All Models Script

Automate updates for all your downloaded models with a script.

```bash
#!/bin/bash
# update_all_models.sh
# Pulls the latest version of all locally installed Ollama models
# Useful for keeping your model library current

echo "Updating all Ollama models..."

# Get list of installed models and update each one
# The awk command extracts just the model name from the list output
ollama list | tail -n +2 | awk '{print $1}' | while read model; do
    echo ""
    echo "Updating: $model"
    ollama pull "$model"
done

echo ""
echo "All models updated!"
```

Save and run the script:

```bash
# Make the script executable
chmod +x update_all_models.sh

# Run the update script
./update_all_models.sh
```

---

## Removing Models

Keep your disk space under control by removing models you no longer need.

### Delete a Single Model

Remove a specific model from local storage.

```bash
# Remove a model by name
ollama rm codellama

# Remove a specific version/tag
ollama rm llama3.2:1b

# Remove multiple models in sequence
ollama rm mistral && ollama rm phi3
```

### Clean Up All Unused Models

Remove all models except the ones you want to keep.

```bash
#!/bin/bash
# cleanup_models.sh
# Removes all models except those in the keep list
# Modify the KEEP array to match your needs

# Models to keep (modify this list)
KEEP=("llama3.2:latest" "nomic-embed-text:latest")

# Get all installed models
ALL_MODELS=$(ollama list | tail -n +2 | awk '{print $1}')

for model in $ALL_MODELS; do
    # Check if model is in keep list
    keep=false
    for keeper in "${KEEP[@]}"; do
        if [ "$model" == "$keeper" ]; then
            keep=true
            break
        fi
    done

    # Remove if not in keep list
    if [ "$keep" = false ]; then
        echo "Removing: $model"
        ollama rm "$model"
    else
        echo "Keeping: $model"
    fi
done
```

### Check Disk Usage

Monitor how much space your models are using.

```bash
# Check total size of Ollama storage directory
du -sh ~/.ollama

# Check size of individual components
du -sh ~/.ollama/models/manifests
du -sh ~/.ollama/models/blobs

# List blobs sorted by size
ls -lhS ~/.ollama/models/blobs/ | head -20
```

---

## Copying and Renaming Models

Create copies of models with different names for organization or customization.

### Create a Model Copy

Copy an existing model to a new name.

```bash
# Copy llama3.2 to a new name
# Useful for creating a base before customization
ollama cp llama3.2 my-llama-base

# Verify the copy exists
ollama list
```

The copy shares the underlying blobs with the original, so disk usage does not double.

### Model Organization Strategy

Use naming conventions to organize your model library.

```bash
# Create project-specific model copies
ollama cp llama3.2 project-alpha/assistant
ollama cp codellama project-alpha/coder

# Create environment-specific copies
ollama cp llama3.2 dev/llama
ollama cp llama3.2 staging/llama
ollama cp llama3.2 prod/llama
```

---

## Creating Custom Models

Build customized models from base models using Modelfiles.

### Modelfile Structure

A Modelfile defines how to customize a base model.

```dockerfile
# Modelfile for a DevOps-focused assistant
# Start from a capable base model
FROM llama3.2:3b

# Define the system prompt that shapes model behavior
SYSTEM """
You are an expert DevOps engineer with deep knowledge of:
- Kubernetes and container orchestration
- CI/CD pipelines and automation
- Infrastructure as Code (Terraform, Pulumi)
- Monitoring and observability
- Cloud platforms (AWS, GCP, Azure)

Provide practical, production-ready advice. Include code examples when relevant.
Always consider security implications in your recommendations.
"""

# Adjust generation parameters
# Lower temperature for more consistent, focused responses
PARAMETER temperature 0.4

# Top-p sampling for controlled diversity
PARAMETER top_p 0.9

# Increase context window for longer conversations
PARAMETER num_ctx 8192

# Stop sequences to control output format
PARAMETER stop "<|end|>"
PARAMETER stop "Human:"
```

### Build Custom Models

Create models from Modelfiles using the create command.

```bash
# Create a custom model from a Modelfile
# The -f flag specifies the Modelfile path
ollama create devops-assistant -f ./Modelfile

# List models to verify creation
ollama list

# Test the custom model
ollama run devops-assistant "How do I set up a Kubernetes deployment with auto-scaling?"
```

### Advanced Modelfile Examples

Create specialized models for different use cases.

```dockerfile
# Modelfile.code-reviewer
# A model optimized for code review tasks
FROM codellama:13b

SYSTEM """
You are a senior code reviewer. Analyze code for:
1. Bugs and logical errors
2. Security vulnerabilities
3. Performance issues
4. Code style and readability
5. Missing error handling

Format your review as:
- CRITICAL: Issues that must be fixed
- WARNING: Issues that should be addressed
- SUGGESTION: Improvements to consider

Be specific and include line references when possible.
"""

# Low temperature for consistent, focused analysis
PARAMETER temperature 0.2

# Higher top_k for more thorough consideration of alternatives
PARAMETER top_k 50

PARAMETER num_ctx 16384
```
```dockerfile
# Modelfile.sql-expert
# A model specialized for SQL and database queries
FROM llama3.2:3b

SYSTEM """
You are an expert database administrator and SQL developer.
You specialize in PostgreSQL, MySQL, and SQLite.

When writing queries:
- Always use parameterized queries to prevent SQL injection
- Include appropriate indexes suggestions
- Optimize for performance
- Add comments explaining complex logic

Format SQL with proper indentation and uppercase keywords.
"""

PARAMETER temperature 0.3
PARAMETER num_ctx 4096
```

Build both models:

```bash
# Create specialized models
ollama create code-reviewer -f Modelfile.code-reviewer
ollama create sql-expert -f Modelfile.sql-expert
```

---

## Managing Models with the API

Perform model management operations programmatically using the API.

### Python Model Manager

A comprehensive class for managing models via the API.

```python
# model_manager.py
# Provides programmatic control over Ollama model operations
# Includes pulling, listing, deleting, and creating models

import requests
import json
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

@dataclass
class ModelInfo:
    """Container for model information."""
    name: str
    size: int
    digest: str
    modified_at: str
    parameter_size: str
    quantization: str
    family: str

    @property
    def size_gb(self) -> float:
        """Return size in gigabytes."""
        return self.size / (1024 ** 3)

class OllamaModelManager:
    """
    Manage Ollama models through the REST API.

    Provides methods for all model management operations including
    pulling, listing, removing, and creating custom models.
    """

    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Initialize the model manager.

        Args:
            base_url: The Ollama server URL (default: http://localhost:11434)
        """
        self.base_url = base_url
        self.session = requests.Session()

    def list_models(self) -> List[ModelInfo]:
        """
        Get all locally available models with detailed information.

        Returns:
            List of ModelInfo objects containing model details
        """
        response = self.session.get(f"{self.base_url}/api/tags")
        response.raise_for_status()

        models = []
        for m in response.json().get("models", []):
            details = m.get("details", {})
            models.append(ModelInfo(
                name=m["name"],
                size=m["size"],
                digest=m["digest"],
                modified_at=m["modified_at"],
                parameter_size=details.get("parameter_size", "unknown"),
                quantization=details.get("quantization_level", "unknown"),
                family=details.get("family", "unknown")
            ))

        return models

    def get_model_info(self, name: str) -> Dict:
        """
        Get detailed information about a specific model.

        Args:
            name: The model name to query

        Returns:
            Dictionary containing complete model information
        """
        response = self.session.post(
            f"{self.base_url}/api/show",
            json={"model": name}
        )
        response.raise_for_status()
        return response.json()

    def pull_model(
        self,
        name: str,
        progress_callback: Optional[Callable[[Dict], None]] = None
    ) -> bool:
        """
        Download a model from the Ollama registry.

        Args:
            name: The model name to pull (e.g., "llama3.2:3b")
            progress_callback: Optional function called with progress updates

        Returns:
            True if pull was successful
        """
        response = self.session.post(
            f"{self.base_url}/api/pull",
            json={"model": name, "stream": True},
            stream=True
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if progress_callback:
                    progress_callback(data)

                # Check for completion or error
                if data.get("status") == "success":
                    return True
                if "error" in data:
                    raise Exception(data["error"])

        return True

    def delete_model(self, name: str) -> bool:
        """
        Remove a model from local storage.

        Args:
            name: The model name to delete

        Returns:
            True if deletion was successful
        """
        response = self.session.delete(
            f"{self.base_url}/api/delete",
            json={"model": name}
        )
        response.raise_for_status()
        return True

    def copy_model(self, source: str, destination: str) -> bool:
        """
        Create a copy of a model with a new name.

        Args:
            source: The source model name
            destination: The new model name

        Returns:
            True if copy was successful
        """
        response = self.session.post(
            f"{self.base_url}/api/copy",
            json={"source": source, "destination": destination}
        )
        response.raise_for_status()
        return True

    def create_model(
        self,
        name: str,
        modelfile: str,
        progress_callback: Optional[Callable[[Dict], None]] = None
    ) -> bool:
        """
        Create a new model from a Modelfile specification.

        Args:
            name: The name for the new model
            modelfile: The Modelfile contents as a string
            progress_callback: Optional function called with progress updates

        Returns:
            True if creation was successful
        """
        response = self.session.post(
            f"{self.base_url}/api/create",
            json={"model": name, "modelfile": modelfile},
            stream=True
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if progress_callback:
                    progress_callback(data)

        return True

    def list_running(self) -> List[Dict]:
        """
        Get models currently loaded in memory.

        Returns:
            List of dictionaries describing running models
        """
        response = self.session.get(f"{self.base_url}/api/ps")
        response.raise_for_status()
        return response.json().get("models", [])

    def unload_model(self, name: str) -> bool:
        """
        Unload a model from memory to free resources.

        Args:
            name: The model name to unload

        Returns:
            True if unload was successful
        """
        # Sending a generate request with keep_alive=0 unloads the model
        response = self.session.post(
            f"{self.base_url}/api/generate",
            json={
                "model": name,
                "prompt": "",
                "keep_alive": 0
            }
        )
        response.raise_for_status()
        return True

def main():
    """Demonstrate model management operations."""
    manager = OllamaModelManager()

    # List all models
    print("=== Installed Models ===")
    for model in manager.list_models():
        print(f"  {model.name}")
        print(f"    Size: {model.size_gb:.2f} GB")
        print(f"    Parameters: {model.parameter_size}")
        print(f"    Quantization: {model.quantization}")
        print()

    # Show running models
    print("=== Running Models ===")
    running = manager.list_running()
    if running:
        for m in running:
            print(f"  {m['name']} - {m['size'] / 1e9:.2f} GB in memory")
    else:
        print("  No models currently loaded")

    # Pull a model with progress display
    print("\n=== Pulling Model ===")
    def show_progress(data):
        status = data.get("status", "")
        if "pulling" in status:
            completed = data.get("completed", 0)
            total = data.get("total", 1)
            percent = (completed / total) * 100 if total > 0 else 0
            print(f"\r  {status}: {percent:.1f}%", end="", flush=True)
        else:
            print(f"\r  {status}                    ")

    # Uncomment to test pulling
    # manager.pull_model("phi3:mini", progress_callback=show_progress)

    # Create a custom model
    print("\n=== Creating Custom Model ===")
    modelfile = '''FROM llama3.2
SYSTEM "You are a helpful coding assistant. Provide clear, well-documented code."
PARAMETER temperature 0.4'''

    # Uncomment to test creation
    # manager.create_model("my-coder", modelfile)
    # print("  Created: my-coder")

if __name__ == "__main__":
    main()
```

---

## Model Storage and Disk Management

Understanding where and how Ollama stores models helps with backup and disk management.

### Storage Locations

Ollama stores models in platform-specific directories.

```bash
# macOS default location
~/.ollama/models/

# Linux default location
~/.ollama/models/

# Windows default location
C:\Users\<username>\.ollama\models\

# Custom location via environment variable
export OLLAMA_MODELS=/custom/path/to/models
```

### Storage Structure

Inspect the storage directory structure.

```bash
# View the directory structure
tree ~/.ollama/models/ -L 2

# Example output:
# ~/.ollama/models/
# ├── blobs/
# │   ├── sha256-1234...
# │   ├── sha256-5678...
# │   └── sha256-abcd...
# └── manifests/
#     └── registry.ollama.ai/
#         └── library/
#             ├── llama3.2/
#             ├── mistral/
#             └── codellama/
```

### Disk Usage Analysis

Monitor and analyze model storage usage.

```bash
# Total Ollama storage size
du -sh ~/.ollama

# Size breakdown by model
for dir in ~/.ollama/models/manifests/registry.ollama.ai/library/*/; do
    model=$(basename "$dir")
    size=$(du -sh "$dir" 2>/dev/null | cut -f1)
    echo "$size    $model"
done | sort -h

# Find largest blob files
ls -lhS ~/.ollama/models/blobs/ | head -10
```

### Moving Model Storage

Relocate models to a different disk or partition.

```bash
# Stop Ollama first
# On macOS: quit the Ollama app
# On Linux: sudo systemctl stop ollama

# Move the models directory
mv ~/.ollama/models /new/location/ollama-models

# Create a symlink to the new location
ln -s /new/location/ollama-models ~/.ollama/models

# Or use the environment variable instead
echo 'export OLLAMA_MODELS=/new/location/ollama-models' >> ~/.bashrc
source ~/.bashrc

# Start Ollama again
ollama serve
```

---

## Model Lifecycle Workflow

A typical workflow for managing models in a development environment.

<svg id="mermaid-1783135958078" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="max-width: 795.69921875px;" viewBox="-8 -8 795.69921875 2156.7578125" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-1783135958078_flowchart-pointEnd" viewBox="0 0 10 10" refX="6" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135958078_flowchart-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135958078_flowchart-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1783135958078_flowchart-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-1783135958078_flowchart-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-1783135958078_flowchart-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><g><g></g><g><path d="M338.113,39L338.113,43.167C338.113,47.333,338.113,55.667,338.179,63.2C338.245,70.734,338.377,77.467,338.443,80.834L338.509,84.201" id="L-A-B-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M287.018,195.022L258.679,209.704C230.34,224.387,173.662,253.752,145.323,273.718C116.984,293.684,116.984,304.251,116.984,309.534L116.984,314.817" id="L-B-C-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M116.984,359.117L116.984,363.284C116.984,367.451,116.984,375.784,116.984,383.234C116.984,390.684,116.984,397.251,116.984,400.534L116.984,403.817" id="L-C-D-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M116.984,448.117L116.984,452.284C116.984,456.451,116.984,464.784,116.984,472.234C116.984,479.684,116.984,486.251,116.984,489.534L116.984,492.817" id="L-D-E-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M372.723,212.508L381.734,224.276C390.746,236.044,408.768,259.581,417.78,280.766C426.791,301.951,426.791,320.784,426.791,337.617C426.791,354.451,426.791,369.284,426.791,384.117C426.791,398.951,426.791,413.784,426.791,428.617C426.791,443.451,426.791,458.284,426.791,473.117C426.791,487.951,426.791,502.784,426.791,517.617C426.791,532.451,426.791,547.284,426.526,559.336C426.261,571.389,425.73,580.66,425.465,585.296L425.2,589.932" id="L-B-F-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M151.461,537.117L158.828,541.284C166.195,545.451,180.928,553.784,213.012,573.206C245.095,592.629,294.528,623.141,319.245,638.397L343.961,653.653" id="L-E-F-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M448.92,778.41L453.382,789.765C457.845,801.12,466.77,823.829,471.233,840.468C475.695,857.106,475.695,867.672,475.695,872.956L475.695,878.239" id="L-F-G-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M475.695,922.539L475.695,928.706C475.695,934.872,475.695,947.206,475.695,958.656C475.695,970.106,475.695,980.672,475.695,985.956L475.695,991.239" id="L-G-H-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M475.695,1035.539L475.695,1039.706C475.695,1043.872,475.695,1052.206,470.885,1060.007C466.074,1067.807,456.453,1075.076,451.642,1078.71L446.832,1082.344" id="L-H-I-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M351.366,744.114L326.311,761.185C301.255,778.256,251.144,812.397,226.089,838.885C201.033,865.372,201.033,884.206,201.033,903.039C201.033,921.872,201.033,940.706,201.033,959.539C201.033,978.372,201.033,997.206,201.033,1014.039C201.033,1030.872,201.033,1045.706,227.973,1058.679C254.912,1071.652,308.791,1082.764,335.731,1088.32L362.671,1093.877" id="L-F-I-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M465.721,1123.139L477.615,1127.539C489.51,1131.939,513.299,1140.739,525.259,1148.506C537.22,1156.273,537.352,1163.006,537.418,1166.373L537.484,1169.74" id="L-I-J-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M469.535,1293.549L422.223,1310.974C374.911,1328.4,280.286,1363.251,226.724,1386.255C173.161,1409.259,160.66,1420.416,154.409,1425.994L148.159,1431.573" id="L-J-K-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M117.05,1435.102L115.373,1428.935C113.695,1422.768,110.34,1410.435,108.662,1382.555C106.984,1354.674,106.984,1311.247,106.984,1269.82C106.984,1228.393,106.984,1188.966,106.984,1161.836C106.984,1134.706,106.984,1119.872,106.984,1105.039C106.984,1090.206,106.984,1075.372,106.984,1060.539C106.984,1045.706,106.984,1030.872,106.984,1014.039C106.984,997.206,106.984,978.372,106.984,959.539C106.984,940.706,106.984,921.872,106.984,903.039C106.984,884.206,106.984,865.372,106.984,831.254C106.984,797.135,106.984,747.732,106.984,700.328C106.984,652.924,106.984,607.521,107.727,581.514C108.47,555.508,109.955,548.898,110.698,545.593L111.44,542.288" id="L-K-E-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M537.588,1361.602L537.505,1367.685C537.421,1373.768,537.255,1385.935,537.171,1397.302C537.088,1408.668,537.088,1419.235,537.088,1424.518L537.088,1429.802" id="L-J-L-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M537.088,1474.102L537.088,1478.268C537.088,1482.435,537.088,1490.768,537.088,1498.218C537.088,1505.668,537.088,1512.235,537.088,1515.518L537.088,1518.802" id="L-L-M-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M537.088,1563.102L537.088,1567.268C537.088,1571.435,537.088,1579.768,537.154,1587.302C537.22,1594.835,537.352,1601.569,537.418,1604.936L537.484,1608.303" id="L-M-N-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M480.612,1744.633L456.427,1760.213C432.243,1775.792,383.874,1806.951,354.595,1837.332C325.315,1867.714,315.123,1897.318,310.028,1912.12L304.932,1926.922" id="L-N-O-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M293.606,1931.934L291.29,1916.296C288.974,1900.659,284.343,1869.384,282.027,1831.913C279.711,1794.441,279.711,1750.773,279.711,1709.105C279.711,1667.438,279.711,1627.77,279.711,1600.519C279.711,1573.268,279.711,1558.435,279.711,1543.602C279.711,1528.768,279.711,1513.935,279.711,1499.102C279.711,1484.268,279.711,1469.435,279.711,1452.602C279.711,1435.768,279.711,1416.935,279.711,1385.805C279.711,1354.674,279.711,1311.247,279.711,1269.82C279.711,1228.393,279.711,1188.966,293.562,1164.756C307.414,1140.546,335.117,1131.553,348.969,1127.056L362.82,1122.559" id="L-O-I-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M591.124,1748.073L611.004,1763.079C630.883,1778.085,670.642,1808.097,690.22,1829.214C709.797,1850.33,709.195,1862.551,708.893,1868.661L708.592,1874.771" id="L-N-P-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M703.875,2028.258L703.792,2034.341C703.708,2040.424,703.542,2052.591,689.453,2064.502C675.365,2076.412,647.356,2088.067,633.351,2093.894L619.346,2099.722" id="L-P-Q-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M512.538,2101.758L495.129,2095.591C477.72,2089.424,442.902,2077.091,425.493,2052.037C408.084,2026.983,408.084,1989.208,408.084,1951.434C408.084,1913.659,408.084,1875.884,408.084,1835.163C408.084,1794.441,408.084,1750.773,408.084,1709.105C408.084,1667.438,408.084,1627.77,419.328,1604.057C430.572,1580.344,453.06,1572.587,464.304,1568.708L475.548,1564.83" id="L-Q-M-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path><path d="M690.666,1888.818L688.831,1880.367C686.997,1871.915,683.327,1855.012,681.493,1824.727C679.658,1794.441,679.658,1750.773,679.658,1709.105C679.658,1667.438,679.658,1627.77,667.152,1604.032C654.646,1580.295,629.634,1572.488,617.128,1568.584L604.622,1564.681" id="L-P-M-0" style="fill:none;" marker-end="url(#mermaid-1783135958078_flowchart-pointEnd)" stroke="currentColor"></path></g><g><g><g transform="translate(0, 0)"></g></g><g transform="translate(116.984375, 283.1171875)"><g transform="translate(-10.7421875, -12)"><foreignObject width="21.484375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">No</div></foreignObject></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g transform="translate(426.791015625, 428.6171875)"><g transform="translate(-13.56640625, -12)"><foreignObject width="27.1328125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Yes</div></foreignObject></g></g><g><g transform="translate(0, 0)"></g></g><g transform="translate(475.6953125, 846.5390625)"><g transform="translate(-13.56640625, -12)"><foreignObject width="27.1328125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Yes</div></foreignObject></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g transform="translate(201.033203125, 959.5390625)"><g transform="translate(-10.7421875, -12)"><foreignObject width="21.484375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">No</div></foreignObject></g></g><g><g transform="translate(0, 0)"></g></g><g transform="translate(185.662109375, 1398.1015625)"><g transform="translate(-10.7421875, -12)"><foreignObject width="21.484375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">No</div></foreignObject></g></g><g><g transform="translate(0, 0)"></g></g><g transform="translate(537.087890625, 1398.1015625)"><g transform="translate(-13.56640625, -12)"><foreignObject width="27.1328125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Yes</div></foreignObject></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g transform="translate(335.505859375, 1838.109375)"><g transform="translate(-13.56640625, -12)"><foreignObject width="27.1328125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Yes</div></foreignObject></g></g><g><g transform="translate(0, 0)"></g></g><g transform="translate(710.400390625, 1838.109375)"><g transform="translate(-10.7421875, -12)"><foreignObject width="21.484375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">No</div></foreignObject></g></g><g transform="translate(703.375, 2064.7578125)"><g transform="translate(-10.7421875, -12)"><foreignObject width="21.484375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">No</div></foreignObject></g></g><g><g transform="translate(0, 0)"></g></g><g transform="translate(679.658203125, 1707.10546875)"><g transform="translate(-13.56640625, -12)"><foreignObject width="27.1328125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Yes</div></foreignObject></g></g></g><g><g id="flowchart-A-42" data-node="true" data-id="A" transform="translate(338.11328125, 19.5)"><rect style="" rx="0" ry="0" x="-73.8984375" y="-19.5" width="147.796875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-66.3984375, -12)"><rect></rect><foreignObject width="132.796875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Identify Use Case</div></foreignObject></g></g><g id="flowchart-B-43" data-node="true" data-id="B" transform="translate(338.11328125, 167.55859375)"><polygon points="78.55859375,0 157.1171875,-78.55859375 78.55859375,-157.1171875 0,-78.55859375" transform="translate(-78.55859375,78.55859375)" style="" fill="none" stroke="currentColor"></polygon><g style="" transform="translate(-51.55859375, -12)"><rect></rect><foreignObject width="103.1171875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Model Exists?</div></foreignObject></g></g><g id="flowchart-C-45" data-node="true" data-id="C" transform="translate(116.984375, 339.6171875)"><rect style="" rx="0" ry="0" x="-90.25" y="-19.5" width="180.5" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-82.75, -12)"><rect></rect><foreignObject width="165.5" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Search Ollama Library</div></foreignObject></g></g><g id="flowchart-D-47" data-node="true" data-id="D" transform="translate(116.984375, 428.6171875)"><rect style="" rx="0" ry="0" x="-102.84375" y="-19.5" width="205.6875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-95.34375, -12)"><rect></rect><foreignObject width="190.6875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Select Appropriate Model</div></foreignObject></g></g><g id="flowchart-E-49" data-node="true" data-id="E" transform="translate(116.984375, 517.6171875)"><rect style="" rx="0" ry="0" x="-46.6328125" y="-19.5" width="93.265625" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-39.1328125, -12)"><rect></rect><foreignObject width="78.265625" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Pull Model</div></foreignObject></g></g><g id="flowchart-F-51" data-node="true" data-id="F" transform="translate(416.791015625, 698.328125)"><polygon points="111.2109375,0 222.421875,-111.2109375 111.2109375,-222.421875 0,-111.2109375" transform="translate(-111.2109375,111.2109375)" style="" fill="none" stroke="currentColor"></polygon><g style="" transform="translate(-84.2109375, -12)"><rect></rect><foreignObject width="168.421875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Needs Customization?</div></foreignObject></g></g><g id="flowchart-G-55" data-node="true" data-id="G" transform="translate(475.6953125, 903.0390625)"><rect style="" rx="0" ry="0" x="-69.3515625" y="-19.5" width="138.703125" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-61.8515625, -12)"><rect></rect><foreignObject width="123.703125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Create Modelfile</div></foreignObject></g></g><g id="flowchart-H-57" data-node="true" data-id="H" transform="translate(475.6953125, 1016.0390625)"><rect style="" rx="0" ry="0" x="-82.80859375" y="-19.5" width="165.6171875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-75.30859375, -12)"><rect></rect><foreignObject width="150.6171875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Build Custom Model</div></foreignObject></g></g><g id="flowchart-I-59" data-node="true" data-id="I" transform="translate(416.791015625, 1105.0390625)"><rect style="" rx="0" ry="0" x="-48.9296875" y="-19.5" width="97.859375" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-41.4296875, -12)"><rect></rect><foreignObject width="82.859375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Test Model</div></foreignObject></g></g><g id="flowchart-J-63" data-node="true" data-id="J" transform="translate(537.087890625, 1267.8203125)"><polygon points="93.28125,0 186.5625,-93.28125 93.28125,-186.5625 0,-93.28125" transform="translate(-93.28125,93.28125)" style="" fill="none" stroke="currentColor"></polygon><g style="" transform="translate(-66.28125, -12)"><rect></rect><foreignObject width="132.5625" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Performance OK?</div></foreignObject></g></g><g id="flowchart-K-65" data-node="true" data-id="K" transform="translate(122.35546875, 1454.6015625)"><rect style="" rx="0" ry="0" x="-122.35546875" y="-19.5" width="244.7109375" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-114.85546875, -12)"><rect></rect><foreignObject width="229.7109375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Try Different Size/Quantization</div></foreignObject></g></g><g id="flowchart-L-69" data-node="true" data-id="L" transform="translate(537.087890625, 1454.6015625)"><rect style="" rx="0" ry="0" x="-86.0859375" y="-19.5" width="172.171875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-78.5859375, -12)"><rect></rect><foreignObject width="157.171875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Deploy to Production</div></foreignObject></g></g><g id="flowchart-M-71" data-node="true" data-id="M" transform="translate(537.087890625, 1543.6015625)"><rect style="" rx="0" ry="0" x="-62.53515625" y="-19.5" width="125.0703125" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-55.03515625, -12)"><rect></rect><foreignObject width="110.0703125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Monitor Usage</div></foreignObject></g></g><g id="flowchart-N-73" data-node="true" data-id="N" transform="translate(537.087890625, 1707.10546875)"><polygon points="94.00390625,0 188.0078125,-94.00390625 94.00390625,-188.0078125 0,-94.00390625" transform="translate(-94.00390625,94.00390625)" style="" fill="none" stroke="currentColor"></polygon><g style="" transform="translate(-67.00390625, -12)"><rect></rect><foreignObject width="134.0078125" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Update Available?</div></foreignObject></g></g><g id="flowchart-O-75" data-node="true" data-id="O" transform="translate(296.494140625, 1951.43359375)"><rect style="" rx="0" ry="0" x="-76.58984375" y="-19.5" width="153.1796875" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-69.08984375, -12)"><rect></rect><foreignObject width="138.1796875" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Pull Latest Version</div></foreignObject></g></g><g id="flowchart-P-79" data-node="true" data-id="P" transform="translate(703.375, 1951.43359375)"><polygon points="76.32421875,0 152.6484375,-76.32421875 76.32421875,-152.6484375 0,-76.32421875" transform="translate(-76.32421875,76.32421875)" style="" fill="none" stroke="currentColor"></polygon><g style="" transform="translate(-49.32421875, -12)"><rect></rect><foreignObject width="98.6484375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Still Needed?</div></foreignObject></g></g><g id="flowchart-Q-81" data-node="true" data-id="Q" transform="translate(567.587890625, 2121.2578125)"><rect style="" rx="0" ry="0" x="-63.171875" y="-19.5" width="126.34375" height="39" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-55.671875, -12)"><rect></rect><foreignObject width="111.34375" height="24"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; white-space: nowrap;">Remove Model</div></foreignObject></g></g></g></g></g></svg>

---

## Best Practices for Model Management

### 1\. Use Specific Tags

Always specify version tags in production to ensure consistency.

```bash
# Development - use latest for experimentation
ollama pull llama3.2

# Production - pin to specific version
ollama pull llama3.2:3b-instruct-q4_K_M
```

### 2\. Monitor Disk Space

Set up alerts before your disk fills up with models.

```bash
#!/bin/bash
# check_ollama_disk.sh
# Alert if Ollama storage exceeds threshold

THRESHOLD_GB=50
CURRENT_GB=$(du -s ~/.ollama 2>/dev/null | awk '{print int($1/1024/1024)}')

if [ "$CURRENT_GB" -gt "$THRESHOLD_GB" ]; then
    echo "WARNING: Ollama storage is ${CURRENT_GB}GB (threshold: ${THRESHOLD_GB}GB)"
    echo "Consider removing unused models with 'ollama rm <model>'"
fi
```

### 3\. Document Custom Models

Keep Modelfiles in version control with your application code.

```bash
# Project structure
my-app/
├── src/
├── models/
│   ├── Modelfile.assistant
│   ├── Modelfile.coder
│   └── Modelfile.reviewer
├── scripts/
│   └── setup_models.sh
└── README.md
```

### 4\. Automate Model Setup

Create setup scripts for new development environments.

```bash
#!/bin/bash
# setup_models.sh
# Sets up all required models for the project

MODELS=(
    "llama3.2:3b"
    "nomic-embed-text"
)

CUSTOM_MODELS=(
    "assistant:Modelfile.assistant"
    "coder:Modelfile.coder"
)

echo "Pulling required models..."
for model in "${MODELS[@]}"; do
    echo "Pulling $model..."
    ollama pull "$model"
done

echo "Creating custom models..."
for entry in "${CUSTOM_MODELS[@]}"; do
    name="${entry%%:*}"
    file="${entry##*:}"
    echo "Creating $name from $file..."
    ollama create "$name" -f "models/$file"
done

echo "Setup complete!"
ollama list
```

### 5\. Regular Cleanup

Schedule periodic cleanup of unused models.

```bash
# Add to crontab for weekly cleanup
# crontab -e
# 0 2 * * 0 /path/to/cleanup_models.sh

#!/bin/bash
# cleanup_models.sh
# Remove models not used in the last 30 days

DAYS_THRESHOLD=30

ollama list | tail -n +2 | while read name id size modified; do
    # Parse the modified date and compare
    # Remove models older than threshold
    echo "Checking: $name (modified: $modified)"
done
```

---

## Troubleshooting Model Issues

### Model Pull Failures

Common issues and solutions when pulling models.

```bash
# Check network connectivity
curl -I https://ollama.com

# Verify disk space
df -h ~/.ollama

# Check for corrupted downloads by re-pulling
ollama rm llama3.2
ollama pull llama3.2

# Use verbose mode for debugging
OLLAMA_DEBUG=1 ollama pull llama3.2
```

### Model Load Failures

Diagnose why a model fails to load.

```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS

# Try a smaller model variant
ollama run llama3.2:1b

# Check GPU availability
nvidia-smi  # NVIDIA GPUs

# Force CPU-only mode by hiding the GPU
# For NVIDIA: CUDA_VISIBLE_DEVICES="-1"
# For AMD:    ROCR_VISIBLE_DEVICES="-1"
CUDA_VISIBLE_DEVICES="-1" ollama run llama3.2
```

### Corrupted Model Recovery

Fix corrupted model installations.

```bash
# Remove the corrupted model completely
ollama rm llama3.2

# Clear any orphaned blobs
# WARNING: Only do this if no other models depend on these blobs

# Re-pull the model fresh
ollama pull llama3.2

# Verify integrity
ollama show llama3.2
```

---

## Conclusion

Effective model management in Ollama involves understanding both the commands and the underlying storage system. Key takeaways:

- **Pull with tags** for consistent, reproducible environments
- **Monitor disk usage** as models can consume significant space
- **Create custom models** using Modelfiles for specialized use cases
- **Use the API** for programmatic model management in applications
- **Automate updates and cleanup** to maintain a healthy model library
- **Document your models** by keeping Modelfiles in version control

With these practices, you can maintain an organized collection of models that serves your development and production needs without wasting resources.

---

*Running AI-powered applications? [OneUptime](https://oneuptime.com/) provides comprehensive monitoring for your infrastructure, including health checks, incident management, and status pages to keep your services reliable.*

![Nawaz Dhandala](https://avatars.githubusercontent.com/nawazdhandala)

@nawazdhandala • Feb 02, 2026 •

Nawaz is building OneUptime with a passion for engineering reliable systems and improving observability.

[GitHub](https://github.com/nawazdhandala)

Technically validated · Jun 08, 2026

### Help improve this post

Every OneUptime blog post is open source. Found a typo, an inaccuracy, or have a clearer way to explain something? Anyone can contribute — your edits make this post better for everyone who reads it next.

[Edit this post on GitHub](https://github.com/oneuptime/blog/tree/master/posts/2026-02-02-ollama-model-management) [Contributing guidelines](https://github.com/oneuptime/blog)