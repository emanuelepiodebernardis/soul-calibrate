"""Population model, personal baseline and personal head."""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression

from .data import N_STATES, User


class RollingBaseline:
    """Personal mean and spread of each feature.

    Starts from an enrollment window (features only, no labels) and then updates
    slowly with an exponential moving average, so one unusual week does not
    become the new normal.
    """

    def __init__(self, X_enroll: np.ndarray, alpha: float = 0.02):
        self.mean = X_enroll.mean(axis=0)
        self.var = X_enroll.var(axis=0) + 1e-6
        self.alpha = alpha

    def transform(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean) / np.sqrt(self.var)

    def update(self, x: np.ndarray) -> None:
        d = x - self.mean
        self.mean = self.mean + self.alpha * d
        self.var = (1 - self.alpha) * (self.var + self.alpha * d * d)


def rolling_transform(X: np.ndarray, n_enroll: int, alpha: float = 0.02) -> np.ndarray:
    """Express each moment against the personal baseline as it stood just before it.

    alpha = 0 keeps the enrollment baseline fixed forever.
    """
    b = RollingBaseline(X[:n_enroll], alpha=alpha)
    out = np.empty_like(X)
    out[:n_enroll] = b.transform(X[:n_enroll])
    for t in range(n_enroll, len(X)):
        out[t] = b.transform(X[t])
        if alpha > 0:
            b.update(X[t])
    return out


def centered_matrix(user: User, n_enroll: int, alpha: float = 0.02) -> np.ndarray:
    return rolling_transform(user.X, n_enroll, alpha)


def fit_population(users: list[User], n_enroll: int, centered: bool,
                   extra: tuple[np.ndarray, np.ndarray, float] | None = None) -> LogisticRegression:
    """Population model. `extra` = (X, y, weight) adds labelled in-domain samples, e.g. answers from a cohort."""
    X = np.vstack([centered_matrix(u, n_enroll)[n_enroll:] if centered else u.X[n_enroll:] for u in users])
    y = np.concatenate([u.report[n_enroll:] for u in users])
    w = np.ones(len(y))
    if extra is not None:
        X = np.vstack([X, extra[0]])
        y = np.concatenate([y, extra[1]])
        w = np.concatenate([w, np.full(len(extra[1]), extra[2])])
    model = LogisticRegression(max_iter=3000, C=1.0)
    model.fit(X, y, sample_weight=w)
    return model


class PersonalHead:
    """A small correction on top of the population model, learned from one user's answers.

    Input: the population model's log-probabilities, optionally followed by the user's
    baseline-normalised features (so the head can learn how this person expresses
    affect). With no or very few answers the head returns the population prediction
    unchanged, and it is shrunk toward the population until answers accumulate.
    """

    def __init__(self, min_labels: int = 4, C: float = 0.3, prior_strength: float = 8.0):
        self.min_labels = min_labels
        self.C = C
        self.prior_strength = prior_strength
        self.n_labels = 0
        self.clf: LogisticRegression | None = None

    def fit(self, logp: np.ndarray, y: np.ndarray) -> None:
        self.n_labels = len(y)
        if len(y) < self.min_labels or len(np.unique(y)) < 2:
            self.clf = None
            return
        self.clf = LogisticRegression(max_iter=1000, C=self.C)
        self.clf.fit(logp, y)

    def predict_proba(self, logp: np.ndarray) -> np.ndarray:
        base = np.exp(logp[:, :N_STATES])
        base = base / base.sum(axis=1, keepdims=True)
        if self.clf is None:
            return base
        p = np.full((logp.shape[0], N_STATES), 1e-6)
        p[:, self.clf.classes_] = self.clf.predict_proba(logp)
        p = p / p.sum(axis=1, keepdims=True)
        # Shrink toward the population: the more answers, the more weight on the person.
        w = self.n_labels / (self.n_labels + self.prior_strength)
        return w * p + (1 - w) * base


def population_logp(model: LogisticRegression, X: np.ndarray) -> np.ndarray:
    p = np.full((X.shape[0], N_STATES), 1e-6)
    p[:, model.classes_] = model.predict_proba(X)
    p = p / p.sum(axis=1, keepdims=True)
    return np.log(p)
