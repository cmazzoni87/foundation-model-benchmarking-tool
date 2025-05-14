# Bring Your Own Endpoint (BYOE) in Bedrock-only FMBench

The Bedrock-only version of FMBench supports benchmarking external REST endpoints against Amazon Bedrock models. This allows for comparative analysis between custom deployments and Bedrock services.

## Why Use BYOE with Bedrock?

BYOE functionality enables several important use cases:

1. **Comparative Analysis**: Directly compare your existing model deployments with Bedrock models
2. **Migration Planning**: Evaluate the performance differences when considering a migration to Bedrock
3. **Multi-provider Benchmarking**: Compare models from different providers against Bedrock offerings
4. **Cost Optimization**: Determine the most cost-effective option between custom deployments and Bedrock

## Setting Up BYOE

To benchmark your own endpoint alongside Bedrock models:

1. Create a configuration file based on the template in `fmbench/configs/byoe/config-byo-custom-rest-predictor-template.yml`
2. Configure your external endpoint:

```yaml
# External custom endpoint
- name: external-endpoint
  model_id: external-model
  model_name: External Custom Model
  ep_name: "https://your-endpoint-url/generate"  # Replace with your endpoint URL
  instance_type: external-model  # Used for pricing reference
  deploy: no  # Important - set to "no" since the endpoint already exists
  instance_count: 1
  inference_script: custom_rest_predictor.py
  inference_spec:
    parameter_set: custom_rest  # Must match a section in inference_parameters
    headers:
      Content-Type: "application/json"
      Authorization: "Bearer your-api-key"  # Replace with your API key
    parameters:
      temperature: 0.1
      max_tokens: 100
      top_p: 0.9
    model_id: "external-model-id"  # If your API requires a model ID
  concurrency_levels:
    - 1
    - 2
  payload_files:
    - payload_en_1000-2000.jsonl
```

3. Include Bedrock models in the same configuration file for direct comparison
4. Define pricing in the `pricing.yml` file for accurate cost comparison

## Types of Predictors

FMBench provides two predictor types for external endpoints:

### CustomRestPredictor

Best for POST-based APIs that require custom request formatting:

- Sends POST requests with a JSON body
- Supports custom headers and authentication
- Extracts generated text from structured responses
- Handles token counting for both input and output

Example configuration in `inference_spec`:

```yaml
inference_spec:
  parameter_set: custom_rest
  headers:
    Content-Type: "application/json"
    Authorization: "Bearer your-api-key"
  parameters:
    temperature: 0.1
    max_tokens: 100
  model_id: "external-model-id"
```

### RESTPredictor

Suitable for simpler GET-based APIs:

- Uses GET requests with query parameters
- More straightforward configuration
- Expects a simpler response format

Example configuration:

```yaml
inference_spec:
  parameter_set: rest_params
  split_input_and_parameters: true
  timeout: 180
  auth:
    api_key: "your-api-key"
```

## Pricing Configuration

Update the `pricing.yml` file to include your external endpoint's pricing:

```yaml
# For API-based services with token pricing
token_based:
  external-model:
    input-per-1k-tokens: 0.0015
    output-per-1k-tokens: 0.0020

# For services with hourly pricing
instance_based:
  external-model: 2.5  # hourly rate
```

The predictors will use token-based pricing if available, or fall back to instance-based pricing.

## Benchmarking Results

When using BYOE with Bedrock models, the benchmarking results will show comparative metrics for:

- Latency (average, P50, P95, P99)
- Token throughput
- Cost per transaction
- Accuracy (if evaluation is enabled)

This allows for direct comparison between external endpoints and Bedrock models to determine the optimal solution for your use case.

## Example Usage

See the template in `fmbench/configs/byoe/config-byo-custom-rest-predictor-template.yml` for a complete example of benchmarking a Bedrock model against an external endpoint.