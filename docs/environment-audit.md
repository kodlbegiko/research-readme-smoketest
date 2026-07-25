# Environment capability audit

Audit date: 2026-07-25 (Asia/Taipei).

| Capability | Status | Evidence / constraint | Operational decision |
|---|---|---|---|
| Search public web | AVAILABLE | Browser search/open tools available | Use for literature and official pages |
| Read papers and technical docs | AVAILABLE | HTML and public PDF access available | Prefer primary/official sources |
| Download public data in container | PARTIALLY AVAILABLE | Container DNS is blocked; browser/GitHub connectors can retrieve public content | Freeze extracted records through connectors |
| Execute Python | AVAILABLE | Python 3.13.5 | Primary implementation language |
| Execute Node.js/TypeScript | AVAILABLE | Node 22.16.0, npm 10.9.2 | Not required by selected pilot |
| Install open-source dependencies | PARTIALLY AVAILABLE | Container has no outbound package network; preinstalled packages work; GitHub Actions can install | Standard-library runtime; CI performs full dev install |
| Create files | AVAILABLE | 39 GiB free disk observed | Build full repository locally |
| Create charts | AVAILABLE | Python/matplotlib available | Not necessary; machine-readable tables are clearer for n=19 |
| Create tests | AVAILABLE | pytest 9.0.2 and pytest-cov 7.0.0 | 65 automated tests |
| GitHub connection | AVAILABLE | Authenticated GitHub connector for `kodlbegiko` | Use existing purpose-matched repository |
| Create new repository | UNAVAILABLE | No repository-creation action exposed | Use existing empty `research-readme-smoketest` repository |
| Modify repository / branch / PR | AVAILABLE | Connector exposes file, tree, commit, branch, PR actions | Publish through a feature branch and PR |
| GitHub Actions / logs | AVAILABLE | Workflow run, jobs, status, and logs actions exposed | Validate full toolchain in CI |
| Tag / Release | UNAVAILABLE | No tag or release creation action exposed | Provide exact owner-action release instructions |
| Local `gh` CLI | UNAVAILABLE | `gh` not installed | Use GitHub connector |
| CPU / memory | AVAILABLE | 5 CPUs, 5.9 GiB RAM, no swap | Select CPU-only static analysis |
| GPU | UNTESTED / NOT NEEDED | No GPU required | Avoid model training |

## Local platform snapshot

```text
Linux x86_64 kernel 6.12.13
Python 3.13.5
Node.js 22.16.0
npm 10.9.2
git 2.47.3
CPU: 5 logical CPUs
RAM: 5.9 GiB total, about 5.1 GiB available during audit
Disk: 39 GiB available on /mnt/data filesystem
```

## Consequence for validity

Public README content was retrieved through GitHub's connector rather than by a locally networked acquisition script. The repository includes an optional standard-library acquisition helper, but the published result uses frozen extracted data so third parties can reproduce the analysis offline.
