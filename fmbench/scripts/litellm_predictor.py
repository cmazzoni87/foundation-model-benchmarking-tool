"""
LiteLLM Predictor Module for FMBench

This module integrates external models (OpenAI, Azure OpenAI, Google) with the benchmarking tool
using the LiteLLM library for a unified interface to multiple providers.
"""

import os
import time
import json
import logging
import litellm
import pandas as pd
from datetime import datetime
from fmbench.scripts import constants
from typing import Dict, Optional, List
from litellm import completion, token_counter, RateLimitError
from fmbench.scripts.stream_responses import get_response_stream
from fmbench.scripts.fmbench_predictor import (FMBenchPredictor, 
                                              FMBenchPredictionResponse)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define supported providers and their models
SUPPORTED_PROVIDERS = {
    "openai": ["gpt-4", "gpt-4o", "gpt-3.5-turbo"],
    "azure": ["azure-gpt-4", "azure-gpt-4o", "azure-gpt-35-turbo"],
    "google": ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
}

# Service name for this predictor type
SERVICE_NAME = constants.PLATFORM_EXTERNAL

class LiteLLMPredictor(FMBenchPredictor):
    """
    Predictor for external models (OpenAI, Azure OpenAI, Google) using LiteLLM.
    """
    
    # Initialize the service name
    _service_name: str = SERVICE_NAME

    # Overriding abstract method
    def __init__(self,
                endpoint_name: str,
                inference_spec: Optional[Dict],
                metadata: Optional[Dict]):
        """
        Initialize the LiteLLM predictor.
        
        Args:
            endpoint_name: The model ID (e.g., gpt-4, azure-gpt-4, gemini-pro)
            inference_spec: Dictionary containing inference parameters
            metadata: Dictionary containing provider metadata (API keys, etc.)
        """
        try:
            # Initialize private member variables
            self._endpoint_name = endpoint_name
            self._inference_spec = inference_spec
            self._metadata = metadata
            
            # Default inference parameters
            self._temperature = 0.1
            self._max_tokens = 100
            self._top_p = 0.9
            self._stream = None
            self._start = None
            self._stop = None
            self._caching = False
            
            # Get provider from model ID prefix
            if endpoint_name.startswith("azure-"):
                self._provider = "azure"
                self._model = endpoint_name.replace("azure-", "")
            elif endpoint_name.startswith("gemini-"):
                self._provider = "google"
                self._model = endpoint_name
            else:
                self._provider = "openai"
                self._model = endpoint_name
                
            # Override defaults with inference spec if provided
            if inference_spec:
                parameters: Optional[Dict] = inference_spec.get('parameters')
                if parameters:
                    self._temperature = parameters.get('temperature', self._temperature)
                    self._max_tokens = parameters.get('max_tokens', self._max_tokens)
                    self._top_p = parameters.get('top_p', self._top_p)
                    self._stream = inference_spec.get("stream", self._stream)
                    self._stop = inference_spec.get("stop_token", self._stop)
                    self._start = inference_spec.get("start_token", self._start)
                    
            # Set up API keys from metadata
            if metadata:
                if self._provider == "openai" and metadata.get("openai_api_key"):
                    os.environ["OPENAI_API_KEY"] = metadata.get("openai_api_key")
                elif self._provider == "azure":
                    if metadata.get("azure_api_key"):
                        os.environ["AZURE_API_KEY"] = metadata.get("azure_api_key")
                    if metadata.get("azure_endpoint"):
                        os.environ["AZURE_API_BASE"] = metadata.get("azure_endpoint")
                    if metadata.get("azure_api_version"):
                        os.environ["AZURE_API_VERSION"] = metadata.get("azure_api_version")
                elif self._provider == "google" and metadata.get("google_api_key"):
                    os.environ["GOOGLE_API_KEY"] = metadata.get("google_api_key")
            
            # Response placeholder
            self._response_json = {}
            
            logger.info(f"Initialized {self._provider} predictor for model {self._model}, "
                        f"temp={self._temperature}, max_tokens={self._max_tokens}, "
                        f"top_p={self._top_p}, stream={self._stream}")
                        
        except Exception as e:
            exception_msg = f"Exception while creating LiteLLM predictor for endpoint_name={endpoint_name}: {e}"
            logger.error(exception_msg)
            raise ValueError(exception_msg)

    def get_prediction(self, payload: Dict) -> FMBenchPredictionResponse:
        """
        Get a prediction from the external model.
        
        Args:
            payload: Dictionary containing the input prompt
            
        Returns:
            FMBenchPredictionResponse with generated text and metrics
        """
        # Extract the prompt from the payload
        prompt_input_data = payload['inputs']
        
        # Variables to track metrics
        latency: Optional[float] = None
        completion_tokens: Optional[int] = None
        prompt_tokens: Optional[int] = None
        TTFT: Optional[float] = None
        TPOT: Optional[float] = None
        TTLT: Optional[float] = None
        response_dict_from_streaming: Optional[Dict] = None
        
        # Add logic to retry if there are throttling errors
        INITIAL_RETRY_DELAY: float = 2.0 
        MAX_RETRY_DELAY: float = 60.0  
        retry_count = 0
        
        while True:
            try:
                # Format as chat messages
                messages = [{"role": "user", "content": prompt_input_data}]
                
                # Prepare the request based on provider
                request = {
                    "model": self._model,
                    "messages": messages,
                    "temperature": self._temperature,
                    "max_tokens": self._max_tokens,
                    "top_p": self._top_p,
                    "stream": self._stream
                }
                
                # Add provider-specific parameters
                if self._provider == "azure":
                    # Azure requires explicit API base and version
                    request["api_base"] = os.environ.get("AZURE_API_BASE")
                    request["api_version"] = os.environ.get("AZURE_API_VERSION")
                
                # Make the API call
                logger.info(f"Invoking {self._model} via {self._provider} to get inference")
                st = time.perf_counter()
                
                response = litellm.completion(**request)
                
                # Extract latency in seconds
                latency = time.perf_counter() - st
                
                # Handle streaming responses
                if self._stream is True:
                    response_dict_from_streaming = get_response_stream(
                        response,
                        st,
                        self._start,
                        self._stop,
                        is_sagemaker=False
                    )
                    TTFT = response_dict_from_streaming.get('TTFT')
                    TPOT = response_dict_from_streaming.get('TPOT')
                    TTLT = response_dict_from_streaming.get('TTLT')
                    response = response_dict_from_streaming['response']
                    self._response_json["generated_text"] = json.loads(response)[0].get('generated_text')
                    
                    # Count tokens for streaming responses
                    prompt_tokens = token_counter(model=self._model, messages=messages)
                    completion_tokens = token_counter(text=self._response_json["generated_text"])
                    logger.info(f"Streaming prompt token count: {prompt_tokens}, "
                                f"completion token count: {completion_tokens}, latency: {latency}")
                    break
                else:
                    # Extract completion text from non-streaming response
                    for choice in response.choices:
                        if choice.message and choice.message.content:
                            self._response_json["generated_text"] = choice.message.content
                            break
                    
                    # Extract token counts from response usage
                    prompt_tokens = response.usage.prompt_tokens
                    completion_tokens = response.usage.completion_tokens
                    
                    # Extract latency
                    latency = response._response_ms / 1000 if hasattr(response, '_response_ms') else latency
                    break
                    
            except RateLimitError as e:
                # Retry with exponential backoff on rate limit errors
                retry_count += 1
                wait_time = min(INITIAL_RETRY_DELAY * (2 ** (retry_count - 1)), MAX_RETRY_DELAY)
                logger.warning(f"Rate limit error: {e}. Retrying in {wait_time:.2f} seconds... (Attempt {retry_count})")
                time.sleep(wait_time)
                
            except Exception as e:
                logger.error(f"Unexpected error during prediction, endpoint_name={self._endpoint_name}, "
                            f"exception={e}")
                raise
        
        return FMBenchPredictionResponse(
            response_json=self._response_json,
            latency=latency,
            time_to_first_token=TTFT,
            time_per_output_token=TPOT,
            time_to_last_token=TTLT,
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens
        )
    
    def calculate_cost(self,
                      instance_type: str,
                      instance_count: int,
                      pricing: Dict,
                      duration: float,
                      prompt_tokens: int,
                      completion_tokens: int) -> float:
        """
        Calculate the cost of inference based on token usage.
        
        Args:
            instance_type: The model ID
            instance_count: Not used for token-based pricing
            pricing: Dictionary containing pricing data
            duration: Not used for token-based pricing
            prompt_tokens: Number of input tokens
            completion_tokens: Number of output tokens
            
        Returns:
            The calculated cost in USD
        """
        experiment_cost: Optional[float] = None
        input_token_cost: Optional[float] = None
        output_token_cost: Optional[float] = None
        
        try:
            logger.info("Calculating cost with token-based pricing")
            # Retrieve pricing information for the model
            token_based_pricing = pricing['pricing']['token_based']
            
            # Calculate cost based on token usage
            model_pricing = token_based_pricing.get(instance_type, None)
            if model_pricing:
                input_token_cost = (prompt_tokens / 1000.0) * model_pricing['input-per-1k-tokens']
                output_token_cost = (completion_tokens / 1000.0) * model_pricing['output-per-1k-tokens']
                experiment_cost = input_token_cost + output_token_cost
                logger.info(f"model={instance_type}, prompt_tokens={prompt_tokens}, "
                            f"input_token_cost={input_token_cost}, completion_tokens={completion_tokens}, "
                            f"output_token_cost={output_token_cost}, experiment_cost={experiment_cost}")
            else:
                logger.error(f"Model pricing for \"{instance_type}\" not found in pricing.yml")
                
        except Exception as e:
            logger.error(f"Exception occurred during cost calculation: {e}")
            
        return experiment_cost

    def get_metrics(self,
                   start_time: datetime,
                   end_time: datetime,
                   period: int = 60) -> pd.DataFrame:
        """
        Get metrics for the external model. Not implemented for external models.
        
        Returns:
            None, as external APIs don't provide standard metrics
        """
        return None

    def shutdown(self) -> None:
        """
        Shutdown the predictor. No resources to clean up for external APIs.
        """
        return None

    @property
    def endpoint_name(self) -> str:
        """The endpoint name property."""
        return self._endpoint_name

    @property
    def inference_parameters(self) -> Dict:
        """The inference parameters property."""
        return dict(
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            top_p=self._top_p
        )

    @property
    def platform_type(self) -> Dict:
        """The platform type property."""
        return constants.PLATFORM_EXTERNAL

def create_predictor(endpoint_name: str, inference_spec: Optional[Dict], metadata: Optional[Dict]):
    """
    Create a LiteLLM predictor for external models.
    
    Args:
        endpoint_name: The model ID (e.g., gpt-4, azure-gpt-4, gemini-pro)
        inference_spec: Dictionary containing inference parameters
        metadata: Dictionary containing provider metadata (API keys, etc.)
        
    Returns:
        A configured LiteLLMPredictor instance
    """
    return LiteLLMPredictor(endpoint_name, inference_spec, metadata)