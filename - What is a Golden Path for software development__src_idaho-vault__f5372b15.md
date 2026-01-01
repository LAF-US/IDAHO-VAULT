---
title: "What is a Golden Path for software development?"
source: "https://www.redhat.com/en/topics/platform-engineering/golden-paths"
author:
published:
created: 2026-04-28
description: "A Golden Path refers to an opinionated, well-documented, and supported way of building and deploying software within an organization."
date created: Tuesday, April 28th 2026, 6:28:58 pm
date modified: Tuesday, April 28th 2026, 6:29:12 pm
---

A Golden Path refers to an opinionated, well-documented, and supported way of building and deploying software within an organization. With a supported path, development teams are able to build more efficiently in ways that meet organizational standards. Golden Paths offer a clear approach for [platform engineers](https://www.redhat.com/en/topics/platform-engineering/what-is-platform-engineering) to guide [DevOps](https://www.redhat.com/en/topics/devops) teams, [AI/MLOps](https://www.redhat.com/en/topics/ai) teams, security, networking or any other IT organization, ensuring consistency, reliability, and efficient use of time and resources.

Depending on the size and maturity of a developer team, there can be varying numbers of Golden Paths. For example, an organization with a newer platform engineering team might have a few Golden Paths addressing key processes like [microservice](https://www.redhat.com/en/topics/microservices/what-are-microservices) development, [CI/CD pipelines](https://www.redhat.com/en/topics/devops/what-cicd-pipeline), infrastructure [provisioning](https://www.redhat.com/en/topics/automation/what-is-provisioning), and [observability](https://www.redhat.com/en/topics/devops/what-is-observability) setup. In contrast, a more mature team might have hundreds of granular Golden Paths such as front-end [application development](https://www.redhat.com/en/topics/cloud-native-apps), data pipelines for analytics or [machine learning (ML)](https://www.redhat.com/en/topics/ai/what-is-machine-learning) workloads, [serverless](https://www.redhat.com/en/topics/cloud-native-apps/what-is-serverless) application development, and security and compliance workflows. Nonetheless, no matter the team size or maturity, Golden Paths have several common components including:

- **Software templates:** A pre-configured microservice boilerplate, like a Python FastAPI template with Docker and CI/CD pipelines set up.
- **Infrastructure provisioning:** Pre-built Terraform or Pulumi modules for cloud resources.
- **Build and deploy pipelines:** Pre-configured GitHub Actions or Jenkins scripts.
- **Observability tools:** Integrated logging and monitoring solutions.
- **Security guidelines:** Pre-applied policies and scans embedded into the workflow.

#### The concept of a Golden Path

The term *Golden Path* was coined by author Frank Herbert in his science fiction novel, *Children of Dune*. The concept of a template (inspired by Herbert's *Golden Path*) for software was [created by Spotify](https://engineering.atspotify.com/2020/08/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem/) to help engineering teams stay aligned with tooling and processes. The approach has since caught on at other organizations, including Google and Netflix, and organizations sometimes give it their own names. Netflix calls it a “Paved Road”.

One way to think of a Golden Path is to imagine baking a cake. The steps required to bake a cake include pre-heating the oven to a specific temperature, gathering the right baking tools, and having the necessary ingredients. It’s more than following a recipe, it’s also making sure you use the right tools and techniques. If you want more people to bake the same cake, you find ways to become more consistent and efficient. It’s the same with a Golden Path. The more you follow a specific template for software development, the more refined the process and product becomes. The steps involved with baking a cake is the implementation of a Golden Path… only without as much sugar.

Software architects, including those at Red Hat®, describe 4 qualities that Golden Paths should follow. They should be optional, transparent, extensible, and customizable.

**Optional**

Golden Paths should be an optional way of building and deploying. To allow and foster innovation, there should be flexibility to drift from the standard workflows. Engineering teams can observe situations where a Golden Path isn’t being used and identify situations where a new Golden Path might be beneficial.

**Transparent**

The processes and tools of Golden Paths should be transparent. Golden Paths create templates that allow various approaches without having to learn the underlying technology. Transparent Golden Paths give development teams the opportunity to gain a better understanding of what’s happening in the background.

**Extensible**

Golden Paths should be extensible, making room for new capabilities and functions to be added. Golden Paths are already customizable because they’re templates that you can adjust based on a situation. But, if a specific use case requires an additional capability, a Golden Path will need to be flexible enough to allow that expansion.

**Customizable**

Golden Paths should be highly customizable based on the needs of the development teams (either internal or third-party ones), based on existing experience the organization already has doing this manually. This gives an opportunity to create standards that will be implemented into these Golden Paths and enhance security in the process.

Golden Paths may differ depending on what is being deployed. However, they should have those 4 qualities of being optional, transparent, extensible, and customizable.

Generally, platform engineers create and maintain Golden Paths to provide development teams with best practices, defined tools, services, resources, and processes that can increase developer productivity. Platform engineering aims to improve productivity and collaboration among teams by encouraging consistency and efficiency. Platform engineering teams focus on identifying challenges in development and mitigating them by providing standard, reusable tools and capabilities via an [internal developer platform (IDP)](https://www.redhat.com/en/topics/platform-engineering/what-is-an-internal-developer-platform). An IDP consists of a standardized set of self-service tools and technologies that developers need to create and deploy code.

Golden Paths can support use cases including:

**Application development**

Application developers aim to build, test, and deliver applications in a standardized and security-focused manner. Golden Paths help them by providing a path to onboard and build more efficiently. By using Golden Paths, application teams can have a unified foundation that enables information-sharing, encourages the creation of shared tools, and enhances agility and mobility throughout the organization.

**Data science**

Data scientists collect, analyze, and interpret data to produce actionable insights. They may also specialize in developing and deploying [artificial intelligence (AI)](https://www.redhat.com/en/topics/ai) and [ML](https://www.redhat.com/en/topics/ai/what-is-machine-learning) systems. Golden Paths help [ML operations (MLOps)](https://www.redhat.com/en/topics/ai/what-is-mlops) teams integrate ML models into software development. Golden Paths can assist data scientists as they develop AI models, and developers can use Golden Paths to implement those models.

**Site reliability engineering (SRE)**

[SRE teams](https://www.redhat.com/en/topics/devops/what-is-sre) are responsible for how code is deployed, configured, and monitored, as well as the availability, latency, change management, emergency response, and capacity management of services in production. Golden Paths offer consistency for SREs in creating scalable and highly reliable software systems.

**System administration (sysadmin)**

Sysadmins deploy, configure, and maintain an organization’s computer systems. Because sysadmins manage thousands of machines, they need scalable and sustainable methods to do that. Golden Paths provide a clear framework for common tasks and processes, by simplifying or automating routines. This can reduce management complexities and lower the risk of errors.

As a self-service template, Golden Paths offer many benefits that support [developer productivity](https://www.redhat.com/en/products/developer-productivity), including:

**Reduced cognitive load:** Standardized processes reduce the cognitive load on developers, freeing up mental space for innovation.

**Faster development:** With defined tasks, development teams can be successful without having to search for tools and figure out processes, relying on existing and established best practices the organization already owns.

**Established consistency:** Shareable templates and better internal processes help with consistency across projects leading to better outcomes and improved quality, regardless if the development team is an internal one or a third party.

**More automation:** Automating repetitive tasks, such as deployments or code testing, makes it easier to apply practices like CI/CD pipelines, [infrastructure as code (IaC)](https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac), and [application programming interface (API) management](https://www.redhat.com/en/topics/api/what-is-api-management).

**Easier onboarding:** With discoverable documentation and tools, new team members can learn a workflow faster, without having to figure out the best approach for every task.

**Better security:** Templates ensure security standards are being met with built-in practices, leading to simplified audits later.

Designing, also referred to as paving, a Golden Path means creating a roadmap that ensures a simple and effective experience. While what’s included in a Golden Path may vary based on goals, there are a few best practices to consider to improve developer productivity.

1. **Define the user.** The most common user of a Golden Path is going to be a development team. Because templates are built and maintained by more than one team or team member, the users will be a specific group of people with different skill sets, like coding, profiling, and security.
2. **Identify the purpose.** The overall purpose of a Golden Path is to increase developer productivity by automating existing practices.
3. **Layout the path step-by-step.** Creating clear steps and guidelines will ensure the user has a seamless and successful framework to complete each task.
4. **Provide tools and resources.** Offering documentation and tools for execution will help give context to the Golden Path.
5. **Integrate with an IDP.** IDPs are where Golden Paths should live and be easily accessible. Integrating a Golden Path ensures that it’s available through the IDP and enables developer self-service.
6. **Measure success and iterate:** To determine if a Golden Path is successful, use metrics to measure success. Those metrics could include DevOps Research and Assessment (DORA) metrics, SPACE Framework, or Flow Framework. Also, gather feedback from users and repeat the process to improve efficiency.

#### Microservices development

One example of when a Golden Path is used is the creation of a new [microservice](https://www.redhat.com/en/topics/microservices/what-are-microservices) from pre-built templates created by operations teams.

Microservices refer to a style of [application architecture](https://www.redhat.com/en/topics/cloud-native-apps/what-is-an-application-architecture) where a collection of independent services communicate through lightweight [APIs](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces). A microservices architecture provides a more efficient approach to application development, allowing for each core function within an application to exist independently. With separated application elements, DevOps teams can work together without getting in the way of one another. This means more developers working on the same app, at the same time, resulting in less time spent in development.

A Golden Path can boost developer productivity even more by creating an efficient process for building, deploying, and managing microservices. A successful Golden Path for microservices integrates a well-structured pipeline with a strong focus on automation, best practices, and [observability](https://www.redhat.com/en/topics/devops/what-is-observability).

#### MLOps delivery

Golden paths can help with [MLOps](https://www.redhat.com/en/topics/ai/what-is-mlops) delivery. Inspired by DevOps and [GitOps](https://www.redhat.com/en/topics/devops/what-is-gitops) principles, MLOps seeks to establish a continuous evolution for integrating ML models into software development processes. By streamlining collaboration between different teams, an MLOps practice fosters agile development and data-driven decision making within organizations. Adopting an MLOps practice minimizes the manual labor involved in looking after a ML model while ensuring its ongoing performance and reliability.

Using a Golden Path as a guideline for ML delivery can help teams with the process of developing, deploying, and managing ML models. Golden Paths help with MLOps by establishing workflows and practices, like automated pipelines, to ensure a reliable and consistent model delivery.

MLOps teams can benefit from having Golden Paths that provide templates that support the various criteria of MLOp standards, while also giving the freedom to adjust as needed based on use cases.

#### Agentic AI

[Agentic AI](https://www.redhat.com/en/topics/ai/what-is-agentic-ai) is a software system designed to interact with data and tools in a way that requires minimal human intervention. It can accomplish tasks by creating a list of steps and performing them autonomously. Agentic AI differs from traditional [automation](https://www.redhat.com/en/topics/automation) by using real-time data, ML models, and feedback loop to make decisions based on context.

To implement agentic AI, a system is created to provide a [large language model (LLM)](https://www.redhat.com/en/topics/ai/what-are-large-language-models) with access to external tools and algorithms that give instructions on how AI agents should use those tools. Like Golden Paths, agentic AI incorporates an optimized and autonomous process for achieving a goal or completing a task, learning and adapting as needed.

Red Hat products and services work together to support software development and provide the flexibility enterprises need to increase team productivity while increasing self-service, accelerating onboarding, and reducing repetitive tasking across teams.

[Red Hat Developer Hub](https://www.redhat.com/en/technologies/cloud-computing/developer-hub) provides a self-service portal where every single development team in the organization can go to consume all Golden Paths, having a central hub for all knowledge and relevant technical documentation for a specific project. With Red Hat Developer Hub, organizations have the option to use existing software templates to start a new application or microservice, or create and utilize their own custom templates for their particular environment.

In conjunction with Red Hat Developer Hub, [Red Hat OpenShift®](https://www.redhat.com/en/technologies/cloud-computing/openshift) allows development teams to use the application tools they trust, including cloud-native, legacy, and modernized applications. [Red Hat OpenShift Pipelines](https://www.redhat.com/en/technologies/cloud-computing/openshift/pipelines) and [Red Hat OpenShift GitOps](https://www.redhat.com/en/technologies/cloud-computing/openshift/gitops), [Red Hat OpenShift Service Mesh](https://www.redhat.com/en/technologies/cloud-computing/openshift/what-is-openshift-service-mesh), [Red Hat OpenShift Serverless](https://www.redhat.com/en/technologies/cloud-computing/openshift/serverless), and many more technologies are already included and integrated with Red Hat OpenShift to help streamline developer workflows and support integration with many other open source tools.

Because security is always a priority, [Red Hat Trusted Software Supply Chain](https://www.redhat.com/en/solutions/trusted-software-supply-chain) helps organizations build security into the components, processes, and practices of their software development. Developers can code, build, deploy, and monitor for software delivery that is compliant with organizational [security practices](https://www.redhat.com/en/resources/platform-engineering-devsecops-analyst-material).