# RQ 5.5.7: Source-Destination Clustering

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** Clustering
**Full ID:** 5.5.7

---

## Research Question

**Primary Question:**
Can participants be grouped into latent classes based on source (-U-) and destination (-D-) memory patterns?

**Scope:**
K-means clustering on random effects from RQ 5.5.6. Tests whether discrete "memory profiles" exist for source-destination spatial memory.

---

## Theoretical Background

The weak-but-stable clustering pattern across Chapter 5 (5.1.5, 5.2.7, 5.3.8, 5.4.7) shows:
- Silhouette < 0.40 (poor cluster quality)
- Jaccard > 0.60 (stable groupings)
- Clustering driven by intercepts only (slopes ≈ 0)

Memory ability appears continuous, not categorical. This should replicate for source-destination.

---

## Hypothesis

**Primary Hypothesis:**
Clustering will show weak quality (silhouette < 0.40) but stable groupings (Jaccard > 0.60), consistent with Chapter 5 pattern.

**Secondary Hypothesis:**
If -U- vs -D- shows a true dissociation (per 5.5.1), clusters may differentiate by location-type-specific intercepts.

---

## Analysis Approach

**Design:**
- K-means clustering (K=1-6, BIC selection)
- Features: -U- intercept, -U- slope, -D- intercept, -D- slope (4 features)
- Validation: Silhouette, Davies-Bouldin, Jaccard bootstrap stability

**Dependencies:**
- RQ 5.5.6 MUST be complete (provides random effects as clustering features)

---

## Notes

**Matches:** RQ 5.1.5 (General Clustering), 5.2.7 (Domain Clustering), 5.3.8 (Paradigm Clustering), 5.4.7 (Congruence Clustering)
**Expected:** Weak quality, intercept-driven clusters (no phenotypes)

**Interpretation:**
- If weak clustering: Memory is continuous dimension (confirms Chapter 5 pattern)
- If strong clustering: Source-destination creates discrete profiles (novel finding)
