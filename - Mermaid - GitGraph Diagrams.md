---
source: "https://mermaid.ai/open-source/syntax/gitgraph.html"
author:
published:
created: 2026-04-13
---
> A Git Graph is a pictorial representation of git commits and git actions(commands) on various branches.

These kind of diagram are particularly helpful to developers and devops teams to share their Git branching strategies. For example, it makes it easier to visualize how git flow works.

Mermaid can render Git diagrams

##### Code:

```
mermaid---
title: Example Git diagram
---
gitGraph
   commit
   commit
   branch develop
   checkout develop
   commit
   commit
   checkout main
   merge develop
   commit
   commit
```

<svg id="mermaid-14" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 475.42498779296875px;" viewBox="-117.42500305175781 -49.79999923706055 475.42498779296875 203.49241638183594" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="350" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="350" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g> <g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 60 68 A 20 20, 0, 0, 0, 80 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 110 88 L 160 88" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 160 88 L 190 88 A 20 20, 0, 0, 0, 210 68 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g><text text-anchor="middle" x="120.28749084472656" y="-25" fill="currentColor">Example Git diagram</text></svg>

In Mermaid, we support the basic git operations like:

- *commit*: Representing a new commit on the current branch.
- *branch*: To create & switch to a new branch, setting it as the current branch.
- *checkout*: To checking out an existing branch and setting it as the current branch.
- *merge*: To merge an existing branch onto the current branch.

With the help of these key git commands, you will be able to draw a gitgraph in Mermaid very easily and quickly. Entity names are often capitalized, although there is no accepted standard on this, and it is not required in Mermaid.

**NOTE**: `checkout` and `switch` can be used interchangeably.

## Syntax

Mermaid syntax for a gitgraph is very straight-forward and simple. It follows a declarative-approach, where each commit is drawn on the timeline in the diagram, in order of its occurrences/presence in code. Basically, it follows the insertion order for each command.

First thing you do is to declare your diagram type using the **gitgraph** keyword. This `gitgraph` keyword, tells Mermaid that you wish to draw a gitgraph, and parse the diagram code accordingly.

Each gitgraph, is initialized with ***main*** branch. So unless you create a different branch, by-default the commits will go to the main branch. This is driven with how git works, where in the beginning you always start with the main branch (formerly called as ***master*** branch). And by-default, `main` branch is set as your ***current branch***.

You make use of ***commit*** keyword to register a commit on the current branch. Let see how this works:

A simple gitgraph showing three commits on the default (***main***) branch:

##### Code:

```
mermaid    gitGraph
       commit
       commit
       commit
```

<svg id="mermaid-64" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 254px;" viewBox="-96 -21.199999809265137 254 85.12606048583984" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="150" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 110 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

If you look closely at the previous example, you can see the default branch `main` along with three commits. Also, notice that by default each commit has been given a unique & random ID. What if you wanted to give your own custom ID to a commit? Yes, it is possible to do that with Mermaid.

### Adding custom commit id

For a given commit you may specify a custom ID at the time of declaring it using the `id` attribute, followed by `:` and your custom value within a `""` quote. For example: `commit id: "your_custom_id"`

Let us see how this works with the help of the following diagram:

##### Code:

```
mermaid    gitGraph
       commit id: "Alpha"
       commit id: "Beta"
       commit id: "Gamma"
```

<svg id="mermaid-77" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 254px;" viewBox="-96 -21.199999809265137 254 76.13492584228516" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="150" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 110 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

In this example, we have given our custom IDs to the commits.

### Modifying commit type

In Mermaid, a commit can be of three type, which render a bit different in the diagram. These types are:

- `NORMAL`: Default commit type. Represented by a solid circle in the diagram
- `REVERSE`: To emphasize a commit as a reverse commit. Represented by a crossed solid circle in the diagram.
- `HIGHLIGHT`: To highlight a particular commit in the diagram. Represented by a filled rectangle in the diagram.

For a given commit you may specify its type at the time of declaring it using the `type` attribute, followed by `:` and the required type option discussed above. For example: `commit type: HIGHLIGHT`

NOTE: If no commit type is specified, `NORMAL` is picked as default.

Let us see how these different commit type look with the help of the following diagram:

##### Code:

```
mermaid    gitGraph
       commit id: "Normal"
       commit
       commit id: "Reverse" type: REVERSE
       commit
       commit id: "Highlight" type: HIGHLIGHT
       commit
```

<svg id="mermaid-113" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 404px;" viewBox="-96 -21.199999809265137 404 85.05155944824219" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="300" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 110 -2" fill="none" stroke="currentColor"></path><path d="M 110 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="-2" r="10" fill="none" stroke="currentColor"></circle><path d="M 105,-7L115,3M105,3L115,-7" fill="none" stroke="currentColor"></path><circle cx="160" cy="-2" r="10" fill="none" stroke="currentColor"></circle><rect x="200" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="204" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

In this example, we have specified different types to each commit. Also, see how we have included both `id` and `type` together at the time of declaring our commits.

### Adding Tags

For a given commit you may decorate it as a **tag**, similar to the concept of tags or release version in git world. You can attach a custom tag at the time of declaring a commit using the `tag` attribute, followed by `:` and your custom value within `""` quote. For example: `commit tag: "your_custom_tag"`

Let us see how this works with the help of the following diagram:

##### Code:

```
mermaid    gitGraph
       commit
       commit id: "Normal" tag: "v1.0.0"
       commit
       commit id: "Reverse" type: REVERSE tag: "RC_1"
       commit
       commit id: "Highlight" type: HIGHLIGHT tag: "8.8.4"
       commit
```

<svg id="mermaid-126" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 454px;" viewBox="-96 -37.20000076293945 454 101.08148956298828" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="350" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 110 -2" fill="none" stroke="currentColor"></path><path d="M 110 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="-2" r="10" fill="none" stroke="currentColor"></circle><path d="M 155,-7L165,3M155,3L165,-7" fill="none" stroke="currentColor"></path><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><rect x="250" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="254" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

In this example, we have given custom tags to the commits. Also, see how we have combined all these attributes in a single commit declaration. You can mix-match these attributes as you like.

### Create a new branch

In Mermaid, in-order to create a new branch, you make use of the `branch` keyword. You also need to provide a name of the new branch. The name has to be unique and cannot be that of an existing branch. A branch name that could be confused for a keyword must be quoted within `""`. Usage examples: `branch develop`, `branch "cherry-pick"`

When Mermaid, reads the `branch` keyword, it creates a new branch and sets it as the current branch. Equivalent to you creating a new branch and checking it out in Git world.

Let see this in an example:

##### Code:

```
mermaid    gitGraph
       commit
       commit
       branch develop
       commit
       commit
       commit
```

<svg id="mermaid-142" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 375.4250183105469px;" viewBox="-117.42500305175781 -21.199999809265137 375.4250183105469 174.7310333251953" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="250" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="250" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 60 68 A 20 20, 0, 0, 0, 80 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 110 88 L 160 88" fill="none" stroke="currentColor"></path><path d="M 160 88 L 210 88" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle></g></svg>

In this example, see how we started with default `main` branch, and pushed two commits on that. Then we created the `develop` branch, and all commits afterwards are put on the `develop` branch as it became the current branch.

### Checking out an existing branch

In Mermaid, in order to switch to an existing branch, you make use of the `checkout` keyword. You also need to provide a name of an existing branch. If no branch is found with the given name, it will result in console error. Usage example: `checkout develop`

When Mermaid, reads the `checkout` keyword, it finds the given branch and sets it as the current branch. Equivalent to checking out a branch in the Git world.

Let see modify our previous example:

##### Code:

```
mermaid    gitGraph
       commit
       commit
       branch develop
       commit
       commit
       commit
       checkout main
       commit
       commit
```

<svg id="mermaid-158" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 475.42498779296875px;" viewBox="-117.42500305175781 -21.199999809265137 475.42498779296875 174.76031494140625" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="350" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="350" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 60 68 A 20 20, 0, 0, 0, 80 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 110 88 L 160 88" fill="none" stroke="currentColor"></path><path d="M 160 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

In this example, see how we started with default `main` branch, and pushed two commits on that. Then we created the `develop` branch, and all three commits afterwards are put on the `develop` branch as it became the current branch. After this we made use of the `checkout` keyword to set the current branch as `main`, and all commit that follow are registered against the current branch, i.e. `main`.

### Merging two branches

In Mermaid, in order to merge or join to an existing branch, you make use of the `merge` keyword. You also need to provide the name of an existing branch to merge from. If no branch is found with the given name, it will result in console error. Also, you can only merge two separate branches, and cannot merge a branch with itself. In such case an error is throw.

Usage example: `merge develop`

When Mermaid, reads the `merge` keyword, it finds the given branch and its head commit (the last commit on that branch), and joins it with the head commit on the **current branch**. Each merge results in a ***merge commit***, represented in the diagram with **filled double circle**.

