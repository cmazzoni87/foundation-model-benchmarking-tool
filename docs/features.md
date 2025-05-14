# `FMBench` features

**Support for Model Evaluations**: FMBench adds support for evaluating models using Majority Voting with a [Panel of LLM Evaluators](https://arxiv.org/abs/2404.18796). Users can now use FMBench to evaluate model accuracy across open-source and custom datasets, thus FMBench enables users to not only measure performance (inference latency, cost, throughput) but also model accuracy.

**Website for better user experience**: FMBench has a [website](https://aws-samples.github.io/foundation-model-benchmarking-tool/) along with an [introduction video](https://youtu.be/yvRCyS0J90c). The website is fully searchable to ease common tasks such as installation, finding the right config file, benchmarking on Bedrock, model evaluation, etc. This website was created based on feedback from several internal teams and external customers.

**Native support for Amazon Bedrock**: FMBench benchmarks and evaluates any Foundation Model (FM) available on Amazon Bedrock. See [list of config files](https://aws-samples.github.io/foundation-model-benchmarking-tool/manifest.html) supported out of the box, you can use these config files either as is or as templates for creating your own custom config.

**Streaming support**: FMBench supports streaming responses from models, allowing you to measure metrics like Time To First Token (TTFT), Time Per Output Token (TPOT), and Time To Last Token (TTLT).

**Multimodal models**: Support for benchmarking multimodal models that can process both text and images.