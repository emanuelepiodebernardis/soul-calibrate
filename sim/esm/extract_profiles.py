"""Per-person emotion profiles from open experience-sampling data (jmbh/EmotionTimeSeries).
Writes person-level summaries only: mean negative and positive affect (0-1), within-person SD and lag-1
autocorrelation of negative affect, and negative-emotion differentiation (1 - mean inter-item correlation)."""
import json, sys
import numpy as np, pyreadr

ROOT = sys.argv[1]
ITEMS = {
    "Bringmann2013": (["Worried", "Anxious", "Sad"], ["Excited", "Relaxed"]),
    "Bringmann2016": (["Angry", "Depressed", "Dysphoric", "Anxious"], ["Relaxed", "Happy"]),
    "Fisher2017": (["irritable", "restless", "worried", "guilty", "afraid", "angry", "hopeless", "down", "tension"],
                   ["energetic", "enthusiastic", "content", "positive"]),
    "Fried2021": (["Irritable", "Worry", "Nervous", "Angry"], ["Relax"]),
    "Rowland2020": (["angry", "anxious", "depressed", "sad"], ["happy", "excited", "relaxed", "satisfied"]),
}
out = []
for ds, (neg, pos) in ITEMS.items():
    df = list(pyreadr.read_r(f"{ROOT}/DataClean/{ds}/data_{ds}.RDS").values())[0]
    for c in neg + pos:
        df[c] = df[c].astype(float)
        lo, hi = np.nanmin(df[c]), np.nanmax(df[c])
        df[c] = (df[c] - lo) / (hi - lo)
    for pid, g in df.groupby("subj_id"):
        g = g[neg + pos].dropna(how="all")
        na = g[neg].mean(axis=1).to_numpy(); pa = g[pos].mean(axis=1).to_numpy()
        ok = ~np.isnan(na)
        if ok.sum() < 30:
            continue
        x = na[ok]
        ar = float(np.corrcoef(x[:-1], x[1:])[0, 1]) if x.std() > 0 else np.nan
        c = g[neg].dropna().corr().to_numpy()
        iu = np.triu_indices(len(neg), 1)
        r = np.nanmean(c[iu]) if len(neg) >= 3 else np.nan
        out.append({"dataset": ds, "n": int(ok.sum()), "na_mean": float(x.mean()), "na_sd": float(x.std()),
                    "na_ar1": ar, "pa_mean": float(np.nanmean(pa)), "neg_diff": None if np.isnan(r) else float(1 - r)})
json.dump(out, open(sys.argv[2], "w"), indent=0)
print(len(out), "people")
