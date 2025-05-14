# Bedrock-only FMBench

This version of the Foundation Model Benchmarking Tool (FMBench) has been streamlined to focus exclusively on Amazon Bedrock models. All deployment options related to SageMaker, EC2, and EKS have been removed, while preserving the core benchmarking and evaluation capabilities.

## Changes in the Bedrock-only Version

### Removed Components

- **SageMaker-specific code**: Deployment, predictor, and metrics collection for SageMaker endpoints
- **EC2-specific code**: Deployment, predictor, and metrics collection for EC2 instances
- **EKS-specific code**: Deployment, predictor, and metrics collection for Kubernetes clusters
- **Non-Bedrock configuration files**: Configuration templates for SageMaker, EC2, and EKS deployments

### Preserved Components

- **Core benchmarking functionality**: Data generation, inference, metric collection, and analysis
- **Bedrock integration**: Full support for all Amazon Bedrock models
- **Bring Your Own Endpoint (BYOE)**: Ability to benchmark external endpoints against Bedrock models
- **Evaluation framework**: Panel of LLM Evaluators (PoLL) for accuracy assessment
- **Multimodal support**: Handling of both text and image inputs for compatible models

### Added Features

- **Automatic Prompt Optimization**: Using the Bedrock Agent Runtime `optimize_prompt` API to automatically format prompts for different model families (Claude, Llama, Mistral, etc.)
- **Model Family Detection**: Automatic detection of model families to apply the right prompt formatting

## Why BYOE is Still Supported

The Bring Your Own Endpoint (BYOE) capability allows users to benchmark external endpoints against Bedrock models, which enables important use cases:

1. **Comparative Analysis**: Direct comparison between existing deployments and Bedrock models
2. **Migration Planning**: Evaluating performance differences when considering a migration to Bedrock
3. **Multi-provider Assessment**: Comparing models from different providers against Bedrock offerings
4. **Cost Optimization**: Determining the most cost-effective solution for specific use cases

For detailed information on using BYOE with Bedrock, see the [BYOE documentation](byoe.md).

## Configuration Changes

Configuration files have been simplified to focus on Bedrock parameters:

- The `role-arn` parameter is no longer required
- Instance type and count parameters are still used for pricing calculations
- The `platform` parameter is now set to `bedrock` by default

Example Bedrock-only configuration:

```yaml
general:
  name: bedrock-benchmark-example

aws:
  region: {region}
  bucket: {write_bucket}
  s3_and_or_local_file_system: s3

experiments:
  - name: claude-sonnet
    model_id: anthropic.claude-3-sonnet-20240229-v1:0
    model_name: Claude 3 Sonnet
    ep_name: anthropic.claude-3-sonnet-20240229-v1:0
    instance_type: anthropic.claude-3-sonnet-20240229-v1:0
    deploy: no
    instance_count: 1
    inference_script: bedrock_predictor.py
    inference_spec:
      parameter_set: bedrock
```

## Auto-Formatted Prompts

The Bedrock-only version includes automatic prompt formatting for different model families. This eliminates the need to create separate prompt templates for each model type, as prompts are automatically optimized for the target model.

The system uses the Bedrock Agent Runtime's `optimize_prompt` API to:

1. Match the exact model ID from your benchmarking configuration with our comprehensive model mapping
2. Format the prompt according to the target model's preferred structure
3. Retain the original prompt for reference and metrics collection

### How Model Matching Works

The optimization system includes:

1. **Exact Model ID Matching**: Directly maps specific Bedrock model IDs (like `anthropic.claude-3-sonnet-20240229-v1:0`) to their optimal target models
2. **Family-Based Fallback**: If an exact match isn't found, detects the model family from the ID and uses an appropriate target
3. **Caching**: Stores optimized prompts to avoid repeated API calls for the same prompt/model combinations

### Supported Model Families

The optimizer supports all Bedrock model families:

- **Claude Models**: All Claude models (Instant, V1, V2, Claude 3 Haiku/Sonnet/Opus, Claude 3.5)
- **Llama Models**: All Llama models (Llama 2, Llama 3, Llama 3.1, Llama 3.2, vision variants)
- **Mistral Models**: All Mistral models (Small, Medium, Large, Mixtral)
- **Titan Models**: All Amazon Titan models (Text, Embeddings, Image)
- **Cohere Models**: All Cohere Command models and embedding models
- **Other Models**: AI21, Stability AI, with appropriate fallbacks

This feature works seamlessly in the background and requires no additional configuration. As new models are added to Bedrock, the optimizer will automatically detect their family and apply the appropriate formatting.

## Workflow Changes

The workflow has been streamlined:

1. **Setup**: Configure environment and AWS credentials
2. **Data Generation**: Create prompt datasets from source data
3. **Model Registration**: Register Bedrock models (no actual deployment needed)
4. **Inference**: Run benchmarks against Bedrock models with auto-formatted prompts
5. **Evaluation**: Assess model accuracy using PoLL
6. **Analysis**: Generate reports and visualizations

The deployment step simply registers models rather than deploying them, since Bedrock models are already deployed and managed by AWS.

## Getting Started

To use the Bedrock-only version:

1. Configure your AWS credentials with Bedrock access
2. Create or modify a configuration file to specify Bedrock models
3. Run FMBench with your configuration file

For detailed instructions, see the [Getting Started guide](gettingstarted.md) and [Bedrock Benchmarking guide](benchmarking_on_bedrock.md).