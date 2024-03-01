# CI/CD Pipeline Documentation

## Overview

This document outlines the Continuous Integration and Continuous Deployment (CI/CD) pipeline designed for FarpointOI project hosted on an AWS EC2 server. The pipeline is triggered by changes pushed or merged into the `dev` branch. Its primary function is to automate the process of building Docker images for all services, pushing them to AWS Elastic Container Registry (ECR), and deploying the updated images on the server, replacing the old containers and images with new ones.

### Pipeline Flow

1. **Trigger**: The pipeline is triggered by any `push` event to the `dev` branch.

2. **Environment Setup**: Runs on an `ubuntu-latest` GitHub Actions runner.

3. **Checkout Code**: The repository code is checked out for use in the pipeline.

4. **Docker Buildx Setup**: (Optional) Set up Docker Buildx for advanced build capabilities.

5. **Amazon ECR Login**: Logs into Amazon ECR with credentials provided through GitHub secrets.

6. **SSL Certificate Configuration**: Creates SSL certificate and key files for the server and transcription services from GitHub secrets.

7. **Build Docker Images**: Utilizes `docker-compose` to build Docker images for the services, injecting environment variables from GitHub secrets.

8. **Tag and Push Docker Images**: Tags the built images with `latest` and pushes them to designated AWS ECR repositories.

9. **Deployment**: The deployment job is dependent on the build-and-push job. It sets up SSH access to the EC2 server, creates a Docker network (if not already present), and executes a series of commands on the server to deploy the new images.

## Key Components

### GitHub Secrets

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`: AWS credentials for ECR access.
- `SSL_CERT`, `SSL_KEY`: SSL certificate and key for secure communication.
- Various application-specific environment variables like `REACT_APP_API_URL`, `FLASK_APP`, `POSTGRES_USER`, etc., which are crucial for the services to run correctly.

### Jobs

#### build-and-push

- **Set up Docker Buildx**: Enhances the building of Docker images with additional features.
- **Login to Amazon ECR**: Authentication step to allow pushing images to ECR.
- **Create SSL files for server and transcription**: Ensures secure connections by using SSL certificates.
- **Build Docker images**: Builds images for all services, making them ready for deployment.
- **Tag and push Docker images to AWS ECR**: Updates the ECR with the latest images for each service.

#### deploy-to-server

- **Setup SSH**: Configures SSH access to the EC2 server for deployment commands.
- **Create Docker Network**: Ensures that a network exists for Docker containers to communicate.
- **Deploy to server**: Executes a series of commands to pull the new Docker images from ECR, stop and remove old containers, and start new ones with the updated images. It also prunes any unused Docker images and updates Nginx configuration if necessary.

## Conclusion

The CI/CD pipeline facilitates the automated building, pushing, and deployment of Docker images for the project's services. It leverages GitHub Actions for automation, AWS ECR for Docker image storage, and AWS EC2 for hosting, ensuring a seamless and efficient deployment process.
