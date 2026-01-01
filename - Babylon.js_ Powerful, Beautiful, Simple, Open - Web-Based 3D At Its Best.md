---
title: "Babylon.js: Powerful, Beautiful, Simple, Open - Web-Based 3D At Its Best"
source: "https://www.babylonjs.com/"
author:
published:
created: 2026-08-13
description: "Babylon.js is one of the world's leading WebGL-based graphics engines. From a new visual scene inspector, best-in-class physically-based rendering, countless performance optimizations, and much more, Babylon.js brings powerful, beautiful, simple, and open 3D to everyone on the web."
---
## Welcome to Babylon.js 9.0

Our mission is to build one of the most powerful, beautiful, simple, and open web rendering engines in the world. Today, web graphics and rendering hit the accelerator with the release of Babylon.js 9.0. It represents a year of new features, optimizations, and performance improvements aimed at helping you create more compelling, interactive web experiences faster than ever.

## Clustered Lighting

When a scene has a lot of lights, per-pixel lighting calculations can get incredibly slow. Babylon.js 9.0 introduces a powerful new Clustered Lighting system that dramatically speeds up lighting calculations by intelligently grouping lights into screen-space tiles and depth slices. At render time, each pixel only calculates lighting from the lights that actually affect it. The result? Scenes with hundreds or even thousands of lights running at buttery smooth frame rates!

