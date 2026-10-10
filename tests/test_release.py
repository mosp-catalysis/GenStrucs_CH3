"""Packaging smoke tests: no torch, model weights, GPU or network required."""
import argparse
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ch3_runner', ROOT / 'run_generation.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ReleaseTests(unittest.TestCase):
    def test_dry_run_has_no_subprocesses_or_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'not_created'
            with patch.object(runner.subprocess, 'run') as execute, redirect_stdout(io.StringIO()):
                self.assertEqual(runner.main(['--dry-run', '--output-dir', str(output)]), 0)
            execute.assert_not_called()
            self.assertFalse(output.exists())

    def test_commands_use_bundled_paths_and_adapter(self):
        args = argparse.Namespace(n_generation=5, device='cpu', batch_size=1)
        commands = runner.build_commands(args, ROOT / 'outputs/test')
        for command in commands:
            self.assertTrue(Path(command[1]).is_file())
        generation = commands[1]
        self.assertEqual(generation[generation.index('--ckpt-path') + 1],
                         str(ROOT / 'data/finetune_model/checkpoint-CH3'))
        self.assertIn('--base-checkpoint', generation)
        self.assertIn('--tokenizer-path', generation)
        self.assertIn('--check-only', commands[0])

    def test_run_orders_stages_and_records_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'run'
            with patch.object(runner.subprocess, 'run') as execute, redirect_stdout(io.StringIO()):
                runner.main(['--output-dir', str(output)])
            self.assertEqual(execute.call_count, 4)
            self.assertTrue((output / 'commands.json').is_file())
            self.assertTrue((output / 'run.log').is_file())

    def test_output_and_scale_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'keep.txt').write_text('original')
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                runner.main(['--dry-run', '--output-dir', tmp])
            self.assertEqual((Path(tmp) / 'keep.txt').read_text(), 'original')
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            runner.main(['--n-generation', '0'])

    def test_manifest_covers_inference_files_only(self):
        config = yaml.safe_load((ROOT / 'config/model_assets.yml').read_text())['model_assets']
        self.assertEqual(len(config['revision']), 40)
        self.assertTrue(set(config['required_paths']) <= set(config['allow_patterns']))
        self.assertTrue(all(path.startswith(('checkpoint-GPT-2M/checkpoint-138890/',
                                            'data/finetune_model/checkpoint-CH3/'))
                            for path in config['allow_patterns']))
        self.assertFalse(any('optimizer' in path or 'MLP' in path for path in config['allow_patterns']))
        self.assertIn('data/finetune_model/checkpoint-CH3/adapter_model.safetensors', config['required_paths'])


if __name__ == '__main__':
    unittest.main()
