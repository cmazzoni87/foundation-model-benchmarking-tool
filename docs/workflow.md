# Workflow for `FMBench`

The workflow for `FMBench` is as follows:

```
Create configuration file
        |
        |-----> Reference models on Amazon Bedrock
                    |
                    |-----> Run inference against Bedrock models
                                     |
                                     |------> Create a benchmarking report
```

1. Create a dataset of different prompt sizes and select one or more such datasets for running the tests.
    1. Currently `FMBench` supports datasets from [LongBench](https://github.com/THUDM/LongBench) and filter out individual items from the dataset based on their size in tokens (for example, prompts less than 500 tokens, between 500 to 1000 tokens and so on and so forth). Alternatively, you can download the folder from [this link](https://huggingface.co/datasets/THUDM/LongBench/resolve/main/data.zip) to load the data.

1. Reference any model available on Amazon Bedrock.
    1. The tools supports all models available on Amazon Bedrock including those from Anthropic, Meta, Amazon, Cohere, and AI21.
    1. Model configuration is customizable in terms of parameters like temperature, max_tokens, and top_p.

1. Benchmark performance in terms of inference latency, transactions per minute and dollar cost per transaction for any model on Amazon Bedrock.
    1. Tests are run for each combination of the configured concurrency levels i.e. transactions (inference requests) sent to the endpoint in parallel and dataset. For example, run multiple datasets of say prompt sizes between 3000 to 4000 tokens at concurrency levels of 1, 2, 4, 6, 8 etc. so as to test how many transactions of what token length can the endpoint handle while still maintaining an acceptable level of inference latency.

1. Generate a report that compares and contrasts the performance of the model over different test configurations and stores the reports in an Amazon S3 bucket.
    1. The report is generated in the [Markdown](https://en.wikipedia.org/wiki/Markdown) format and consists of plots, tables and text that highlight the key results and provide an overall recommendation on what is the best model to use for a dataset of interest.
    1. The report is created as an artifact of reproducible research so that anyone having access to the models can run the code and recreate the same results and report.

1. Multiple [configuration files](https://github.com/aws-samples/foundation-model-benchmarking-tool/tree/main/src/fmbench/configs/bedrock) that can be used as reference for benchmarking different models on Amazon Bedrock.