"""Generate the seven charts for the clusters "For the curious" blog post.

Saves PNGs to ../assets/clusters-blog-{name}.png at 150 dpi.
Palette comes from the merna.org portfolio.
"""

from __future__ import annotations

import os
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_distances, manhattan_distances
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
np.random.seed(7)

CREAM = "#f5efe0"
NAVY = "#2c3e50"
BRASS = "#b8945a"
CLUSTER_COLORS = ["#a5c5e8", "#e8c585", "#e8a5a5", "#a5e8b5", "#c5a5e8"]
GRAY = "#7a7a7a"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "assets"))
os.makedirs(OUT_DIR, exist_ok=True)


def apply_style(ax):
    ax.set_facecolor(CREAM)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(NAVY)
        ax.spines[side].set_linewidth(1.0)
    ax.tick_params(colors=NAVY)
    ax.title.set_color(NAVY)
    ax.xaxis.label.set_color(NAVY)
    ax.yaxis.label.set_color(NAVY)


def new_fig(w=7.5, h=4.8):
    mpl.rcParams["font.family"] = ["Source Sans 3", "Source Sans Pro", "DejaVu Sans", "sans-serif"]
    fig, ax = plt.subplots(figsize=(w, h), facecolor=CREAM)
    apply_style(ax)
    return fig, ax


def save(fig, name):
    path = os.path.join(OUT_DIR, f"clusters-blog-{name}.png")
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=CREAM, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------------------
# Synthetic streaming-service dataset (used by several charts)
# ---------------------------------------------------------------------------

def make_customers():
    rng = np.random.default_rng(11)
    blueprints = [
        dict(name="casual",          center=(4, 2, 15, 1),  n=500, std=3),
        dict(name="regular",         center=(25, 5, 25, 2), n=600, std=5),
        dict(name="heavy",           center=(40, 8, 35, 3), n=400, std=6),
        dict(name="explorer",        center=(15, 12, 30, 4),n=300, std=4),
        dict(name="premium-casual",  center=(10, 3, 50, 2), n=200, std=4),
    ]
    rows = []
    truth = []
    for k, bp in enumerate(blueprints):
        mu = np.array(bp["center"], dtype=float)
        s = bp["std"]
        pts = rng.normal(loc=mu, scale=s, size=(bp["n"], 4))
        rows.append(pts)
        truth.extend([k] * bp["n"])
    X = np.vstack(rows)
    X[:, 0] = np.clip(X[:, 0], 0, None)
    X[:, 1] = np.clip(X[:, 1], 0, None)
    X[:, 2] = np.clip(X[:, 2], 0, None)
    X[:, 3] = np.clip(X[:, 3], 1, None)
    return pd.DataFrame(X, columns=["watch_hours", "genre_variety", "monthly_spend", "device_count"]), np.array(truth)


# ---------------------------------------------------------------------------
# 1. Convergence across random seeds (within-cluster SSE per iteration)
# ---------------------------------------------------------------------------

def chart_convergence():
    df, _ = make_customers()
    X = StandardScaler().fit_transform(df.values)
    fig, ax = new_fig(7.5, 4.2)
    seeds = [3, 11, 19, 27, 41]
    palette = [NAVY, BRASS, "#6a8eb8", "#c27c5a", "#8a9b6e"]
    for s, color in zip(seeds, palette):
        rng = np.random.default_rng(s)
        idx = rng.choice(len(X), size=5, replace=False)
        centers = X[idx].copy()
        sse_per_iter = []
        for _ in range(20):
            d = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
            assign = d.argmin(axis=1)
            sse = float(((X - centers[assign]) ** 2).sum())
            sse_per_iter.append(sse)
            new_centers = np.array([
                X[assign == k].mean(axis=0) if (assign == k).any() else centers[k]
                for k in range(5)
            ])
            shift = np.linalg.norm(new_centers - centers)
            centers = new_centers
            if shift < 1e-4:
                break
        ax.plot(range(1, len(sse_per_iter) + 1), sse_per_iter, marker="o",
                color=color, linewidth=2.0, markersize=4, label=f"seed {s}", alpha=0.85)
    ax.set_xlabel("iteration")
    ax.set_ylabel("within-cluster sum of squares (J)")
    ax.set_title("K-means decreases J at every step. Different seeds, different minima.",
                 fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    save(fig, "convergence")


# ---------------------------------------------------------------------------
# 2. PCA projection of K=5 result
# ---------------------------------------------------------------------------

def chart_result_k5():
    df, _ = make_customers()
    X = StandardScaler().fit_transform(df.values)
    km = KMeans(n_clusters=5, n_init=10, random_state=7)
    labels = km.fit_predict(X)
    pca = PCA(n_components=2, random_state=7)
    XY = pca.fit_transform(X)
    centroids_xy = pca.transform(km.cluster_centers_)

    fig, ax = new_fig(7.5, 5.0)
    for k in range(5):
        m = labels == k
        ax.scatter(XY[m, 0], XY[m, 1], s=12, color=CLUSTER_COLORS[k],
                   alpha=0.7, edgecolor="none", label=f"cluster {k+1}")
    for k in range(5):
        ax.scatter(centroids_xy[k, 0], centroids_xy[k, 1], marker="X",
                   color=BRASS, s=200, linewidths=2.0, edgecolor=NAVY, zorder=5)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("K = 5 K-means on standardized features, projected to PC1 / PC2",
                 fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=9, loc="best", ncol=2)
    save(fig, "result-k5")


# ---------------------------------------------------------------------------
# 3. Elbow plot
# ---------------------------------------------------------------------------

def chart_elbow():
    df, _ = make_customers()
    X = StandardScaler().fit_transform(df.values)
    ks = list(range(1, 11))
    inertias = []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=7)
        km.fit(X)
        inertias.append(km.inertia_)
    fig, ax = new_fig(7.5, 4.2)
    ax.axvspan(3, 5, color=BRASS, alpha=0.12, label="defensible range")
    ax.plot(ks, inertias, marker="o", color=NAVY, linewidth=2.0, markersize=6)
    ax.set_xlabel("K (number of clusters)")
    ax.set_ylabel("inertia (sum of squared distances)")
    ax.set_title("Elbow plot. The bend is real but it is also a judgment call.",
                 fontsize=11, loc="left")
    ax.set_xticks(ks)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    save(fig, "elbow")


