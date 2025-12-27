# Version Matrix Reference

**CRITICAL:** Never hardcode versions. Always use Context7 to get current versions.

**Enforcement:** A PreToolUse hook blocks HelmRelease writes with empty version fields.

## Using Context7 for Latest Versions (REQUIRED)

**Mandatory workflow** - fetch latest versions via Context7 before scaffolding:

### Step 1: Resolve Library ID

```
Tool: resolve-library-id
Parameter: libraryName="cert-manager"
```

### Step 2: Get Documentation with Version

```
Tool: get-library-docs
Parameters:
  context7CompatibleLibraryID: "/jetstack/cert-manager"
  topic: "helm installation"
  mode: "code"
```

## Component Library IDs

| Component | Library Name | Context7 ID |
|-----------|--------------|-------------|
| cert-manager | cert-manager | /jetstack/cert-manager |
| ingress-nginx | ingress-nginx | /kubernetes/ingress-nginx |
| external-secrets | external-secrets | /external-secrets/external-secrets |
| external-dns | external-dns | /kubernetes-sigs/external-dns |
| prometheus | kube-prometheus-stack | /prometheus-community/helm-charts |

## Reference Versions (OUTDATED - DO NOT USE)

**WARNING:** These versions are outdated. Always use Context7 to get current versions.

| Component | Chart Version | App Version |
|-----------|---------------|-------------|
| cert-manager | v1.17.0 | v1.17.0 |
| ingress-nginx | 4.12.0 | 1.12.0 |
| external-secrets | 0.15.0 | v0.15.0 |
| external-dns | 1.16.0 | 0.16.0 |
| kube-prometheus-stack | 68.0.0 | v0.80.0 |

## Flux Components

| Component | API Version | Notes |
|-----------|-------------|-------|
| HelmRelease | helm.toolkit.fluxcd.io/v2 | Stable since Flux 2.0 |
| HelmRepository | source.toolkit.fluxcd.io/v1 | Stable |
| Kustomization | kustomize.toolkit.fluxcd.io/v1 | Stable |
| GitRepository | source.toolkit.fluxcd.io/v1 | Stable |
| ImageRepository | image.toolkit.fluxcd.io/v1 | Stable |
| ImagePolicy | image.toolkit.fluxcd.io/v1 | Stable |
| ImageUpdateAutomation | image.toolkit.fluxcd.io/v1 | Stable |

## Deprecated API Versions

**DO NOT USE:**

| Deprecated | Replacement |
|------------|-------------|
| helm.toolkit.fluxcd.io/v2beta1 | helm.toolkit.fluxcd.io/v2 |
| helm.toolkit.fluxcd.io/v2beta2 | helm.toolkit.fluxcd.io/v2 |
| source.toolkit.fluxcd.io/v1beta2 | source.toolkit.fluxcd.io/v1 |
| kustomize.toolkit.fluxcd.io/v1beta2 | kustomize.toolkit.fluxcd.io/v1 |
| image.toolkit.fluxcd.io/v1beta2 | image.toolkit.fluxcd.io/v1 |
| external-secrets.io/v1beta1 | external-secrets.io/v1 |

## Version Fetching Script

```bash
#!/bin/bash
# scripts/get-latest-version.sh

COMPONENT=$1

case $COMPONENT in
  cert-manager)
    curl -s https://api.github.com/repos/cert-manager/cert-manager/releases/latest | jq -r '.tag_name'
    ;;
  ingress-nginx)
    curl -s https://api.github.com/repos/kubernetes/ingress-nginx/releases/latest | jq -r '.tag_name'
    ;;
  external-secrets)
    curl -s https://api.github.com/repos/external-secrets/external-secrets/releases/latest | jq -r '.tag_name'
    ;;
  external-dns)
    curl -s https://api.github.com/repos/kubernetes-sigs/external-dns/releases/latest | jq -r '.tag_name'
    ;;
  *)
    echo "Unknown component: $COMPONENT"
    exit 1
    ;;
esac
```

## Helm Chart Repositories

| Component | Repository URL |
|-----------|----------------|
| cert-manager | https://charts.jetstack.io |
| ingress-nginx | https://kubernetes.github.io/ingress-nginx |
| external-secrets | https://charts.external-secrets.io |
| external-dns | https://kubernetes-sigs.github.io/external-dns |
| prometheus-stack | https://prometheus-community.github.io/helm-charts |

## Kubernetes Compatibility

| Flux Version | Min K8s | Max K8s |
|--------------|---------|---------|
| 2.4.x | 1.28 | 1.31 |
| 2.3.x | 1.27 | 1.30 |
| 2.2.x | 1.26 | 1.29 |

| cert-manager | Min K8s | Max K8s |
|--------------|---------|---------|
| 1.17.x | 1.26 | 1.31 |
| 1.16.x | 1.26 | 1.31 |
| 1.15.x | 1.25 | 1.30 |

## Upgrade Considerations

### cert-manager

- Check CRD changes between versions
- Apply new CRDs before upgrading HelmRelease
- Test with `kubectl apply --dry-run=server`

### external-secrets

- ESO v1 API is stable (no breaking changes expected)
- Check provider-specific changes in release notes

### ingress-nginx

- Check for deprecated annotations
- Verify IngressClass configuration
- Test with canary deployment

## Version Pinning Strategy

### Development

```yaml
version: ">=1.0.0"  # Allow minor/patch updates
```

### Production

```yaml
version: "1.17.0"  # Pin exact version
```

### Recommended

```yaml
version: "~1.17.0"  # Allow patch updates (1.17.x)
```
