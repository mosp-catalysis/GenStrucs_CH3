# Dataset Generation: Distributed Generative Transformers for Catalyst Structures

This repository documents the generation procedure of the dataset used in  
**Targeted Exploration of Ten-Million Catalyst Candidates for Methane Conversion via Distributed Generative Transformers.**

Generated catalyst surface structures produced by this model are provided in 

---

## Overview of the Generation Pipeline

The dataset generation follows a two-stage workflow:

1. **Model training / fine-tuning**  
2. **Large-scale structure generation (inference)**

This repository focuses on **stage (2)**.  
For **model training and fine-tuning**, users should refer to the original CatGPT implementation.

---

## Model Training and Fine-Tuning

The generative model architecture, tokenizer design, and training procedures are based on **CatGPT**, a Transformer-based framework for catalyst structure generation.

> **Important**  
> All training codes are **not reimplemented here**.  
> Please refer to the official CatGPT repository for full details:

🔗 **CatGPT official repository**  
https://github.com/SeoinBack/CatGPT

That repository provides:
- Tokenization schemes for catalyst structures
- Training and fine-tuning scripts
- Dataset preparation utilities

---

## Structure Generation (Inference)

Once a trained or fine-tuned model checkpoint is available, catalyst structures are generated using the provided generation script.

### Generation Script

Structure generation is performed using the `script/generate_gpu.py`

The output is a serialized .pkl file containing generated token sequences.
At this stage, no decoding, filtering, or geometry relaxation is applied.

## Decoding and Conversion to XYZ Format

The generated .pkl files are converted into readable atomistic structures using: `script/transfer_xyz.py` 

This script decodes token sequences and writes valid structures into simple XYZ files.



















