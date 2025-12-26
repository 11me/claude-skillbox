# GitOps Project Structure Reference

## Complete Directory Layout

```
gitops/
├── clusters/                           # Flux orchestration (per-cluster)
│   ├── dev/
│   │   ├── 00-crds.yaml                # CRD Kustomizations
│   │   ├── 02-secrets-operator.yaml    # ESO operator
│   │   ├── 03-secrets-store.yaml       # ClusterSecretStore
│   │   ├── 04-external-dns.yaml        # DNS automation (optional)
│   │   ├── 05-ingress-nginx.yaml       # Ingress controller
│   │   ├── 06-cert-manager.yaml        # TLS certificates
│   │   ├── 07-cert-manager-issuer.yaml # ClusterIssuer
│   │   ├── 99-apps-dev.yaml            # Application deployment
│   │   ├── flux-system/                # Flux bootstrap
│   │   │   ├── gotk-components.yaml    # Flux controllers
│   │   │   ├── gotk-sync.yaml          # GitRepository + Kustomization
│   │   │   └── kustomization.yaml
│   │   └── kustomization.yaml          # Root kustomization
│   ├── staging/                        # Same structure as dev
│   └── prod/                           # Same structure as dev
│
├── infra/                              # Infrastructure components
│   ├── components/
│   │   ├── base/                       # Base HelmReleases
│   │   │   ├── cert-manager/
│   │   │   │   ├── helm.yaml           # HelmRepository + HelmRelease
│   │   │   │   └── kustomization.yaml
│   │   │   ├── external-dns/
│   │   │   ├── external-secrets-operator/
│   │   │   ├── ingress-nginx/
│   │   │   └── secrets-store/          # ClusterSecretStore
│   │   │
│   │   └── crds/                       # CRD management
│   │       ├── cert-manager/
│   │       │   ├── kustomization.yaml  # GitRepository + Kustomization
│   │       │   └── kustomization.yaml
│   │       ├── external-secrets/
│   │       └── prometheus-operator/    # Optional
│   │
│   ├── dev/                            # Dev environment values
│   │   ├── cert-manager/
│   │   │   ├── kustomization.yaml      # References base + values
│   │   │   └── values.yaml
│   │   ├── cert-manager-issuer/
│   │   │   ├── kustomization.yaml
│   │   │   └── clusterissuer.yaml      # LetsEncrypt issuer
│   │   ├── external-dns/
│   │   ├── ingress-nginx/
│   │   ├── secrets-operator/
│   │   └── secrets-store/
│   │
│   ├── staging/                        # Staging values
│   └── prod/                           # Prod values
│
├── apps/                               # Application deployments
│   ├── base/                           # Base HelmReleases
│   │   └── {app-name}/
│   │       ├── helm.yaml               # HelmRelease referencing charts/app
│   │       └── kustomization.yaml
│   │
│   ├── dev/                            # Dev environment
│   │   ├── {app-name}/
│   │   │   ├── kustomization.yaml      # Patches + ConfigMapGenerator
│   │   │   ├── kustomizeconfig.yaml    # ConfigMap name reference
│   │   │   ├── values.yaml             # Dev values
│   │   │   ├── patches.yaml            # Image tag with marker
│   │   │   └── secrets/
│   │   │       └── {app}.external.yaml # ExternalSecret
│   │   ├── image-automation.yaml       # All ImageRepository/Policy/Automation
│   │   ├── namespace.yaml              # Namespace with ESO label
│   │   └── kustomization.yaml          # Root app kustomization
│   │
│   ├── staging/
│   └── prod/
│
└── charts/                             # Helm charts
    └── app/                            # Generic application chart
        ├── Chart.yaml
        ├── values.yaml
        ├── README.md
        └── templates/
            ├── _helpers.tpl
            ├── deployment.yaml
            ├── service.yaml
            ├── ingress.yaml
            ├── hpa.yaml
            ├── pdb.yaml
            └── serviceaccount.yaml
```

## File Contents Reference

### clusters/{env}/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - 00-crds.yaml
  - 02-secrets-operator.yaml
  - 03-secrets-store.yaml
  - 05-ingress-nginx.yaml
  - 06-cert-manager.yaml
  - 07-cert-manager-issuer.yaml
  - 99-apps-dev.yaml
