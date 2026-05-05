# ⚽ FIFA 23 Players Statistics Dashboard
### Project 8 — Data Visualization Final Project

---


| ID        | Name                      | Worked on Charts            |
|-----------|---------------------------|-----------------------------|
| 931250594 | Abanoub Shenouda Samy     | Column, Bar, Stack, Cluster |
| 931250568 | Safia Mohamed AbdelMonsef | Scatter, Bubble             |
| 931230132 | Sara Mohamed Shokry       | Histogram                   |
| 931250568 | Doha Mohamed Ibrahim      | Box, Violin                 |
| 931250626 | Roaa Mohamed AbdelHamid   | Line, Area                  |

## 📁 Folder Structure

```
FIFA_Final_PROJECT/
├── app.py                            ← Main Dash application
├── requirements.txt                  ← Python dependencies
├── preprocessing.ipynb               ← Data cleaning & EDA notebook
├── README.md
│
├── charts/
│   ├── config.py                     ← Shared colors, layout, axis, border
│   ├── chart_01_column_bar.py        ← Week 1 & 2: Column + Bar
│   ├── chart_02_stacked_clustered.py ← Week 2: Stacked + Clustered (4 types)
│   ├── chart_03_scatter.py           ← Week 3: Scatter (2 variants)
│   ├── chart_04_bubble.py            ← Week 4: Bubble (2 variants)
│   ├── chart_05_histogram.py         ← Week 5: Histogram + KDE (3 variants)
│   ├── chart_06_box.py               ← Week 6: Box + Notched (3 variants)
│   ├── chart_07_violin.py            ← Week 7: Violin + Median (3 variants)
│   ├── chart_08_line.py              ← Week 8: Line + Moving Average (3 variants)
│   └── chart_09_area.py              ← Week 9: Area + Stacked (3 variants)
│
├── data/
│   ├── male_players.csv              ← Original FIFA 23 dataset (~18,000 players)
│   └── male_players_cleaned.csv      ← Cleaned  FIFA 23 dataset (demo: 5,000 players)

```

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Configuration
python config.py

# 3. Run all charts (optional, can run individually)
python charts/chart_01_column_bar.py
python charts/chart_02_stacked_clustered.py
python charts/chart_03_scatter.py
python charts/chart_04_bubble.py
python charts/chart_05_histogram.py
python charts/chart_06_box.py
python charts/chart_07_violin.py
python charts/chart_08_line.py
python charts/chart_09_area.py

# 4. Run dashboard
python app.py

# 5. Open browser
# → http://0.0.0.0:8050/     # replace 0.0.0.0 → localhost → https://localhost:8050/
```

---

## 🎛️ Dashboard Controls

| Control | Description                                                |
|---------|------------------------------------------------------------|
| **🏆 League** | Filter by league — [All] selects all / [None] deselects all |
| **🎯 Position** | Filter by player position                                  |
| **⭐ Overall Range** | Drag to set min/max overall rating                         |
| **📅 Edition** | Toggle FIFA 23 edition                                     |
| **↺ Reset All** | Restore all filters to default                             |

---

## 📊 Charts & Dr. Guidelines

| Week | Chart | Key Rules Applied |
|------|-------|------------------|
| 1–2 | Column + Bar | 10 Rules: Border, Zero, Labels, Magnitudes, Winner-Left |
| 2 | Stacked + Clustered | Color: lighter→darker same hue per segment |
| 3 | Scatter | IQR outlier detection, label on outlier, one color per cluster |
| 4 | Bubble | Size ∝ market value, lightyellow outlier + label |
| 5 | Histogram | nbins=25, opacity=0.45, density, KDE fill overlay |
| 6 | Box | px.box, points='outliers', opacity=0.7, notched option |
| 7 | Violin | COLORS[i] silhouette, white median dot, median annotation |
| 8 | Line | linewidth=2, end-labels, rolling MA, no forced zero |
| 9 | Area | fill_between, stackgroup, Y-axis MUST start at zero |

---

## 📦 Dataset

**FIFA 23 Complete Player Dataset** — Kaggle (stefanoleone992)  
link: https://www.kaggle.com/datasets/stefanoleone992/fifa-23-complete-player-dataset
File: `male_players.csv` (~18,000 players) | Demo: `male_players_cleaned.csv` (5,000 players)
