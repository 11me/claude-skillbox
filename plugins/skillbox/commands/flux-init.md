---
name: flux-init
description: Initialize a new Flux GitOps project with multi-environment structure
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, mcp__plugin_context7_context7__resolve-library-id, mcp__plugin_context7_context7__get-library-docs
---

# Initialize Flux GitOps Project

This command scaffolds a complete Flux GitOps project structure with multi-environment support.

## Workflow

### Step 1: Gather Project Information

Use AskUserQuestion to collect:

1. **Project name** - Name for the GitOps repository
2. **Environments** - Which environments to create (default: dev, staging, prod)
3. **Secrets provider** - AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, or HashiCorp Vault
4. **Infrastructure components** - Select from: cert-manager, ingress-nginx, external-secrets, external-dns, prometheus

### Step 2: Fetch Current Versions

Use Context7 to get latest versions for selected infrastructure components:

```
resolve-library-id: "cert-manager"
get-library-docs: topic="installation" or "helm"
```

Extract version from documentation or use version-matrix.md as fallback.

### Step 3: Create Directory Structure

Create the following structure:

```
{project-name}/
├── clusters/
│   ├── dev/
│   │   ├── flux-system/          # Flux bootstrap (create empty, bootstrap populates)
│   │   ├── 00-crds.yaml
│   │   ├── 02-secrets-operator.yaml
│   │   ├── 10-cert-manager.yaml
│   │   ├── 20-ingress.yaml
│   │   ├── 99-apps.yaml
│   │   └── kustomization.yaml
│   ├── staging/
│   │   └── ... (same structure)
│   └── prod/
│       └── ... (same structure)
├── infra/
│   ├── components/
│   │   ├── base/
│   │   │   └── {component}/
│   │   │       ├── helmrelease.yaml
│   │   │       └── kustomization.yaml
│   │   └── crds/
│   │       └── {component}/
│   │           └── kustomization.yaml
│   ├── dev/
│   │   └── {component}/
│   │       ├── kustomization.yaml
│   │       └── values.yaml
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── apps/
│   ├── base/
│   │   └── .gitkeep
│   ├── dev/
│   │   └── .gitkeep
│   ├── staging/
│   │   └── .gitkeep
│   └── prod/
│       └── .gitkeep
└── charts/
    └── app/                      # Copy from skill assets
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
            ├── _helpers.tpl
            ├── deployment.yaml
            ├── service.yaml
            ├── ingress.yaml
            └── hpa.yaml
```

### Step 4: Generate Manifests

Read examples from skill directory and adapt:

1. **Cluster Kustomizations** - Use `examples/cluster-kustomization.yaml` as template
2. **HelmRelease base** - Use `examples/helmrelease-base.yaml` as template
3. **Environment patches** - Use `examples/helmrelease-env-patch.yaml` as template

### Step 5: Create Infrastructure Components

For each selected component:

1. Create `infra/components/base/{component}/` with HelmRelease
2. Create `infra/components/crds/{component}/` if component has CRDs
3. Create `infra/{env}/{component}/` for each environment
4. Add component to `clusters/{env}/` orchestration

### Step 6: Configure External Secrets

Based on selected secrets provider, create:

1. `infra/components/base/external-secrets/` with HelmRelease
2. `infra/{env}/external-secrets/` with ClusterSecretStore for provider

Use `examples/external-secret.yaml` as reference.

### Step 7: Copy Generic Helm Chart

Copy the generic Helm chart from skill assets:

```
assets/charts/app/ → {project}/charts/app/
```

### Step 8: Create README

Generate a README.md with:

- Project structure overview
- Bootstrap instructions for Flux
- How to add new applications
- Environment-specific configuration

## Output

After completion, provide:

1. Summary of created structure
2. Next steps for Flux bootstrap:
   ```bash
   flux bootstrap github \
     --owner=<org> \
     --repository=<repo> \
     --path=clusters/dev \
     --personal
   ```
3. How to add first application using `/flux-add-app`

## References

- Load `references/project-structure.md` for detailed layout
- Load `references/infra-components.md` for component patterns
- Load `references/version-matrix.md` for version lookup
