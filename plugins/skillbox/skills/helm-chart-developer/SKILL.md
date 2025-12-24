---
name: helm-chart-developer
description: Build/refactor production Helm charts and GitOps deploy via Flux HelmRelease + Kustomize overlays. Includes External Secrets Operator patterns (ExternalSecret per app/env + ClusterSecretStore) and optional chart-managed ExternalSecret templates. Use when authoring Helm charts, converting raw manifests to Helm, designing values/schema, or debugging helm template/lint/dry-run issues.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# Helm Chart Developer

## Purpose / When to Use

Use this skill when:
- Creating new Helm charts from scratch
- Converting raw Kubernetes manifests to Helm
- Designing values.yaml API and schema
- Setting up GitOps deployment with Flux HelmRelease
- Integrating External Secrets Operator (ESO)
- Debugging `helm template`, `helm lint`, `helm install --dry-run`
- Setting up multi-environment overlays (dev/prod)

## Definition of Done (DoD)

Before completing any Helm chart work:

1. **Linting**: `helm lint .` passes
2. **Template rendering**: `helm template <release> .` succeeds
3. **Dry-run**: `helm install <release> . --dry-run --debug` works
4. **Two secrets modes validated**:
   - GitOps mode: `--set secrets.existingSecretName=<name>`
   - Chart-managed ESO: `--set secrets.externalSecret.enabled=true`

Run `/helm-validate` to execute all checks.

## Step-by-Step Workflow

### 1. Chart Structure

```
charts/app/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── externalsecret.yaml  # optional, gated
│   ├── hpa.yaml
│   ├── pdb.yaml
│   └── serviceaccount.yaml
```

### 2. Values API Contract

See [reference-gitops-eso.md](reference-gitops-eso.md) for full details.

Key sections:
- `image`: repository, tag, pullPolicy
- `secrets`: existingSecretName, externalSecret.*, inject.envFrom
- `service`: enabled, type, port
- `ingress`: enabled, className, hosts, tls
- `resources`: requests, limits
- `autoscaling`: enabled, minReplicas, maxReplicas

### 3. Secrets Integration

**Mode A: ExternalSecret in Overlay (Recommended)**

Chart only references secret by name:
```yaml
# values.yaml
secrets:
  existingSecretName: "app-secrets"
  inject:
    envFrom: true
```

ExternalSecret lives in GitOps overlay, not in chart.

**Mode B: Chart-Managed ExternalSecret (Optional)**

Chart renders ExternalSecret when enabled:
```yaml
secrets:
  externalSecret:
    enabled: true
    refreshInterval: 1h
    refreshPolicy: OnChange
    secretStoreRef:
      kind: ClusterSecretStore
      name: aws-secrets-manager
    dataFrom:
      extractKey: "fce/dev/app"
    target:
      name: "app-secrets"
      creationPolicy: Owner
```

### 4. Flux + Kustomize Recipe

**Values Composition Order** (important!):
1. Chart defaults (`charts/app/values.yaml`)
2. Environment values (`apps/dev/app/values.yaml`)
3. ConfigMap via Kustomize generator
4. HelmRelease `valuesFrom` references ConfigMap
5. HelmRelease `spec.values` patches (highest priority)

See snippets:
- [flux-helmrelease.base.yaml](snippets/flux-helmrelease.base.yaml)
- [flux-helmrelease.dev.patch.yaml](snippets/flux-helmrelease.dev.patch.yaml)
- [kustomize.configmapgenerator.yaml](snippets/kustomize.configmapgenerator.yaml)

### 5. ESO Patterns

**ClusterSecretStore** (cluster-wide):
```yaml
apiVersion: external-secrets.io/v1
kind: ClusterSecretStore
metadata:
  name: aws-secrets-manager
spec:
  conditions:
    - namespaceSelector:
        matchLabels:
          eso.fce.global/enabled: "true"
  provider:
    aws:
      service: SecretsManager
      region: me-central-1
```

**ExternalSecret** (per app/env):
```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
spec:
  refreshPolicy: OnChange  # GitOps-deterministic
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-secrets-manager
  dataFrom:
    - extract:
        key: fce/dev/app
  target:
    name: app-secrets
    creationPolicy: Owner
```

### 6. Pitfalls

- **CRD ordering**: ESO CRDs must exist before ExternalSecret. Use Flux Kustomization `dependsOn`.
- **OpenAPI validation**: Use `install.disableOpenAPIValidation: true` in HelmRelease if needed.
- **No secrets in values.yaml**: Always use ExternalSecret or existingSecretName.

## Examples

Prompts that should activate this skill:

1. "Create a Helm chart for my Node.js app"
2. "Convert these Kubernetes manifests to Helm"
3. "Add External Secrets integration to my chart"
4. "Set up Flux HelmRelease for my app"
5. "Debug why helm template is failing"
6. "Design values.yaml schema for multi-environment deployment"
7. "Add ingress with TLS to my Helm chart"
8. "Integrate AWS Secrets Manager with my chart"
9. "Set up Kustomize overlays for dev and prod"
10. "Fix helm lint errors in my chart"

## Related Files

- [reference-gitops-eso.md](reference-gitops-eso.md) - Full GitOps + ESO reference
- [snippets/](snippets/) - Ready-to-use YAML snippets

## Version History

- 1.0.0 — Initial release with Flux + ESO patterns
