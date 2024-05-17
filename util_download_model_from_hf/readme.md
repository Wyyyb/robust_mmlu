---
language:
- en
dataset_info:
  features:
  - name: question_id
    dtype: int64
  - name: question
    dtype: string
  - name: options
    sequence: string
  - name: answer
    dtype: string
  - name: answer_index
    dtype: int64
  - name: cot_content
    dtype: string
  - name: category
    dtype: string
  - name: src
    dtype: string
  splits:
  - name: test
    num_bytes: 8946036
    num_examples: 12187
  - name: validation
    num_bytes: 62972
    num_examples: 70
  download_size: 4298444
  dataset_size: 9009008
configs:
- config_name: default
  data_files:
  - split: test
    path: data/test-*
  - split: validation
    path: data/validation-*
license: mit
task_categories:
- question-answering
tags:
- evaluation
pretty_name: MMLU-Pro
size_categories:
- 10K<n<100K
---

# MMLU-Pro Dataset Introduction

Introducing MMLU-Pro dataset, a more **robust** and **challenging** massive multi-task understanding dataset tailored to more rigorously benchmark large language models' capabilities. This dataset contains 12K complex questions across various disciplines. 

## 1. What's new about MMLU-Pro

Compared to original MMLU, there are three major differences:

- The original MMLU dataset only contains 4 options, MMLU-Pro increases it to 10 options. The increase in options will make the evaluation more realistic and challenging. The random guessing will lead to a much lower score.
- The original MMLU dataset contains mostly knowledge-driven questions without requiring much reasoning. Therefore, PPL results are normally better than CoT. In our dataset, we increase the problem difficulty and integrate more reasoning-focused problems. In MMLU-Pro, CoT can be 20% higher than PPL. 
- Due to the increase of options, we found that the model performance becomes more robust. For example, Llama-2-7B performance variance on MMLU-Pro is within 1% with several different prompts. In contrast, the performance variance on original MMLU can be as huge as 4-5%.

## 2. Dataset Summary

- **Questions and Options:** Each question within the dataset typically has **ten** multiple-choice options, except for some that were reduced during the manual review process to remove unreasonable choices. This increase from the original **four** options per question is designed to enhance complexity and robustness, necessitating deeper reasoning to discern the correct answer among a larger pool of potential distractors.
  
- **Sources:** The dataset consolidates questions from several sources:
  - **Original MMLU Questions:** Part of the dataset is coming from the original MMLU dataset. We remove the trivial and ambiguous questions.
  - **STEM Website:** Hand picking high-quality STEM problems from the Internet.
  - **TheoremQA:** High-quality human-annotated questions requiring theorems to solve.
  - **Scibench:** Science questions from college exams.

- **Disciplines Covered by the Newly Added Data:** The subjects that have been enhanced with questions from STEM Website, TheoremQA, and SciBench are biology, business, chemistry, computer science, economics, engineering, math, physics and psychology.

| Discipline       | Number of Questions | From Original MMLU | Newly Added |
|:-----------------|:--------------------|:-------------------|:------------|
| Math             | 1357                | 852	              | 505         |
| Physics          | 1312                | 419	              | 893         |
| Chemistry        | 1143                | 180	              | 963         |
| Law              | 1120                | 1120	              | 0           |
| Engineering      | 972                 | 67	              | 905         |
| Other            | 942                 | 942	              | 0           |
| Health           | 825                 | 825	              | 0           |
| Psychology       | 818                 | 510	              | 308         |
| Economics        | 861                 | 454	              | 407         |
| Business         | 796                 | 159	              | 637         |
| Biology          | 722                 | 222	              | 500         |
| Philosophy       | 511                 | 511	              | 0           |
| Computer Science | 418                 | 282	              | 136         |
| History          | 390                 | 390	              | 0           |
| **Total**        | **12187**           | 6933	              | 5254        |

