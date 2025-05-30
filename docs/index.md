# Benchmark foundation models on Amazon Bedrock

`FMBench` is a Python package for running performance benchmarks for **any Foundation Model (FM)** deployed on **Amazon Bedrock**. 

Here are some salient features of `FMBench`:

1. **Highly flexible**: allows you to test models with different parameters such as temperature, max tokens, and top_p, as well as testing different prompt sizes and concurrency levels.

1. **Benchmark any Bedrock model**: it can be used to benchmark any model available through Amazon Bedrock, including models from Anthropic (Claude), Meta (Llama), AI21, Cohere, and Amazon.

1. **Run anywhere**: it can be run on any AWS platform where we can run Python, such as Amazon EC2, Amazon SageMaker, or even the AWS CloudShell. _It is important to run this tool on an AWS platform so that internet round trip time does not get included in the end-to-end response time latency_.

## The need for benchmarking

<!-- markdown-link-check-disable -->
Customers often wonder which model on Amazon Bedrock is best for _their specific use-case_ and _their specific price performance requirements_. While model evaluation metrics are available on several leaderboards ([`HELM`](https://crfm.stanford.edu/helm/lite/latest/#/leaderboard), [`LMSys`](https://chat.lmsys.org/?leaderboard)), but the price performance comparison can be notoriously hard to find and even more harder to trust. In such a scenario, we think it is best to be able to run performance benchmarking yourself on either on your own dataset or on a similar (task wise, prompt size wise) open-source datasets such as ([`LongBench`](https://huggingface.co/datasets/THUDM/LongBench), [`QMSum`](https://paperswithcode.com/dataset/qmsum)). This is the problem that [`FMBench`](https://github.com/aws-samples/foundation-model-benchmarking-tool/tree/main) solves.
<!-- markdown-link-check-enable -->

## [`FMBench`](https://github.com/aws-samples/foundation-model-benchmarking-tool/tree/main): an open-source Python package for FM benchmarking on AWS

`FMBench` runs inference requests against models available on Amazon Bedrock. The metrics such as inference latency, transactions per-minute, error rates and cost per transactions are captured and presented in the form of a Markdown report containing explanatory text, tables and figures. The figures and tables in the report provide insights into what might be the best model for your use case.

## Determine the optimal model for your generative AI workload

Use `FMBench` to determine model accuracy using a panel of LLM evaluators (PoLL [[1]](#1)). Here is one of the plots generated by `FMBench` to help answer the accuracy question for various FMs on Amazon Bedrock (the model ids in the charts have been blurred out on purpose, you can find them in the actual plot generated on running FMBench).

![Accuracy trajectory with prompt size](img/accuracy_trajectory_per_payload.png)

![Overall accuracy](img/overall_candidate_model_majority_voting_accuracy.png)


## References
<a id="1">[1]</a> 
[Pat Verga et al., "Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models",    arXiv:2404.18796, 2024.](https://arxiv.org/abs/2404.18796)