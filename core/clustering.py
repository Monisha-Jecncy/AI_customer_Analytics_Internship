"""
K-Means clustering engine.
Handles automatic K selection (elbow + silhouette), fitting, and cluster profiling.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from config.settings import MAX_K, RANDOM_STATE


def auto_select_k(X: np.ndarray, max_k: int = MAX_K) -> dict:
    """
    Search 2..max_k and pick the best K by silhouette score.
    Returns dict with inertias, silhouettes and the chosen K.
    """
    upper = min(max_k, len(X) - 1)
    ks = list(range(2, max(3, upper + 1)))
    inertias, silhouettes = [], []

    for k in ks:
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(X)
        inertias.append(float(km.inertia_))
        silhouettes.append(float(silhouette_score(X, labels)))

    best_k = ks[int(np.argmax(silhouettes))]
    return {
        "ks": ks,
        "inertias": inertias,
        "silhouettes": silhouettes,
        "best_k": best_k,
        "best_silhouette": max(silhouettes),
    }


def run_kmeans(X: np.ndarray, k: int) -> tuple[np.ndarray, KMeans]:
    """Fit K-Means and return (labels, fitted_model)."""
    km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    labels = km.fit_predict(X)
    return labels, km


def profile_clusters(df: pd.DataFrame, feature_cols: list[str],
                     labels: np.ndarray) -> pd.DataFrame:
    """Build a per-cluster summary (mean of each feature + size)."""
    tmp = df[feature_cols].copy()
    tmp["Cluster"] = labels
    profile = tmp.groupby("Cluster").mean().round(2)
    profile["Size"] = tmp.groupby("Cluster").size()
    profile["Percent"] = (profile["Size"] / len(df) * 100).round(1)
    return profile.reset_index()
