# EduInvest

EduInvest is a lightweight educational desktop application created for a hackathon. It blends a simple PyQt6 GUI with market data from `yfinance` and a placeholder AI model to help students learn about stock movement prediction in a fun, game-like environment.

---

## Project overview

- Name: EduInvest
- Type: Desktop application (Python, PyQt6)
- Purpose: Teach basic market intuition by letting students guess whether a selected stock will go up or down; compare with an AI prediction and display price history.
- Hackathon: Quick-prototyped for learning, demo, and discussion.

---

## Features

- Interactive GUI built with PyQt6.
- Trending stock list and random stock selection for a short game.
- AI model (placeholder) that predicts Up/Down for the next trading day.
- Embedded matplotlib chart showing recent close prices for the selected ticker.
- Simple scoring and streak system to make learning rewarding.
- Modular code to swap-in a real model in the future.

---

## How it works (high level)

1. The GUI selects a stock (random from a curated list).
2. It fetches historical price data using `yfinance` and displays a 1-year close-price chart.
3. A placeholder AI function returns a direction (`Up` / `Down`) for the next day.
4. The user guesses whether the price will go up or down. The app reveals whether the AI was right and updates the score and streak.

---

## Installation (macOS-focused)

This project depends on Python and several packages. The heavy ML dependencies (`torch`, `torch_geometric`) are intentionally left for advanced users to install separately.

Prerequisites
- macOS (Intel or Apple Silicon)
- Python 3.10 or 3.11 (recommend using `pyenv` or the python.org installer)
- Xcode command line tools (for compiling wheels when necessary): `xcode-select --install`

Quick install (recommended for demo / student use)

1. Open a Terminal and clone or extract the project folder.
2. Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the lightweight dependencies (does not include `torch` or `torch_geometric`):

```bash
pip install -r requirements.txt
```

4. Install PyTorch (CPU-only recommended for ease):

```bash
# Example: CPU wheel install (check https://pytorch.org/get-started/locally/ for latest)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

5. If you need GNN features, follow the instructions at https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html to install `torch_geometric` and its dependencies.

6. Run the app:

```bash
python eduinvest.py
```

---

## How to run the app

- With the venv active, run `python eduinvest.py`.
- The GUI will open. Click the Up or Down buttons to make guesses. The app picks a new random stock after each guess and updates the price chart.

---

## The AI component

- The repository includes a simple placeholder function that returns `Up` or `Down` (and previously a confidence). This is intentionally lightweight for the hackathon demo.
- The placeholder is located in `eduinvest.py` (the `model_predict_direction` function delegates to a model wrapper). The real model would be a PyTorch model that consumes three modalities (time-series transformer, GNN, sentiment LSTM) in `model.py`.
- For the demo, the AI provides a direction that the UI compares against the user's guess.

