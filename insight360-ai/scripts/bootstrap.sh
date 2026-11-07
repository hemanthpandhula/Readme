#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/Readme/Readme/insight360-ai
python datasets/generate_data.py
python etl/pipelines/run_etl.py --mode full
