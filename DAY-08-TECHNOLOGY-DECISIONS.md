# Day 08 — Technology Selection & Build vs Buy

## Objective

Learn how architects make technology decisions based on evidence rather than popularity.

## Evaluate technologies using

- business requirements
- latency
- scale
- cost
- security
- privacy
- team expertise
- operational burden
- vendor lock-in
- long-term maintenance

## Example decision

Open-weight self-hosting vs managed proprietary model.

### Self-hosting advantages

- control
- data locality
- customization
- predictable infrastructure economics at sufficient scale

### Self-hosting costs

- GPUs
- operations
- upgrades
- reliability
- security
- platform engineering

### Managed model advantages

- rapid adoption
- low infrastructure burden
- strong capabilities

### Managed model costs

- per-token pricing
- provider dependency
- API limits
- data/privacy considerations

## ADR template

### Decision

What was chosen?

### Context

What problem are we solving?

### Options

What alternatives were evaluated?

### Trade-offs

What do we gain and lose?

### Consequences

What becomes easier or harder?

## Exercise

Create an ADR for choosing between:

- managed proprietary model
- self-hosted open-weight model
- hybrid model strategy

## Deliverable

One completed ADR.
