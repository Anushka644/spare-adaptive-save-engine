# Spare — Adaptive Save Engine

A prototype of a behavior-aware saving system that dynamically determines how much money to save based on user context.

## 🚀 What this is

This project simulates the decision engine behind a fintech product that:
- Automatically saves money when users spend
- Adapts savings based on balance and behavior
- Avoids over-saving during financial stress

## 🧠 Key Features

- Context scoring system (0–100)
- Mode-based decision engine (Boost / Normal / Safe / Skip)
- Hard safety rules (balance floor, caps, thresholds)
- Human-readable explanations for every decision

## 🧪 Demo Scenarios

- Post-salary → higher savings
- Normal spending → balanced savings
- Month-end → reduced or skipped savings
- Low balance → no savings

## 🛠️ Tech

- Python
- Streamlit

## ▶️ Run locally

```bash
pip install streamlit
streamlit run spare_engine.py