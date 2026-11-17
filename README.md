# SQL Server & SSIS Modernization Blueprint
### A Zaryn Data Engineering Portfolio Showcase

A modernization blueprint with a runnable Python/SQLite demonstration of incremental loading, reconciliation, and failure recovery. This local starter illustrates validation logic; it does not run SSIS, connect to SQL Server, or deploy Azure/Fabric resources. This is not a client migration.

## Business Problem

Manufacturers and wholesale distributors need a defensible way to validate replacement integrations before moving away from established nightly jobs. The demonstration compares a checkpoint-based load with a full-history reconstruction of the same synthetic source.

## Run Locally

Use Python 3.10 or later with its standard-library SQLite support. No third-party packages or cloud account are required. From the repository root:

```bash
python pipeline.py
python pipeline.py
python -m unittest -v
```

The first command creates or updates `output/demo.db` and prints a JSON summary. The second run should apply zero new events while still reconciling the target. Use `--source` and `--database` to select alternate demo files. Use a dedicated database, never a customer or unrelated SQLite file.

## Included Dataset and Implementation

- `data/sample/changes.csv`: five fabricated order-change events; no customer data
- `pipeline.py`: sequence validation, incremental upserts/deletes, reconciliation, and transactional checkpoint updates
- `test_pipeline.py`: four automated tests
- [Assessment checklist](docs/assessment-checklist.md): broader modernization discovery and acceptance plan

The CSV uses a global, contiguous `change_seq` starting at 1, `order_id`, `operation` (`U` for upsert or `D` for delete), and a nonnegative integer `amount_cents`. All amounts use one assumed currency. This is an append-only change-log contract, not timestamp-based CDC.

## Expected Results

The first run applies five events and leaves two orders: O100 at 12000 cents and O300 at 5000 cents. O200 is deleted. The reconciled total is 17000 cents and the committed checkpoint is 5. A repeat run applies zero events.

## How the Demonstration Works

1. Validate that the complete source history has unique, contiguous sequence numbers.
2. Rebuild an expected current state from that full history in memory.
3. Read the last committed target checkpoint.
4. Apply only later events to SQLite using parameterized SQL.
5. Compare every target key and amount with the expected state.
6. Commit target writes and the checkpoint together only after reconciliation succeeds.

The failure test injects an exception after writes and checks that both target changes and checkpoint advancement roll back. Schema initialization is separate from the load transaction.

## Local Validation

Four tests passed in the development sandbox before publication: reconciliation and rerun, incremental update/delete processing, failure rollback and recovery, and duplicate-sequence rejection. No SSIS or SQL Server runtime tests have been performed.

## Boundaries and Limitations

- Supply the complete immutable history on every run; delta-only files are not supported.
- Historical event mutation is unsupported. Reconciliation compares final state, not an audit hash of every event.
- Use a single writer. Concurrent orchestration and production locking are outside this starter.
- Full-history reconciliation is in memory and is not a large-scale benchmark.
- This is a reference algorithm, not an executable legacy SSIS baseline or proof of package equivalence.
- SQL Server T-SQL, an actual SSIS package, Azure Data Factory/Fabric pipelines, deployment automation, and production monitoring remain to be implemented and tested.

## Modernization Roadmap

- [x] Add synthetic data and a runnable local reference algorithm
- [x] Test incremental changes, reruns, reconciliation, and rollback locally
- [ ] Establish a representative SQL Server/SSIS baseline
- [ ] Implement and validate the selected Microsoft target
- [ ] Compare baseline and replacement outputs against the same extraction boundary
- [ ] Rehearse cutover and rollback with documented acceptance criteria

## Discuss a Similar Project

Zaryn Data Engineering | Manufacturing & Wholesale Distribution

Email: [admin@zaryndata.onmicrosoft.com](mailto:admin@zaryndata.onmicrosoft.com)

Do not send credentials or confidential datasets in an initial inquiry.
