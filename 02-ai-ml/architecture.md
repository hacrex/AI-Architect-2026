# Day 02 — Architecture Decision Matrices

> **Reference Document**: This file contains unique decision frameworks and matrices. For full explanations, see `notes.md`.

---

## Quick Reference Tables

### Model Selection Checklist

Use this when evaluating any model:

| Question | Yes → | No → |
|----------|-------|------|
| Does it meet quality requirements? | Proceed | Keep looking |
| Can it meet latency targets? | Proceed | Consider smaller model |
| Does it fit the budget at scale? | Proceed | Optimize routing |
| Can we meet privacy requirements? | Proceed | Consider self-hosted |
| Does our team have skills to operate? | Proceed | Consider managed |
| Can we switch providers later? | Proceed | Evaluate lock-in cost |

---

### Decision Speed Run

| Question | Answer |
|----------|--------|
| Simple factual query? | → GPT-3.5 / Haiku |
| Needs reasoning? | → GPT-4 / Sonnet |
| Long context analysis? | → GPT-4 / Opus |
| Need citations? | → RAG |
| Need consistent style? | → Fine-tuning |
| Strict data privacy? | → Self-hosted |
| Rapid prototype? | → Managed API |
| High volume? | → Model routing |

---

### Cost Quick Reference

| Model | Input/1K | Output/1K | Best For |
|-------|----------|-----------|----------|
| GPT-3.5-turbo | $0.001 | $0.002 | Simple, high-volume |
| GPT-4 | $0.03 | $0.06 | Complex, quality-critical |
| GPT-4-turbo | $0.01 | $0.03 | Balanced |
| Claude 3 Haiku | $0.00025 | $0.00125 | Fast, cheap |
| Claude 3 Sonnet | $0.003 | $0.015 | Balanced |
| Claude 3 Opus | $0.015 | $0.075 | Highest quality |

---

### RAG vs Fine-Tuning Quick Decision

```
┌─────────────────────────────────────────┐
│     Is the problem about KNOWLEDGE?     │
├─────────────────────────────────────────┤
│  YES → RAG                              │
│  NO  → Is it about BEHAVIOR?            │
│         YES → Fine-tuning               │
│         NO  → Prompt engineering        │
└─────────────────────────────────────────┘
```

---

### Context Window Budget Rule

```
Total Context Window (e.g., 128K tokens)
├── System Instructions: 10-20%
├── Conversation History: 20-30%
├── Retrieved Documents: 30-40%
├── User Prompt: 5-10%
└── Response Buffer: 20-30%  ← NEVER FILL THIS
```

---

### Architecture Pattern Quick Reference

| Pattern | When to Use | Trade-off |
|---------|-------------|-----------|
| **Single Model** | Simple use case, limited budget | Lower quality or higher cost |
| **Model Gateway** | Need reliability, fallback | Added latency |
| **Model Router** | High volume, diverse complexity | Classification overhead |
| **RAG + Router** | Knowledge + quality needs | Complexity |
| **Self-hosted** | Privacy, scale, control | Operations burden |

---

### Monthly Cost Estimation Template

```
Requests/month: ___________
├── Simple (50%): ___ × $0.001 = $___
├── Normal (35%): ___ × $0.03  = $___
└── Complex (15%): ___ × $0.06 = $___

Total: $___/month
```

---

## Decision Frameworks

See `notes.md` for detailed explanations of:

- Model Selection Decision Framework (Section 18)
- RAG vs Fine-Tuning Decision Matrix (Section 16)
- Managed vs Self-Hosted Decision Matrix (Section 17)
- Token Economics (Section 6)
- Model Routing Architecture (Section 5)
