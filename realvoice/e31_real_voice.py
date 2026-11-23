"""E31: the first check on real voice. Does personal calibration still help on top of a strong open speech model?

Run on a machine with internet access (the models and the data are downloaded there):

    pip install -r realvoice/requirements.txt
    python realvoice/e31_real_voice.py --data path/to/RAVDESS --encoder emotion2vec --out realvoice/results
    python realvoice/e31_real_voice.py --data path/to/RAVDESS --encoder mfcc --out realvoice/results   # no model download

Data: RAVDESS speech (24 actors, 8 emotions; Zenodo record 1188976, "Audio_Speech_Actors_01-24.zip"), or any
folder with a CSV `path,speaker,label` (`--csv`). Emotions are mapped to the engine's four states.

Encoders:
* emotion2vec: open speech-emotion foundation model (FunASR; default iic/emotion2vec_plus_base), utterance embedding
  plus its own zero-shot emotion scores;
* mfcc: 40 MFCCs (mean and standard deviation), a weak classic baseline that needs no model download.

Protocol, leave one speaker out. For the held-out speaker, half of their clips are the calibration pool and half the
test clips. Scored on the test clips only, per speaker, then averaged:
* zero-shot: the encoder's own emotion scores mapped to the four states (emotion2vec+ only);
* generic: a linear head trained on the other speakers;
* + personal baseline: every speaker's features normalised by their own unlabeled clips (for the held-out speaker,
  only the calibration pool, no labels);
* + k answers: the head refit with k labeled clips of the held-out speaker from the calibration pool (k = 2, 4, 8, 16),
  weighted up, as the user's answers would be;
* + signature (docs/29, the engine's SignatureModel): RAVDESS actors read the same two sentences in a neutral tone and
  in every emotion, which is the fixed-sentence protocol. The emotion directions are learned from the other speakers
  (a 3-dimensional discriminant projection of their features, each speaker measured against their own neutral clips);
  the held-out speaker's neutral clips in the calibration pool are the enrollment, and j clips per state from the pool
  are their tagged readings (j = 0, 1, 2, 4). Voice only: RAVDESS has no body signals and no daily sessions.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

STATES = ["calm", "energized", "tense", "low"]
RAVDESS = {"01": "calm", "02": "calm", "03": "energized", "04": "low", "05": "tense", "06": "tense",
           "07": "tense", "08": "energized"}          # neutral, calm, happy, sad, angry, fearful, disgust, surprised
E2V_TO_STATE = {"neutral": "calm", "happy": "energized", "surprised": "energized", "angry": "tense",
                "fearful": "tense", "disgusted": "tense", "sad": "low"}
KS = (2, 4, 8, 16)
SIG_JS = (0, 1, 2, 4)


# ---------------------------------------------------------------------------------------------- data

def load_ravdess(root: Path) -> list[dict]:
    """RAVDESS file names: modality-channel-emotion-intensity-statement-repetition-actor.wav (speech: 03-01-...)."""
    items = []
    for f in sorted(root.rglob("03-01-*.wav")):
        parts = f.stem.split("-")
        if len(parts) == 7 and parts[2] in RAVDESS:
            items.append({"path": str(f), "speaker": parts[6], "label": RAVDESS[parts[2]], "neutral": parts[2] == "01"})
    return items


def load_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        return [{"path": r["path"], "speaker": r["speaker"], "label": r["label"],
                 "neutral": (r.get("neutral") or "").strip().lower() in ("1", "true", "yes")}
                for r in csv.DictReader(fh) if r["label"] in STATES]


# ---------------------------------------------------------------------------------------------- encoders

def encode_mfcc(paths: list[str]) -> tuple[np.ndarray, None]:
    import librosa
    rows = []
    for p in paths:
        y, sr = librosa.load(p, sr=16000)
        m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        rows.append(np.concatenate([m.mean(1), m.std(1)]))
    return np.array(rows), None


def encode_emotion2vec(paths: list[str], model_id: str) -> tuple[np.ndarray, np.ndarray | None]:
    from funasr import AutoModel
    model = AutoModel(model=model_id, disable_update=True)
    feats, zero = [], []
    for p in paths:
        r = model.generate(p, granularity="utterance", extract_embedding=True)[0]
        feats.append(np.asarray(r["feats"]).reshape(-1))
        probs = np.zeros(len(STATES))
        for lab, sc in zip(r.get("labels", []), r.get("scores", [])):
            name = str(lab).split("/")[-1].strip().lower()       # labels look like "生气/angry"
            if name in E2V_TO_STATE:
                probs[STATES.index(E2V_TO_STATE[name])] += float(sc)
        zero.append(probs)
    z = np.array(zero)
    return np.array(feats), (z if z.sum() > 0 else None)


def encode(items: list[dict], encoder: str, cache: Path, model_id: str) -> tuple[np.ndarray, np.ndarray | None]:
    cache.mkdir(parents=True, exist_ok=True)
    tag = encoder if encoder == "mfcc" else f"{encoder}-{model_id.replace('/', '_')}"
    fx, fz = cache / f"{tag}.npy", cache / f"{tag}_zero.npy"
    if fx.exists():
        return np.load(fx), (np.load(fz) if fz.exists() else None)
    paths = [it["path"] for it in items]
    X, Z = encode_mfcc(paths) if encoder == "mfcc" else encode_emotion2vec(paths, model_id)
    np.save(fx, X)
    if Z is not None:
        np.save(fz, Z)
    return X, Z


# ---------------------------------------------------------------------------------------------- protocol

def _head():
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0))


def _normalise(X: np.ndarray, ref: np.ndarray) -> np.ndarray:
    return (X - ref.mean(0)) / (ref.std(0) + 1e-6)


def _scores(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    from sklearn.metrics import balanced_accuracy_score
    return {"accuracy": float(np.mean(y_true == y_pred)), "balanced": float(balanced_accuracy_score(y_true, y_pred))}


def _signature_model():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))
    from soulcal.anchors import SignatureModel
    return SignatureModel


def _signature_arms(X, y, spk, s, pool, test, others, neutral, js) -> dict:
    """The fixed-sentence signature for held-out speaker ``s`` (see the module docstring)."""
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    SignatureModel = _signature_model()

    def ref(idx):                                         # the speaker's neutral clips, or all of them if none
        n = idx[neutral[idx]] if neutral is not None else idx[:0]
        return n if len(n) >= 2 else idx

    Xr = X.copy()
    for o in np.unique(spk[others]):
        idx = np.where(spk == o)[0]
        Xr[idx] = _normalise(X[idx], X[ref(idx)])
    lda = LinearDiscriminantAnalysis(n_components=min(3, len(STATES) - 1)).fit(Xr[others], y[others])
    P = lda.transform(Xr)
    # population directions in z units: each other speaker against their own neutral clips, then averaged per state
    zs, ys = [], []
    for o in np.unique(spk[others]):
        idx = np.where(spk == o)[0]
        r = ref(idx)
        zs.append((P[idx] - P[r].mean(0)) / (P[r].std(0) + 1e-3))
        ys.append(y[idx])
    zs, ys = np.vstack(zs), np.concatenate(ys)
    pop = np.array([zs[ys == k].mean(0) if np.any(ys == k) else np.zeros(P.shape[1]) for k in range(len(STATES))])
    hp = lda.transform(_normalise(X, X[ref(pool)]))         # held-out speaker, measured against the pool only
    enroll = ref(pool)
    used = set(enroll.tolist())                           # a clip is either enrollment or a tagged reading
    out = {}
    for j in js:
        m = SignatureModel(n_features=P.shape[1], population=pop)
        for i in enroll:
            m.add_enrollment(hp[i])
        for k in range(len(STATES)):
            tag = [i for i in pool if y[i] == k and i not in used][:j]
            for i in tag:
                m.add_tagged(STATES[k], hp[i], use_anchor=False)
        pred = np.array([STATES.index(max(pr, key=pr.get)) for pr in (m.proba(hp[i], use_anchor=False) for i in test)])
        name = "+ signature (neutral sentences)" if j == 0 else f"+ signature, {j} tagged per state"
        out[name] = _scores(y[test], pred)
    return out


def evaluate(X: np.ndarray, y: np.ndarray, spk: np.ndarray, Z: np.ndarray | None = None, seed: int = 0,
             ks=KS, answer_weight: float = 5.0, neutral: np.ndarray | None = None, sig_js=SIG_JS) -> dict:
    """Leave one speaker out; returns mean and per-speaker scores for every setting."""
    rng = np.random.default_rng(seed)
    out: dict = {}
    for s in np.unique(spk):
        test_spk = np.where(spk == s)[0]
        rng.shuffle(test_spk)
        pool, test = test_spk[: len(test_spk) // 2], test_spk[len(test_spk) // 2:]
        others = np.where(spk != s)[0]
        res = {}
        if Z is not None:
            res["zero-shot"] = _scores(y[test], Z[test].argmax(1))
        g = _head().fit(X[others], y[others])
        res["generic"] = _scores(y[test], g.predict(X[test]))
        Xn = X.copy()
        for o in np.unique(spk[others]):
            idx = np.where(spk == o)[0]
            Xn[idx] = _normalise(X[idx], X[idx])
        Xn[test_spk] = _normalise(X[test_spk], X[pool])                 # held-out speaker: unlabeled pool only
        b = _head().fit(Xn[others], y[others])
        res["+ personal baseline"] = _scores(y[test], b.predict(Xn[test]))
        for k in ks:
            ans = pool[: min(k, len(pool))]
            Xa = np.vstack([Xn[others], Xn[ans]])
            ya = np.concatenate([y[others], y[ans]])
            w = np.concatenate([np.ones(len(others)), np.full(len(ans), answer_weight)])
            h = _head()
            h.fit(Xa, ya, logisticregression__sample_weight=w)
            res[f"+ {k} answers"] = _scores(y[test], h.predict(Xn[test]))
        if sig_js:
            res.update(_signature_arms(X, y, spk, s, pool, test, others, neutral, sig_js))
        out[str(s)] = res
    settings = list(next(iter(out.values())).keys())
    mean = {k: {m: float(np.mean([out[s][k][m] for s in out])) for m in ("accuracy", "balanced")} for k in settings}
    return {"mean": mean, "per_speaker": out, "speakers": len(out)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="RAVDESS folder")
    ap.add_argument("--csv", help="or a CSV with path,speaker,label (label in calm/energized/tense/low)")
    ap.add_argument("--encoder", choices=["emotion2vec", "mfcc"], default="emotion2vec")
    ap.add_argument("--model", default="iic/emotion2vec_plus_base")
    ap.add_argument("--out", default="realvoice/results")
    ap.add_argument("--seeds", type=int, default=3)
    a = ap.parse_args()
    items = load_csv(Path(a.csv)) if a.csv else load_ravdess(Path(a.data))
    if not items:
        raise SystemExit("no clips found")
    out = Path(a.out)
    X, Z = encode(items, a.encoder, out / "cache", a.model)
    y = np.array([STATES.index(it["label"]) for it in items])
    spk = np.array([it["speaker"] for it in items])
    neutral = np.array([bool(it.get("neutral")) for it in items])
    runs = [evaluate(X, y, spk, Z, seed=s, neutral=neutral if neutral.any() else None) for s in range(a.seeds)]
    mean = {k: {m: float(np.mean([r["mean"][k][m] for r in runs])) for m in ("accuracy", "balanced")}
            for k in runs[0]["mean"]}
    lines = [f"# E31 on real voice: {a.encoder}" + ("" if a.encoder == "mfcc" else f" ({a.model})"), "",
             f"{len(items)} clips, {runs[0]['speakers']} speakers, leave one speaker out, {a.seeds} splits. "
             "Four states (chance 25%).", "", "| Setting | Accuracy | Balanced accuracy |", "| --- | --- | --- |"]
    lines += [f"| {k} | {v['accuracy']:.3f} | {v['balanced']:.3f} |" for k, v in mean.items()]
    out.mkdir(parents=True, exist_ok=True)
    (out / f"E31_{a.encoder}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / f"E31_{a.encoder}.json").write_text(json.dumps({"mean": mean, "runs": runs}, indent=1), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
