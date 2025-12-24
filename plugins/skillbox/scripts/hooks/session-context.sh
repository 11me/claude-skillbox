#!/usr/bin/env bash
set -euo pipefail

cat <<'TXT'
You are working in a GitOps repo with this standard layout:

gitops/
├── charts/app/              # Universal Helm chart
├── apps/
│   ├── base/                # Base HelmRelease
│   ├── dev/                 # Dev overlay: values + patches + ExternalSecret
│   └── prod/                # Prod overlay: values + patches + ExternalSecret
└── infra/                   # external-secrets-operator, cert-manager, etc.

Rules:
- No literal secrets in values.yaml. Use ExternalSecret -> Secret, then envFrom.secretRef in chart values.
- Values composition order: chart defaults -> env values.yaml -> ConfigMap (kustomize) -> HelmRelease valuesFrom -> patch overrides
- Prefer ExternalSecret refreshPolicy=OnChange for deterministic updates (unless explicitly requested otherwise).
- Always validate with /helm-validate before completing work.
- Create /checkpoint before ending session.
TXT
