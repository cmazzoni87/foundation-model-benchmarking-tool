# Getting started with `FMBench`

`FMBench` is available as a Python package on [PyPi](https://pypi.org/project/fmbench) and is run as a command line tool once it is installed. All data that includes metrics, reports and results are stored in an Amazon S3 bucket.

While technically you can run `FMBench` on any AWS compute, practically speaking it's best to run it on a SageMaker Notebook to benchmark Amazon Bedrock models.

**Intro Video**

[![FMBench Intro](img/fmbench-thumbnail.png)](https://www.youtube.com/watch?v=yvRCyS0J90c)

## Running `FMBench` on Amazon SageMaker Notebook

1. Launch the AWS CloudFormation template included in this repository using one of the buttons from the table below. The CloudFormation template creates Amazon S3 buckets, Amazon IAM role and an Amazon SageMaker Notebook with this repository cloned.

   |AWS Region                |     Link        |
   |:------------------------:|:-----------:|
   |us-east-1 (N. Virginia)    | [<img src="../img/ML-FMBT-cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=fmbench&templateURL=https://aws-blogs-artifacts-public.s3.amazonaws.com/artifacts/ML-FMBT/template.yml) |
   |us-west-2 (Oregon)    | [<img src="../img/ML-FMBT-cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=fmbench&templateURL=https://aws-blogs-artifacts-public.s3.amazonaws.com/artifacts/ML-FMBT/template.yml) |
   |us-gov-west-1 (GovCloud West)    | [<img src="../img/ML-FMBT-cloudformation-launch-stack.png">](https://us-gov-west-1.console.amazonaws-us-gov.com/cloudformation/home?region=us-gov-west-1#/stacks/new?stackName=fmbench&templateURL=https://aws-blogs-artifacts-public.s3.amazonaws.com/artifacts/ML-FMBT/template.yml) |

2. Once the CloudFormation stack is created, navigate to SageMaker Notebooks and open the `fmbench-notebook`.

3. On the `fmbench-notebook` open a Terminal and run the following commands.

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   export PATH="$HOME/.local/bin:$PATH"
   uv venv .fmbench_python312 --python 3.12
   source .fmbench_python312/bin/activate
   uv pip install -U fmbench
   ```

4. Now you are ready to run `fmbench` with the following command line. We will use a sample config file placed in the S3 bucket by the CloudFormation stack for a quick first run.
   
   ```bash
   account=`aws sts get-caller-identity | jq .Account | tr -d '"'`
   region=`aws configure get region`
   fmbench --config-file s3://sagemaker-fmbench-read-${region}-${account}/configs/bedrock/config-bedrock-claude.yml > fmbench.log 2>&1
   ```

5. Open another terminal window and do a `tail -f` on the `fmbench.log` file to see all the traces being generated at runtime.
   
   ```bash
   tail -f fmbench.log
   ```

6. The generated reports and metrics are available in the `sagemaker-fmbench-write-<replace_w_your_aws_region>-<replace_w_your_aws_account_id>` bucket. The metrics and report files are also downloaded locally and in the `results` directory (created by `FMBench`) and the benchmarking report is available as a markdown file called `report.md` in the `results` directory.