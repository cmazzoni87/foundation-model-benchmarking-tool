# Direct Prompting in FMBench

FMBench now uses a direct prompting approach that eliminates template complexity and focuses on what matters: evaluating model performance with your exact prompts.

## Direct Prompt Approach

With the simplified direct prompting approach:

1. **Your prompt is used exactly as provided** - No templates, no transformations
2. **Automatic optimization** - Prompts are optimized for each model's style via the Bedrock Agent Runtime API
3. **Clean evaluation** - Results are evaluated based on the exact outputs from your prompts

## How It Works

When benchmarking models:

1. You provide prompts directly in your dataset
2. FMBench passes these prompts directly to the model (with optional optimization)
3. The model responses are collected and evaluated

## Configuration Example

```yaml
general:
  name: direct-prompting-benchmark
  direct_prompting: true  # Enable direct prompting mode

aws:
  region: us-east-1
  s3_and_or_local_file_system: local

source_data_files:
  - file:/path/to/your/prompts.jsonl  # File with raw prompts

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
```

## Dataset Format

Your input dataset should contain prompts exactly as you want them sent to the models:

```jsonl
{"inputs": "Explain the concept of recursion in programming.", "ground_truth": "Recursion is a programming technique where a function calls itself directly or indirectly to solve a problem."}
{"inputs": "What is the capital of France?", "ground_truth": "Paris"}
```

## Prompt Optimization (Optional)

If you enable prompt optimization, the system will:

1. Take your raw prompt exactly as provided
2. Use the optimization API to format it for the target model
3. Send the optimized version to the model

This ensures your content remains intact while benefiting from model-specific formatting.

## Benefits of Direct Prompting

1. **Simplicity** - No need to learn template syntax or manage template files
2. **Control** - Your prompts are used exactly as you provide them
3. **Consistency** - The same prompt content is used across all models
4. **Transparency** - Clear relationship between your input and the benchmark results

## Evaluation Process

The evaluation process remains unchanged - model outputs are still assessed for accuracy against ground truth by the Panel of LLM Evaluators.

## Migrating from Templates

If you were previously using templates:

1. Remove any template references from your configuration
2. Ensure your input data contains fully-formed prompts
3. Set `direct_prompting: true` in your configuration