# Quickstart - Run FMBench Locally

FMBench is now designed to run completely locally on your machine, making it simple to benchmark models from various providers without complex infrastructure requirements.

## Install FMBench

Install FMBench using pip:

```bash
# Create a virtual environment (recommended)
python -m venv ~/.venv/fmbench
source ~/.venv/fmbench/bin/activate

# Install FMBench
pip install -U fmbench
```

## Setup Local Environment

Create directories for configurations, data, and results:

```bash
# Create directories
mkdir -p ~/fmbench/{configs,results}

# Set environment variables for local mode
export FMBENCH_LOCAL_MODE=yes
export FMBENCH_RESULTS_DIR=~/fmbench/results
```

## Create a Configuration File

Create a simple configuration file for benchmarking external models:

```bash
cat > ~/fmbench/configs/openai-config.yml << EOF
general:
  name: openai-benchmark

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

experiments:
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

inference_parameters:
  openai:
    temperature: 0.1
    max_tokens: 100
    api_keys:
      OPENAI_API_KEY: "your-api-key-here"
EOF
```

## Run the Benchmark

Run FMBench with your configuration file:

```bash
# Set your API key (optional, can also be in the config file)
export OPENAI_API_KEY="your-api-key-here"

# Run the benchmark
fmbench --config-file ~/fmbench/configs/openai-config.yml --local-mode yes
```

## View Results

Once the benchmark completes, you can view the results:

```bash
# View the generated report
cat ~/fmbench/results/report.md

# Explore detailed metrics
ls -la ~/fmbench/results/metrics/
```

## Examples for Different Providers

### OpenAI Example

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

inference_parameters:
  openai:
    temperature: 0.1
    max_tokens: 100
    api_keys:
      OPENAI_API_KEY: "your-api-key-here"
```

### Azure OpenAI Example

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

### Google Example

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

## Comparing Multiple Models

You can compare multiple models by adding them to the same configuration file:

```yaml
experiments:
  - name: gpt-4
    model_id: gpt-4
    model_name: GPT-4
    ep_name: gpt-4
    instance_type: gpt-4
    deploy: no
    inference_script: litellm_predictor.py
    inference_spec:
      parameter_set: openai
    
  - name: gpt-3.5-turbo
    model_id: gpt-3.5-turbo
    model_name: GPT-3.5 Turbo
    ep_name: gpt-3.5-turbo
    instance_type: gpt-3.5-turbo
    deploy: no
    inference_script: litellm_predictor.py
    inference_spec:
      parameter_set: openai
      
  - name: gemini-pro
    model_id: gemini-pro
    model_name: Gemini Pro
    ep_name: gemini-pro
    instance_type: gemini-pro
    deploy: no
    inference_script: litellm_predictor.py
    inference_spec:
      parameter_set: google
```

## Next Steps

For more details on local mode and advanced configurations, see our [Local Mode Documentation](local_mode.md).

For information on benchmarking external models (OpenAI, Azure, Google), see [External Models Benchmarking](external_models.md).