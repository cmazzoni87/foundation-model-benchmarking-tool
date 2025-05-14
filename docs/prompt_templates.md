# Prompt Templates in FMBench

FMBench uses a simplified prompt template approach to ensure consistent benchmarking across different models. This document explains how the prompt template system works and how to customize it for your needs.

## Generic Prompt Template

FMBench comes with a single generic prompt template that works well across most model types:

```text
You are a helpful assistant. Please answer the following question.

Context information is provided below:
```
{context}
```

Question: {input}

Provide a clear and concise answer based on the given context. If the answer is not in the context, say "I don't know."
```

This template uses two main placeholders:
- `{context}`: Replaced with relevant context information
- `{input}`: Replaced with the user's question

## Customizing Prompts

If you need to use a different prompt format, you can:

1. Edit the existing `prompt_template_generic.txt` file
2. Create your own template file in the `fmbench/prompt_template/` directory

Your template file should be named with a clear, descriptive name (e.g., `prompt_template_custom.txt`).

## Using Custom Templates

To use a custom template, specify it in your configuration file:

```yaml
general:
  name: my-benchmark
  prompt_template: custom  # Will use prompt_template_custom.txt

# Rest of your configuration...
```

If no prompt template is specified, FMBench will use the generic template by default.

## Template Variables

The following variables can be used in prompt templates:

| Variable     | Description                                 |
|--------------|---------------------------------------------|
| `{context}`  | Reference material or background information |
| `{input}`    | The user query or question                  |
| `{system}`   | Optional system prompt (if supported)       |

## Prompt Optimization

When using the prompt optimization feature through AWS Bedrock Agent Runtime, your template will be automatically formatted according to the target model's requirements while preserving your core prompt structure.

## Evaluation Templates

The evaluation templates used for model accuracy assessment are in the `prompt_template/eval_criteria/` directory. These templates follow a specific structure for consistent model evaluation and should generally not be modified unless you're implementing a custom evaluation method.