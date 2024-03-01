# FarpointOI Setup Guide

This comprehensive setup guide walks you through configuring your local or deployment environment for FarpointOI.

## Prerequisites

Before beginning the setup process, ensure the following prerequisites are met:

- An operational Ubuntu server for deployment or a compatible local system.
- AWS CLI and AWS ECR must be configured on the Ubuntu server for deployment purposes.

## Setup Steps

### 1. AWS CLI and ECR Configuration (For Deployment)

First, install and configure the AWS CLI on your Ubuntu server. This tool enables you to interact with AWS services directly from the command line.

```bash
# Install AWS CLI
sudo apt-get install awscli -y

# Configure AWS CLI with your credentials
aws configure
```

During configuration, you will be prompted to enter your AWS Access Key ID, Secret Access Key, Region, and output format. These credentials are essential for authenticating your server with AWS services.

### 2. Docker Installation and AWS ECR Authentication

Install Docker on your system to create, manage, and run containerized applications. Authenticate Docker with AWS ECR to allow pulling and pushing images to your repository.

```bash
# Install Docker and its components
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# Authenticate Docker to AWS ECR
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

Replace `<your-region>`, `<your-aws-account-id>`, and `<your-region>` with your specific AWS details.

### 3. PostgreSQL Setup

Install and configure PostgreSQL, a robust and scalable database system, to manage FarpointOI's data.

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib -y

# Start and enable PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create a user and database for FarpointOI
sudo -u postgres psql -c "CREATE USER farpointoi WITH PASSWORD '<password>';"
sudo -u postgres psql -c "CREATE DATABASE farpointoi;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE farpointoi TO farpointoi;"
```

### 4. Firewall Configuration for PostgreSQL (You can configure it with the security groupts in AWS)

Optionally, configure your firewall to allow traffic on the PostgreSQL default port, enhancing security and connectivity.

```bash
# Open PostgreSQL port on the firewall
sudo ufw allow 5432/tcp
```

### 5. SSL and Nginx Configuration

Install Nginx and configure SSL to secure your application, ensuring data is safely encrypted during transmission.

```bash
# Install Nginx
sudo apt-get install nginx -y

# Update Nginx configuration for SSL
sudo cp /path/to/your/nginx.conf /etc/nginx/nginx.conf
sudo systemctl reload nginx
```

### 6. Google Developer Console Configuration

Adjust your Google Developer Console settings to align with your deployment, updating redirect URLs and JavaScript origins as necessary.

### 7. GitHub Repository Setup

Clone the FarpointOI repository to your server or local machine, ensuring you're working with the most current development branch.

```bash
# Clone the FarpointOI repository
git clone -b dev <your-repo-url>
```

### 8. Environment Variables Setup

Configure your environment variables by copying the `.env` file to the client, server, and transcription directories, filling in the necessary details to connect your application components.

### 9. Docker Compose Setup

Use Docker Compose to build and run your FarpointOI containers, simplifying the management of application services.

```bash
# Start services with Docker Compose
docker-compose -f docker-compose.yml up -d
```

### 10. Accessing the Application

Finally, access FarpointOI through your web browser by navigating to `localhost` or the deployed URL, such as `https://oi.farpointhq.com`.

By following these detailed steps, your FarpointOI environment will be fully configured and ready for operational use. Enjoy the power and flexibility of Farpoint's operational intelligence at your fingertips.
