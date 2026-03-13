# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview
This is a central DevOps core repository that contains reusable GitHub Actions CI/CD workflows for enterprise Java application delivery. It serves as a shared pipeline template that can be called by individual Java service repositories.

## Architecture
- All reusable GitHub Actions workflows are stored in `.github/workflows/`
- Primary workflow: `java-standard-ci.yml` - A reusable enterprise Java delivery pipeline designed to be invoked via `workflow_call` from other repositories
- The pipeline includes: code checkout, Java environment setup, build execution, Trivy security scanning, and automatic delivery report generation

## Common Operations
### Using the reusable Java workflow
To use the `java-standard-ci.yml` workflow in a Java service repository, add the following to your workflow file:
```yaml
jobs:
  deliver:
    uses: your-org/my-devops-core/.github/workflows/java-standard-ci.yml@main
    with:
      service_name: "your-service-name"
      java_version: "17" # Optional, defaults to 17
      build_command: "mvn clean package -DskipTests" # Optional, custom build command
```

### Repository Management
- This repository contains only GitHub Actions workflow definitions, no application source files, build steps, or tests for the repository itself
- All changes should be made to workflow files in `.github/workflows/`
- When modifying workflows, test changes in feature branches before merging to main to avoid breaking dependent pipelines
