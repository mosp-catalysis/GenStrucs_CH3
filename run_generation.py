#!/usr/bin/env python3
"""CH3 generation -> XYZ conversion -> formula/material metadata, without MLP."""
import argparse
import json
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def positive(value):
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return value


def build_commands(args, output):
    config = ROOT / "config/config.yml"
    base = ROOT / "checkpoint-GPT-2M/checkpoint-138890"
    adapter = ROOT / "data/finetune_model/checkpoint-CH3"
    generated = output / "generated"
    analysis = output / "analysis"
    generation = [sys.executable, str(ROOT / "script/generate.py"),
                  "--config", str(config), "--adsorbate", "CH3",
                  "--ckpt-path", str(adapter), "--base-checkpoint", str(base),
                  "--tokenizer-path", str(adapter), "--save-path", str(generated),
                  "--n-generation", str(args.n_generation), "--device", args.device]
    if args.batch_size:
        generation.extend(["--batch-size", str(args.batch_size)])
    return [
        [sys.executable, str(ROOT / "script/download_models.py"), "--check-only"],
        generation,
        [sys.executable, str(ROOT / "script/ASE_check_manual.py"), "--config", str(config),
         "--adsorbate", "CH3", "--tokenizer-path", str(adapter),
         "--pkl-path", str(generated / "generated_CH3.pkl"), "--output-dir", str(analysis)],
        [sys.executable, str(ROOT / "script/index_xyz_metadata.py"), "--config", str(config),
         "--adsorbate", "CH3", "--adsorbate-formula", "CH3",
         "--xyz-dir", str(analysis / "xyz"), "--output-dir", str(analysis)],
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-generation", type=positive, default=5)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--batch-size", type=positive)
    parser.add_argument("--output-dir", help="Fresh output directory (relative to this repository).")
    parser.add_argument("--dry-run", action="store_true", help="Print commands only; no model loading or writes.")
    args = parser.parse_args(argv)
    output = Path(args.output_dir or f"outputs/ch3_{datetime.now():%Y%m%d_%H%M%S_%f}")
    if not output.is_absolute():
        output = ROOT / output
    output = output.resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error(f"Output must be a new or empty directory: {output}")
    commands = build_commands(args, output)
    for command in commands:
        print(shlex.join(command), flush=True)
    if args.dry_run:
        print("[dry-run] No downloads, model inference or output writes performed.")
        return 0
    # Check local assets before creating outputs. Download is a separate action.
    subprocess.run(commands[0], cwd=ROOT, check=True)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "commands.json").open("x", encoding="utf-8") as handle:
        json.dump(commands, handle, indent=2)
    with (output / "run.log").open("x", encoding="utf-8") as log:
        for command in commands[1:]:
            log.write(shlex.join(command) + "\n")
            log.flush()
            subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
    print(f"[done] XYZ: {output / 'analysis/xyz'}")
    print(f"[done] Metadata: {output / 'analysis/xyz_metadata.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
