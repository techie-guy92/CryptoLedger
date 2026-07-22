# CryptoLedger

[![Pipeline Status](https://gitlab.com/techie-guy92/cryptoledger/badges/main/pipeline.svg)](https://gitlab.com/techie-guy92/cryptoledger/-/pipelines)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-grade Django application deployed on Kubernetes with GitOps, featuring automated CI/CD, TLS management, persistent storage, and a complete observability stack.

---

## Quick Start

```bash
# Clone the repository
git clone git@gitlab.com:techie-guy92/cryptoledger.git
cd cryptoledger

# Install dependencies
cd app/source
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

---

## Overview

CryptoLedger is a Django-based cryptocurrency portfolio tracking application built for modern cloud-native environments. It leverages Kubernetes, Helm, and Argo CD for GitOps-driven deployments, ensuring consistency and reliability across environments.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                USERS                                        │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 Main                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRAEFIK INGRESS                                     │
│                    (TLS termination with cert-manager)                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DJANGO SERVICE                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│   DJANGO DEPLOYMENT     │ │   POSTGRES STATEULSET   │ │   PERSISTENT STORAGE    │
│   (3 replicas)          │ │   (1 replica)           │ │   (Longhorn PVCs)       │
│   - Gunicorn            │ │   - PostgreSQL 15       │ │   - Media files         │
│   - django-prometheus   │ │   - postgres-exporter   │ │   - Database            │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
```

---

## Technology Stack

### Backend
| Component             | Technology                         |
|-----------------------|------------------------------------|
| **Framework**         | Django 5.1 + Django REST Framework |
| **Server**            | Gunicorn                           |
| **Database**          | PostgreSQL 15                      |
| **Authentication**    | JWT (SimpleJWT)                    |
| **API Documentation** | drf-spectacular (OpenAPI)          |

### Infrastructure
| Component              | Technology                          |
|------------------------|-------------------------------------|
| **Orchestration**      | Kubernetes                          |
| **Package Management** | Helm                                |
| **CI/CD**              | GitLab CI                           |
| **GitOps**             | Argo CD                             |
| **Container Registry** | Local registry (192.168.122.1:5000) |

### Networking & Security
| Component              | Technology               |
|------------------------|--------------------------|
| **Ingress Controller** | Traefik                  |
| **TLS Management**     | cert-manager             |
| **Network Policies**   | Kubernetes NetworkPolicy |
| **RBAC**               | Kubernetes RBAC          |

### Storage
| Component            | Technology             |
|----------------------|------------------------|
| **Storage Provider** | Longhorn               |
| **Persistence**      | PersistentVolumeClaims |

### Monitoring
| Component               | Technology        |
|-------------------------|-------------------|
| **Metrics Collection**  | Prometheus        |
| **Visualization**       | Grafana           |
| **Application Metrics** | django-prometheus |
| **Database Metrics**    | postgres-exporter |
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
├── argocd/                       # Argo CD GitOps
│   └── applications/
│       ├── cryptoledger-application.yaml
│       └── cryptoledger-monitoring-application.yaml
│
├── monitoring/                   # Monitoring stack
│   ├── manifests/
│   ├── dashboards/
│   ├── alerts/
│   ├── recording_rules/
│   ├── runbooks/
│   └── scripts/
│
├── secrets/                      # Secrets (encrypted)
│   └── secret.yaml
│
├── .gitlab-ci.yml               # CI/CD pipeline
└── README.md
```

---

## CI/CD Pipeline

The project uses **GitLab CI** with a self-hosted runner for automated builds and deployments.

### Pipeline Stages

```yaml
stages:
  - lint           # Code formatting checks (Black, isort)
  - build          # Docker image build and push
  - test           # Django unit tests
  - update-manifests # Update Helm values with new image tag
```

### Workflow

```
1. Push code to GitLab
         ↓
2. Lint: Black & isort checks
         ↓
3. Build: Docker image → Local registry
         ↓
4. Test: Django unit tests
         ↓
5. Update manifests: values.yaml updated
         ↓
6. Argo CD detects change → Deploys to Kubernetes
```

---

## Deployment

### Prerequisites

- Kubernetes cluster
- Helm 3+
- Argo CD
- cert-manager
- Longhorn (or other CSI storage)
- Local container registry

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

The application is managed via Argo CD using the **App-of-Apps** pattern:

```bash
# Apply the root application
kubectl apply -f argocd/root.yaml
```

Argo CD will automatically:
- Deploy the application
- Monitor for drift
- Auto-sync on Git changes
- Rollback on failure

---

## Monitoring

### Application Metrics

Exported via `django-prometheus` at `/metrics` endpoint:
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

Pre-configured Grafana dashboards:
- Django Application Dashboard (ID: 17613)
- PostgreSQL Dashboard (ID: 9628)
- Blackbox Exporter Dashboard (ID: 13659)
- GitLab Dashboard (ID: 3749)

---

## Security

| Feature              | Implementation                                        |
|----------------------|-------------------------------------------------------|
| **TLS**              | Automatic certificates via cert-manager               |
| **Network Policies** | PostgreSQL access restricted to Django and monitoring |
| **Secrets**          | Encrypted with Sealed Secrets or SOPS                 |
| **RBAC**             | Role-based access control examples included           |
| **Authentication**   | JWT tokens with configurable lifetimes                |

---

## Environment Variables

Create a `.env` file in `app/source/`:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,crypto.local
DATABASE_URL=postgresql://user:pass@postgres:5432/db
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Merge Request

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
- Longhorn Storage
- NFS
- cert-manager
- Traefik Ingress
