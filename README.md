<h1 align="center">
        <img src="https://github.com/aws-samples/foundation-model-benchmarking-tool/blob/main/img/fmbt-small.png?raw=true" width="25"></img> FMBench
</h1>

<p align="center">
    <p align="center">Benchmark any Foundation Model - Direct and Simple
    <br>
</p>
<h4 align="center"><a href="" target="_blank">OpenAI</a> | <a href="" target="_blank">Azure</a> | <a href="" target="_blank">Google</a> | <a href="" target="_blank">Anthropic</a></h4>
<h4 align="center">
    <a href="https://pypi.org/project/fmbench/" target="_blank">
        <img src="https://img.shields.io/pypi/v/fmbench.svg" alt="PyPI Version">
    </a>    
</h4>


🚨 **What's new**: Radically simplified with direct prompting - your prompts, exactly as you write them. 🚨

`FMBench` is a Python package for benchmarking any foundation model with a focus on simplicity and directness. The tool runs locally on your machine and supports models from major providers including OpenAI, Azure, Google, and Anthropic.

## Key Features

1. **Direct Prompting**: Your prompts are used exactly as written, no templates or transformations
2. **Smart Optimization**: Optional automatic formatting for each model's style
3. **Local Operation**: Run benchmarks directly on your machine without cloud dependencies
4. **Multi-Provider Support**: Test models from any provider with a unified approach

## Quickstart

```bash
# Install FMBench
pip install -U fmbench

# Set up local environment
mkdir -p ~/fmbench/{configs,results}
export FMBENCH_LOCAL_MODE=yes
export FMBENCH_RESULTS_DIR=~/fmbench/results

# Create a configuration file
cat > ~/fmbench/configs/config.yml << EOF
general:
  name: direct-benchmark
  direct_prompting: true

aws:
  region: us-east-1
  s3_and_or_local_file_system: local

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

inference_parameters:
  openai:
    temperature: 0.1
    max_tokens: 100
    api_keys:
      OPENAI_API_KEY: "your-api-key-here"
EOF

# Run the benchmark
fmbench --config-file ~/fmbench/configs/config.yml --local-mode yes
```

## Supported Models

| Provider                      | Models                                     |
|:------------------------------|:-------------------------------------------|
| **OpenAI**                    | GPT-4, GPT-4o, GPT-3.5 Turbo              |
| **Azure OpenAI**              | Azure GPT-4, Azure GPT-4o, Azure GPT-3.5   |
| **Google**                    | Gemini Pro, Gemini 1.5 Pro, Gemini 1.5 Flash|
| **Anthropic**                 | Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku |

## What's New

### 2.1.6

1. **Direct Prompting**: Your prompts used exactly as provided - no templates
2. **Simplified Local Mode**: Run benchmarks on your machine with minimal setup
3. **External Model Support**: Test any model from major providers
4. **No Infrastructure Required**: No AWS resources needed

[See full release history](./release_history.md)

## Dataset Format

Your input dataset should contain prompts exactly as you want them sent to models:

```jsonl
{"inputs": "Explain quantum computing.", "ground_truth": "Quantum computing uses quantum bits..."}
{"inputs": "What is the capital of France?", "ground_truth": "Paris"}
```

## Simple Three-Step Setup

1. **Install FMBench**:
   ```bash
   pip install -U fmbench
   ```

2. **Create a configuration file** with your model settings

3. **Run your benchmark**:
   ```bash
   export FMBENCH_LOCAL_MODE=yes
   fmbench --config-file ~/fmbench/configs/config.yml --local-mode yes
   ```

## Documentation

For detailed instructions, see:
- [Quickstart Guide](https://aws-samples.github.io/foundation-model-benchmarking-tool/quickstart.html)
- [Direct Prompting](https://aws-samples.github.io/foundation-model-benchmarking-tool/direct_prompting.html)
- [External Models Guide](https://aws-samples.github.io/foundation-model-benchmarking-tool/external_models.md)

## Support

- Schedule Demo 👋 - send us an email 🙂
- [Community Discord 💭](https://discord.gg/ydXV8mYFtF)
- Our emails ✉️ aroraai@amazon.com / madhurpt@amazon.com


## Contributors

<a href="https://github.com/aws-samples/foundation-model-benchmarking-tool/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=aws-samples/foundation-model-benchmarking-tool" />
</a>

## License

This library is licensed under the MIT-0 License. See the [LICENSE](./LICENSE) file.