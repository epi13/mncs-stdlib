# Migrated corpora and fixtures

Every file below moved from `mncs-language` at Stage F with its owning
test harness (harnesses stay in `mncs-language` and read across repos).

| File | Owning test(s) |
| --- | --- |
| `execution/ansi-parser-corpus.json` | (unreferenced witness) |
| `execution/arch-classify-corpus.json` | `arch_classify.rs` |
| `execution/arch-classify-host-corpus.json` | `arch_classify.rs` |
| `execution/atlas-json-projection-corpus.json` | (unreferenced witness) |
| `execution/atlas-json-scan-corpus.json` | (unreferenced witness) |
| `execution/channel-corpus.json` | `channel_contract.rs` |
| `execution/chunk-corpus.json` | `collections.rs` |
| `execution/clock-scan-corpus.json` | `clock_effects.rs` |
| `execution/family-coherence-aggregate-corpus.json` | `family_coherence.rs` |
| `execution/family-coherence-compatibility-corpus.json` | `family_envelopes.rs` |
| `execution/family-coherence-drift-corpus.json` | `family_coherence.rs` |
| `execution/family-coherence-impact-corpus.json` | `family_coherence.rs` |
| `execution/family-coherence-promotion-corpus.json` | `family_coherence.rs` |
| `execution/family-coherence-transition-corpus.json` | `family_coherence.rs` |
| `execution/family-version-corpus.json` | `family_envelopes.rs` |
| `execution/fixed-corpus.json` | `fixed_scores.rs` |
| `execution/fleet-tokens-corpus.json` | `token_sets.rs` |
| `execution/jit-binding-corpus.json` | `jit_orchestration.rs` |
| `execution/jit-depends-corpus.json` | `jit_orchestration.rs` |
| `execution/jit-lifecycle-corpus.json` | `jit_orchestration.rs` |
| `execution/jit-plan-corpus.json` | `jit_orchestration.rs` |
| `execution/jit-profile-corpus.json` | `jit_orchestration.rs` |
| `execution/jit-proof-corpus.json` | `jit_orchestration.rs` |
| `execution/jit-session-corpus.json` | `jit_orchestration.rs` |
| `execution/jit-types-corpus.json` | `jit_orchestration.rs` |
| `execution/journal-corpus.json` | `journal.rs` |
| `execution/json-cursor-corpus.json` | `library_core.rs` |
| `execution/json-cursor-wide-key-corpus.json` | `library_core.rs` |
| `execution/json-emit-corpus.json` | `json_emit.rs` |
| `execution/json-emit-roundtrip-corpus.json` | `json_emit.rs` |
| `execution/json-probe-corpus.json` | `json_recognition.rs` |
| `execution/json-projection-corpus.json` | `json_recognition.rs` |
| `execution/json-stream-corpus.json` | `json_recognition.rs` |
| `execution/library-consumer-corpus.json` | `library_resolution.rs` |
| `execution/library-core-contracts-corpus.json` | `library_core.rs` |
| `execution/library-core-geometry-extra-corpus.json` | `abi_boundary.rs` |
| `execution/library-core-logic-corpus.json` | (unreferenced witness) |
| `execution/library-core-mask-corpus.json` | `abi_boundary.rs` |
| `execution/library-core-ordering-corpus.json` | (unreferenced witness) |
| `execution/library-core-ravel-linked-corpus.json` | `library_core.rs` |
| `execution/library-core-result-corpus.json` | `backend_family.rs`, `library_core.rs` |
| `execution/library-core-sequences-corpus.json` | `library_core.rs` |
| `execution/library-core-sequences-extra-corpus.json` | `abi_boundary.rs` |
| `execution/library-core-status-corpus.json` | `backend_family.rs`, `library_core.rs` |
| `execution/library-core-status-summary-request.json` | `library_core.rs` |
| `execution/library-core-status-wrong-corpus.json` | `library_core.rs` |
| `execution/library-core-unsigned-encoding-corpus.json` | `abi_boundary.rs` |
| `execution/library-core-unsigned-mutant-corpus.json` | `abi_boundary.rs` |
| `execution/library-core-unsigned-sequences-corpus.json` | `abi_boundary.rs` |
| `execution/library-core-vector-corpus.json` | `library_core.rs` |
| `execution/library-core-vector-u64-corpus.json` | `abi_boundary.rs` |
| `execution/library-core-view-over-capacity-corpus.json` | `abi_boundary.rs` |
| `execution/library-std-encoding-corpus.json` | `library_core.rs` |
| `execution/library-std-fnv1a-corpus.json` | `library_core.rs` |
| `execution/partition-corpus.json` | `pressure_effect_partition.rs` |
| `execution/platform-capability-corpus.json` | `platform_capability.rs` |
| `execution/pressure-validated-spelling-corpus.json` | `abi_boundary.rs` |
| `execution/pressure-wide-stage-scans-corpus.json` | `collections.rs` |
| `execution/profile06-boolean-operators-corpus.json` | `backend_family.rs`, `profile06_payload_sums.rs` |
| `execution/profile06-payload-sums-corpus.json` | `profile06_payload_sums.rs` |
| `execution/profile06-random-split-corpus.json` | `profile06_random.rs` |
| `execution/profile07-bounded-data-corpus.json` | `profile07_bounded_data.rs` |
| `execution/profile07-serialization-corpus.json` | `profile07_bounded_data.rs` |
| `execution/profile08-branchless-corpus.json` | `profile08_branchless_vectors.rs` |
| `execution/profile08-numeric-boundary-corpus.json` | `profile08_numeric_boundary.rs` |
| `execution/profile08-vectors-corpus.json` | `profile08_branchless_vectors.rs` |
| `execution/profile09-stdlib-namespace-consumer-corpus.json` | `library_resolution.rs` |
| `execution/proof-dep-admission-corpus.json` | (unreferenced witness) |
| `execution/proof-dep-corpus.json` | `proof_admission.rs`, `proof_dep.rs`, `proof_dep_admission.rs` |
| `execution/proof-kernel-corpus.json` | `proof_demo.rs`, `proof_kernel.rs`, `proof_kernel.rs` |
| `execution/proof-kernel-fuzz-corpus.json` | `proof_kernel.rs` |
| `execution/relation-corpus.json` | `collections.rs` |
| `execution/rfc-status-corpus.json` | `rfc_ledger.rs` |
| `execution/scope-corpus.json` | `task_scope.rs` |
| `execution/semantic-image-laws-corpus.json` | (unreferenced witness) |
| `execution/semantic-vision-laws-corpus.json` | (unreferenced witness) |
| `execution/sha256-corpus.json` | `sha256_pure.rs` |
| `execution/sort-corpus.json` | `collections.rs` |
| `execution/status-generic-consumer-corpus.json` | `library_core.rs` |
| `execution/store-corpus.json` | `store_contracts.rs` |
| `execution/subtype-windows-corpus.json` | `abi_boundary.rs`, `emit_scratchtrack_p010_gap.rs` |
| `execution/task-corpus.json` | `task_lifecycle.rs` |
| `execution/text-map-corpus.json` | `library_core.rs` |
| `execution/text-scan-corpus.json` | `arch_classify.rs`, `text_scan.rs` |
| `execution/text-utf8-corpus.json` | `library_core.rs`, `stdlib_bundle.rs` |
| `execution/token-set-corpus.json` | `token_sets.rs` |