# ---------------------------------------------------------------------------
# 4. Silhouette scores
# ---------------------------------------------------------------------------

def chart_silhouette():
    df, _ = make_customers()
    X = StandardScaler().fit_transform(df.values)
    ks = list(range(2, 11))
    scores = []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=7)
        labels = km.fit_predict(X)
        rng = np.random.default_rng(7)
        sample = rng.choice(len(X), size=min(800, len(X)), replace=False)
        scores.append(silhouette_score(X[sample], labels[sample]))
    best = int(np.argmax(scores))
    fig, ax = new_fig(7.5, 4.2)
    bars = ax.bar(ks, scores, color="#cdbf9c", edgecolor=NAVY, linewidth=1.0)
    bars[best].set_color(BRASS)
    bars[best].set_edgecolor(NAVY)
    bars[best].set_linewidth(2.0)
    ax.set_xlabel("K")
    ax.set_ylabel("mean silhouette score")
    ax.set_title("Silhouette scores. Best K is marked. Elbow and silhouette may disagree.",
                 fontsize=11, loc="left")
    ax.set_xticks(ks)
    save(fig, "silhouette")


# ---------------------------------------------------------------------------
# 5. Stability via bootstrap (consensus matrix)
# ---------------------------------------------------------------------------

def chart_stability():
    df, _ = make_customers()
    X_full = StandardScaler().fit_transform(df.values)
    rng = np.random.default_rng(7)
    sample_idx = rng.choice(len(X_full), size=400, replace=False)
    X = X_full[sample_idx]
    n = len(X)
    co_count = np.zeros((n, n), dtype=np.int32)
    sel_count = np.zeros((n, n), dtype=np.int32)
    B = 50
    for b in range(B):
        boot = rng.integers(0, n, size=n)
        unique = np.unique(boot)
        km = KMeans(n_clusters=5, n_init=5, random_state=b)
        lab = km.fit_predict(X[boot])
        # map back to original index labels via taking first occurrence
        first_label = {}
        for j, idx in enumerate(boot):
            if idx not in first_label:
                first_label[idx] = lab[j]
        present = np.array(sorted(first_label.keys()))
        labels_present = np.array([first_label[i] for i in present])
        eq = labels_present[:, None] == labels_present[None, :]
        co_count[np.ix_(present, present)] += eq.astype(np.int32)
        sel_count[np.ix_(present, present)] += 1
    consensus = np.where(sel_count > 0, co_count / np.maximum(sel_count, 1), 0.0)

    # sort rows/cols by a final reference clustering for block structure
    ref = KMeans(n_clusters=5, n_init=10, random_state=7).fit_predict(X)
    order = np.argsort(ref)
    M = consensus[np.ix_(order, order)]

    cmap = LinearSegmentedColormap.from_list("cl-consensus", [CREAM, BRASS, NAVY])
    fig, ax = new_fig(5.4, 5.0)
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("customers (sorted by cluster)")
    ax.set_ylabel("customers (sorted by cluster)")
    ax.set_title("Consensus matrix, 50 bootstrap K-means at K = 5.\nDark blocks = co-assigned often. Light boundaries = unstable.",
                 fontsize=10.5, loc="left")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.outline.set_edgecolor(NAVY)
    cbar.ax.tick_params(colors=NAVY)
    save(fig, "stability")


