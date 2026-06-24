---
title: "Tailscale Docs"
source: "https://tailscale.com/docs/features/containers/docker"
author:
published: 2026-03-23
created: 2026-06-23
description: "Explore how to use Tailscale inside Docker containers."
---
## Docker

Installing applications like web servers, databases, or self-hosted services directly on your machine can create challenges. Each service needs specific dependencies that can conflict with other software, setup requires multiple steps, and removal can be difficult. To access these services remotely, you typically need to expose them to the public internet, which creates security risks. [Docker](https://www.docker.com/) containers solve these problems by packaging each application with everything it needs in an isolated environment. You can run multiple services without conflicts, test software without cluttering your system, and remove containers cleanly. When you connect Docker containers to your tailnet, you can securely access these services from anywhere without public exposure.

Common use cases include running self-hosted applications such as Plex, Grafana, and Home Assistant, accessing development databases and tools remotely, connecting microservices across different hosts, and testing applications in isolated environments. Refer to [Tailscale Docker code examples](https://github.com/tailscale-dev/docker-guide-code-examples) in GitHub, for more ideas and examples of what you can install alongside the Tailscale client in a container.

#### [Understanding Docker components](https://tailscale.com/docs/features/containers/docker/docker-components)

Docker components overview covering Engine that runs containers, Dockerfiles that define images, images that package apps, containers that run them, and Compose for multi container setups.

#### [Connect a Docker container to your tailnet with standalone Docker](https://tailscale.com/docs/features/containers/docker/how-to/connect-docker-standalone)

Run the Tailscale Docker image using a single command to create and authenticate a container to your tailnet.

#### [Connect a Docker container to your tailnet with Docker Compose](https://tailscale.com/docs/features/containers/docker/how-to/connect-docker-container)

Set up a Tailscale-connected container using Docker Compose with nginx, allowing secure access to the service over your tailnet.

#### [Connect a Docker container to your tailnet with an alternative Docker manager](https://tailscale.com/docs/features/containers/docker/how-to/connect-docker-alt-manager)

Run the Tailscale Docker image with alternative container managers like Podman, Portainer, or Colima using the same configuration.

#### [Docker configuration parameters](https://tailscale.com/docs/features/containers/docker/docker-params)

Use Docker environment variables to configure how a Tailscale container authenticates, connects to your tailnet, and exposes services.

![](https://www.youtube.com/watch?v=YTjYXii4WzI)