# CryptoLedger

CryptoLedger is a production-style Django application deployed on Kubernetes using Helm and managed through GitOps with Argo CD. The project demonstrates modern cloud-native deployment practices, secure networking, TLS automation, persistent storage, and a complete monitoring stack.

## Features

* Django + Django REST Framework
* PostgreSQL database
* JWT authentication
* Gunicorn application server
* Persistent media storage
* Kubernetes-native deployment with Helm
* GitOps deployment using Argo CD
* Automatic TLS certificate management with cert-manager
* Monitoring with Prometheus and Grafana
* PostgreSQL metrics via postgres-exporter
* Django application metrics via django-prometheus
* NetworkPolicies for database isolation
* RBAC examples for users and ServiceAccounts

---

# Architecture

```text
                        Users
                          │
                          ▼
                  Traefik Ingress
                          │
                          ▼
                  Django Service
                          │
                          ▼
                 Django Deployments
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
      Persistent Media          PostgreSQL Service
              │                       │
              ▼                       ▼
             PVC                 PostgreSQL StatefulSet
                                        │
                                        ▼
                                       PVC
```

Monitoring stack:

```text
Django (/metrics)
        │
        ▼
Service
        │
        ▼
ServiceMonitor
        │
        ▼
Prometheus
        │
        ▼
Grafana
```

Database monitoring:

```text
PostgreSQL
      │
      ▼
postgres-exporter
      │
      ▼
Service
      │
      ▼
ServiceMonitor
      │
      ▼
Prometheus
```

---

# Technology Stack

## Backend

* Python
* Django
* Django REST Framework
* Gunicorn

## Database

* PostgreSQL 15

## Containerization

* Docker

## Orchestration

* Kubernetes
* Helm

## GitOps

* Argo CD

## Networking

* Traefik Ingress Controller
* Kubernetes Services
* NetworkPolicies

## Storage

* Longhorn
* PersistentVolumeClaims

## Security

* cert-manager
* RBAC
* TLS certificates

## Monitoring

* kube-prometheus-stack
* Prometheus
* Grafana
* postgres-exporter
* django-prometheus

---

# Project Structure

```text
app/
├── chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── statefulset.yaml
│       ├── ingress.yaml
│       ├── services.yaml
│       ├── configmap.yaml
│       ├── pvc.yaml
│       ├── networkpolicy.yaml
│       └── ...
│
├── config/
├── main/
├── users/
└── manage.py

monitoring/
├── manifests/
├── dashboards/
├── alerts/
├── recording_rules/
├── runbooks/
└── scripts/
```

---

# Deployment Components

The application is deployed using Helm and includes:

* Namespace
* ConfigMap
* Secrets (external)
* Django Deployment
* PostgreSQL StatefulSet
* Services
* Ingress
* PersistentVolumeClaims
* NetworkPolicies
* Migration Job
* Collectstatic Job

---

# Monitoring

The project exports both infrastructure and application metrics.

## Django metrics

Exported using:

* django-prometheus

Example metrics:

* HTTP request count
* Request latency
* Response status codes
* Python runtime metrics
* Process metrics
* Database migration metrics

## PostgreSQL metrics

Exported using:

* postgres-exporter

Example metrics:

* Connections
* Transactions
* Locks
* Cache hit ratio
* WAL
* Query statistics

---

# Security

## NetworkPolicies

Database access is restricted to:

* Django application
* Monitoring components

No other Pods can communicate with PostgreSQL.

## TLS

Certificates are automatically issued and renewed by cert-manager.

## RBAC

The repository includes examples of:

* ClusterRole
* ClusterRoleBinding
* Role
* RoleBinding
* ServiceAccounts

---

# GitOps

Deployment is managed by Argo CD.

Workflow:

```text
Git Push
     │
     ▼
Argo CD
     │
     ▼
Helm
     │
     ▼
Kubernetes Cluster
```

---

# Storage

Persistent storage is provided through Longhorn.

Volumes include:

* PostgreSQL data
* Django media files

---

# Future Improvements

Planned enhancements include:

* Automated Grafana dashboard provisioning
* Blackbox Exporter
* Alertmanager notification channels
* Loki for centralized logging
* CI/CD pipeline integration
* Horizontal Pod Autoscaler
* PodDisruptionBudgets
* Redis and Celery support

---

# Learning Objectives

This project demonstrates practical knowledge of:

* Docker
* Kubernetes
* Helm
* GitOps
* Argo CD
* Stateful applications
* Persistent storage
* Ingress
* TLS management
* RBAC
* Prometheus monitoring
* Grafana dashboards
* NetworkPolicies
* Production-oriented Kubernetes architecture
