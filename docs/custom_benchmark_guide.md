# Step-by-Step Guide: Benchmarking Models with Custom Dataset and Judges

This guide will help you benchmark Llama4, Nova-Lite, Mistral-Large, GPT-4o, Claude 3.5 Sonnet, Claude 3.7, and DeepSeek models using a custom dataset with Claude and DeepSeek as judges.

## Prerequisites

- Python 3.8+
- pip or conda

## Setup

1. Install FMBench:
   ```bash
   pip install -U fmbench
   ```

2. Set up local environment:
   ```bash
   mkdir -p ~/fmbench/{configs,results,datasets}
   export FMBENCH_LOCAL_MODE=yes
   export FMBENCH_RESULTS_DIR=~/fmbench/results
   ```

## Prepare Custom Dataset

1. Create a JSONL file with prompts and ground truth responses:
   ```bash
   cat > ~/fmbench/datasets/custom_dataset.jsonl << EOF
   {"inputs": "Your first prompt here", "ground_truth": "Expected answer"}
   {"inputs": "Your second prompt here", "ground_truth": "Expected answer"}
   EOF
   ```

## Create Configuration File

1. Create a config file for the benchmark:
   ```bash
   cat > ~/fmbench/configs/custom_benchmark.yml << EOF
   general:
     name: custom-model-benchmark
     direct_prompting: true
     dataset_file: ~/fmbench/datasets/custom_dataset.jsonl

   aws:
     region: us-east-1
     s3_and_or_local_file_system: local

   experiments:
     - name: llama-4
       model_id: meta.llama3:8b-instruct-v1:0
       model_name: Llama-4
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: litellm
       deploy: no

     - name: nova-lite
       model_id: anthropic.claude-3-haiku-20240307-v1:0
       model_name: Nova-Lite
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: litellm
       deploy: no

     - name: mistral-large
       model_id: mistral.mistral-large-latest
       model_name: Mistral-Large
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: litellm
       deploy: no

     - name: gpt-4o
       model_id: gpt-4o
       model_name: GPT-4o
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: openai
       deploy: no

     - name: claude-3-5-sonnet
       model_id: claude-3-5-sonnet-20240620
       model_name: Claude-3-5-Sonnet
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: anthropic
       deploy: no

     - name: claude-3-7
       model_id: claude-3-opus-20240229
       model_name: Claude-3-7
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: anthropic
       deploy: no

     - name: deepseek
       model_id: deepseek-ai/deepseek-coder-33b-instruct
       model_name: DeepSeek
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: litellm
       deploy: no

   inference_parameters:
     litellm:
       temperature: 0.1
       max_tokens: 1024
       api_keys:
         ANTHROPIC_API_KEY: "your-anthropic-key"
         MISTRAL_API_KEY: "your-mistral-key"
         DEEPSEEK_API_KEY: "your-deepseek-key"

     openai:
       temperature: 0.1
       max_tokens: 1024
       api_keys:
         OPENAI_API_KEY: "your-openai-key"

     anthropic:
       temperature: 0.1
       max_tokens: 1024
       api_keys:
         ANTHROPIC_API_KEY: "your-anthropic-key"

   evaluators:
     - name: claude-judge
       model_id: claude-3-sonnet-20240229
       model_name: Claude-Judge
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: anthropic
       deploy: no

     - name: deepseek-judge
       model_id: deepseek-ai/deepseek-coder-33b-instruct
       model_name: DeepSeek-Judge
       inference_script: litellm_predictor.py
       inference_spec:
         parameter_set: litellm
       deploy: no
   EOF
   ```

2. Replace the API keys with your actual keys.

## Run the Benchmark

1. Execute the benchmark:
   ```bash
   fmbench --config-file ~/fmbench/configs/custom_benchmark.yml --local-mode yes
   ```

## Analyze Results

1. Results will be stored in the specified results directory:
   ```bash
   ls ~/fmbench/results
   ```

2. Use the FMBench analysis tools to visualize performance:
   ```bash
   python -m fmbench.analytics.metrics_plot ~/fmbench/results/custom-model-benchmark
   ```

## Troubleshooting

- If you encounter API rate limits, adjust the concurrency settings in the config file.
- For model-specific errors, check the provider documentation for parameter requirements.
- Verify API keys are correctly set and have sufficient permissions.

## Next Steps

- Customize evaluation criteria by modifying judge prompts
- Experiment with different temperature and parameter settings
- Add more varied prompts to your dataset for comprehensive evaluation