# Attribution and source provenance

The original catalyst generation framework, structure-string representation
and related generation/decoding utilities are based on **CatGPT**, by
**Dong Hyeon Mok and Seoin Back**:

- Original repository: https://github.com/SeoinBack/CatGPT
- Paper: https://arxiv.org/abs/2407.14040
- Related journal DOI: https://doi.org/10.1021/jacs.4c11504

The project author, **RileyLi911**, adapted the CatGPT code and carried out
the model training and subsequent research workflow:

- **Base pretraining:** `checkpoint-GPT-2M/checkpoint-138890` was trained from
  scratch by RileyLi911. It was not initialized from a CatGPT-author-provided
  pretrained checkpoint.
- **CH3 fine-tuning:** `data/finetune_model/checkpoint-CH3` was trained by
  RileyLi911 as a LoRA adapter on the self-trained base model.
- **Downstream work:** structure generation, screening and associated code
  modifications were carried out by the project author.
- **Weight distribution:** our group provides these author-trained model
  weights through the linked Hugging Face repository maintained by RileyLi911.
  RileyLi911 performed their training; our group is not redistributing
  CatGPT-author-provided weights.

CatGPT is credited for the original architecture, methods and reused code.
That attribution does not assign this project's training, checkpoints or
downstream screening work to the CatGPT authors. This repository packages the
inference portion of RileyLi911's work; it does not include the full training
or screening workflows and is not an official CatGPT release.

The immediate source for this bundle is
https://github.com/RileyLi911/autocata at commit
`d2cfed21d00be37fb3a0527d660d839ffbe88fe1`.

| Bundled path | Source / changes |
| --- | --- |
| `script/generate.py` | AutoCata generation entry; CPU/CUDA, explicit base checkpoint and PEFT adapter loading |
| `script/ASE_check_manual.py` | AutoCata tokenizer decoding and XYZ reconstruction |
| `script/index_xyz_metadata.py` | AutoCata formula/material indexing |
| `script/download_models.py` | AutoCata Hugging Face downloader |
| `autocata_core/utils/generation_utils.py` | CatGPT-derived structure-string / cell conversion utilities, retained from AutoCata |
| `autocata_core/__init__.py`, `autocata_core/utils/__init__.py` | Minimal AutoCata package support |
| `run_generation.py`, legacy filename wrappers, configs, environment, docs, tests | Packaging additions for this CH3 distribution |

The upstream repository inspected on 2026-10-10 at commit
`58c00ba835a92623e2140b42e9b17f11fb869011` had no standalone LICENSE/COPYING
file in its tree. This observation concerns the reused upstream code, not
the training provenance of RileyLi911's model weights. No replacement license
for upstream code is asserted here. Retain upstream code attribution; terms
for this project's author-trained weights must be stated separately by the
project author. A paper's license is not automatically a software or model
license.

Suggested citation for the original work:

```bibtex
@article{mok2024catgpt,
  title={Generative Language Model for Catalyst Discovery},
  author={Mok, Dong Hyeon and Back, Seoin},
  journal={arXiv preprint arXiv:2407.14040},
  year={2024},
  doi={10.48550/arXiv.2407.14040}
}
```