## Fixtures

| File |
| --- |
| `source/ansi-parser-probe.mncs` |
| `source/application-entry.mncs` |
| `source/clock-scan.mncs` |
| `source/fleet-tokens.mncs` |
| `source/host-read-scan.mncs` |
| `source/json-cursor-probe.mncs` |
| `source/json-emit-roundtrip.mncs` |
| `source/json-probe.mncs` |
| `source/json-projection-probe.mncs` |
| `source/json-stream-probe.mncs` |
| `source/library-consumer.mncs` |
| `source/library-core-status-wrong.mncs` |
| `source/pressure-validated-spelling.mncs` |
| `source/pressure-wide-stage-scans.mncs` |
| `source/profile06-boolean-operators.mncs` |
| `source/profile06-payload-sums.mncs` |
| `source/profile06-random-split.mncs` |
| `source/profile07-bounded-data.mncs` |
| `source/profile07-serialization.mncs` |
| `source/profile08-branchless.mncs` |
| `source/profile08-numeric-boundary.mncs` |
| `source/profile08-vectors.mncs` |
| `source/profile09-stdlib-namespace-consumer.mncs` |
| `source/status-generic-consumer.mncs` |
| `source/subtype-windows.mncs` |
| `source/semantic/image_mutant.mncs` |
| `source/semantic/vision_mutant.mncs` |
| `source/arch/classify.mncs` |
| `consumers/ravel-core-snapshot.mncs` |
