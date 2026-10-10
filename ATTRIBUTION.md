# Attribution and source provenance

The original catalyst generation framework, structure-string representation
and related generation/decoding utilities are based on **CatGPT**, by
**Dong Hyeon Mok and Seoin Back**:

- Original repository: https://github.com/SeoinBack/CatGPT
- Paper: https://arxiv.org/abs/2407.14040
- Related journal DOI: https://doi.org/10.1021/jacs.4c11504

This repository is an adapted CH3 inference distribution, not an original
implementation of CatGPT or an official upstream CatGPT release. Training and
fine-tuning methodology should be obtained from the original authors' work.
The base and CH3-adapter files linked in the README are distributed by
our group; this is not a claim that they are the original authors' official
checkpoint release.

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
file in its tree. No replacement license for upstream code or model weights
is asserted here. Retain attribution and check applicable upstream/model
permissions before redistribution. A paper's license is not automatically a
software or model license.

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
