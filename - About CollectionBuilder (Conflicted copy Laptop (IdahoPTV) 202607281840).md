---
title: "About CollectionBuilder"
source: "https://collectionbuilder.github.io/about.html"
author:
published:
created: 2026-07-20
description: "CollectionBuilder is an open source tool for creating digital collection and exhibit websites that are driven by metadata and powered by modern static web technology."
---
## About CollectionBuilder

## What is CollectionBuilder?

CollectionBuilder is a set of flexible, static web [templates](https://collectionbuilder.github.io/templates.html) for creating digital collection and exhibit websites. These templates are driven by metadata and powered by modern static web technology. Using three primary components—a spreadsheet of metadata, a directory of assets, and a configuration file—CollectionBuilder helps users to build and customize sustainable, digital collections and exhibits for free, learning valuable development practices in the process.

## How does it work?

CollectionBuilder uses the static site generator Jekyll, together with well documented workflows, to help users generate digital collections and exhibits from their own spreadsheets and digital media.

Each CollectionBuilder template exists as a repository on GitHub that users are asked to copy and modify by replacing the default values, metadata spreadsheet, and digital objects with their own. Once replaced, CollectionBuilder iterates over a user’s data to create a series of static HTML, CSS, and JavaScript files that can be served from any web server. With these customized files, CollectionBuilder builds maps, timelines, word clouds, and other visualizations, as well as browsing features, item pages, and new, reusable data formats that can be downloaded by users and processed/indexed by machines.

## How Can I Use It?

We have extensive, learning-focused [Documentation](https://collectionbuilder.github.io/cb-docs/) to get you started. In short:

- Choose a template that matches your project goals.
- Go to that template’s GitHub repository.
- Copy the template by clicking “Use This Template.”
- Upload your metadata to the \_data directory
- And then edit the \_config.yml to point to that file.

You’ll need to make sure your metadata has [a few required fields](https://collectionbuilder.github.io/cb-docs/docs/metadata/), but other than that, CollectionBuilder is adaptable to a wide variety of data.

## Who’s Behind This?

CollectionBuilder is designed and maintained by librarians at the [University of Idaho](https://www.lib.uidaho.edu/), following the [Lib-Static](https://lib-static.github.io/) approach, a methodology committed to leveraging static-web technologies and librarians’ specialized skills in metadata and classification to create engaging web publications.

The project comes out of work done at the University of [[Idaho]] library’s digital humanities lab, the [Center for Digital Inquiry and Learning](https://www.lib.uidaho.edu/).

CollectionBuilder has received support from the University of Idaho Library, and grants from Institute for Museum and Library Services (IMLS) and National Endowment for the Humanities (NEH).

## What are you using to build a CollectionBuilder site?

CollectionBuilder uses 4 main components:

1. [Jekyll](https://jekyllrb.com/) - a static website builder (i.e. NO SERVERS!!!) that builds websites from data files using the [Liquid](https://shopify.github.io/liquid/basics/introduction/) templating language (which you don’t need to know, but which is easily readable and usable) and [Markdown](https://en.wikipedia.org/wiki/Markdown) files for content
2. [Git/GitHub](https://github.com/) - a way to collaborate, track changes, and import pre-built services
3. [Bootstrap](https://getbootstrap.com/) - a CSS/Javascript Package for easier development
4. Data Files - We use [Comma Separated Values (CSV) files](https://en.wikipedia.org/wiki/Comma-separated_values) that are just simple version of a spreadsheet and text files written in [YAML (.yml)](https://en.wikipedia.org/wiki/YAML), which are basically lists formatted in a specific fashion.

## What are you using to build the visualizations and display features?

Our visualizations and features are built using a combination of our own designs with a variety of open source libraries (all of which are contained within each repository to promote site sustainability). All code is available for customization.

The open source libraries include:

- [DataTables](https://datatables.net/) - for an automatically generated Table on our data pages.
- [Leaflet js](http://leafletjs.com/) - for our maps.
- [Spotlight gallery](https://github.com/nextapps-de/spotlight) - for images on our item pages.
- [TimelineJS](https://timeline.knightlab.com/) - for an optional timeline visualization.
- [lazysizes](https://github.com/aFarkas/lazysizes) - for efficient image loading.
- [Lunr.js](https://lunrjs.com/) - for client-side search.

## What is your Design Philosophy?

Well, I don’t know if we’d call it a philosophy …

CollectionBuilder builds digital collection and exhibit sites that encourage investigation and discovery. Our item and visualization pages are built with connections between them so that a user can follow their own interests when exploring a digital collection.

***Our intention is to embed users in the contents and context of a collection in order for them to experience the accretive magic of the “special collections” that archivists and librarians have labored for years to preserve and make accessible.***

## How does that work in practice?

For example, if a user were interested in seeing all the images in our [Barnard Stockbridge Photography Collection](https://www.lib.uidaho.edu/digital/barstock/) pertaining to the 1910 “Big Burn” forest fire, they could [browse the collection](https://www.lib.uidaho.edu/digital/barstock/browse.html#fire) by searching for “fire” on the browse page.

[![demo image](https://collectionbuilder.github.io/images/dlf-presentation.jpg)](https://collectionbuilder.github.io/images/dlf-presentation.jpg)

An illustrative diagram of the ways collection items are connected to the larger context of the digital collections in which they are presented

Then, when looking at individual item pages, they could link out to the year [1910](https://www.lib.uidaho.edu/digital/barstock/timeline.html#1910) on the timeline page and see the wide variety of images collected during that year by the studio.

And perhaps that would lead them to investigate some other [subject terms](https://www.lib.uidaho.edu/digital/barstock/subjects.html) or to focus on a particular town [via the map](https://www.lib.uidaho.edu/digital/barstock/map.html).

As one examines these collections more closely, one can get a larger sense of the collection and the era, as well as its connection to one’s own area and time frame.

*In short:* CollectionBuilder rewards high quality metadata and description by allowing users to interactively explore it.

## What is your methodology?

We call the methodology we use to build CollectionBuilder [Lib-Static](https://lib-static.github.io/).

## Do you really need a “methodology”?

Not really. No. But as we built CollectionBuilder and other static tools like [Oral History as Data](https://uidaholib.github.io/oral-history-as-data/), we noticed that our approach was increasingly divergent from most academic library web development practice. Basically, we brainstormed some principles we were following, thought of a catchy name, and Lib-Static was born.

## So what is Lib-Static?

Lib-Static argues that the systems libraries have been locked into, particularly concerning digital collections, serve neither the librarians/GLAM professionals that maintain them and prepare their content nor the collections we are trying to promote using them.

CollectionBuilder, like other Lib-Static frameworks and projects, prioritizes pragmatic, sustainable, and simplified approaches to web development infrastructure, with a focus on leveraging the particular skills of digital knowledge workers in libraries and museums, empowering them to take control of their web systems.

## Where is your support coming from?

CollectionBuilder receives ongoing support in the form of staff support, development time, and funding from the [University of Idaho Library](https://www.lib.uidaho.edu/). At University of Idaho, [digital scholarship projects](https://cdil.lib.uidaho.edu/projects/) and [digital collections](https://www.lib.uidaho.edu/digital/) are built with CollectionBuilder, based at the [Center for Digital Inquiry and Learning](https://cdil.lib.uidaho.edu/).

CollectionBuilder is also being fully adopted and developed at [Iowa State University Library](https://digitalcollections.lib.iastate.edu/).

### Past Sponsors

#### IMLS

From 2022 to 2025 we were supported by a ***National Leadership Grant for Libraries*** from the [Institute for Museum and Library Services (IMLS)](https://www.imls.gov/), titled [“Growing CollectionBuilder, A Sustainable Digital Exhibit Framework and Static Web Development Model”](https://www.imls.gov/grants/awarded/lg-252326-ols-22).

Over the course of the grant we **expanded our team** to include University of Idaho Digital Scholarship Librarian Julia Stone and **piloted an [incentives program](https://collectionbuilder.github.io/funded-opportunities/)** to encourage contributions to CollectionBuilder from Information and Library Science instructors and students as well as digital librarians.

We were grateful to have the support of our talented **Advisory Board** over the course of this grant cycle:

- **Maggie Dull**, Director of Metadata Strategies, University of Rochester
- **Alex Merrill**, Head of Library Systems & Technical Operations, Washington State University
- **Kate Thornhill**, Digital Scholarship Librarian, University of Oregon
- **John A. Walsh**, Associate Professor of Information Science, Indiana University

#### NEH

From **2021 to 2023**, we worked with colleagues from the University of Oregon on a [Digital Humanities Advancement grant from the National Endowment for the Humanities (NEH)](https://securegrants.neh.gov/publicquery/main.aspx?f=1&gn=HAA-281018-21) to develop Learn-Static, a series of digital humanities instructional modules for static web based projects and learning outcomes. More information can be found on the [Learn-Static website](https://learn-static.github.io/).

**NEH Grant Advisory Board**:

- **Chelcie Juliet Rowell**, Associate Head of Digital Collections Discovery, Harvard University
- **Anne B. McGrail**, Professor of Writing and Literature, Lane Community College
- **Alanna Prince**, English PhD Student, Northeastern University

#### IMLS

From **2019 to 2021**, we were supported by a ***National Leadership Grant for Libraries*** from the [Institute for Museum and Library Services (IMLS)](https://www.imls.gov/grants/awarded/lg-34-19-0064-19) that helped us to build, document, and promote CollectionBuilder.

See a condensed version of our final report below for more details.

**IMLS Grant Advisory Board**:

- **Marii Nyrop**, Senior Research Data Engineer, New York University
- **Alex Merrill**, Head of Library Systems & Technical Operations, Washington State University
- **Kimberly Christen**, Associate Vice Chancellor for Research Advancement and Partnerships, Washington State University
- **Alexander Gil Fuentes**, Senior Lecturer II & Associate Research Faculty of Digital Humanities, Yale University
- **Ammon Shepherd**, Digital Humanities Developer, University of Virginia
- **Laura Bucholz**, Discovery & Systems Librarian, Reed College

## How are others using CollectionBuilder?

CollectionBuilder sites continue to proliferate around the world. Check out the [CollectionBuilder Examples](https://collectionbuilder.github.io/cb-examples/) site which features projects created by a variety of individuals, organizations, and institutions.

Interested in sharing your work? [Submit your own CollectionBuilder project](https://docs.google.com/forms/d/e/1FAIpQLSfOhjLOh4nCg6XY_6pdLit28I5ACxV-y_eokiBl1xp4OG-IhQ/viewform) to be featured in the example collections!

## Where can I learn more?

We’ve presented and written ***a lot*** about CollectionBuilder. Below is a list of our publications, workshops, and presentations.

##### CollectionBuilder Publications

##### CollectionBuilder Presentations and Workshops

## Who Runs This Ship?

Core team:

![picture of Olivia Wikle](https://collectionbuilder.github.io/images/people/wikle.jpg)  

**Olivia Wikle**

Co-Project Director  
*Head, Digital Scholarship and Initiatives, Iowa State University Library*

![picture of Evan Peter Williamson](https://collectionbuilder.github.io/images/people/williamson.jpg)  

**Evan Peter Williamson**

Technical Director  
*Head, Digital Scholarship and Open Strategies, University of Idaho Library*

![picture of Devin Becker](https://collectionbuilder.github.io/images/people/becker.jpg)  

**Devin Becker**

Project Director  
*Associate Dean for Research & Instruction, University of Idaho Library*

Collaborators:

- Julia Stone, Digital Scholarship Librarian, Portland State University (past CB Community Liaison and Digital Scholarship Librarian, University of Idaho Library)
- Jylisa Doney, Social Sciences Librarian, University of Idaho
- Marco Seiferle Valencia, Open Education Librarian, University of Idaho
- Derek Enos, Developer

Advisors:

- Maggie Dull, University of Rochester
- Kate Thornhill, University of Oregon
- John A. Walsh, Indiana University
- Alex Merrill, Washington State University
- Kim Christen, Washington State University
- Alex Gil, Columbia University
- Marii Nyrop, New York University
- Laura Bucholtz, Reed College
- Ammon Shepherd, University of Virginia

Former Graduate Assistants:

- Chelsea Codling, MA Archaeology ‘20, University of Idaho
- Michael Decker, MA English ‘21, University of Idaho

## Partners

- [North Carolina Digital Collections](http://digital.ncdcr.gov/) (State Library of North Carolina and State Archives of North Carolina)
- [New College Digital Collections](https://dss.ncf.edu/digitalcollections/) (New College of Florida)
- [Latah County Historical Society](https://www.latahcountyhistoricalsociety.org/)
- [US Latino Digital Humanities (USLDH)](https://artepublicopress.com/digital-humanities/)

## Contact & Help

Our [documentation](https://collectionbuilder.github.io/cb-docs/) contains detailed walk through information for starting CollectionBuilder projects and our [Tutorials page](https://collectionbuilder.github.io/tutorials.html) provides our latest videos – *but we want your questions!*

CollectionBuilder is building a learning community, so one of the best ways to get help, and help others in the process, is to ask questions on the [CollectionBuilder Discussion Forum](https://github.com/orgs/CollectionBuilder/discussions). Always provide a link to your repository as it makes understanding and debugging the issue *much* easier!

### How To Get in Touch

Have questions, comments, or concerns for CollectionBuilder developers? You’re welcome to contact any or all of us:

- [CollectionBuilder Discussion Forum](https://github.com/orgs/CollectionBuilder/discussions) (informal space to ask questions, provide feedback, debug, share and connect!)
- CollectionBuilder Team ([collectionbuilder.team@gmail.com](mailto:collectionbuilder.team@gmail.com))
- Evan Williamson ([ewilliamson@uidaho.edu](mailto:ewilliamson@uidaho.edu))
- Devin Becker ([dbecker@uidaho.edu](mailto:dbecker@uidaho.edu))
- Olivia Wikle ([omwikle@iastate.edu](mailto:omwikle@iastate.edu))

### Other Resources

- [Contributing](https://github.com/CollectionBuilder/collectionbuilder.github.io/blob/main/CONTRIBUTING.md) (tips and conventions)
- [Project Code of Conduct](https://github.com/CollectionBuilder/collectionbuilder.github.io/blob/main/CODE_OF_CONDUCT.md)

#idaho