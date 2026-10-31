# genpark-personal-agent-retinal-microvasculature-av-ratio-stroke-risk-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Digital fundus photography arteriolar-to-venular diameter ratio (AVR) and fractal dimension cerebral microvascular stroke stratifier.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `stratify_retinal_av_ratio_stroke_risk`
- **Category**: `personal_agent`

### Method Documentation
Analyze retinal fundus microvasculature geometry including Arteriolar-to-Venular Ratio (AVR) and fractal dimension (Df).
Retinal microvessels share embryological, anatomical, and physiological characteristics with cerebral small vessels.
Computes Central Retinal Arteriolar Equivalent (CRAE), Central Retinal Venular Equivalent (CRVE), and 10-year stroke hazard ratio.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "stratify_retinal_av_ratio_stroke_risk",
    "arguments": {
    "crae_microns": 152.0,
    "crve_microns": 218.0,
    "fractal_dimension": 1.44,
    "systolic_bp": 122
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
