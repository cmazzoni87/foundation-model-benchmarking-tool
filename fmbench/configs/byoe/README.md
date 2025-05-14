# Bring Your Own Endpoint (BYOE) in Bedrock-only FMBench

The Bedrock-only version of FMBench still supports benchmarking external endpoints against Bedrock models. This allows you to compare performance, cost, and accuracy between your custom endpoints and Bedrock models.

## What is BYOE?

Bring Your Own Endpoint (BYOE) allows you to:
- Benchmark an existing REST endpoint against Bedrock models
- Compare external model deployments with Bedrock services
- Use custom pricing models for external endpoints

## How to Use BYOE

1. See the template configuration file `config-byo-custom-rest-predictor-template.yml` in this directory
2. Configure your external endpoint information:
   - Set the `ep_name` to your endpoint URL
   - Configure custom headers, authentication, and parameters
   - Set the `inference_script` to either:
     - `custom_rest_predictor.py` - For POST requests with custom parameters
     - `rest_predictor.py` - For simpler GET-based endpoints
3. Set `deploy: no` since your endpoint already exists
4. Run FMBench as normal

## Custom vs. REST Predictor

FMBench includes two types of predictors for external endpoints:

1. **CustomRestPredictor** (`custom_rest_predictor.py`):
   - Uses POST requests
   - Supports custom headers, authentication
   - Allows custom request body formatting
   - Extracts generated text from completion responses

2. **RESTPredictor** (`rest_predictor.py`):
   - Uses GET requests
   - Simpler interface for basic REST endpoints
   - Good for endpoints that accept query parameters

Choose the one that best matches your endpoint's API requirements.

## Pricing for External Endpoints

You can configure pricing for your external endpoints in the `pricing.yml` file:

```yaml
# For token-based pricing (like API-based services)
token_based:
  external-model:
    input-per-1k-tokens: 0.001
    output-per-1k-tokens: 0.002

# For instance-based pricing (like EC2-hosted models)
instance_based:
  external-model: 2.5  # hourly rate
```

The predictors will attempt to use token-based pricing first, then fall back to instance-based if not available.

## Example Configuration

See the template configuration file for a complete example of benchmarking a Bedrock model against an external endpoint.