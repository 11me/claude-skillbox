---
name: flux-add-infra
description: Add infrastructure component (cert-manager, ingress-nginx, external-secrets, etc.) to GitOps project
arguments:
  - name: component
    description: "Component name: cert-manager, ingress-nginx, external-secrets, external-dns, prometheus, metrics-server"
    required: true
allowed-tools: Read, Write, Edit, Glob, Grep, mcp__plugin_context7_context7__resolve-library-id, mcp__plugin_context7_context7__get-library-docs
---

# Add Infrastructure Component

This command adds an infrastructure component to an existing Flux GitOps project.

## Supported Components

| Component | Chart Repository | Has CRDs |
|-----------|------------------|----------|
| cert-manager | jetstack | Yes |
| ingress-nginx | ingress-nginx | No |
| external-secrets | external-secrets | Yes |
| external-dns | bitnami | No |
| prometheus | prometheus-community | Yes |
| metrics-server | metrics-server | No |

## Workflow

### Step 1: Validate Component

Check that `{component}` is in the supported list. If not, inform user and suggest alternatives.

### Step 2: Detect Project Structure

Use Glob to find existing GitOps structure:

```
**/clusters/*/kustomization.yaml
**/infra/components/base/*/helmrelease.yaml
```

Identify:
- Available environments (dev, staging, prod)
- Existing infrastructure components
- Project root directory

### Step 3: Get Latest Version

Use Context7 to fetch current chart version:

```
resolve-library-id: "{component}"
get-library-docs: topic="helm" or "installation"
```

Extract version or use `references/version-matrix.md` as fallback.

### Step 4: Create Base Component

Create `infra/components/base/{component}/`:

**helmrelease.yaml:**
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: {component}
spec:
  interval: 30m
  chart:
    spec:
      chart: {chart-name}
      version: "{version}"
      sourceRef:
        kind: HelmRepository
        name: {repo-name}
        namespace: flux-system
  install:
    crds: Skip  # If has CRDs
  upgrade:
    crds: Skip
    remediation:
      retries: 3
```

**kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: {namespace}
resources:
  - helmrelease.yaml
```

### Step 5: Create CRDs (if applicable)

If component has CRDs, create `infra/components/crds/{component}/`:

**kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - https://github.com/{org}/{repo}/releases/download/v{version}/crds.yaml
```

### Step 6: Create Environment Overlays

For each environment (dev, staging, prod), create `infra/{env}/{component}/`:

**kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../components/base/{component}
configMapGenerator:
  - name: {component}-values
    files:
      - values.yaml
generatorOptions:
  disableNameSuffixHash: true
```

**values.yaml:**
```yaml
# Environment-specific values for {component}
# Customize per environment
```

### Step 7: Update Cluster Orchestration

For each environment, update `clusters/{env}/` with appropriate numbered Kustomization:

Determine correct number based on dependencies:
- 00: CRDs (prune: false)
- 02: secrets-operator (external-secrets)
- 10: cert-manager
- 20: ingress controllers
- 30: monitoring (prometheus, metrics-server)
- 40: dns (external-dns)

Create `clusters/{env}/XX-{component}.yaml`:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: {component}
  namespace: flux-system
spec:
  interval: 1h
  retryInterval: 1m
  timeout: 5m
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./infra/{env}/{component}
  prune: true
  wait: true
  dependsOn:
    - name: {dependency}  # Based on component type
```

Update `clusters/{env}/kustomization.yaml` to include new file.

### Step 8: Create HelmRepository (if needed)

Check if HelmRepository exists in `infra/components/base/sources/`. If not, create:

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata:
  name: {repo-name}
  namespace: flux-system
spec:
  interval: 1h
  url: {repo-url}
```

## Component-Specific Patterns

### cert-manager

- Namespace: cert-manager
- CRDs: Yes (install separately)
- Dependencies: CRDs first
- Common values: installCRDs: false

### ingress-nginx

- Namespace: ingress-nginx
- Dependencies: cert-manager (for TLS)
- Common values: controller.service.type, controller.ingressClassResource

### external-secrets

- Namespace: external-secrets
- CRDs: Yes
- Dependencies: CRDs first
- Requires: ClusterSecretStore configuration per environment

### prometheus

- Namespace: monitoring
- CRDs: Yes (ServiceMonitor, PodMonitor, etc.)
- Dependencies: CRDs first
- Common values: server.retention, alertmanager.enabled

## Output

After completion, provide:

1. Summary of created files
2. Reminder to commit and push changes
3. How to verify deployment: `flux reconcile kustomization {component} --with-source`

## References

- Load `references/infra-components.md` for detailed patterns
- Load `references/version-matrix.md` for versions
- Use `examples/helmrelease-base.yaml` as template
