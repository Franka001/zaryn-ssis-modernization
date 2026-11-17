# Integration Modernization Assessment

A proposed discovery and acceptance checklist for the portfolio demonstration. This is not a completed assessment of a customer environment.

## Current-State Inventory

- SQL Server and SSIS versions, execution environments, and support requirements
- Packages, SQL Agent jobs, schedules, dependencies, and owners
- Source and target systems, connectors, custom scripts, and third-party components
- Authentication, network paths, gateways, and runtime dependencies
- Data volumes, batch windows, concurrency, and recovery objectives
- Business rules, report dependencies, and sensitive-data classifications

## Decision Record

For each workflow, record the requirement, retain/improve/migrate recommendation, alternatives considered, evidence, risks, and implementation effort assumptions. Do not select a cloud platform merely to replace a working component. Identify platform-specific gaps that require redesign.

## Replacement Requirements

- Explicit business keys and source-to-target mappings
- Stable extraction boundaries and a documented strategy for updates and deletes
- Durable batch logging and quarantine rules
- Idempotent target writes and controlled retries
- Watermark advancement only after successful acceptance and publication
- Credentials outside source control and least-privilege access

## Reconciliation Plan

Use the same source snapshot or extraction boundary for both workflows. Compare business keys, row counts, nulls, duplicates, quantities, and monetary totals by the relevant business grain. Define decimal precision and tolerance before testing. Log discrepancies and require review rather than silently discarding them.

## Failure Tests

Interrupt extraction, transformation, and publication separately. Confirm that failed batches do not advance checkpoints or publish incomplete results. Replay the batch and verify that records are not duplicated. Test source corrections, late-arriving records, cancellation/deletion rules, and credential failures.

## Cutover and Rollback Plan

Define the owner, maintenance window, source snapshot, final legacy run, target acceptance checks, and consumer switch. Prevent conflicting writers. Record explicit rollback triggers and the procedure to restore the prior consumer path and reconcile any writes since cutover. Rehearse before a production decision.

## Handover

Document deployment, configuration, access, monitoring, alert routing, recovery, escalation, cost assumptions, and ownership. Record outstanding risks and unsupported scenarios. Mark each validation item as not run, passed, or failed with evidence; never treat an unchecked item as successful.
