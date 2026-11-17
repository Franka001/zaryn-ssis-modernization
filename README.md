# SQL Server & SSIS Modernization Blueprint
### A Zaryn Data Engineering Portfolio Showcase

A phased modernization demonstration for businesses that rely on SQL Server and SSIS integrations for operational reporting.

> Status: Design-stage portfolio blueprint. This version contains documentation only. It does not yet include an SSIS package, replacement pipeline, deployment artifacts, or measured reconciliation results. This is not a client migration.

## Business Problem

A manufacturer or wholesale distributor relies on nightly integrations and needs a practical path to improve reliability, documentation, and maintainability without an unnecessary wholesale rewrite.

## Proposed Demonstration

Use synthetic sales and inventory data to document an existing integration scenario, assess its dependencies, and implement one replacement workflow after selecting a justified target.

## Modernization Options to Evaluate

| Option | Assessment question |
|---|---|
| Retain and improve SSIS | Can the requirements be met through configuration, logging, testing, and support improvements? |
| Azure Data Factory | Does the workload fit the required connectors, network access, orchestration, and deployment approach? |
| Microsoft Fabric | Does the target analytics environment support the required connectivity, transformations, governance, and capacity assumptions? |

Azure Data Factory and Data Factory in Microsoft Fabric are separate options, not interchangeable names. The final target will be selected and documented during implementation. No automatic package conversion is promised.

## Planned Evidence

- Existing-state architecture and dependency inventory
- Retain, improve, or migrate decision record
- One representative legacy workflow and one replacement
- Source-to-target mapping and reconciliation tests
- Incremental processing and safe rerun demonstration
- Cutover, rollback, and operating runbooks

## Validation and Cutover Criteria

Compare legacy and replacement outputs against the same source snapshot. Reconcile keys, row counts, quantities, and monetary totals with documented precision and tolerances. Test updates, cancellations, duplicate delivery, and failures. Do not cut over until agreed acceptance checks pass and rollback has been rehearsed. No test results are available in this version.

## Implementation Roadmap

- [x] Define demonstration scope and assessment checklist
- [ ] Generate synthetic sources and establish the legacy baseline
- [ ] Add a representative SSIS package or executable legacy workflow with its exact limitations
- [ ] Document and justify the target platform
- [ ] Implement one replacement integration
- [ ] Add reconciliation and recovery tests
- [ ] Publish reproducible setup and measured results
- [ ] Rehearse cutover and rollback

## Documentation

[Assessment checklist](docs/assessment-checklist.md)

## Limitations

Documentation only: no executable migration or deployed Azure/Fabric environment is included. Connectivity, runtime support, licensing, costs, and operational requirements must be verified for the selected environment. No performance improvements or savings are claimed.

## Discuss a Similar Project

Zaryn Data Engineering | Manufacturing & Wholesale Distribution

Email: [admin@zaryndata.onmicrosoft.com](mailto:admin@zaryndata.onmicrosoft.com)

Describe your integration challenge and source systems at a high level. Do not send credentials or confidential datasets.