```

### clusters/{env}/00-crds.yaml

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: crds
  namespace: flux-system
spec:
  interval: 10m
  path: ./infra/components/crds
  prune: false  # CRITICAL: Never delete CRDs
  sourceRef:
    kind: GitRepository
    name: flux-system
  healthChecks:
    - apiVersion: kustomize.toolkit.fluxcd.io/v1
      kind: Kustomization
      name: cert-manager-crds
    - apiVersion: kustomize.toolkit.fluxcd.io/v1
      kind: Kustomization
      name: external-secrets-crds
```

### clusters/{env}/99-apps-dev.yaml

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps-dev
  namespace: flux-system
spec:
  dependsOn:
    - name: ingress-nginx
    - name: secrets-store
  interval: 15m
  timeout: 10m
  path: ./apps/dev
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
  wait: true
```

### infra/components/base/{component}/helm.yaml

```yaml
---
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata:
  name: component-name
  namespace: flux-system
spec:
  interval: 1h
  url: https://charts.example.io

---
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: component-name
  namespace: flux-system
spec:
  interval: 30m
  targetNamespace: component-namespace
  chart:
    spec:
      chart: chart-name
      version: "1.0.0"
      sourceRef:
        kind: HelmRepository
        name: component-name
        namespace: flux-system
  install:
    createNamespace: true
    crds: Skip
  upgrade:
    remediation:
      retries: 3
    crds: Skip
  valuesFrom:
    - kind: ConfigMap
      name: component-name-values
      valuesKey: values.yaml
```

### infra/{env}/{component}/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: flux-system

resources:
  - ../../components/base/component-name

generatorOptions:
  disableNameSuffixHash: true

configMapGenerator:
  - name: component-name-values
    files:
      - values.yaml
```

### apps/{env}/{app}/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: app-namespace

resources:
  - ../../base/app-name
  - secrets/app-name.external.yaml

patches:
  - path: patches.yaml

generatorOptions:
  disableNameSuffixHash: true

configMapGenerator:
  - name: app-name-values
    files:
      - values.yaml=values.yaml

configurations:
  - kustomizeconfig.yaml
```

### apps/{env}/{app}/patches.yaml

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: app-name
spec:
  values:
    image:
      tag: dev-abc123-12345 # {"$imagepolicy": "flux-system:app-name-dev:tag"}
```

### apps/{env}/{app}/kustomizeconfig.yaml

```yaml
nameReference:
  - kind: ConfigMap
    version: v1
    fieldSpecs:
      - path: spec/valuesFrom/name
        kind: HelmRelease
  - kind: Secret
    version: v1
    fieldSpecs:
      - path: spec/valuesFrom/name
        kind: HelmRelease
```

### apps/{env}/namespace.yaml

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: app-namespace
  labels:
    eso.domain.com/enabled: "true"  # Required for ClusterSecretStore access
```

## Naming Conventions

| Resource | Pattern | Example |
|----------|---------|---------|
| HelmRelease | `{app-name}` | `fce-web` |
| ConfigMap (values) | `{app-name}-values` | `fce-web-values` |
| ExternalSecret | `{app-name}-{env}` | `fce-web-dev` |
| ImageRepository | `{app-name}-{env}` | `fce-web-dev` |
| ImagePolicy | `{app-name}-{env}` | `fce-web-dev` |
| ImageUpdateAutomation | `{app-name}-auto-{env}` | `fce-web-auto-dev` |
| Namespace | `{env}` or `{app-name}` | `dev` |

## Environment Differences

| Aspect | Dev | Staging | Prod |
|--------|-----|---------|------|
| Image tag pattern | `dev-{sha}-{run_id}` | `staging-{sha}` | `v{semver}` |
| ImagePolicy | numerical (run_id) | numerical | semver |
| Auto-deploy | On push to main | On PR merge | On git tag |
| Replicas | 1-2 | 2 | 3+ |
| Resource limits | Low | Medium | High |
| Certificate issuer | letsencrypt-staging | letsencrypt-staging | letsencrypt-prod |
