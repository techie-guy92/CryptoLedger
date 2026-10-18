# CryptoLedger

[![Pipeline Status](https://gitlab.com/techie-guy92/cryptoledger/badges/main/pipeline.svg)](https://gitlab.com/techie-guy92/cryptoledger/-/pipelines)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-grade Django application deployed on Kubernetes with GitOps, featuring automated CI/CD, TLS management, persistent storage, and a complete observability stack.

---

## Overview

CryptoLedger is a Django-based cryptocurrency portfolio tracking application built for modern cloud-native environments. It leverages Kubernetes, Helm, and Argo CD for GitOps-driven deployments, ensuring consistency and reliability across environments.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 USERS                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             NGINX INGRESS                                   │
│                    (TLS termination with cert-manager)                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DJANGO SERVICE (ClusterIP)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│   DJANGO DEPLOYMENT     │ │   POSTGRES StatefulSet  │ │   PERSISTENT STORAGE    │
│   (3 replicas)          │ │   (1 replica)           │ │   (Ceph PVCs)           │
│   - Gunicorn            │ │   - PostgreSQL 15       │ │   - Media files         │
│   - django-prometheus   │ │   - postgres-exporter   │ │   - Database            │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
```

---

## Technology Stack

### Backend

| Component | Technology |
|---|---|
| **Framework** | Django 5.1 + Django REST Framework |
| **Server** | Gunicorn |
| **Database** | PostgreSQL 15 |
| **Authentication** | JWT (SimpleJWT) |
| **API Documentation** | drf-spectacular (OpenAPI) |

### Infrastructure

| Component | Technology |
|---|---|
| **Orchestration** | Kubernetes |
| **Package Management** | Helm |
| **CI/CD** | GitLab CI |
| **GitOps** | Argo CD |
| **Container Registry** | Local registry (`<registry-host>:5000`) |

### Networking & Security

| Component | Technology |
|---|---|
| **CNI** | Calico |
| **Ingress Controller** | Nginx |
| **Load Balancer** | MetalLB |
| **TLS Management** | cert-manager |
| **Network Policies** | Kubernetes NetworkPolicy |
| **RBAC** | Kubernetes RBAC |

### Storage

| Component | Technology |
|---|---|
| **Storage Provider** | Ceph (RBD & CephFS) |
| **Persistence** | PersistentVolumeClaims |

### Monitoring

| Component | Technology |
|---|---|
| **Metrics Collection** | Prometheus |
| **Visualization** | Grafana |
| **Application Metrics** | django-prometheus |
| **Database Metrics** | postgres-exporter |
| **Blackbox Monitoring** | Blackbox Exporter |

---

## Project Structure

```
CryptoLedger/
├── app/
│   ├── chart/                    # Helm chart
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       ├── statefulset.yaml
│   │       ├── ingress.yaml
│   │       ├── services.yaml
│   │       ├── configmap.yaml
│   │       ├── pvc.yaml
│   │       ├── networkpolicy.yaml
│   │       ├── migration-job.yaml
│   │       └── collectstatic-job.yaml
│   └── source/                   # Django application
│       ├── config/
│       ├── main/
│       ├── users/
│       ├── manage.py
│       ├── requirements.txt
│       └── Dockerfile
│
├── argocd/                       # Argo CD GitOps (App-of-Apps)
│   ├── root.yaml                 # Root application
│   └── applications/
│       ├── cryptoledger-app-application.yaml
│       └── cryptoledger-monitoring-application.yaml
│
├── monitoring/                   # Monitoring stack
│   ├── manifests/
│   ├── dashboards/
│   ├── alerts/
│   ├── runbooks/
│   └── scripts/
│
├── secrets/                      # Encrypted secrets
│   └── secret.yaml
│
├── .gitlab-ci.yml                # CI/CD pipeline
├── Jenkinsfile                   # Optional Jenkins pipeline
└── README.md
```

---

## Local Development

The Quick Start below runs Django directly on your host with SQLite, which is suitable **only for local development**. For production, deploy via Helm/Argo CD (see [Deployment](#deployment)).

### Prerequisites

- Python 3.12+
- `pip` and `virtualenv`

### Steps

```bash
# Clone the repository
git clone git@gitlab.com:techie-guy92/cryptoledger.git
cd cryptoledger/app/source

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations (SQLite by default for local dev)
python manage.py migrate

# Run the development server
python manage.py runserver
```

> **Note:** For a full local stack (PostgreSQL, monitoring), use `app/source/docker-compose.yml`.

---

## CI/CD Pipeline

The project uses **GitLab CI** with a self-hosted runner for automated builds and deployments.

### Pipeline Stages

```yaml
stages:
  - lint              # Code formatting checks (Black, isort)
  - test              # Django unit tests
  - build             # Docker image build and push
  - update-manifests  # Update Helm values with new image tag
```

### Workflow

```
1. Push code to GitLab
         ↓
2. Lint: Black & isort checks
         ↓
3. Test: Django unit tests
         ↓
4. Build: Docker image → Local registry
         ↓
5. Update manifests: values.yaml updated
         ↓
6. Argo CD detects change → Deploys to Kubernetes
```

---

## Deployment

### Prerequisites

- Kubernetes 1.28+
- Helm 3.12+
- Argo CD 2.9+
- cert-manager 1.13+
- Ceph (Rook) or any CSI-compatible storage
- A reachable container registry (local registry in dev setups)

### Deploy with Helm

```bash
# Install the application
helm upgrade --install cryptoledger ./app/chart \
  --namespace crypto \
  --create-namespace \
  --set image.tag=v1.3.0

# Uninstall
helm uninstall cryptoledger -n crypto
```

### GitOps with Argo CD

The application is managed via Argo CD using the **App-of-Apps** pattern. `argocd/root.yaml` is the parent application that reconciles the children under `argocd/applications/`.

```bash
# Apply the root application
kubectl apply -f argocd/root.yaml
```

Argo CD will automatically:

- Deploy the application
- Monitor for drift
- Auto-sync on Git changes
- Roll back on failure

### Verify the Deployment

```bash
# Check pods and services
kubectl get pods,svc -n crypto

# Check the ingress and certificate
kubectl get ingress,certificate -n crypto

# Health check (adjust host to your ingress hostname)
curl -k https://crypto.local/healthz
```

---

## Monitoring

### Application Metrics

Exported via `django-prometheus` at `/metrics`:

- HTTP request count and latency
- Response status codes
- Python runtime metrics
- Database migration status

### Database Metrics

Exported via `postgres-exporter`:

- Connection count
- Transaction throughput
- Cache hit ratio
- WAL statistics

### Dashboards

Pre-configured Grafana dashboards are auto-provisioned from `monitoring/dashboards/`:

- Django Application Dashboard (ID: 17613)
- PostgreSQL Dashboard (ID: 9628)
- Blackbox Exporter Dashboard (ID: 13659)
- GitLab Dashboard (ID: 3749)

---

## Security

| Feature | Implementation |
|---|---|
| **TLS** | Automatic certificates via cert-manager |
| **Network Policies** | PostgreSQL access restricted to Django and monitoring |
| **Secrets** | SOPS-encrypted files under `secrets/` (Sealed Secrets supported as an alternative) |
| **RBAC** | Role-based access control examples included |
| **Authentication** | JWT tokens with configurable lifetimes |

---

## Environment Variables

Create a `.env` file in `app/source/`:

```env
# Core
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,crypto.local

# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/db

# JWT (SimpleJWT)
JWT_ACCESS_TOKEN_LIFETIME=15m
JWT_REFRESH_TOKEN_LIFETIME=7d

# Required behind Nginx Ingress with TLS
CSRF_TRUSTED_ORIGINS=https://crypto.local
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
USE_X_FORWARDED_HOST=True
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Format your code locally with `black .` and `isort .`
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing`)
6. Open a Merge Request

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Soheil Daliri**

- GitLab: [@techie-guy92](https://gitlab.com/techie-guy92)
- GitHub: [@techie-guy92](https://github.com/techie-guy92)

---

## Acknowledgments

- Django REST Framework
- Argo CD
- GitLab CI
- Prometheus & Grafana
- Rook Ceph
- Calico
- MetalLB
- Nginx Ingress
- cert-manager