Let us modify our previous example to merge our two branches:

##### Code:

```
mermaid    gitGraph
       commit
       commit
       branch develop
       commit
       commit
       commit
       checkout main
       commit
       commit
       merge develop
       commit
       commit
```

<svg id="mermaid-177" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 625.4249877929688px;" viewBox="-117.42500305175781 -21.199999809265137 625.4249877929688 174.79025268554688" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="500" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="500" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 60 68 A 20 20, 0, 0, 0, 80 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 110 88 L 160 88" fill="none" stroke="currentColor"></path><path d="M 160 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 210 88 L 340 88 A 20 20, 0, 0, 0, 360 68 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 410 -2" fill="none" stroke="currentColor"></path><path d="M 410 -2 L 460 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="410" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

In this example, see how we started with default `main` branch, and pushed two commits on that. Then we created the `develop` branch, and all three commits afterwards are put on the `develop` branch as it became the current branch. After this we made use of the `checkout` keyword to set the current branch as `main`, and all commits that follow are registered against the current branch, i.e. `main`. After this we merge the `develop` branch onto the current branch `main`, resulting in a merge commit. Since the current branch at this point is still `main`, the last two commits are registered against that.

You can also decorate your merge with similar attributes as you did for the commit using:

- `id` --> To override the default ID with custom ID
- `tag` --> To add a custom tag to your merge commit
- `type` --> To override the default shape of merge commit. Here you can use other commit type mentioned earlier.

And you can choose to use none, some or all of these attributes together. For example: `merge develop id: "my_custom_id" tag: "my_custom_tag" type: REVERSE`

Let us see how this works with the help of the following diagram:

##### Code:

```
mermaid    gitGraph
       commit id: "1"
       commit id: "2"
       branch nice_feature
       checkout nice_feature
       commit id: "3"
       checkout main
       commit id: "4"
       checkout nice_feature
       branch very_nice_feature
       checkout very_nice_feature
       commit id: "5"
       checkout main
       commit id: "6"
       checkout nice_feature
       commit id: "7"
       checkout main
       merge nice_feature id: "customID" tag: "customTag" type: REVERSE
       checkout very_nice_feature
       commit id: "8"
       checkout main
       commit id: "9"
```

<svg id="mermaid-207" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 700.3578491210938px;" viewBox="-192.35781860351562 -37.20000076293945 700.3578491210938 252.2866973876953" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="500" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="500" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-125.49531555175781" y="0.8000001907348633" width="109.49531555175781" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-135.4953155517578, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">nice_feature</tspan></text></g></g> <line x1="0" y1="178" x2="500" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-165.35781860351562" y="0.8000001907348633" width="149.35781860351562" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-175.35781860351562, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">very_nice_feature</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 60 68 A 20 20, 0, 0, 0, 80 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 110 158 A 20 20, 0, 0, 0, 130 178 L 210 178" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 310 88" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 310 88 L 340 88 A 20 20, 0, 0, 0, 360 68 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 210 178 L 410 178" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 460 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><path d="M 355,-7L365,3M355,3L365,-7" fill="none" stroke="currentColor"></path><circle cx="410" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

### Cherry Pick commit from another branch

Similar to how 'git' allows you to cherry-pick a commit from **another branch** onto the **current** branch, Mermaid also supports this functionality. You can also cherry-pick a commit from another branch using the `cherry-pick` keyword.

To use the `cherry-pick` keyword, you must specify the id using the `id` attribute, followed by `:` and your desired commit id within a `""` quote. For example:

`cherry-pick id: "your_custom_id"`

Here, a new commit representing the cherry-pick is created on the current branch, and is visually highlighted in the diagram with a **cherry** and a tag depicting the commit id from which it is cherry-picked from.

A few important rules to note here are:

1. You need to provide the `id` for an existing commit to be cherry-picked. If given commit id does not exist it will result in an error. For this, make use of the `commit id:$value` format of declaring commits. See the examples from above.
2. The given commit must not exist on the current branch. The cherry-picked commit must always be a different branch than the current branch.
3. Current branch must have at least one commit, before you can cherry-pick, otherwise it will cause an error is throw.
4. When cherry-picking a merge commit, providing a parent commit ID is mandatory. If the parent attribute is omitted or an invalid parent commit ID is provided, an error will be thrown.
5. The specified parent commit must be an immediate parent of the merge commit being cherry-picked.

Let see an example:

##### Code:

```
mermaid    gitGraph
        commit id: "ZERO"
        branch develop
        branch release
        commit id:"A"
        checkout main
        commit id:"ONE"
        checkout develop
        commit id:"B"
        checkout main
        merge develop id:"MERGE"
        commit id:"TWO"
        checkout release
        cherry-pick id:"MERGE" parent:"B"
        commit id:"THREE"
        checkout develop
        commit id:"C"
```

<svg id="mermaid-256" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 575.4249877929688px;" viewBox="-117.42500305175781 -21.199999809265137 575.4249877929688 253.1576690673828" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="450" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="450" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="178" x2="450" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-86.07343673706055" y="0.8000001907348633" width="70.07343673706055" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-96.07343673706055, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">release</tspan></text></g></g></g><g><path d="M 10 -2 L 10 158 A 20 20, 0, 0, 0, 30 178 L 60 178" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 110 -2" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 160 88" fill="none" stroke="currentColor"></path><path d="M 110 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 160 88 L 190 88 A 20 20, 0, 0, 0, 210 68 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 60 178 L 310 178" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 210 158 A 20 20, 0, 0, 0, 230 178 L 310 178" fill="none" stroke="currentColor"></path><path d="M 310 178 L 360 178" fill="none" stroke="currentColor"></path><path d="M 160 88 L 410 88" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="307" cy="180" r="2.75" fill="#fff"></circle><circle cx="313" cy="180" r="2.75" fill="#fff"></circle><line x1="313" y1="179" x2="310" y2="173" stroke="#fff"></line><line x1="307" y1="179" x2="310" y2="173" stroke="#fff"></line><circle cx="360" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="410" cy="88" r="10" fill="none" stroke="currentColor"></circle></g></svg>

## GitGraph specific configuration options

In Mermaid, you have the option to configure the gitgraph diagram. You can configure the following options:

- `showBranches`: Boolean, default is `true`. If set to `false`, the branches are not shown in the diagram.
- `showCommitLabel`: Boolean, default is `true`. If set to `false`, the commit labels are not shown in the diagram.
- `mainBranchName`: String, default is `main`. The name of the default/root branch.
- `mainBranchOrder`: Position of the main branch in the list of branches. default is `0`, meaning, by default `main` branch is the first in the order.
- `parallelCommits`: Boolean, default is `false`. If set to `true`, commits x distance away from the parent are shown at the same level in the diagram.

Let's look at them one by one.

## Hiding Branch names and lines

Sometimes you may want to hide the branch names and lines from the diagram. You can do this by using the `showBranches` keyword. By default its value is `true`. You can set it to `false` using directives.

Usage example:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'base'
  gitGraph:
    showBranches: false
---
      gitGraph
        commit
        branch hotfix
        checkout hotfix
        commit
        branch develop
        checkout develop
        commit id:"ash" tag:"abc"
        branch featureB
        checkout featureB
        commit type:HIGHLIGHT
        checkout main
        checkout hotfix
        commit type:NORMAL
        checkout develop
        commit type:REVERSE
        checkout featureB
        commit
        checkout main
        merge hotfix
        checkout featureB
        commit
        checkout develop
        branch featureA
        commit
        checkout develop
        merge hotfix
        checkout featureA
        commit
        checkout featureB
        commit
        checkout develop
        merge featureA
        branch release
        checkout release
        commit
        checkout main
        commit
        checkout release
        merge main
        checkout develop
        merge release
```

## Commit labels Layout: Rotated or Horizontal

Mermaid supports two types of commit labels layout. The default layout is **rotated**, which means the labels are placed below the commit circle, rotated at 45 degrees for better readability. This is particularly useful for commits with long labels.

The other option is **horizontal**, which means the labels are placed below the commit circle centred horizontally, and are not rotated. This is particularly useful for commits with short labels.

You can change the layout of the commit labels by using the `rotateCommitLabel` keyword in the directive. It defaults to `true`, which means the commit labels are rotated.

Usage example: Rotated commit labels

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'base'
  gitGraph:
    rotateCommitLabel: true
---
gitGraph
  commit id: "feat(api): ..."
  commit id: "a"
  commit id: "b"
  commit id: "fix(client): .extra long label.."
  branch c2
  commit id: "feat(modules): ..."
  commit id: "test(client): ..."
  checkout main
  commit id: "fix(api): ..."
  commit id: "ci: ..."
  branch b1
  commit
  branch b2
  commit
```