# ---------------------------------------------------------------------------
# 6. Same data, four stories (2 x 2)
# ---------------------------------------------------------------------------

def assign_with_distance(X, centroids, metric):
    if metric == "manhattan":
        d = manhattan_distances(X, centroids)
    elif metric == "cosine":
        d = cosine_distances(X, centroids)
    else:
        d = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
    return d.argmin(axis=1)


def kmedoid_like(X, k, metric, n_iter=20, seed=7):
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(X), size=k, replace=False)
    centroids = X[idx].copy()
    for _ in range(n_iter):
        labels = assign_with_distance(X, centroids, metric)
        new = []
        for c in range(k):
            pts = X[labels == c]
            if len(pts) == 0:
                new.append(centroids[c]); continue
            if metric == "manhattan":
                new.append(np.median(pts, axis=0))
            else:
                new.append(pts.mean(axis=0))
        new = np.array(new)
        if np.allclose(new, centroids, atol=1e-4):
            centroids = new; break
        centroids = new
    return labels, centroids


def chart_comparison():
    df, _ = make_customers()
    X = StandardScaler().fit_transform(df.values)
    pca = PCA(n_components=2, random_state=7)
    XY = pca.fit_transform(X)

    cases = [
        ("K = 3, Euclidean",  3, "euclidean"),
        ("K = 5, Euclidean",  5, "euclidean"),
        ("K = 5, Manhattan",  5, "manhattan"),
        ("K = 5, Cosine",     5, "cosine"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(9, 7.5), facecolor=CREAM)
    for ax, (title, k, metric) in zip(axes.flat, cases):
        apply_style(ax)
        if metric == "euclidean":
            km = KMeans(n_clusters=k, n_init=10, random_state=7)
            labels = km.fit_predict(X)
        else:
            labels, _ = kmedoid_like(X, k, metric)
        for c in range(k):
            m = labels == c
            ax.scatter(XY[m, 0], XY[m, 1], s=8, color=CLUSTER_COLORS[c % 5],
                       alpha=0.7, edgecolor="none")
        ax.set_title(title, fontsize=11, color=NAVY, loc="left")
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    fig.suptitle("Same customers. Four reasonable choices. Four different stories.",
                 fontsize=12.5, color=NAVY)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    path = os.path.join(OUT_DIR, "clusters-blog-comparison.png")
    fig.savefig(path, dpi=150, facecolor=CREAM, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------------------
# 7. Where K-means breaks (1 x 3)
# ---------------------------------------------------------------------------

def make_moons():
    rng = np.random.default_rng(3)
    n = 300
    t1 = rng.uniform(0, np.pi, n)
    t2 = rng.uniform(0, np.pi, n)
    x1 = np.column_stack([np.cos(t1), np.sin(t1)]) + rng.normal(0, 0.06, (n, 2))
    x2 = np.column_stack([1 - np.cos(t2), 1 - np.sin(t2) - 0.5]) + rng.normal(0, 0.06, (n, 2))
    return np.vstack([x1, x2])


def make_density():
    rng = np.random.default_rng(5)
    dense = rng.normal([0, 0], 0.25, (400, 2))
    sparse = rng.normal([3.5, 0], 1.4, (120, 2))
    return np.vstack([dense, sparse])


def make_outliers():
    rng = np.random.default_rng(9)
    a = rng.normal([0, 0], 0.5, (200, 2))
    b = rng.normal([3, 0], 0.5, (200, 2))
    outliers = np.array([[10, 8], [11, 7], [12, 8], [-8, -7], [-9, -6]])
    return np.vstack([a, b, outliers])


def chart_failures():
    cases = [
        ("non-spherical (moons)", make_moons(), 2),
        ("unequal density",        make_density(), 2),
        ("outlier sensitivity",    make_outliers(), 2),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(11, 4), facecolor=CREAM)
    for ax, (title, X, k) in zip(axes, cases):
        apply_style(ax)
        km = KMeans(n_clusters=k, n_init=10, random_state=7)
        labels = km.fit_predict(X)
        for c in range(k):
            m = labels == c
            ax.scatter(X[m, 0], X[m, 1], s=12, color=CLUSTER_COLORS[c],
                       alpha=0.75, edgecolor="none")
        ax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
                   marker="X", color=BRASS, s=140, linewidths=1.6, edgecolor=NAVY, zorder=5)
        ax.set_title(title, fontsize=11, color=NAVY, loc="left")
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("K-means does what its objective tells it to. The objective is the limit.",
                 fontsize=12, color=NAVY)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    path = os.path.join(OUT_DIR, "clusters-blog-failures.png")
    fig.savefig(path, dpi=150, facecolor=CREAM, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    chart_convergence()
    chart_result_k5()
    chart_elbow()
    chart_silhouette()
    chart_stability()
    chart_comparison()
    chart_failures()
    print("ALL DONE.")
