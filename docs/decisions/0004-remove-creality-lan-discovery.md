# 0004: Remove Creality LAN auto-discovery

**Status:** Accepted
**Date:** 2026-11-08
**Decided by:** maintainer
**Answers:** [goals Q10](../goals.md#5-feature-scope-decisions)

## Context

OrcaSlicer can scan the LAN for Creality K-series printers using mDNS. The only call site is `CrealityHostDiscovery.cpp`, reached from `CrealityDiscoveryDialog`, which `PhysicalPrinterDialog` opens for the Creality host type ([use map](../dependency-use-map.md) O1). The vendored `deps_src/mdns` is a CrealityPrint C++ wrapper under AGPL-3.0 around a public-domain mDNS library ([mDNS review](../mdns-provenance-license-review.md)). The maintainer has never seen the feature work properly.

## Decision

**Remove the feature as one unit:** `CrealityDiscoveryDialog.*`, `CrealityHostDiscovery.*`, the discovery entry point in `PhysicalPrinterDialog.cpp`, `deps_src/mdns`, and its link item. Manual printer host/IP entry for Creality printers stays and must keep working.

## Alternatives considered

- **Optional build, off by default.** This would keep provenance tracking and maintenance for a feature nobody on the project has seen work, which goes against goal G4 and the validation-honesty principle. Rejected.

## Consequences

- One AGPL-licensed vendored component and its notice bookkeeping go away.
- Validation: build passes; the `deps_src/mdns` component is absent from the use map; a manual Creality host connection is tested by hand on the 2.5.0 base ([0002](0002-base-on-orcaslicer-2.5.0.md)).

## Revisit when

- someone contributes a discovery implementation that is demonstrated working on real Creality hardware.
