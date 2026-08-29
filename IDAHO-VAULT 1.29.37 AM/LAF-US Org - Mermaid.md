---
created: 2026-04-13
status: active
related:
  - LAF
  - UNIFIED (US) SWARM
  - LAF-10-MVP-SWARM-WORKFLOW
  - '- Claude - Mermaid Chart'
  - mermaid
  - organization
  - architecture
authority: LOGAN
---

# LAF-US Org Topology

**LAF-US = LAF-SECRET + LAF-PRIVATE + LAF-PERSONAL + LAF-PUBLIC + LAF-PUBLISH**

```mermaid
flowchart LR
    subgraph LAF-US["LAF-US"]
        direction LR
        subgraph SECRET["LAF-SECRET"]
        end
        subgraph PRIVATE["LAF-PRIVATE"]
        end
        subgraph PERSONAL["LAF-PERSONAL"]
            VAULT["IDAHO-VAULT"]
        end
        subgraph PUBLIC["LAF-PUBLIC"]
        end
        subgraph PUBLISH["LAF-PUBLISH"]
            GEMSTONE["THE-GEMSTONE"]
        end
    end
```

---

> LAF-US is the sum of its five repo cores, ordered from most private to most public.
> Each named project lives inside exactly one repo core that matches its visibility tier.
