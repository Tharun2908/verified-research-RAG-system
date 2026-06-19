"""
backend/app/monitoring/metrics.py

Central definition of all custom Prometheus metrics. Define once here (module-level
singletons), import and update everywhere. The /metrics endpoint mounted in main.py
(make_asgi_app) automatically exposes everything registered here.

Metric types:
  Counter   - monotonic count of events (requests, errors). Read as a rate over time.
  Gauge     - a value that goes up and down (the latest unsupported_claim_rate).
  Histogram - a distribution, bucketed, for percentiles (per-stage latency -> p50/p95/p99).
"""

from prometheus_client import Counter, Gauge, Histogram

# --- Counters: total events (rate computed by Prometheus over time) ---------
RESEARCH_REQUESTS = Counter(
    "research_requests_total",
    "Total number of verified-research requests processed.",
)

RESEARCH_ERRORS = Counter(
    "research_errors_total",
    "Total number of verified-research requests that raised an error.",
)

CLAIMS_VERIFIED = Counter(
    "claims_verified_total",
    "Total number of individual claims verified.",
)

# Counter with a LABEL: lets you break the count down by label value (here, the verdict).
# Prometheus stores one timeseries per label value, so you can graph Supported vs
# Weak vs Unsupported counts separately.
CLAIMS_BY_LABEL = Counter(
    "claims_by_label_total",
    "Total claims verified, broken down by support label.",
    ["label"],   # "Supported" | "Weak" | "Unsupported"
)

# --- Gauge: the headline ML metric, latest value (fluctuates up/down) --------
UNSUPPORTED_CLAIM_RATE = Gauge(
    "unsupported_claim_rate",
    "Unsupported-claim rate of the most recent verified-research job (0..1).",
)

GROUNDING_SCORE = Gauge(
    "grounding_score",
    "Mean grounding (support) score of the most recent verified-research job (0..1).",
)

# --- Histograms: per-stage latency, for percentiles and the M10 bottleneck ---
# Buckets chosen to span fast stub latencies up through realistic real-model latencies
# (seconds). Prometheus computes p50/p95/p99 from these buckets.
_LATENCY_BUCKETS = (0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)

STAGE_LATENCY = Histogram(
    "stage_latency_seconds",
    "Latency of each pipeline stage in seconds.",
    ["stage"],   # "retrieve" | "generate" | "extract" | "verify" | "persist"
    buckets=_LATENCY_BUCKETS,
)

REQUEST_LATENCY = Histogram(
    "verify_request_latency_seconds",
    "End-to-end latency of a full verified-research request in seconds.",
    buckets=_LATENCY_BUCKETS,
)
