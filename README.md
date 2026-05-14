# DockerForge CI/CD Pipeline

This project is a demonstration of a fully automated, local CI/CD pipeline built from scratch using DevOps best practices.

## Technologies Used
* **Backend:** Python / Flask
* **Version Control:** Git / GitHub
* **CI/CD:** Jenkins (running locally on Windows)
* **Containerization:** Docker
* **Testing:** Pytest
* **Webhook Tunneling:** ngrok

## Architecture Workflow
1. Developer pushes code to GitHub.
2. GitHub Webhook securely pings local Jenkins via ngrok tunnel.
3. Jenkins clones the repository and installs dependencies in an isolated virtual environment.
4. Pytest runs automated unit tests.
5. If tests pass, Jenkins builds a lightweight Docker Image (`python:3.10-slim`).
6. Jenkins safely stops and removes the old container, then deploys the new container.
7. A final `curl` command hits the live Flask API to update the visual monitoring dashboard.

## Current Status
* CI/CD automation is fully functional and hands-free!

* Update: Testing the automated GitHub Webhook trigger! (Build #13)

lalal