![image/png](https://cdn-uploads.huggingface.co/production/uploads/636a35eff8d9af4aea181608/d4XNCwgTVABO3N1tCJQlj.png)

 
## 3. Dataset Construction

![image/png](https://cdn-uploads.huggingface.co/production/uploads/636a35eff8d9af4aea181608/kP6hA-T7ldXxOvqTJf42X.png)

- **Initial Filtering:** The construction process began with a comprehensive review of the original MMLU dataset to identify and retain only those questions that meet a higher threshold of difficulty and relevance.
  
- **Question Collection and Integration:** Additional questions were carefully selected from STEM websites, theoremQA, and scibench based on their ability to challenge the analytical capabilities of advanced models. The selection criteria focused on the complexity of the problems and the quality of the questions.
  
- **Option Augmentation:** To further enhance the dataset, we employed GPT-4 to augment the number of choices per question from **four** to **ten**. This process was not merely about adding more options but involved generating plausible distractors that require discriminative reasoning to navigate.
  
- **Expert Review:** Each question and its associated options underwent rigorous scrutiny by a panel of over ten experts. These experts ensured that the questions are not only challenging and comprehensive but also accurate and fair. This step was crucial to maintain the integrity and utility of the dataset as a benchmarking tool.


## 4. Leaderboard

The following are the accuracies of various seminal models evaluated on MMLU-Pro: 

|Models                       | Prompting | Original MMLU   | Overall | Biology | Business | Chemistry | ComputerScience  | Economics | Engineering | Health | History | Law   | Math  | Philosophy | Physics | Psychology | Other |
|:----------------------------|:----------|:----------------|:--------|:--------|:---------|:----------|:-----------------|:-----------|------------|:-------|:--------|:------|:------|:-----------|:--------|:-----------|:------|
| GPT-4o                      | CoT       | 0.887           | 0.7149  | 0.8504  | 0.7852   | 0.7428    | 0.7512           | 0.784     | 0.5401      | 0.7152 | 0.6718  | 0.5393| 0.762 | 0.6947     | 0.7355  | 0.7726     | 0.7091|
| GPT-4-Turbo                 | CoT       | 0.864           | 0.6258  | 0.8186  | 0.6621   | 0.6325    | 0.6914           | 0.7329    | 0.3591      | 0.6824 | 0.6462  | 0.492 | 0.6455| 0.6047     | 0.5488  | 0.7433     | 0.6773|
| Claude-3-Sonnet             | CoT       | 0.815           | 0.5793	| 0.6717  | 0.6658	 | 0.5424	 | 0.5933	        | 0.6876	| 0.4547	  | 0.6339 | 0.5359	 |0.4268 | 0.5475| 0.5753	  | 0.5625	| 0.6736	 | 0.6444|
| Llama-3-70B-Instruct        | CoT       | 0.820           | 0.5541  | 0.777   | 0.5804   | 0.4733    | 0.61             | 0.676     | 0.4146      | 0.6582 | 0.5615  | 0.4036| 0.5232| 0.5479     | 0.4962  | 0.6834     | 0.5679|
| DeepSeek V2                 | CoT       | 0.785           | 0.5305  | 0.669   | 0.6055   | 0.5053    | 0.4833           | 0.6458    | 0.323       | 0.5751 | 0.4526  | 0.3816| 0.5409| 0.53       | 0.5229  | 0.6385     | 0.5913|
| Llama-3-70B                 | CoT       | 0.795           | 0.4995  | 0.7147  | 0.4887   | 0.3893    | 0.5359           | 0.6074    | 0.3086      | 0.5903 | 0.5103  | 0.3241| 0.4731| 0.5793     | 0.4863  | 0.6736     | 0.5456|
| MAmmoTH2-8x7B               | CoT       | 0.683           | 0.482   | 0.698	  | 0.54     | 0.417     | 0.483            | 0.603	    | 0.335	      | 0.526  | 0.4846	 | 0.325 | 0.487 | 0.4618     |	0.443	| 0.588	     | 0.496 |
| MAmmoTH2-8B                 | CoT       | 0.646           | 0.4101  | 0.6108  | 0.4899	 | 0.3945	 | 0.409	        | 0.547	    | 0.2685	  | 0.3939 | 0.3794	 | 0.2232| 0.4458| 0.3581	  | 0.3689	| 0.511	     | 0.415 |
| Phi-3-mini-4k-instruct      | CoT       | 0.688           | 0.4096  | 0.626   | 0.4623   | 0.308     | 0.4043           | 0.5668    | 0.2346      | 0.4715 | 0.3615  | 0.2848 | 0.3817 | 0.3953    | 0.3537  | 0.6015    | 0.4352|
| Yi-34B                      | CoT       | 0.763           | 0.4087  | 0.608   | 0.3882   | 0.2773    | 0.4211           | 0.525     | 0.3138      | 0.5164 | 0.4744  | 0.2893 | 0.325  | 0.4384    | 0.3255  | 0.588     | 0.5042|
| Mixtral-8x7B-Instruct-v0.1  | CoT       | 0.714           | 0.404   | 0.633   | 0.4008   | 0.3141    | 0.4043           | 0.5192    | 0.2695      | 0.463  | 0.3897  | 0.2884 | 0.3478 | 0.4481    | 0.3636  | 0.5611    | 0.4416|
| Mixtral-8x7B-v0.1           | CoT       | 0.706           | 0.3893  | 0.6011  | 0.3354   | 0.2782    | 0.4522           | 0.4971    | 0.2716      | 0.4448 | 0.4256  | 0.2616 | 0.3368 | 0.4384    | 0.3613  | 0.5489    | 0.4406|
| Llama-3-8B-Instruct         | CoT       | 0.684           | 0.3831  | 0.6593  | 0.3756   | 0.2686    | 0.3852           | 0.4994    | 0.2963      | 0.457  | 0.3667  | 0.2491| 0.339 | 0.3562     | 0.3239  | 0.5526     | 0.414 |
| Llama-2-70B                 | CoT       | 0.697           | 0.3609  | 0.5845  | 0.3719   | 0.2222    | 0.3541           | 0.4623    | 0.2366      | 0.4024 | 0.4103  | 0.2696| 0.2668| 0.4364     | 0.2873  | 0.5672     | 0.4565|
| Llama-3-8B                  | CoT       | 0.666           | 0.3392  | 0.5748  | 0.3191   | 0.2318    | 0.3517           | 0.4309    | 0.2644      | 0.4036 | 0.3513  | 0.1964| 0.2903| 0.3601     | 0.2927  | 0.5049     | 0.3822|
| Mistral-7B                  | CoT       | 0.625           | 0.2981  | 0.4958  | 0.2776   | 0.1977    | 0.3062           | 0.3775    | 0.2346      | 0.3455 | 0.2974  | 0.1839 | 0.2439 | 0.3483    | 0.25    | 0.4658    | 0.3418|
| Yi-6B                       | CoT       | 0.632           | 0.2562  | 0.4418  | 0.2751   | 0.1347    | 0.2392           | 0.3484    | 0.1924      | 0.3103 | 0.2667  | 0.1875 | 0.1842 | 0.3033    | 0.1845  | 0.3888    | 0.327 |
| Llama-2-13B                 | CoT       | 0.538           | 0.2445  | 0.403   | 0.2374   | 0.1584    | 0.2297           | 0.3124    | 0.1955      | 0.2897 | 0.2462  | 0.1661| 0.1592| 0.2877     | 0.1951  | 0.3973     | 0.3174|
| Llama-2-7B                  | CoT       | 0.457           | 0.194   | 0.3393  | 0.1872   | 0.1277    | 0.1699           | 0.2962    | 0.1358      | 0.2242 | 0.1846  | 0.1634| 0.1231| 0.2172     | 0.1555  | 0.3142     | 0.1985|

The non-CoT results are reported in the following table. As you can see, the performance drop by as much as 18% without chain-of-thought reasoning. It reflects the challenge of our dataset.

|Models                       | Prompting | Overall | Biology | Business | Chemistry | ComputerScience  | Economics | Engineering | Health | History | Law   | Math  | Philosophy | Physics | Psychology | Other |
|:----------------------------|:----------|:--------|:--------|:---------|:----------|:-----------------|:-----------|------------|:-------|:--------|:------|:------|:-----------|:--------|:-----------|:------|
| GPT-4o                      | Direct    | 0.5346  | 0.8102  | 0.392    | 0.3447    | 0.5813           | 0.6899    | 0.3981      | 0.6933 | 0.6949  | 0.542 | 0.3427| 0.6614     | 0.3971  | 0.7628     | 0.6391|
| GPT-4-Turbo                 | Direct    | 0.4836  | 0.7825  | 0.353    | 0.308     | 0.5526           | 0.6365    | 0.3292      | 0.6485 | 0.6231  | 0.4813| 0.2623| 0.589      | 0.3582  | 0.7323     | 0.5881|
| DeepSeek V2                 | Direct    | 0.4709  | 0.7365  | 0.3736   | 0.3319    | 0.5215           | 0.6023    | 0.4002      | 0.5751 | 0.5526  | 0.4154| 0.3451| 0.5431     | 0.371   | 0.6826     | 0.5224|