<svg id="mermaid-318" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 604px;" viewBox="-96 -21.199999809265137 604 354.23541259765625" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-318-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="hsl(40.5882352941, 60%, 83.3333333333%)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(-79.4117647059, 60%, 83.3333333333%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="500" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="500" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-50.3125" y="0.8000001907348633" width="34.3125" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-60.3125, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">c2</tspan></text></g></g> <line x1="0" y1="178" x2="500" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-51.3125" y="0.8000001907348633" width="35.3125" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-61.3125, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">b1</tspan></text></g></g> <line x1="0" y1="268" x2="500" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-51.3125" y="0.8000001907348633" width="35.3125" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-61.3125, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">b2</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 110 -2" fill="none" stroke="currentColor"></path><path d="M 110 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 160 68 A 20 20, 0, 0, 0, 180 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 210 88 L 260 88" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 360 158 A 20 20, 0, 0, 0, 380 178 L 410 178" fill="none" stroke="currentColor"></path><path d="M 410 178 L 410 248 A 20 20, 0, 0, 0, 430 268 L 460 268" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="410" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="268" r="10" fill="none" stroke="currentColor"></circle></g></svg>

Usage example: Horizontal commit labels

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'base'
  gitGraph:
    rotateCommitLabel: false
---
gitGraph
  commit id: "feat(api): ..."
  commit id: "a"
  commit id: "b"
  commit id: "fix(client): .extra long label.."
  branch c2
  commit id: "feat(modules): ..."
  commit id: "test(client): ..."
  checkout main
  commit id: "fix(api): ..."
  commit id: "ci: ..."
  branch b1
  commit
  branch b2
  commit
```

<svg id="mermaid-322" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 574px;" viewBox="-66 -21.199999809265137 574 206.6999969482422" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-322-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="hsl(40.5882352941, 60%, 83.3333333333%)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(-79.4117647059, 60%, 83.3333333333%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="500" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-39" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-49, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="48" x2="500" y2="48" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-20.3125" y="0.8000001907348633" width="34.3125" height="22.399999618530273" transform="translate(-19, 36)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-30.3125, 36.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">c2</tspan></text></g></g> <line x1="0" y1="98" x2="500" y2="98" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-21.3125" y="0.8000001907348633" width="35.3125" height="22.399999618530273" transform="translate(-19, 86)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-31.3125, 86.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">b1</tspan></text></g></g> <line x1="0" y1="148" x2="500" y2="148" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-21.3125" y="0.8000001907348633" width="35.3125" height="22.399999618530273" transform="translate(-19, 136)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-31.3125, 136.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">b2</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 110 -2" fill="none" stroke="currentColor"></path><path d="M 110 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 160 28 A 20 20, 0, 0, 0, 180 48 L 210 48" fill="none" stroke="currentColor"></path><path d="M 210 48 L 260 48" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 360 78 A 20 20, 0, 0, 0, 380 98 L 410 98" fill="none" stroke="currentColor"></path><path d="M 410 98 L 410 128 A 20 20, 0, 0, 0, 430 148 L 460 148" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="48" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="48" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="410" cy="98" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="148" r="10" fill="none" stroke="currentColor"></circle></g></svg>

## Hiding commit labels

Sometimes you may want to hide the commit labels from the diagram. You can do this by using the `showCommitLabel` keyword. By default its value is `true`. You can set it to `false` using directives.

Usage example:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'base'
  gitGraph:
    showBranches: false
    showCommitLabel: false
---
      gitGraph
        commit
        branch hotfix
        checkout hotfix
        commit
        branch develop
        checkout develop
        commit id:"ash"
        branch featureB
        checkout featureB
        commit type:HIGHLIGHT
        checkout main
        checkout hotfix
        commit type:NORMAL
        checkout develop
        commit type:REVERSE
        checkout featureB
        commit
        checkout main
        merge hotfix
        checkout featureB
        commit
        checkout develop
        branch featureA
        commit
        checkout develop
        merge hotfix
        checkout featureA
        commit
        checkout featureB
        commit
        checkout develop
        merge featureA
        branch release
        checkout release
        commit
        checkout main
        commit
        checkout release
        merge main
        checkout develop
        merge release
```

## Customizing main branch name

Sometimes you may want to customize the name of the main/default branch. You can do this by using the `mainBranchName` keyword. By default its value is `main`. You can set it to any string using directives.

Usage example:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'base'
  gitGraph:
    showBranches: true
    showCommitLabel: true
    mainBranchName: 'MetroLine1'
---
      gitGraph
        commit id:"NewYork"
        commit id:"Dallas"
        branch MetroLine2
        commit id:"LosAngeles"
        commit id:"Chicago"
        commit id:"Houston"
        branch MetroLine3
        commit id:"Phoenix"
        commit type: HIGHLIGHT id:"Denver"
        commit id:"Boston"
        checkout MetroLine1
        commit id:"Atlanta"
        merge MetroLine3
        commit id:"Miami"
        commit id:"Washington"
        merge MetroLine2 tag:"MY JUNCTION"
        commit id:"Boston"
        commit id:"Detroit"
        commit type:REVERSE id:"SanFrancisco"
```

<svg id="mermaid-342" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 899.5499877929688px;" viewBox="-141.5500030517578 -37.20000076293945 899.5499877929688 272.8901062011719" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-342-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="hsl(40.5882352941, 60%, 83.3333333333%)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(-79.4117647059, 60%, 83.3333333333%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="750" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-114.55000305175781" y="0.8000001907348633" width="98.55000305175781" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-124.55000305175781, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">MetroLine1</tspan></text></g></g> <line x1="0" y1="88" x2="750" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-114.55000305175781" y="0.8000001907348633" width="98.55000305175781" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-124.55000305175781, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">MetroLine2</tspan></text></g></g> <line x1="0" y1="178" x2="750" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-114.55000305175781" y="0.8000001907348633" width="98.55000305175781" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-124.55000305175781, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">MetroLine3</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 60 68 A 20 20, 0, 0, 0, 80 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 110 88 L 160 88" fill="none" stroke="currentColor"></path><path d="M 160 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 210 88 L 210 158 A 20 20, 0, 0, 0, 230 178 L 260 178" fill="none" stroke="currentColor"></path><path d="M 260 178 L 310 178" fill="none" stroke="currentColor"></path><path d="M 560 -2 L 610 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 410 -2" fill="none" stroke="currentColor"></path><path d="M 610 -2 L 410 -2" fill="none" stroke="currentColor"></path><path d="M 410 -2 L 460 -2" fill="none" stroke="currentColor"></path><path d="M 460 -2 L 510 -2" fill="none" stroke="currentColor"></path><path d="M 510 -2 L 560 -2" fill="none" stroke="currentColor"></path><path d="M 210 88 L 540 88 A 20 20, 0, 0, 0, 560 68 L 560 -2" fill="none" stroke="currentColor"></path><path d="M 610 -2 L 660 -2" fill="none" stroke="currentColor"></path><path d="M 660 -2 L 710 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="178" r="10" fill="none" stroke="currentColor"></circle><rect x="300" y="168" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="304" y="172" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="410" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="410" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="460" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="560" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="560" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="610" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="710" cy="-2" r="10" fill="none" stroke="currentColor"></circle><path d="M 705,-7L715,3M705,3L715,-7" fill="none" stroke="currentColor"></path></g></svg>

Look at the imaginary railroad map created using Mermaid. Here, we have changed the default main branch name to `MetroLine1`.

## Customizing branch ordering

In Mermaid, by default the branches are shown in the order of their definition or appearance in the diagram code.

Sometimes you may want to customize the order of the branches. You can do this by using the `order` keyword next the branch definition. You can set it to a positive number.

Mermaid follows the given precedence order of the `order` keyword.

- Main branch is always shown first as it has default order value of `0`. (unless its order is modified and changed from `0` using the `mainBranchOrder` keyword in the config)
- Next, All branches without an `order` are shown in the order of their appearance in the diagram code.
- Next, All branches with an `order` are shown in the order of their `order` value.

To fully control the order of all the branches, you must define `order` for all the branches.

Usage example:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'base'
  gitGraph:
    showBranches: true
    showCommitLabel: true
---
      gitGraph
      commit
      branch test1 order: 3
      branch test2 order: 2
      branch test3 order: 1
```

<svg id="mermaid-381" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 155.28750610351562px;" viewBox="-97.2874984741211 -21.199999809265137 155.28750610351562 308.3999938964844" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-381-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="hsl(40.5882352941, 60%, 83.3333333333%)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(-79.4117647059, 60%, 83.3333333333%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="50" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="50" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-70.28750228881836" y="0.8000001907348633" width="54.28750228881836" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-80.28750228881836, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">test3</tspan></text></g></g> <line x1="0" y1="178" x2="50" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-70.28750228881836" y="0.8000001907348633" width="54.28750228881836" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-80.28750228881836, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">test2</tspan></text></g></g> <line x1="0" y1="268" x2="50" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-70.28750228881836" y="0.8000001907348633" width="54.28750228881836" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-80.28750228881836, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">test1</tspan></text></g></g></g><g></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

Look at the diagram, all the branches are following the order defined.

Usage example:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'base'
  gitGraph:
    showBranches: true
    showCommitLabel: true
    mainBranchOrder: 2
---
      gitGraph
      commit
      branch test1 order: 3
      branch test2
      branch test3
      branch test4 order: 1
```

<svg id="mermaid-388" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 155.69064331054688px;" viewBox="-97.69062805175781 -21.199999809265137 155.69064331054688 398.3999938964844" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-388-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="hsl(40.5882352941, 60%, 83.3333333333%)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(-79.4117647059, 60%, 83.3333333333%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="50" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-70.28750228881836" y="0.8000001907348633" width="54.28750228881836" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-80.28750228881836, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">test2</tspan></text></g></g> <line x1="0" y1="88" x2="50" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-70.28750228881836" y="0.8000001907348633" width="54.28750228881836" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-80.28750228881836, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">test3</tspan></text></g></g> <line x1="0" y1="178" x2="50" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-70.69062423706055" y="0.8000001907348633" width="54.69062423706055" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-80.69062423706055, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">test4</tspan></text></g></g> <line x1="0" y1="268" x2="50" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="358" x2="50" y2="358" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-70.28750228881836" y="0.8000001907348633" width="54.28750228881836" height="22.399999618530273" transform="translate(-19, 346)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-80.28750228881836, 346.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">test1</tspan></text></g></g></g><g></g><g><circle cx="10" cy="268" r="10" fill="none" stroke="currentColor"></circle></g></svg>

Look at the diagram, here, all the branches without a specified order are drawn in their order of definition. Then, `test4` branch is drawn because the order of `1`. Then, `main` branch is drawn because the order of `2`. And, lastly `test1` is drawn because the order of `3`.

NOTE: Because we have overridden the `mainBranchOrder` to `2`, the `main` branch is not drawn in the beginning, instead follows the ordering.

Here, we have changed the default main branch name to `MetroLine1`.

## Orientation (v10.3.0+)

Mermaid supports three graph orientations: **Left-to-Right** (default), **Top-to-Bottom**, and **Bottom-to-Top**.

You can set this with either `LR:` (for [**Left-to-Right**](#left-to-right-default-lr)), `TB:` (for [**Top-to-Bottom**](#top-to-bottom-tb)) or `BT:` (for [**Bottom-to-Top**](#bottom-to-top-bt)) after `gitGraph`.

### Left to Right (default, LR:)

In Mermaid, the default orientation is for commits to run from left to right and for branches to be stacked on top of one another.

However, you can set this explicitly with `LR:` after `gitGraph`.

Usage example:

##### Code:

```
mermaid    gitGraph LR:
       commit
       commit
       branch develop
       commit
       commit
       checkout main
       commit
       commit
       merge develop
       commit
       commit
```

<svg id="mermaid-419" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 575.4249877929688px;" viewBox="-117.42500305175781 -21.199999809265137 575.4249877929688 174.98043823242188" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="450" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="450" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g><g><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 60 68 A 20 20, 0, 0, 0, 80 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 110 88 L 160 88" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 160 88 L 290 88 A 20 20, 0, 0, 0, 310 68 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 410 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="410" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

### Top to Bottom (TB:)

In `TB` (**Top-to-Bottom**) orientation, the commits run from top to bottom of the graph and branches are arranged side-by-side.

To orient the graph this way, you need to add `TB:` after gitGraph.

Usage example:

##### Code:

```
mermaid    gitGraph TB:
       commit
       commit
       branch develop
       commit
       commit
       checkout main
       commit
       commit
       merge develop
       commit
       commit
```

<svg id="mermaid-432" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 216.357421875px;" viewBox="-64.6449203491211 -8 216.357421875 506.7262268066406" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="30" x2="0" y2="480" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-27.5" y="0" width="53" height="22.399999618530273" fill="none" stroke="currentColor"></rect><g><g transform="translate(-22.5, 0)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="107.5" y1="30" x2="107.5" y2="480" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="69.28750038146973" y="0" width="74.42499923706055" height="22.399999618530273" fill="none" stroke="currentColor"></rect><g><g transform="translate(74.28750038146973, 0)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g><g><path d="M 0 40 L 0 90" fill="none" stroke="currentColor"></path><path d="M 0 90 L 87.5 90 A 20 20, 0, 0, 1, 107.5 110 L 107.5 140" fill="none" stroke="currentColor"></path><path d="M 107.5 140 L 107.5 190" fill="none" stroke="currentColor"></path><path d="M 0 90 L 0 240" fill="none" stroke="currentColor"></path><path d="M 0 240 L 0 290" fill="none" stroke="currentColor"></path><path d="M 0 290 L 0 340" fill="none" stroke="currentColor"></path><path d="M 107.5 190 L 107.5 320 A 20 20, 0, 0, 1, 87.5 340 L 0 340" fill="none" stroke="currentColor"></path><path d="M 0 340 L 0 390" fill="none" stroke="currentColor"></path><path d="M 0 390 L 0 440" fill="none" stroke="currentColor"></path></g><g><circle cx="0" cy="40" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="90" r="10" fill="none" stroke="currentColor"></circle><circle cx="107.5" cy="140" r="10" fill="none" stroke="currentColor"></circle><circle cx="107.5" cy="190" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="240" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="290" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="340" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="340" r="6" fill="none" stroke="currentColor"></circle><circle cx="0" cy="390" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="440" r="10" fill="none" stroke="currentColor"></circle></g></svg>

### Bottom to Top (BT:) (v11.0.0+)

In `BT` (**Bottom-to-Top**) orientation, the commits run from bottom to top of the graph and branches are arranged side-by-side.

To orient the graph this way, you need to add `BT:` after gitGraph.

Usage example:

##### Code:

```
mermaid    gitGraph BT:
       commit
       commit
       branch develop
       commit
       commit
       checkout main
       commit
       commit
       merge develop
       commit
       commit
```

<svg id="mermaid-445" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 215.38430786132812px;" viewBox="-63.671817779541016 22 215.38430786132812 488.3999938964844" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="480" x2="0" y2="30" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-27.5" y="480" width="53" height="22.399999618530273" fill="none" stroke="currentColor"></rect><g><g transform="translate(-22.5, 480)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="107.5" y1="480" x2="107.5" y2="30" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="69.28750038146973" y="480" width="74.42499923706055" height="22.399999618530273" fill="none" stroke="currentColor"></rect><g><g transform="translate(74.28750038146973, 480)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g><g><path d="M 0 440 L 0 390" fill="none" stroke="currentColor"></path><path d="M 0 390 L 87.5 390 A 20 20, 0, 0, 0, 107.5 370 L 107.5 340" fill="none" stroke="currentColor"></path><path d="M 107.5 340 L 107.5 290" fill="none" stroke="currentColor"></path><path d="M 0 390 L 0 240" fill="none" stroke="currentColor"></path><path d="M 0 240 L 0 190" fill="none" stroke="currentColor"></path><path d="M 0 190 L 0 140" fill="none" stroke="currentColor"></path><path d="M 107.5 290 L 107.5 160 A 20 20, 0, 0, 0, 87.5 140 L 0 140" fill="none" stroke="currentColor"></path><path d="M 0 140 L 0 90" fill="none" stroke="currentColor"></path><path d="M 0 90 L 0 40" fill="none" stroke="currentColor"></path></g><g><circle cx="0" cy="40" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="90" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="140" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="140" r="6" fill="none" stroke="currentColor"></circle><circle cx="0" cy="190" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="240" r="10" fill="none" stroke="currentColor"></circle><circle cx="107.5" cy="290" r="10" fill="none" stroke="currentColor"></circle><circle cx="107.5" cy="340" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="390" r="10" fill="none" stroke="currentColor"></circle><circle cx="0" cy="440" r="10" fill="none" stroke="currentColor"></circle></g></svg>

## Parallel commits (v10.8.0+)

Commits in Mermaid display temporal information in gitgraph by default. For example if two commits are one commit away from its parent, the commit that was made earlier is rendered closer to its parent. You can turn this off by enabling the `parallelCommits` flag.

### Temporal Commits (default, parallelCommits: false)

##### Code:

```
mermaid---
config:
  gitGraph:
    parallelCommits: false
---
gitGraph:
  commit
  branch develop
  commit
  commit
  checkout main
  commit
  commit
```

<svg id="mermaid-455" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 375.4250183105469px;" viewBox="-117.42500305175781 -21.199999809265137 375.4250183105469 174.2997589111328" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="250" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="250" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="160" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

### Parallel commits (parallelCommits: true)

##### Code:

```
mermaid---
config:
  gitGraph:
    parallelCommits: true
---
gitGraph:
  commit
  branch develop
  commit
  commit
  checkout main
  commit
  commit
```

<svg id="mermaid-459" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 275.4250183105469px;" viewBox="-117.42500305175781 -21.199999809265137 275.4250183105469 174.4385986328125" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="150" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="150" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 60 -2" fill="none" stroke="currentColor"></path><path d="M 60 -2 L 110 -2" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="-2" r="10" fill="none" stroke="currentColor"></circle></g></svg>

## Themes

Mermaid supports a bunch of pre-defined themes which you can use to find the right one for you. PS: you can actually override an existing theme's variable to get your own custom theme going. Learn more about [theming your diagram](https://mermaid.ai/open-source/config/theming.html).

The following are the different pre-defined theme options:

- `base`
- `forest`
- `dark`
- `default`
- `neutral`

**NOTE**: To change theme you can either use the `initialize` call or *directives*. Learn more about [directives](https://mermaid.ai/open-source/config/directives.html) Let's put them to use, and see how our sample diagram looks in different themes:

### Base Theme

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'base'
---
      gitGraph
        commit
        branch hotfix
        checkout hotfix
        commit
        branch develop
        checkout develop
        commit id:"ash" tag:"abc"
        branch featureB
        checkout featureB
        commit type:HIGHLIGHT
        checkout main
        checkout hotfix
        commit type:NORMAL
        checkout develop
        commit type:REVERSE
        checkout featureB
        commit
        checkout main
        merge hotfix
        checkout featureB
        commit
        checkout develop
        branch featureA
        commit
        checkout develop
        merge hotfix
        checkout featureA
        commit
        checkout featureB
        commit
        checkout develop
        merge featureA
        branch release
        checkout release
        commit
        checkout main
        commit
        checkout release
        merge main
        checkout develop
        merge release
```

<svg id="mermaid-502" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1032.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 1032.4781494140625 538.20751953125" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-502-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="hsl(40.5882352941, 60%, 83.3333333333%)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(-79.4117647059, 60%, 83.3333333333%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="900" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="900" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-76.94843673706055" y="0.8000001907348633" width="60.94843673706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-86.94843673706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">hotfix</tspan></text></g></g> <line x1="0" y1="178" x2="900" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="268" x2="900" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-96.13750076293945" y="0.8000001907348633" width="80.13750076293945" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-106.13750076293945, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureB</tspan></text></g></g> <line x1="0" y1="358" x2="900" y2="358" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 346)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 346.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g> <line x1="0" y1="448" x2="900" y2="448" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-86.07343673706055" y="0.8000001907348633" width="70.07343673706055" height="22.399999618530273" transform="translate(-19, 436)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-96.07343673706055, 436.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">release</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 60 158 A 20 20, 0, 0, 0, 80 178 L 110 178" fill="none" stroke="currentColor"></path><path d="M 110 178 L 110 248 A 20 20, 0, 0, 0, 130 268 L 160 268" fill="none" stroke="currentColor"></path><path d="M 60 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 110 178 L 260 178" fill="none" stroke="currentColor"></path><path d="M 160 268 L 310 268" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 210 88 L 340 88 A 20 20, 0, 0, 0, 360 68 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 310 268 L 410 268" fill="none" stroke="currentColor"></path><path d="M 260 178 L 260 338 A 20 20, 0, 0, 0, 280 358 L 460 358" fill="none" stroke="currentColor"></path><path d="M 260 178 L 510 178" fill="none" stroke="currentColor"></path><path d="M 210 88 L 210 123 A 10 10, 0, 0, 0, 220 133 L 500 133 A 10 10, 0, 0, 1, 510 143 L 510 178" fill="none" stroke="currentColor"></path><path d="M 460 358 L 560 358" fill="none" stroke="currentColor"></path><path d="M 410 268 L 610 268" fill="none" stroke="currentColor"></path><path d="M 510 178 L 660 178" fill="none" stroke="currentColor"></path><path d="M 560 358 L 640 358 A 20 20, 0, 0, 0, 660 338 L 660 178" fill="none" stroke="currentColor"></path><path d="M 660 178 L 660 428 A 20 20, 0, 0, 0, 680 448 L 710 448" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 760 -2" fill="none" stroke="currentColor"></path><path d="M 710 448 L 810 448" fill="none" stroke="currentColor"></path><path d="M 760 -2 L 790 -2 A 20 20, 0, 0, 1, 810 18 L 810 448" fill="none" stroke="currentColor"></path><path d="M 660 178 L 860 178" fill="none" stroke="currentColor"></path><path d="M 810 448 L 840 448 A 20 20, 0, 0, 0, 860 428 L 860 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="178" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="258" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="262" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="178" r="10" fill="none" stroke="currentColor"></circle><path d="M 255,173L265,183M255,183L265,173" fill="none" stroke="currentColor"></path><circle cx="310" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="410" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="560" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="610" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="710" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="760" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="6" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="6" fill="none" stroke="currentColor"></circle></g></svg>

### Forest Theme

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'forest'
---
      gitGraph
        commit
        branch hotfix
        checkout hotfix
        commit
        branch develop
        checkout develop
        commit id:"ash" tag:"abc"
        branch featureB
        checkout featureB
        commit type:HIGHLIGHT
        checkout main
        checkout hotfix
        commit type:NORMAL
        checkout develop
        commit type:REVERSE
        checkout featureB
        commit
        checkout main
        merge hotfix
        checkout featureB
        commit
        checkout develop
        branch featureA
        commit
        checkout develop
        merge hotfix
        checkout featureA
        commit
        checkout featureB
        commit
        checkout develop
        merge featureA
        branch release
        checkout release
        commit
        checkout main
        commit
        checkout release
        merge main
        checkout develop
        merge release
```

<svg id="mermaid-506" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1032.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 1032.4781494140625 538.1637573242188" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-506-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="hsl(78.1578947368, 18.4615384615%, 64.5098039216%)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(98.961038961, 60%, 74.9019607843%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="900" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="900" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-76.94843673706055" y="0.8000001907348633" width="60.94843673706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-86.94843673706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">hotfix</tspan></text></g></g> <line x1="0" y1="178" x2="900" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="268" x2="900" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-96.13750076293945" y="0.8000001907348633" width="80.13750076293945" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-106.13750076293945, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureB</tspan></text></g></g> <line x1="0" y1="358" x2="900" y2="358" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 346)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 346.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g> <line x1="0" y1="448" x2="900" y2="448" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-86.07343673706055" y="0.8000001907348633" width="70.07343673706055" height="22.399999618530273" transform="translate(-19, 436)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-96.07343673706055, 436.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">release</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 60 158 A 20 20, 0, 0, 0, 80 178 L 110 178" fill="none" stroke="currentColor"></path><path d="M 110 178 L 110 248 A 20 20, 0, 0, 0, 130 268 L 160 268" fill="none" stroke="currentColor"></path><path d="M 60 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 110 178 L 260 178" fill="none" stroke="currentColor"></path><path d="M 160 268 L 310 268" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 210 88 L 340 88 A 20 20, 0, 0, 0, 360 68 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 310 268 L 410 268" fill="none" stroke="currentColor"></path><path d="M 260 178 L 260 338 A 20 20, 0, 0, 0, 280 358 L 460 358" fill="none" stroke="currentColor"></path><path d="M 260 178 L 510 178" fill="none" stroke="currentColor"></path><path d="M 210 88 L 210 123 A 10 10, 0, 0, 0, 220 133 L 500 133 A 10 10, 0, 0, 1, 510 143 L 510 178" fill="none" stroke="currentColor"></path><path d="M 460 358 L 560 358" fill="none" stroke="currentColor"></path><path d="M 410 268 L 610 268" fill="none" stroke="currentColor"></path><path d="M 510 178 L 660 178" fill="none" stroke="currentColor"></path><path d="M 560 358 L 640 358 A 20 20, 0, 0, 0, 660 338 L 660 178" fill="none" stroke="currentColor"></path><path d="M 660 178 L 660 428 A 20 20, 0, 0, 0, 680 448 L 710 448" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 760 -2" fill="none" stroke="currentColor"></path><path d="M 710 448 L 810 448" fill="none" stroke="currentColor"></path><path d="M 760 -2 L 790 -2 A 20 20, 0, 0, 1, 810 18 L 810 448" fill="none" stroke="currentColor"></path><path d="M 660 178 L 860 178" fill="none" stroke="currentColor"></path><path d="M 810 448 L 840 448 A 20 20, 0, 0, 0, 860 428 L 860 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="178" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="258" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="262" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="178" r="10" fill="none" stroke="currentColor"></circle><path d="M 255,173L265,183M255,183L265,173" fill="none" stroke="currentColor"></path><circle cx="310" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="410" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="560" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="610" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="710" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="760" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="6" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="6" fill="none" stroke="currentColor"></circle></g></svg>

### Default Theme

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
---
      gitGraph
        commit type:HIGHLIGHT
        branch hotfix
        checkout hotfix
        commit
        branch develop
        checkout develop
        commit id:"ash" tag:"abc"
        branch featureB
        checkout featureB
        commit type:HIGHLIGHT
        checkout main
        checkout hotfix
        commit type:NORMAL
        checkout develop
        commit type:REVERSE
        checkout featureB
        commit
        checkout main
        merge hotfix
        checkout featureB
        commit
        checkout develop
        branch featureA
        commit
        checkout develop
        merge hotfix
        checkout featureA
        commit
        checkout featureB
        commit
        checkout develop
        merge featureA
        branch release
        checkout release
        commit
        checkout main
        commit
        checkout release
        merge main
        checkout develop
        merge release
```

<svg id="mermaid-510" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1032.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 1032.4781494140625 537.107177734375" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="900" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="900" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-76.94843673706055" y="0.8000001907348633" width="60.94843673706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-86.94843673706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">hotfix</tspan></text></g></g> <line x1="0" y1="178" x2="900" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="268" x2="900" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-96.13750076293945" y="0.8000001907348633" width="80.13750076293945" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-106.13750076293945, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureB</tspan></text></g></g> <line x1="0" y1="358" x2="900" y2="358" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 346)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 346.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g> <line x1="0" y1="448" x2="900" y2="448" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-86.07343673706055" y="0.8000001907348633" width="70.07343673706055" height="22.399999618530273" transform="translate(-19, 436)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-96.07343673706055, 436.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">release</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 60 158 A 20 20, 0, 0, 0, 80 178 L 110 178" fill="none" stroke="currentColor"></path><path d="M 110 178 L 110 248 A 20 20, 0, 0, 0, 130 268 L 160 268" fill="none" stroke="currentColor"></path><path d="M 60 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 110 178 L 260 178" fill="none" stroke="currentColor"></path><path d="M 160 268 L 310 268" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 210 88 L 340 88 A 20 20, 0, 0, 0, 360 68 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 310 268 L 410 268" fill="none" stroke="currentColor"></path><path d="M 260 178 L 260 338 A 20 20, 0, 0, 0, 280 358 L 460 358" fill="none" stroke="currentColor"></path><path d="M 260 178 L 510 178" fill="none" stroke="currentColor"></path><path d="M 210 88 L 210 123 A 10 10, 0, 0, 0, 220 133 L 500 133 A 10 10, 0, 0, 1, 510 143 L 510 178" fill="none" stroke="currentColor"></path><path d="M 460 358 L 560 358" fill="none" stroke="currentColor"></path><path d="M 410 268 L 610 268" fill="none" stroke="currentColor"></path><path d="M 510 178 L 660 178" fill="none" stroke="currentColor"></path><path d="M 560 358 L 640 358 A 20 20, 0, 0, 0, 660 338 L 660 178" fill="none" stroke="currentColor"></path><path d="M 660 178 L 660 428 A 20 20, 0, 0, 0, 680 448 L 710 448" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 760 -2" fill="none" stroke="currentColor"></path><path d="M 710 448 L 810 448" fill="none" stroke="currentColor"></path><path d="M 760 -2 L 790 -2 A 20 20, 0, 0, 1, 810 18 L 810 448" fill="none" stroke="currentColor"></path><path d="M 660 178 L 860 178" fill="none" stroke="currentColor"></path><path d="M 810 448 L 840 448 A 20 20, 0, 0, 0, 860 428 L 860 178" fill="none" stroke="currentColor"></path></g><g><rect x="0" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="4" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="178" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="258" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="262" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="178" r="10" fill="none" stroke="currentColor"></circle><path d="M 255,173L265,183M255,183L265,173" fill="none" stroke="currentColor"></path><circle cx="310" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="410" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="560" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="610" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="710" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="760" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="6" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="6" fill="none" stroke="currentColor"></circle></g></svg>

### Dark Theme

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'dark'
---
      gitGraph
        commit
        branch hotfix
        checkout hotfix
        commit
        branch develop
        checkout develop
        commit id:"ash" tag:"abc"
        branch featureB
        checkout featureB
        commit type:HIGHLIGHT
        checkout main
        checkout hotfix
        commit type:NORMAL
        checkout develop
        commit type:REVERSE
        checkout featureB
        commit
        checkout main
        merge hotfix
        checkout featureB
        commit
        checkout develop
        branch featureA
        commit
        checkout develop
        merge hotfix
        checkout featureA
        commit
        checkout featureB
        commit
        checkout develop
        merge featureA
        branch release
        checkout release
        commit
        checkout main
        commit
        checkout release
        merge main
        checkout develop
        merge release
```

<svg id="mermaid-514" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1032.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 1032.4781494140625 537.0089721679688" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-514-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#cccccc" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(180, 0%, 18.3529411765%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="900" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="900" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-76.94843673706055" y="0.8000001907348633" width="60.94843673706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-86.94843673706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">hotfix</tspan></text></g></g> <line x1="0" y1="178" x2="900" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="268" x2="900" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-96.13750076293945" y="0.8000001907348633" width="80.13750076293945" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-106.13750076293945, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureB</tspan></text></g></g> <line x1="0" y1="358" x2="900" y2="358" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 346)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 346.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g> <line x1="0" y1="448" x2="900" y2="448" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-86.07343673706055" y="0.8000001907348633" width="70.07343673706055" height="22.399999618530273" transform="translate(-19, 436)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-96.07343673706055, 436.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">release</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 60 158 A 20 20, 0, 0, 0, 80 178 L 110 178" fill="none" stroke="currentColor"></path><path d="M 110 178 L 110 248 A 20 20, 0, 0, 0, 130 268 L 160 268" fill="none" stroke="currentColor"></path><path d="M 60 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 110 178 L 260 178" fill="none" stroke="currentColor"></path><path d="M 160 268 L 310 268" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 210 88 L 340 88 A 20 20, 0, 0, 0, 360 68 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 310 268 L 410 268" fill="none" stroke="currentColor"></path><path d="M 260 178 L 260 338 A 20 20, 0, 0, 0, 280 358 L 460 358" fill="none" stroke="currentColor"></path><path d="M 260 178 L 510 178" fill="none" stroke="currentColor"></path><path d="M 210 88 L 210 123 A 10 10, 0, 0, 0, 220 133 L 500 133 A 10 10, 0, 0, 1, 510 143 L 510 178" fill="none" stroke="currentColor"></path><path d="M 460 358 L 560 358" fill="none" stroke="currentColor"></path><path d="M 410 268 L 610 268" fill="none" stroke="currentColor"></path><path d="M 510 178 L 660 178" fill="none" stroke="currentColor"></path><path d="M 560 358 L 640 358 A 20 20, 0, 0, 0, 660 338 L 660 178" fill="none" stroke="currentColor"></path><path d="M 660 178 L 660 428 A 20 20, 0, 0, 0, 680 448 L 710 448" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 760 -2" fill="none" stroke="currentColor"></path><path d="M 710 448 L 810 448" fill="none" stroke="currentColor"></path><path d="M 760 -2 L 790 -2 A 20 20, 0, 0, 1, 810 18 L 810 448" fill="none" stroke="currentColor"></path><path d="M 660 178 L 860 178" fill="none" stroke="currentColor"></path><path d="M 810 448 L 840 448 A 20 20, 0, 0, 0, 860 428 L 860 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="178" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="258" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="262" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="178" r="10" fill="none" stroke="currentColor"></circle><path d="M 255,173L265,183M255,183L265,173" fill="none" stroke="currentColor"></path><circle cx="310" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="410" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="560" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="610" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="710" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="760" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="6" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="6" fill="none" stroke="currentColor"></circle></g></svg>

### Neutral Theme

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'neutral'
---
      gitGraph
        commit
        branch hotfix
        checkout hotfix
        commit
        branch develop
        checkout develop
        commit id:"ash" tag:"abc"
        branch featureB
        checkout featureB
        commit type:HIGHLIGHT
        checkout main
        checkout hotfix
        commit type:NORMAL
        checkout develop
        commit type:REVERSE
        checkout featureB
        commit
        checkout main
        merge hotfix
        checkout featureB
        commit
        checkout develop
        branch featureA
        commit
        checkout develop
        merge hotfix
        checkout featureA
        commit
        checkout featureB
        commit
        checkout develop
        merge featureA
        branch release
        checkout release
        commit
        checkout main
        commit
        checkout release
        merge main
        checkout develop
        merge release
```

<svg id="mermaid-518" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1032.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 1032.4781494140625 538.156982421875" role="graphics-document document" aria-roledescription="gitGraph"><g></g><defs><linearGradient id="mermaid-518-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="hsl(0, 0%, 83.3333333333%)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(0, 0%, 88.9215686275%)" stop-opacity="1"></stop></linearGradient></defs><g></g><g><line x1="0" y1="-2" x2="900" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="900" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-76.94843673706055" y="0.8000001907348633" width="60.94843673706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-86.94843673706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">hotfix</tspan></text></g></g> <line x1="0" y1="178" x2="900" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="268" x2="900" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-96.13750076293945" y="0.8000001907348633" width="80.13750076293945" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-106.13750076293945, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureB</tspan></text></g></g> <line x1="0" y1="358" x2="900" y2="358" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 346)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 346.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g> <line x1="0" y1="448" x2="900" y2="448" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-86.07343673706055" y="0.8000001907348633" width="70.07343673706055" height="22.399999618530273" transform="translate(-19, 436)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-96.07343673706055, 436.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">release</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 60 158 A 20 20, 0, 0, 0, 80 178 L 110 178" fill="none" stroke="currentColor"></path><path d="M 110 178 L 110 248 A 20 20, 0, 0, 0, 130 268 L 160 268" fill="none" stroke="currentColor"></path><path d="M 60 88 L 210 88" fill="none" stroke="currentColor"></path><path d="M 110 178 L 260 178" fill="none" stroke="currentColor"></path><path d="M 160 268 L 310 268" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 210 88 L 340 88 A 20 20, 0, 0, 0, 360 68 L 360 -2" fill="none" stroke="currentColor"></path><path d="M 310 268 L 410 268" fill="none" stroke="currentColor"></path><path d="M 260 178 L 260 338 A 20 20, 0, 0, 0, 280 358 L 460 358" fill="none" stroke="currentColor"></path><path d="M 260 178 L 510 178" fill="none" stroke="currentColor"></path><path d="M 210 88 L 210 123 A 10 10, 0, 0, 0, 220 133 L 500 133 A 10 10, 0, 0, 1, 510 143 L 510 178" fill="none" stroke="currentColor"></path><path d="M 460 358 L 560 358" fill="none" stroke="currentColor"></path><path d="M 410 268 L 610 268" fill="none" stroke="currentColor"></path><path d="M 510 178 L 660 178" fill="none" stroke="currentColor"></path><path d="M 560 358 L 640 358 A 20 20, 0, 0, 0, 660 338 L 660 178" fill="none" stroke="currentColor"></path><path d="M 660 178 L 660 428 A 20 20, 0, 0, 0, 680 448 L 710 448" fill="none" stroke="currentColor"></path><path d="M 360 -2 L 760 -2" fill="none" stroke="currentColor"></path><path d="M 710 448 L 810 448" fill="none" stroke="currentColor"></path><path d="M 760 -2 L 790 -2 A 20 20, 0, 0, 1, 810 18 L 810 448" fill="none" stroke="currentColor"></path><path d="M 660 178 L 860 178" fill="none" stroke="currentColor"></path><path d="M 810 448 L 840 448 A 20 20, 0, 0, 0, 860 428 L 860 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="178" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="258" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="262" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="178" r="10" fill="none" stroke="currentColor"></circle><path d="M 255,173L265,183M255,183L265,173" fill="none" stroke="currentColor"></path><circle cx="310" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="410" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="460" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="510" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="560" cy="358" r="10" fill="none" stroke="currentColor"></circle><circle cx="610" cy="268" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="660" cy="178" r="6" fill="none" stroke="currentColor"></circle><circle cx="710" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="760" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="10" fill="none" stroke="currentColor"></circle><circle cx="810" cy="448" r="6" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="10" fill="none" stroke="currentColor"></circle><circle cx="860" cy="178" r="6" fill="none" stroke="currentColor"></circle></g></svg>

## Customize using Theme Variables

Mermaid allows you to customize your diagram using theme variables which govern the look and feel of various elements of the diagram.

For understanding let us take a sample diagram with theme `default`, the default values of the theme variables is picked automatically from the theme. Later on we will see how to override the default values of the theme variables.

See how the default theme is used to set the colors for the branches:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
---
       gitGraph
       commit
       branch develop
       commit tag:"v1.0.0"
       commit
       checkout main
       commit type: HIGHLIGHT
       commit
       merge develop
       commit
       branch featureA
       commit
```

<svg id="mermaid-531" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 532.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 532.4781494140625 264.4385986328125" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="400" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="400" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="178" x2="400" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 240 88 A 20 20, 0, 0, 0, 260 68 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 310 158 A 20 20, 0, 0, 0, 330 178 L 360 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="178" r="10" fill="none" stroke="currentColor"></circle></g></svg>

> #### IMPORTANT:
> 
> Mermaid supports the theme variables to override the default values for **up to 8 branches**, i.e., you can set the color/styling of up to 8 branches using theme variables. After this threshold of 8 branches, the theme variables are reused in the cyclic manner, i.e. the 9th branch will use the color/styling of the 1st branch, or the branch at index position '8' will use the color/styling of the branch at index position '0'. *More on this in the next section. See examples on **Customizing branch label colors** below*

### Customizing branch colors

You can customize the branch colors using the `git0` to `git7` theme variables. Mermaid allows you to set the colors for up-to 8 branches, where `git0` variable will drive the value of the first branch, `git1` will drive the value of the second branch and so on.

NOTE: Default values for these theme variables are picked from the selected theme. If you want to override the default values, you can use the `initialize` call to add your custom theme variable values.

Example:

Now let's override the default values for the `git0` to `git3` variables:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
  themeVariables:
      'git0': '#ff0000'
      'git1': '#00ff00'
      'git2': '#0000ff'
      'git3': '#ff00ff'
      'git4': '#00ffff'
      'git5': '#ffff00'
      'git6': '#ff00ff'
      'git7': '#00ffff'
---
       gitGraph
       commit
       branch develop
       commit tag:"v1.0.0"
       commit
       checkout main
       commit type: HIGHLIGHT
       commit
       merge develop
       commit
       branch featureA
       commit
```

<svg id="mermaid-555" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 532.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 532.4781494140625 264.5266571044922" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="400" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="400" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="178" x2="400" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 240 88 A 20 20, 0, 0, 0, 260 68 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 310 158 A 20 20, 0, 0, 0, 330 178 L 360 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="178" r="10" fill="none" stroke="currentColor"></circle></g></svg>

See how the branch colors are changed to the values specified in the theme variables.

### Customizing branch label colors

You can customize the branch label colors using the `gitBranchLabel0` to `gitBranchLabel7` theme variables. Mermaid allows you to set the colors for up-to 8 branches, where `gitBranchLabel0` variable will drive the value of the first branch label, `gitBranchLabel1` will drive the value of the second branch label and so on.

Lets see how the default theme is used to set the colors for the branch labels:

Now let's override the default values for the `gitBranchLabel0` to `gitBranchLabel2` variables:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
  themeVariables:
    'gitBranchLabel0': '#ffffff'
    'gitBranchLabel1': '#ffffff'
    'gitBranchLabel2': '#ffffff'
    'gitBranchLabel3': '#ffffff'
    'gitBranchLabel4': '#ffffff'
    'gitBranchLabel5': '#ffffff'
    'gitBranchLabel6': '#ffffff'
    'gitBranchLabel7': '#ffffff'
    'gitBranchLabel8': '#ffffff'
    'gitBranchLabel9': '#ffffff'
---
  gitGraph
    checkout main
    branch branch1
    branch branch2
    branch branch3
    branch branch4
    branch branch5
    branch branch6
    branch branch7
    branch branch8
    branch branch9
    checkout branch1
    commit
```

<svg id="mermaid-571" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 176.74533081054688px;" viewBox="-118.74531555175781 -21.199999809265137 176.74533081054688 848.4000244140625" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="50" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="50" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.3375015258789" y="0.8000001907348633" width="75.3375015258789" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.3375015258789, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch1</tspan></text></g></g> <line x1="0" y1="178" x2="50" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.3375015258789" y="0.8000001907348633" width="75.3375015258789" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.3375015258789, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch2</tspan></text></g></g> <line x1="0" y1="268" x2="50" y2="268" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.3375015258789" y="0.8000001907348633" width="75.3375015258789" height="22.399999618530273" transform="translate(-19, 256)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.3375015258789, 256.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch3</tspan></text></g></g> <line x1="0" y1="358" x2="50" y2="358" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.74531173706055" y="0.8000001907348633" width="75.74531173706055" height="22.399999618530273" transform="translate(-19, 346)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.74531173706055, 346.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch4</tspan></text></g></g> <line x1="0" y1="448" x2="50" y2="448" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.3375015258789" y="0.8000001907348633" width="75.3375015258789" height="22.399999618530273" transform="translate(-19, 436)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.3375015258789, 436.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch5</tspan></text></g></g> <line x1="0" y1="538" x2="50" y2="538" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.3375015258789" y="0.8000001907348633" width="75.3375015258789" height="22.399999618530273" transform="translate(-19, 526)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.3375015258789, 526.8000001907349)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch6</tspan></text></g></g> <line x1="0" y1="628" x2="50" y2="628" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.74531173706055" y="0.8000001907348633" width="75.74531173706055" height="22.399999618530273" transform="translate(-19, 616)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.74531173706055, 616.8000001907349)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch7</tspan></text></g></g> <line x1="0" y1="718" x2="50" y2="718" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.3375015258789" y="0.8000001907348633" width="75.3375015258789" height="22.399999618530273" transform="translate(-19, 706)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.3375015258789, 706.8000001907349)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch8</tspan></text></g></g> <line x1="0" y1="808" x2="50" y2="808" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-91.3375015258789" y="0.8000001907348633" width="75.3375015258789" height="22.399999618530273" transform="translate(-19, 796)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-101.3375015258789, 796.8000001907349)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">branch9</tspan></text></g></g></g><g></g><g><circle cx="10" cy="88" r="10" fill="none" stroke="currentColor"></circle></g></svg>

Here, you can see that `branch8` and `branch9` colors and the styles are being picked from branch at index position `0` (`main`) and `1` (`branch1`) respectively, i.e., **branch themeVariables are repeated cyclically**.

### Customizing Commit colors

You can customize commit using the `commitLabelColor` and `commitLabelBackground` theme variables for changes in the commit label color and background color respectively.

Example: Now let's override the default values for the `commitLabelColor` to `commitLabelBackground` variables:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
  themeVariables:
    commitLabelColor: '#ff0000'
    commitLabelBackground: '#00ff00'
---
       gitGraph
       commit
       branch develop
       commit tag:"v1.0.0"
       commit
       checkout main
       commit type: HIGHLIGHT
       commit
       merge develop
       commit
       branch featureA
       commit
```

<svg id="mermaid-584" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 532.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 532.4781494140625 263.0162658691406" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="400" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="400" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="178" x2="400" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 240 88 A 20 20, 0, 0, 0, 260 68 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 310 158 A 20 20, 0, 0, 0, 330 178 L 360 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="178" r="10" fill="none" stroke="currentColor"></circle></g></svg>

See how the commit label color and background color are changed to the values specified in the theme variables.

### Customizing Commit Label Font Size

You can customize commit using the `commitLabelFontSize` theme variables for changing in the font size of the commit label.

Example: Now let's override the default values for the `commitLabelFontSize` variable:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
  themeVariables:
    commitLabelColor: '#ff0000'
    commitLabelBackground: '#00ff00'
    commitLabelFontSize: '16px'
---
       gitGraph
       commit
       branch develop
       commit tag:"v1.0.0"
       commit
       checkout main
       commit type: HIGHLIGHT
       commit
       merge develop
       commit
       branch featureA
       commit
```

<svg id="mermaid-597" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 532.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 532.4781494140625 287.4460754394531" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="400" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="400" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="178" x2="400" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 240 88 A 20 20, 0, 0, 0, 260 68 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 310 158 A 20 20, 0, 0, 0, 330 178 L 360 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="178" r="10" fill="none" stroke="currentColor"></circle></g></svg>

See how the commit label font size changed.

### Customizing Tag Label Font Size

You can customize commit using the `tagLabelFontSize` theme variables for changing in the font size of the tag label.

Example: Now let's override the default values for the `tagLabelFontSize` variable:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
  themeVariables:
    commitLabelColor: '#ff0000'
    commitLabelBackground: '#00ff00'
    tagLabelFontSize: '16px'
---
       gitGraph
       commit
       branch develop
       commit tag:"v1.0.0"
       commit
       checkout main
       commit type: HIGHLIGHT
       commit
       merge develop
       commit
       branch featureA
       commit
```

<svg id="mermaid-610" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 532.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 532.4781494140625 264.8923797607422" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="400" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="400" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="178" x2="400" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 240 88 A 20 20, 0, 0, 0, 260 68 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 310 158 A 20 20, 0, 0, 0, 330 178 L 360 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="178" r="10" fill="none" stroke="currentColor"></circle></g></svg>

See how the tag label font size changed.

### Customizing Tag colors

You can customize tag using the `tagLabelColor`,`tagLabelBackground` and `tagLabelBorder` theme variables for changes in the tag label color,tag label background color and tag label border respectively. Example: Now let's override the default values for the `tagLabelColor`, `tagLabelBackground` and to `tagLabelBorder` variables:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
  themeVariables:
    tagLabelColor: '#ff0000'
    tagLabelBackground: '#00ff00'
    tagLabelBorder: '#0000ff'
---
       gitGraph
       commit
       branch develop
       commit tag:"v1.0.0"
       commit
       checkout main
       commit type: HIGHLIGHT
       commit
       merge develop
       commit
       branch featureA
       commit
```

<svg id="mermaid-620" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 532.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 532.4781494140625 264.5198669433594" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="400" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="400" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="178" x2="400" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 240 88 A 20 20, 0, 0, 0, 260 68 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 310 158 A 20 20, 0, 0, 0, 330 178 L 360 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="178" r="10" fill="none" stroke="currentColor"></circle></g></svg>

See how the tag colors are changed to the values specified in the theme variables.

### Customizing Highlight commit colors

You can customize the highlight commit colors in relation to the branch it is on using the `gitInv0` to `gitInv7` theme variables. Mermaid allows you to set the colors for up-to 8 branches specific highlight commit, where `gitInv0` variable will drive the value of the first branch's highlight commits, `gitInv1` will drive the value of the second branch's highlight commit label and so on.

Example:

Now let's override the default values for the `git0` to `git3` variables:

##### Code:

```
mermaid---
config:
  logLevel: 'debug'
  theme: 'default'
  themeVariables:
    'gitInv0': '#ff0000'
---
       gitGraph
       commit
       branch develop
       commit tag:"v1.0.0"
       commit
       checkout main
       commit type: HIGHLIGHT
       commit
       merge develop
       commit
       branch featureA
       commit
```

<svg id="mermaid-636" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 532.4781494140625px;" viewBox="-124.4781265258789 -21.199999809265137 532.4781494140625 264.7970275878906" role="graphics-document document" aria-roledescription="gitGraph"><g></g><g></g><g><line x1="0" y1="-2" x2="400" y2="-2" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-69" y="0.8000001907348633" width="53" height="22.399999618530273" transform="translate(-19, -14)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-79, -13.199999809265137)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">main</tspan></text></g></g> <line x1="0" y1="88" x2="400" y2="88" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-90.42499923706055" y="0.8000001907348633" width="74.42499923706055" height="22.399999618530273" transform="translate(-19, 76)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-100.42499923706055, 76.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">develop</tspan></text></g></g> <line x1="0" y1="178" x2="400" y2="178" stroke="currentColor" stroke-opacity="0.2"></line><rect style="" rx="4" ry="4" x="-97.4781265258789" y="0.8000001907348633" width="81.4781265258789" height="22.399999618530273" transform="translate(-19, 166)" fill="none" stroke="currentColor"></rect><g><g transform="translate(-107.4781265258789, 166.80000019073486)"><text><tspan xml:space="preserve" dy="1em" x="0" fill="currentColor">featureA</tspan></text></g></g></g><g><path d="M 10 -2 L 10 68 A 20 20, 0, 0, 0, 30 88 L 60 88" fill="none" stroke="currentColor"></path><path d="M 60 88 L 110 88" fill="none" stroke="currentColor"></path><path d="M 10 -2 L 160 -2" fill="none" stroke="currentColor"></path><path d="M 160 -2 L 210 -2" fill="none" stroke="currentColor"></path><path d="M 210 -2 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 110 88 L 240 88 A 20 20, 0, 0, 0, 260 68 L 260 -2" fill="none" stroke="currentColor"></path><path d="M 260 -2 L 310 -2" fill="none" stroke="currentColor"></path><path d="M 310 -2 L 310 158 A 20 20, 0, 0, 0, 330 178 L 360 178" fill="none" stroke="currentColor"></path></g><g><circle cx="10" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="60" cy="88" r="10" fill="none" stroke="currentColor"></circle><circle cx="110" cy="88" r="10" fill="none" stroke="currentColor"></circle><rect x="150" y="-12" width="20" height="20" fill="none" stroke="currentColor"></rect><rect x="154" y="-8" width="12" height="12" fill="none" stroke="currentColor"></rect><circle cx="210" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="260" cy="-2" r="6" fill="none" stroke="currentColor"></circle><circle cx="310" cy="-2" r="10" fill="none" stroke="currentColor"></circle><circle cx="360" cy="178" r="10" fill="none" stroke="currentColor"></circle></g></svg>

See how the highlighted commit color on the first branch is changed to the value specified in the theme variable `gitInv0`.