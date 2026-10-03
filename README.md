# Multi-Armed Bandit Experiments

Two early Python experiments from 2023: a nine-machine slot simulation using UCB, and a comparison of UCB, Thompson Sampling (TS), and Explore-Then-Commit (ETC) using MovieLens 1M rating distributions.

This repository preserves the original code, saved notebook outputs, and exported reports as a record of learning and practice. It was organized for GitHub in October 2026. The historical algorithms and results have not been rewritten or fully rerun; implementation limitations are documented in [legacy notes](docs/legacy-notes.md).

## Experiments

| Experiment | Model | Main files |
| --- | --- | --- |
| Nine-machine simulation | Select a machine using UCB on average net reward; sample a prize and play cost | [slot machine.py](slot_simulation/slot%20machine.py), [data.py](slot_simulation/data.py) |
| MovieLens comparison | Treat 18 movie genres as arms and sample 1–5 star rewards from each genre's historical rating distribution | [Homework.ipynb](movielens/Homework.ipynb), [Homework_v2.ipynb](movielens/Homework_v2.ipynb) |

The MovieLens notebooks cover five comparisons:

- UCB, ETC, and TS over 50,000 steps, with multiple runs.
- Horizons from 500 to 5,000,000 steps.
- Different ETC exploration lengths.
- Different UCB exploration parameters.
- Four algorithm variants over 1,000,000 steps.

The environment pools ratings by genre. User demographics are loaded but are not used to personalize arm selection.

## Historical results

[Browse all 15 recovered figures](results/README.md), or read the original [HTML report](reports/Homework.html) and [10-page PDF](reports/Homework%281%29%20-%20Jupyter%20Notebook.pdf). The PDF records an export on 29 June 2023.

![Historical UCB, ETC, and TS trajectories over 50,000 steps](results/figures/Homework-cell-05-output-00.png)

The figure above is a saved historical output, not a new reproduction. Some saved outputs do not match the current notebook source: in particular, the v2 horizon-comparison figure repeats a 500-step result. See [version differences and limitations](docs/legacy-notes.md) before interpreting algorithm rankings.

## Running the original code

Use a Python virtual environment. `requirements.txt` lists the packages imported by the historical programs; it is not a reconstruction of the original 2023 environment.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The nine-machine simulation uses only the Python standard library:

```sh
cd slot_simulation
python "slot machine.py"
```

This executes the original 100,000-play configuration, including its documented data and multiplier issues. It prints results to the terminal; no historical terminal output was recovered.

For MovieLens, first follow the [dataset setup instructions](movielens/data/README.md), then start Jupyter with the experiment directory as the working directory:

```sh
cd movielens
python -m notebook
```

Open `Homework.ipynb`, or one of the independent `UCB.ipynb`, `TS.ipynb`, and `ETC.ipynb` notebooks. Review the legacy notes first. The long-horizon cells can take substantial time; the current standalone multiprocessing script uses 500 steps and 100 runs:

```sh
python Multi_processing_Q2.py
```

## Repository layout

```text
slot_simulation/       Original nine-machine simulation and input tables
movielens/            Original comparison and independent algorithm notebooks
movielens/data/       Dataset instructions; raw MovieLens data is excluded
illustrations/        Hypothetical curves, not simulation results
reports/              Original HTML and PDF exports
results/              Figures extracted from saved notebook outputs
docs/legacy-notes.md  Historical version differences and known limitations
archive-manifest.json SHA-256 fingerprints of recovered artifacts
scripts/              Lightweight archive integrity check
```

To check that the preserved files still match the recovery snapshot:

```sh
python3 scripts/check_archive.py
```

This checks file hashes, Python/notebook syntax, and figure signatures. It does not execute experiments or validate historical scientific conclusions. When changing an algorithm, keep the recovered files intact and add a separate implementation with its own results and environment record.

## Dataset attribution

MovieLens 1M is provided by GroupLens Research. Raw dataset files are not included because its [usage terms](https://files.grouplens.org/datasets/movielens/ml-1m-README.txt) require separate permission for redistribution. Download it from the [official dataset page](https://grouplens.org/datasets/movielens/1m/).

F. Maxwell Harper and Joseph A. Konstan. 2015. *The MovieLens Datasets: History and Context*. ACM Transactions on Interactive Intelligent Systems, 5(4), Article 19. [DOI: 10.1145/2827872](https://doi.org/10.1145/2827872).

---

中文说明：这是对 2023 年两组多臂老虎机实践的历史归档，保留原程序和已有结果。2026 年只做整理与完整性检查，未重新跑完整实验。已知数据、指标和版本问题见 `docs/legacy-notes.md`；MovieLens 原始数据请从官方获取。
