# Benchmarking External Models with FMBench

This document explains how to use the FMBench tool to benchmark external LLMs (OpenAI, Azure OpenAI, Google) alongside AWS Bedrock models.

## Overview

The FMBench tool now supports benchmarking external models using the LiteLLM library, which provides a unified interface to multiple LLM providers. This feature allows you to:

1. Compare Bedrock models with popular models from other providers
2. Benchmark your existing LLM deployments across different platforms
3. Evaluate cost-performance tradeoffs between different providers

## Prerequisites

Before benchmarking external models, you'll need:

1. API keys for the external providers you want to benchmark
2. The LiteLLM Python package installed (included in the FMBench requirements)
3. A configuration file that includes your external models

## Supported Providers and Models

The following external providers and models are supported:

### OpenAI
- GPT-4
- GPT-4o
- GPT-3.5 Turbo

### Azure OpenAI
- Azure GPT-4
- Azure GPT-4o
- Azure GPT-3.5 Turbo

### Google
- Gemini Pro
- Gemini 1.5 Pro
- Gemini 1.5 Flash

## Configuration

To benchmark external models, you'll need to create a configuration file that specifies your API keys and the models you want to evaluate. A template is provided at `fmbench/configs/external/config-external-models-template.yml`.

### API Key Configuration

External model API keys are specified in the `inference_parameters` section of the configuration file:

```yaml
inference_parameters:
  # Parameters for OpenAI models
  openai:
    temperature: 0.1
    max_tokens: 100
    top_p: 0.9
    api_keys:
      OPENAI_API_KEY: "YOUR_OPENAI_API_KEY"
  
  # Parameters for Azure OpenAI models
  azure_openai:
    temperature: 0.1
    max_tokens: 100
    top_p: 0.9
    api_version: "2023-05-15"
    base_url: "https://your-resource-name.openai.azure.com"
    api_keys:
      AZURE_OPENAI_API_KEY: "YOUR_AZURE_API_KEY"
  
  # Parameters for Google models
  google:
    temperature: 0.1
    max_tokens: 100
    top_p: 0.9
    api_keys:
      GOOGLE_API_KEY: "YOUR_GOOGLE_API_KEY"
```

Replace the placeholder API keys with your actual keys.

### Model Configuration

Each external model must be configured in the `experiments` section:

```yaml
# OpenAI model example
- name: gpt-4o
  model_id: gpt-4o
  model_name: GPT-4o
  ep_name: gpt-4o
  instance_type: gpt-4o  # Used for pricing reference
  deploy: no
  instance_count: 1
  inference_script: litellm_predictor.py
  inference_spec:
    parameter_set: openai
  concurrency_levels:
    - 1
    - 2
  payload_files:
    - payload_en_1000-2000.jsonl
```

Key points for external model configuration:
- Set `inference_script` to `litellm_predictor.py`
- Set `parameter_set` to the appropriate provider type (openai, azure_openai, or google)
- Set `instance_type` to match the model ID in the pricing.yml file
- Always set `deploy: no` for external models

## Pricing Configuration

External model pricing is configured in the `pricing.yml` file under the `token_based` section. The pricing for popular models is already included:

```yaml
token_based:
  # OpenAI Models
  gpt-4o:
    input-per-1k-tokens: 0.005
    output-per-1k-tokens: 0.015
  gpt-4:
    input-per-1k-tokens: 0.03
    output-per-1k-tokens: 0.06
  gpt-3.5-turbo:
    input-per-1k-tokens: 0.0005
    output-per-1k-tokens: 0.0015
  # Azure OpenAI Models (same pricing as OpenAI)
  azure-gpt-4:
    input-per-1k-tokens: 0.03
    output-per-1k-tokens: 0.06
  # Google Models
  gemini-pro:
    input-per-1k-tokens: 0.00025
    output-per-1k-tokens: 0.0005
```

If you need to add pricing for a new model, follow the same format with the appropriate rates per 1,000 tokens.

## Running the Benchmark

To run a benchmark with external models:

1. Create a copy of the template configuration file:
   ```
   cp fmbench/configs/external/config-external-models-template.yml fmbench/configs/external/my-benchmark.yml
   ```

2. Edit the configuration file to include your API keys and customize the models and datasets.

3. Run the benchmark using the standard FMBench command:
   ```
   python -m fmbench.main --config_file fmbench/configs/external/my-benchmark.yml
   ```

## Security Considerations

When working with external API keys:

1. **Never commit API keys to source control**. Consider using environment variables or AWS Secrets Manager.
2. Be aware of your API usage limits and costs when running benchmarks.
3. Ensure you comply with each provider's terms of service regarding benchmarking.

## Limitations

There are a few limitations to be aware of when benchmarking external models:

1. No infrastructure metrics (like CPU/GPU utilization) are available for external APIs.
2. External API rate limits may affect concurrency testing.
3. Network latency might impact performance comparisons with Bedrock.
4. Token counting may vary slightly between providers.

## Troubleshooting

If you encounter issues when benchmarking external models:

1. Verify your API keys are correct and have sufficient permissions
2. Check that you have the latest version of LiteLLM installed
3. For Azure OpenAI, verify your endpoint URL and API version
4. Check for rate limiting errors in the logs

For further assistance, please open an issue on the GitHub repository.