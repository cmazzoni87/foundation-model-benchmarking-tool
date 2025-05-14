# Running FMBench Locally

This guide explains how to run FMBench completely locally, with minimal AWS dependencies.

## Overview

FMBench now supports a simplified local mode that allows you to:
1. Run benchmarks directly on your local machine
2. Store all data on your local filesystem
3. Focus on benchmarking external models (OpenAI, Azure, Google) without AWS infrastructure

## Quick Setup

Setting up FMBench locally is simple:

```bash
# Install FMBench
pip install -U fmbench

# Create directories for configurations and results
mkdir -p ~/fmbench/{configs,results}

# Set environment variables for local mode
export FMBENCH_LOCAL_MODE=yes
export FMBENCH_RESULTS_DIR=~/fmbench/results
```

## Creating a Local Configuration File

Create a configuration file for external models:

```bash
cat > ~/fmbench/configs/external-config.yml << EOF
general:
  name: external-models-benchmark

aws:
  region: us-east-1  # Still needed for formatting, but no AWS services used
  s3_and_or_local_file_system: local

run_steps:
  0_setup.ipynb: yes
  1_generate_data.ipynb: yes
  2_deploy_model.ipynb: yes
  3_run_inference.ipynb: yes
  4_get_evaluations.ipynb: yes
  5_model_metric_analysis.ipynb: yes
  6_cleanup.ipynb: no

source_data_files:
  - hf:THUDM/LongBench/2wikimqa_e/test

# Configure external models (OpenAI, Azure, Google)
experiments:
  - name: gpt-4
    model_id: gpt-4
    model_name: GPT-4
    ep_name: gpt-4
    instance_type: gpt-4
    deploy: no
    instance_count: 1
    inference_script: litellm_predictor.py
    inference_spec:
      parameter_set: openai
    concurrency_levels:
      - 1
    payload_files:
      - payload_en_1000-2000.jsonl

# Add API keys in the inference_parameters section
inference_parameters:
  openai:
    temperature: 0.1
    max_tokens: 100
    api_keys:
      OPENAI_API_KEY: "your-api-key-here"
EOF
```

## Running the Benchmark

```bash
# Run FMBench with your configuration
fmbench --config-file ~/fmbench/configs/external-config.yml --local-mode yes
```

## Adding More Models

You can add different models to your configuration file:

### OpenAI Models

```yaml
experiments:
  - name: gpt-4
    model_id: gpt-4
    model_name: GPT-4
    ep_name: gpt-4
    instance_type: gpt-4
    deploy: no
    instance_count: 1
    inference_script: litellm_predictor.py
    inference_spec:
      parameter_set: openai
    concurrency_levels:
      - 1
    payload_files:
      - payload_en_1000-2000.jsonl
      
  - name: gpt-3.5-turbo
    model_id: gpt-3.5-turbo
    model_name: GPT-3.5 Turbo
    ep_name: gpt-3.5-turbo
    instance_type: gpt-3.5-turbo
    deploy: no
    instance_count: 1
    inference_script: litellm_predictor.py
    inference_spec:
      parameter_set: openai
    concurrency_levels:
      - 1
    payload_files:
      - payload_en_1000-2000.jsonl
```

### Azure OpenAI Models

```yaml
experiments:
  - name: azure-gpt-4
    model_id: gpt-4
    model_name: Azure GPT-4
    ep_name: azure-gpt-4
    instance_type: azure-gpt-4
    deploy: no
    instance_count: 1
    inference_script: litellm_predictor.py
    inference_spec:
      parameter_set: azure_openai
    concurrency_levels:
      - 1
    payload_files:
      - payload_en_1000-2000.jsonl

inference_parameters:
  azure_openai:
    temperature: 0.1
    max_tokens: 100
    api_version: "2023-05-15"
    base_url: "https://your-resource-name.openai.azure.com"
    api_keys:
      AZURE_OPENAI_API_KEY: "your-azure-api-key"
```

### Google Models

```yaml
experiments:
  - name: gemini-pro
    model_id: gemini-pro
    model_name: Gemini Pro
    ep_name: gemini-pro
    instance_type: gemini-pro
    deploy: no
    instance_count: 1
    inference_script: litellm_predictor.py
    inference_spec:
      parameter_set: google
    concurrency_levels:
      - 1
    payload_files:
      - payload_en_1000-2000.jsonl

inference_parameters:
  google:
    temperature: 0.1
    max_tokens: 100
    api_keys:
      GOOGLE_API_KEY: "your-google-api-key"
```

## Tips for Local Mode

1. **Data Sources**: Local mode supports both Hugging Face datasets and local files:
   ```yaml
   # For Hugging Face datasets (downloads locally)
   source_data_files:
     - hf:THUDM/LongBench/2wikimqa_e/test

   # For local files
   source_data_files:
     - file:/path/to/your/dataset.jsonl
   ```

2. **Environment Variables**:
   ```bash
   export FMBENCH_LOCAL_MODE=yes           # Enable local mode
   export FMBENCH_RESULTS_DIR=~/results    # Where to store results
   export FMBENCH_TEMP_DIR=~/temp          # Where to store temporary files
   ```

3. **API Keys**: You can also set API keys as environment variables instead of in the config file:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   export AZURE_API_KEY="your-azure-api-key"
   export GOOGLE_API_KEY="your-google-api-key"
   ```

## Viewing Results

After running a benchmark, you'll find all results in the directory specified by `FMBENCH_RESULTS_DIR`:
```bash
# View the benchmark report
cat ~/fmbench/results/report.md

# Explore detailed metrics
ls -la ~/fmbench/results/metrics/
```

## Common Issues and Solutions

1. **Missing API keys**: Ensure you've set the correct API keys either in the config file or as environment variables.

2. **Dataset errors**: If you see errors loading datasets, try using a different Hugging Face dataset or a local file.

3. **Python dependencies**: If you encounter dependency issues, create a virtual environment:
   ```bash
   python -m venv ~/.venv/fmbench
   source ~/.venv/fmbench/bin/activate
   pip install -U fmbench
   ```