[Learn more about Clustered Lighting in Babylon.js](https://aka.ms/babylon9CLDoc)

![A dark scene with dozens of glowing fireflies illuminating stone ruins and vegetation, demonstrating clustered lighting with many light sources](https://www.babylonjs.com/assets/img/clusteredLighting.png) ![A sci-fi corridor with a glowing electronic sign casting colored light onto surrounding metallic walls](https://www.babylonjs.com/assets/img/texturedAreaLights.png)

## Textured Area Lights

Building on the Area Lights introduced in Babylon.js 8.0, area lights in Babylon.js 9.0 now support emission textures! This means you can use any image as a light source for your rectangular area light, enabling effects like stained glass projections, LED panel displays, or cinematic lighting setups, all with physically accurate light emission. An offline texture processing tool is available for production workflows, and a runtime processing option is provided for quick prototyping.

[Learn more about Textured Area Lights in Babylon.js](https://aka.ms/babylon9TALDoc)

## Node Particle Editor

Introducing the Node Particle Editor (NPE), a brand-new visual tool that lets you create complex particle systems using a powerful, non-destructive node graph. If you're familiar with Babylon's Node Material Editor, you'll feel right at home! The NPE gives you complete control over every aspect of your particle systems from emission shapes and sprite sheets to update behaviors and sub-emitters, all through an intuitive drag-and-connect interface.

[Learn more about Node Particle Editor in Babylon.js](https://aka.ms/babylon9NPEDoc)

![A fiery sun rendered entirely with particles, glowing bright orange and yellow against a black background](https://www.babylonjs.com/assets/img/nodeParticleEditor.png) ![Glowing purple and pink particles forming a swirling pattern against a dark purple background](https://www.babylonjs.com/assets/img/particleFlowMaps.png)

## Particle Flow Maps and Attractors

Babylon.js 9.0 introduces Flow Maps, a screen-aligned texture that controls the direction and intensity of forces applied to particles based on their position on the screen. Each pixel in the flow map encodes a 3D direction vector and strength, giving you fine-grained, artistic control over particle movement. Babylon.js 9.0 adds gravity attractors to the particle system toolkit. Attractors can be repositioned and adjusted in real time, making it easy to create dynamic, interactive particle effects like swirling vortexes, magnetic fields, or explosion shockwaves.

[Learn more about Particle Flow Maps in Babylon.js](https://aka.ms/babylon9PartFMDoc)

## Volumetric Lighting

Realistic light shafts streaming through fog, dust, or haze can transform a scene from flat to cinematic. Babylon.js 9.0 makes this easier than ever with a powerful new Volumetric Lighting system. The result is stunningly realistic light scattering with configurable extinction and phase parameters that give you artistic control over how light interacts with the atmosphere. The system supports directional light sources, and takes full advantage of WebGPU compute shaders for optimal performance.

[Learn more about Volumetric Lighting in Babylon.js](https://aka.ms/babylon9vlDoc)

![A dark industrial interior with visible light shafts streaming through openings, creating volumetric god rays](https://www.babylonjs.com/assets/img/volumetricLighting.png) ![The Babylon.js Playground showing a Gaussian splat of a cathedral interior with bright sunlight streaming through arched windows](https://www.babylonjs.com/assets/img/frameGraph.png)

## Frame Graph

One of the most transformative features in Babylon.js 9.0 is the Frame Graph system. Introduced as an alpha feature in 8.0, the Frame Graph is now a fully realized v1 feature that gives you complete, fine-grained control over the entire rendering pipeline. You declare what resources each task needs and produces, and the system intelligently manages texture allocation, reuse, and optimization. This means substantial GPU memory savings and a level of rendering flexibility that was simply not possible before.

[Learn more about Frame Graph in Babylon.js](https://aka.ms/babylon9FGDoc)

## Animation Retargeting

Animation retargeting is a game-changer for anyone working with character animations. New in Babylon.js 9.0, the retargeting system allows you to take an animation created for one character and apply it to a completely different character, even if they have different skeleton structures, bone proportions, or naming conventions. This means you can share an entire library of locomotion, combat, or facial animations across many characters. An interactive Animation Retargeting Tool is also available!

[Learn more about Animation Retargeting in Babylon.js](https://aka.ms/babylon9ARDoc)

![Three different 3D characters sharing the same animation pose, demonstrating animation retargeting across different body types](https://www.babylonjs.com/assets/img/animationRetargeting.png) ![A Gaussian splat capture of an outdoor fire pit scene with red chairs and a cartoon cat character](https://www.babylonjs.com/assets/img/gaussianSplat.png)

## Advanced Gaussian Splat Support

Babylon.js 9.0 takes Gaussian Splatting to the next level. This release brings a host of advanced capabilities including support for multiple file formats (.PLY,.splat,.SPZ, and Self-Organizing Gaussians.SOG/.SOGS), Triangular Splatting for opaque mesh-like rendering, shadow casting support, and the ability to combine multiple Gaussian Splat assets into a single scene with global splat sorting. You can now programmatically create, modify, and download Gaussian Splat data, and each part of a composite splat scene can be independently transformed and animated.

[Learn more about Gaussian Splatting in Babylon.js](https://aka.ms/babylon9GSDoc)

## Babylon.js Editor

The Babylon.js Editor continues to evolve as a powerful desktop application for building Babylon.js experiences. Available on Windows, macOS, and Linux, the Editor provides a full scene editing environment with support for scripting, physics, asset management, and project building, all wrapped in a familiar, intuitive interface. With Babylon.js 9.0, the Editor receives updates and improvements to keep pace with the latest engine features.

[Learn more about Babylon.js Editor](https://aka.ms/babylon9EditorDoc)

![The Babylon.js Editor desktop application showing a dimly lit room scene with asset browser, inspector, and scene hierarchy panels](https://www.babylonjs.com/assets/img/babylonEditor.png) ![A colorful 3D scene with glowing crystals, candles, and floating particles being inspected with the new Inspector v2 overlay](https://www.babylonjs.com/assets/img/inspectorV2.png)

## Inspector v2

Introducing Inspector v2, a ground-up rebuild of Babylon's beloved debugging and inspection tool. The new Inspector features a modern, extensible architecture built on a service-oriented model with full React-based UI components. It supports overlay and inline layout modes, light and dark themes, and is fully extensible through static and dynamic extensions. Developers can now add custom panes, toolbar items, property editors, and debug views, all through a clean, well-documented API.

[Learn more about Inspector v2 in Babylon.js](https://aka.ms/babylon9iv2Doc)

## Babylon Viewer Updates

The Babylon.js Lightweight Viewer, introduced in 8.0, continues to receive enhancements in 9.0. The Viewer makes it easy to embed stunning 3D content on any web page with just a few lines of HTML. This update brings expanded attribute support, new rendering options including SSAO and tone mapping controls, improved environment and skybox configuration, and enhanced animation and interaction controls. Whether you need a quick product showcase or a fully interactive 3D embed, the Viewer has you covered.

[Learn more about Babylon.js Viewer](https://aka.ms/babylon9VDoc)

![A detailed 3D model of a hooded fantasy archer character rendered in the Babylon.js Viewer](https://www.babylonjs.com/assets/img/viewerUpdates.png) ![The Babylon.js Playground with multi-file editing showing TypeScript code tabs and a 3D character model preview](https://www.babylonjs.com/assets/img/playgroundUpdates.png)

## Playground Updates

The Babylon.js Playground, the beloved online sandbox for experimenting with Babylon.js, receives quality-of-life updates in 9.0. With features like CTRL+Space code templates for quickly inserting common code patterns, the ability to host your own snippet server for private and authenticated content, and improved support for external asset loading, the Playground continues to be the fastest way to prototype, share, and learn Babylon.js.

[Learn more about Playground Updates in Babylon.js](https://aka.ms/babylon9PGDoc)

## Large World Rendering

When working with very large world coordinates, 32-bit floating point numbers lose precision, causing visible jittering. Babylon.js 9.0 solves this with a comprehensive Large World Rendering / Floating Origin system. By keeping the active camera conceptually at the world origin and offsetting all geometry and shader uniforms, no matter how far you travel, the values sent to the GPU are always small and precise. The system also integrates with Havok physics through a multi-region architecture.

[Learn more about Large World Rendering in Babylon.js](https://aka.ms/babylon9LWDoc)

![Side-by-side comparison showing jittering artifacts with floating origin off versus smooth rendering with floating origin on](https://www.babylonjs.com/assets/img/largeWorldRendering.png) ![A 3D rendered planet with a dark, textured surface viewed from space against a black background](https://www.babylonjs.com/assets/img/geospatialCamera.png)

## Geospatial Camera

Babylon.js 9.0 introduces the all-new Geospatial Camera, a purpose-built camera designed for orbiting a spherical planet. It provides map-like interactions right out of the box: drag to pan the globe, scroll to zoom toward the cursor, and right-click to tilt. It comes with configurable limits, smooth animated flights via flyToAsync, collision detection, and automatic clip plane adjustment based on altitude.

[Learn more about Geospatial Camera in Babylon.js](https://aka.ms/babylon9GSCDoc)

## 3D Tiles Support

3D Tiles is an open standard created by Cesium and adopted by the Open Geospatial Consortium (OGC) for streaming massive, heterogeneous 3D geospatial datasets. Babylon.js 9.0 brings 3D Tiles support through integration with the NASA/AMMOS 3DTilesRendererJS library, which handles tile set traversal, level-of-detail selection, and tile loading. Paired with the new Geospatial Camera, this opens the door to stunning geospatial web applications.

[Learn more about 3D Tiles in Babylon.js](https://aka.ms/babylon93DTDoc)

![An aerial 3D view of Central Park and surrounding New York City buildings rendered with 3D Tiles geospatial data](https://www.babylonjs.com/assets/img/3dTiles.png) ![A panoramic view of mountain ranges at sunrise with realistic atmospheric haze and light scattering](https://www.babylonjs.com/assets/img/physicallyBasedAtmosphere.png)

## Physically Based Atmosphere

Babylon.js 9.0 introduces a stunning Physically Based Atmosphere addon that provides realistic sky and aerial perspective rendering. Using physically accurate Rayleigh and Mie scattering models, along with ozone absorption and multiple scattering, the atmosphere produces breathtaking sunrises, sunsets, and day-night cycles. It integrates seamlessly with PBR materials and directional lights, and supports customizable scattering parameters to create atmospheres for any planet, from Earth to entirely alien worlds.

[Learn more about Physically Based Atmosphere in Babylon.js](https://aka.ms/babylon9ATMDoc)

## OpenPBR Support

Babylon.js 9.0 begins implementation of OpenPBR, an open standard developed by Autodesk and Adobe that defines an artist-friendly, interoperable material model. OpenPBR is designed so that materials authored with it look consistent across any platform that supports the standard. Babylon.js now maps many of the OpenPBR parameter groups, including Base, Specular, Coat, Thin-film, and more, to the existing PBR material system. This is a significant step toward industry-wide material interoperability and ensures that Babylon.js stays at the forefront of rendering standards.

[Learn more about OpenPBR in Babylon.js](https://aka.ms/babylon9OPBRDoc)

![A glossy dark red sphere with clear coat and specular reflections rendered using the OpenPBR material model](https://www.babylonjs.com/assets/img/openPBR.png) ![A realistic shark model resting on a sandy ocean floor with soft environment-based shadows and underwater lighting](https://www.babylonjs.com/assets/img/dynamicIBLShadows.png)

## Dynamic IBL Shadows

Image-Based Lighting (IBL) has been a cornerstone of Babylon.js rendering for years, and in version 9.0, IBL gets even better with Dynamic IBL Shadows. Building on the IBL Shadow feature first introduced in 8.0 by Adobe, this update brings enhanced, dynamic environment shadows that respond to changes in lighting conditions in real time. Both light and shadow for the scene environment can now be approximated from a source image with greater fidelity and flexibility than ever before.

[Learn more about Dynamic IBL Shadows in Babylon.js](https://aka.ms/babylon9IBLSDoc)

## Signed Distance Field Text

Rendering crisp, scalable text in 3D environments has always been a challenge. Babylon.js 9.0 introduces Signed Distance Field (SDF) text rendering, a technique that produces resolution-independent, beautifully smooth text at any size or zoom level. Unlike traditional bitmap fonts that become blurry or pixelated when scaled, SDF text maintains sharp edges and clean outlines no matter how close you get. This is perfect for in-world UI, labels, signage, HUD elements, and any scenario where readable text needs to exist in 3D space.

[Learn more about SDF Text in Babylon.js](https://aka.ms/babylon9sdfDoc)

![Bright pink text rendered in 3D perspective on a black surface, demonstrating crisp signed distance field text at various depths](https://www.babylonjs.com/assets/img/sdfText.png) ![A grayscale 3D scene with objects highlighted by colored outlines, including a blue-outlined car and other industrial objects](https://www.babylonjs.com/assets/img/outlineRenderer.png)

## Outline Renderer

Babylon.js 9.0 introduces a new Outline Renderer that makes it easy to add stylized outlines to meshes in your scene. Whether you're building a cartoon-shaded world, highlighting selected objects, or creating a technical visualization, the Outline Renderer provides clean, customizable outlines that integrate seamlessly with the rest of the rendering pipeline.

[Learn more about Outline Renderer in Babylon.js](https://aka.ms/babylon9OLDoc)

![A dark industrial scene with a glowing orange light source on the floor near stairs, demonstrating spatial audio positioning](https://www.babylonjs.com/assets/img/audioEngine.png)

## Audio Engine Updates

Sound is a critical part of any immersive experience, and Babylon.js 9.0 continues the evolution of the audio engine that was overhauled in 8.0. This release brings further refinements, expanded features, and improved API ergonomics aligned with modern web-audio standards. The modular audio engine makes it easier than ever to add spatial audio, ambient soundscapes, and interactive sound effects to your Babylon.js experiences.

[Learn more about Audio Engine in Babylon.js](https://aka.ms/babylon9AudioDoc)

## 3MF Exporter

Babylon.js 9.0 brings a new exporter, allowing you to export your scene geometry to the popular 3D printing format 3MF!

[Learn more about 3MF Exporter in Babylon.js](https://aka.ms/babylon93MFdoc)

![Side-by-side comparison of a pirate figurine exported as STL at 28.5 MB versus 3MF at 11.1 MB, showing the same quality at smaller file size](https://www.babylonjs.com/assets/img/3mfExporter.png)

## Just the Tip of the Iceberg

We don't take it lightly when we say that Babylon.js is fully-featured. Dive in to see how far this rabbit hole goes!

[![](https://www.babylonjs.com/assets/img/HexButtonStates.svg)](https://www.babylonjs.com/specifications/)

[Full List of Features](https://www.babylonjs.com/specifications/)## NOTABLE EXPERIENCES

[![](https://www.babylonjs.com/assets/img/moreButtonStates.svg)](https://www.babylonjs.com/community)

[MORE](https://www.babylonjs.com/community)<iframe allow="clipboard-write; web-share" src="chrome-extension://cnjifjpddelmedmihgijeibhnjfabmlf/side-panel.html?context=iframe"></iframe>