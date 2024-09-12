# Architecture Overview
This document describes the architecture of the application designed to handle deep learning models 
with significant memory and loading requirements, and supporting lots of simultaneous users.

## System Architecture
1. User Requests
Users interact with the application via web or app clients. These requests are routed to the backend
services for processing.
2. Load Balancer
AWS Application Load Balancer (ALB) is used to distribute incoming requests across multiple Kubernetes
Pods. This ensures high availability and responsiveness
3. Kubernetes Cluster
The application is deployed on a Kubernetes cluster to manage and scale containerized services. Each
Pod within the cluster may host one or more instances of a model, depending on resource requirements
- Pods: Each Pod can run one or more instances of deep learning models
- Deployments: Manage and scale Pods on demand
4. Compute Resources
Amazon EC2 instances with high memory and CPU are used for running the model containers.
5. Model Storage
Amazon S3 is used to store large model files. This allows for efficient storage, versioning and 
model retrieval.
6. Database
Amazon RDS manages database interactions for persisting user data and model metadata. SQLite is only
used as the engine for local development (possibly upgrade it to Postgresql)
7. Monitoring and Logging
AWS CloudWatch is used for monitoring application performance and logging. This also includes setting
up alarms for metrics like memory usage and latency.

## Component Interaction
1. User requests are sent to the Load Balancer
2. The Load Balancer routes requests to appropriate Kubernetes Pods based on traffic and load
3. Each Kubernetes Pod runs on one or more instances of deep learning models
4. Models are loaded from Amazon S3 into memory when needed
5. User data and model metadata are persisted in Amazon RDS
6. AWs Cloudwatch monitors the system and logs performance metrics

## Code Evolution
### Model Loading and Caching
- Lazy Loading: Models are loaded into memory only when needed
- Caching: Implement caching to keep models in memory for reuse
### Concurrency Handling
- Asynchronous Processing: Use async frameworks/functions for efficient request handling
- Concurrency Control: Manage concurrent access to models to prevent data corruption

## Scaling Strategy
1. Containerization with Docker: Each model is containerized using Docker
2. Kubernetes for Orchestration: Deploy and manage containers using Kubernetes, with autoscaling
to handle increased load
3. AWS Infrastructure: Utilize AWS services like EKS for Kubernetes management, S3 for model 
storage, and RDS for database management 
