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

Welcome to the MMLU-Pro dataset, a refined and advanced extension of the original MMLU dataset tailored to benchmark and challenge large language models. This dataset is meticulously constructed to test the limits of large language models by presenting them with highly complex and nuanced questions across various disciplines.

## 1. Dataset Summary

The MMLU-Pro dataset is designed to be a rigorous testing ground for large language models, aiming to highlight the distinctions in capabilities among different systems. It incorporates a selection of challenging questions that require advanced reasoning, comprehension, and problem-solving skills. This dataset is particularly valuable for researchers and developers seeking to evaluate the depth and breadth of understanding that their models can achieve.

## 2. Dataset Structure Overview

- **Questions and Options:** Each question within the dataset is accompanied by ten multiple-choice options. This increase from the original four options per question is intended to add complexity, requiring deeper reasoning to identify the correct answer among more potential distractors.
  
- **Sources:** The dataset consolidates questions from several reputable sources:
  - **Original MMLU Questions:** Selected for their complexity and relevance.
  - **Stemez Website:** Known for its rigorously curated STEM-focused questions.
  - **TheoremQA and Scibench Datasets**
  
- **Categories:** To facilitate targeted research, questions are meticulously categorized by their source and subject area. This categorization helps researchers focus on specific domains or compare model performances across different types of content. The categories include:
  - **Biology**
  - **Business**
  - **Chemistry**
  - **Computer Science**
  - **Economics**
  - **Engineering**
  - **Health**
  - **History**
  - **Law**
  - **Math**
  - **Philosophy**
  - **Physics**
  - **Psychology**
  - Other categories are grouped under **Other**, which includes miscellaneous fields like politics, culture, geography, among others.

## 3. Dataset Construction

- **Initial Filtering:** The construction process began with a comprehensive review of the original MMLU dataset to identify and retain only those questions that meet a higher threshold of difficulty and relevance.
  
- **Question Collection and Integration:** Additional questions were carefully selected from stemez, theoremQA, and scibench based on their ability to challenge the analytical capabilities of advanced models. The selection criteria focused on the complexity of the problems and the quality of the questions.
  
- **Augmentation with GPT-4:** To further enhance the dataset, we employed GPT-4 to augment the number of choices per question from **four** to **ten**. This process was not merely about adding more options but involved generating plausible distractors that require discriminative reasoning to navigate.
  
- **Expert Review:** Each question and its associated options underwent rigorous scrutiny by a panel of over ten experts. These experts ensured that the questions are not only challenging and comprehensive but also accurate and fair. This step was crucial to maintain the integrity and utility of the dataset as a benchmarking tool.


