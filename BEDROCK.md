# Summary of Changes

This repository has been modified to focus exclusively on benchmarking Foundation Models on Amazon Bedrock. The following changes were made:

## Code Changes

1. **Removed Platform Constants**: Updated `constants.py` to remove references to SageMaker, EC2, and EKS platforms, keeping only Bedrock.
2. **Simplified Main Script**: Removed the SageMaker role-arn parameter from `main.py` along with other non-Bedrock options.
3. **Updated Global Variables**: Modified `globals.py` to remove SageMaker/EC2/EKS specific variables and settings.
4. **Simplified Deployment**: Modified the deployment notebook to work only with Bedrock models.
5. **Dependencies**: Removed unnecessary dependencies from `pyproject.toml` related to EC2, SageMaker, and EKS.

## Configuration and Documentation

1. **Removed Non-Bedrock Configurations**: Removed all configuration files related to EC2, SageMaker, and EKS deployments.
2. **Bedrock Template**: Created a simplified Bedrock-specific configuration template.
3. **Updated Documentation**: Modified documentation files to focus only on Bedrock benchmarking.
4. **Updated mkdocs.yml**: Simplified navigation to include only Bedrock-relevant pages.

## Features Retained

1. **Performance Benchmarking**: The ability to measure latency, throughput, and cost for different Bedrock models.
2. **Model Evaluation**: Support for evaluating model accuracy using the Panel of LLM Evaluators.
3. **Configuration Flexibility**: Support for different inference parameters, concurrency levels, and prompt sizes.
4. **Streaming Support**: Maintained capability for streaming responses and measuring metrics like TTFT, TPOT, and TTLT.
5. **Multimodal Support**: Maintained capability for benchmarking multimodal models.

## Version

- Updated to version 3.0.0 to reflect the significant changes in functionality.