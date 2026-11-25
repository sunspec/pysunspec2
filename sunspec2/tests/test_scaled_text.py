"""The CLI must display physical units, not unscaled register values (#112)."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from sunspec2.file.client import FileClientModel


@pytest.mark.parametrize('raw,scale,expected', [
    (52000, -3, '52.0'), (52, 1, '520.0'), (52, 0, '52'),
    (0, -3, '0.0'), (None, -3, 'None'),
])
def test_point_text_uses_scale_factor(raw, scale, expected):
    model = FileClientModel(model_id=103, data={'ID': 103, 'A': raw, 'A_SF': scale})
    assert model.A.get_text().split() == ['A', expected, 'A']
    assert model.A.value == raw  # Displaying the value must not alter register data.
    assert model.A_SF.get_text().split() == ['A_SF', str(scale)]


def test_cli_displays_scaled_units(tmp_path):
    data_file = tmp_path / 'inverter.json'
    data_file.write_text(json.dumps({'models': [
        {'ID': 103, 'L': 50, 'A': 52000, 'A_SF': -3, 'W': 1234, 'W_SF': 0},
    ]}))
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, str(root / 'scripts/suns.py'), '-t', 'file', '-m', str(data_file)],
        cwd=str(root), capture_output=True, text=True, timeout=10,
        env=dict(os.environ, PYTHONPATH=str(root)),
    )
    assert result.returncode == 0, result.stderr
    rows = [line.split() for line in result.stdout.splitlines()]
    assert ['A', '52.0', 'A'] in rows
    assert ['W', '1234', 'W'] in rows
    assert ['A_SF', '-3'] in rows
