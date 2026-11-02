# Acme Shop

Services behind the Acme online shop: **checkout**, **payments**, **inventory** and the **gateway** in front of them.
Every push to `main` that changes a service runs the **Deploy to production** workflow, which records a
GitHub Deployment to the `production` environment.

| Service | Path | Team | Version |
| --- | --- | --- | --- |
| checkout | `services/checkout` | checkout-team | see `services/checkout/VERSION` |
| payments | `services/payments` | payments-team | see `services/payments/VERSION` |
| inventory | `services/inventory` | supply-chain | see `services/inventory/VERSION` |
| gateway | `services/gateway` | platform-eng | see `services/gateway/VERSION` |

Production manifests live in `deploy/production/`, one per service; the image tag follows the service's `VERSION`.

## Working on a service

```bash
scripts/run-tests.sh          # unit tests for every service, standard library only
```

Open a pull request with the template: what changes, why, risk and rollback.

## Releasing

```bash
scripts/simulate-release.sh checkout 12.6.2            # release branch + PR link
scripts/simulate-release.sh checkout 12.6.2 --direct   # straight to main
```

## Monitoring

Production is monitored in Paprika (workspace *Acme Operations*). Paprika's GitHub connection reads this
repository's commits, pull requests and deployments to explain incidents, and its agents open follow-up
issues here.
