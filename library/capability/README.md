# `capability/` — reserved

This directory is reserved for capability/effect-shape declarations
(`mncs.io`, `mncs.fs`, `mncs.net`, `mncs.time`, `mncs.random`,
process/execution, device/accelerator, environment/config,
Fabric/distributed operations — see `ARCHITECTURE.md`).

It remains empty until the governing language features exist. No
placeholder syntax is invented to fill it. Importing or naming a
capability API must never grant authority: operations stay subject to
the language's declared effect/capability closure.
