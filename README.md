# GenStrucs_CH3: CH3 catalyst structure generation

Generate catalyst slab + CH3 candidate structures from a pretrained GPT-2
base and a CH3 LoRA adapter, then decode sampled tokens to extended XYZ.
This standalone inference package is extracted from
[AutoCata](https://github.com/RileyLi911/autocata) for
[GenStrucs_CH3](https://github.com/mosp-catalysis/GenStrucs_CH3).

**Both the base model and the CH3 adapter provided here were trained by
this project's author, RileyLi911.** The base model was pretrained from
scratch, and CH3 fine-tuning, subsequent structure generation and screening
were performed by the project author using modified CatGPT-based code.
No pretrained weights supplied by the CatGPT authors were used.

The model architecture, structure representation and reused portions of code
are based on [CatGPT](https://github.com/SeoinBack/CatGPT), by Dong Hyeon Mok
and Seoin Back. Please credit and cite their
[original work](https://arxiv.org/abs/2407.14040) for those contributions.
This code/method attribution is separate from the provenance of this project's
trained model weights and downstream research.

This repository distributes the inference portion of the author's work:
generation, adapter loading, model downloading, XYZ conversion and indexing.
The author's training and downstream screening workflows are not included in
this inference package. See [ATTRIBUTION.md](ATTRIBUTION.md) for the detailed
division of contributions and source provenance.

## 1. Install

```bash
git clone https://github.com/mosp-catalysis/GenStrucs_CH3.git
cd GenStrucs_CH3
conda env create -f env.yaml
conda activate genstrucs-ch3
```

Alternatively, install `requirements.txt` into a fresh Python 3.9 environment.
The dependencies are the generation/decoding subset of AutoCata; no fairchem,
PyG or MLP weights are required. CPU is supported and is the default in the
wrapper. GPU users need a compatible PyTorch CUDA installation and NVIDIA
driver. This bundle does not install drivers or a distributed runtime.

## 2. Download the models

Our group provides the author-trained model files through the repository
maintained by RileyLi911:

**https://huggingface.co/RileyLi911/autocata-models**

| Asset | Training provenance |
| --- | --- |
| `checkpoint-GPT-2M/checkpoint-138890` | Base model pretrained **from scratch by RileyLi911** using modified CatGPT-based code |
| `data/finetune_model/checkpoint-CH3` | CH3 LoRA adapter **fine-tuned by RileyLi911** on that self-trained base |

These are this project's trained weights, not weights released by CatGPT.

The included manifest pins revision
`3ae5ea6c131efae80cbe3ce8ec29aa9e653983bb` and downloads only the base model,
CH3 adapter and their tokenizers. It excludes optimizer/training state, other
adsorbates and all MLP models.

```bash
python script/download_models.py --dry-run
python script/download_models.py
python script/download_models.py --check-only
```

Required layout after download:

```text
checkpoint-GPT-2M/checkpoint-138890/
  config.json
  model.safetensors
  tokenizer.json
  tokenizer_config.json
  special_tokens_map.json
data/finetune_model/checkpoint-CH3/
  adapter_config.json
  adapter_model.safetensors
  tokenizer.json
  tokenizer_config.json
  special_tokens_map.json
```

Direct browsing: [base checkpoint](https://huggingface.co/RileyLi911/autocata-models/tree/3ae5ea6c131efae80cbe3ce8ec29aa9e653983bb/checkpoint-GPT-2M/checkpoint-138890)
and [CH3 adapter](https://huggingface.co/RileyLi911/autocata-models/tree/3ae5ea6c131efae80cbe3ce8ec29aa9e653983bb/data/finetune_model/checkpoint-CH3).
For an offline machine, download elsewhere and copy these directories with
their relative paths intact. `--check-only` checks required file presence,
not file integrity or model quality.

The CH3 checkpoint is a **LoRA adapter**, not a full standalone GPT-2 model.
Both directories are needed. The adapter metadata contains a historical
server path for its base; the loader explicitly supplies the local base model
so users do not need to recreate that server path or edit the model files.

Do not commit weights to GitHub. They are excluded by `.gitignore`; publish
code here and retain the model-download links above.

## 3. Generate and convert

Preview commands without loading models, downloading assets or creating files:

```bash
python run_generation.py --n-generation 5 --device cpu --dry-run
```

Run a small CPU example after downloading models:

```bash
python run_generation.py --n-generation 5 --device cpu \
  --output-dir outputs/ch3_smoke_001
```

For GPU generation, after the small example works:

```bash
python run_generation.py --n-generation 100 --device cuda --batch-size 8 \
  --output-dir outputs/ch3_cuda_001
```

The wrapper checks local model files, generates token sequences, converts them
to XYZ and creates formula/material indexes. It refuses nonempty output
directories. Without `--output-dir`, it uses a timestamped directory.
Progress from the underlying scripts is saved to `run.log`.

```text
outputs/ch3_smoke_001/
  commands.json
  run.log
  generated/generated_CH3.pkl
  analysis/
    xyz/sample_*.xyz
    summary.txt
    bad_samples.txt
    xyz_metadata.csv
    xyz_invalid_adsorbate.csv
    material_summary.csv
```

`--n-generation` counts sampled sequences, not guaranteed valid or unique
CH3 structures. The decoder preserves the source behavior: it can export
reconstructable structures even when validation flags are false. Inspect
`summary.txt`, `bad_samples.txt` and the metadata; `adsorbate_valid=true`
only verifies the trailing atom formula. It does not establish chemical
stability, reasonable adsorption geometry or low energy. No relaxation,
energy filtering, deduplication or MLP calculation is performed.

## Advanced: individual stages

```bash
python script/generate.py --config config/config.yml --adsorbate CH3 \
  --ckpt-path data/finetune_model/checkpoint-CH3 \
  --base-checkpoint checkpoint-GPT-2M/checkpoint-138890 \
  --tokenizer-path data/finetune_model/checkpoint-CH3 \
  --save-path outputs/manual_001/generated --n-generation 5 --device cpu

python script/ASE_check_manual.py --config config/config.yml --adsorbate CH3 \
  --tokenizer-path data/finetune_model/checkpoint-CH3 \
  --pkl-path outputs/manual_001/generated/generated_CH3.pkl \
  --output-dir outputs/manual_001/analysis

python script/index_xyz_metadata.py --config config/config.yml --adsorbate CH3 \
  --xyz-dir outputs/manual_001/analysis/xyz --output-dir outputs/manual_001/analysis
```

Use fresh directories for individual stages too. Only load trusted pickle
files. `script/generate_gpu.py` and `script/transfer_xyz.py` retain the old
filenames as thin wrappers; their CLI is the current one shown above, not a
promise of compatibility with every historical argument. Generation batch
size and sampling defaults are in `config/config.yml`; full sequence length
is 1024, matching the base model's context window. Generation is stochastic,
and this package does not claim to reproduce a historical large-scale
dataset exactly. Data archives from the original study are not included.

## Validation and repository update

```bash
python -m unittest discover -s tests -v
```

The lightweight tests exercise command construction, no-inference dry-runs,
model manifest selection and output protection. Model file listings/configs
were checked remotely during preparation, but no weights were downloaded and
no inference was run. A clean dependency installation and real model smoke
test remain necessary on the user's execution machine.

To update an existing checkout, copy **the contents of this distribution**
into the repository root, preserving its `.git` directory/history. Include
the `autocata_core/`, `config/`, `script/` and `tests/` directories, not just
the two old scripts. Keep `.gitignore`, README and attribution alongside them.
The package includes no `.git`, credentials, model weights or old results.
