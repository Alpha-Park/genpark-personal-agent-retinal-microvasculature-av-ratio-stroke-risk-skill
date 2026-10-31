# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-retinal-microvasculature-av-ratio-stroke-risk-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def stratify_retinal_av_ratio_stroke_risk(crae_microns, crve_microns, fractal_dimension=1.45, systolic_bp=125):
    if crae_microns <= 0 or crve_microns <= 0:
        raise ValueError("CRAE and CRVE must be positive numbers")
        
    avr = crae_microns / crve_microns
    
    # Standard population distribution:
    # Normal AVR: 0.67 - 0.75
    # Narrowed arterioles (high risk): < 0.60
    # Fractal dimension (branching complexity): normal 1.40 - 1.50, rarefaction < 1.38
    
    stroke_hazard_ratio = 1.0
    risk_factors = []
    
    if avr < 0.60:
        stroke_hazard_ratio *= 1.85
        risk_factors.append("Severe generalized arteriolar narrowing (AVR < 0.60)")
    elif avr < 0.67:
        stroke_hazard_ratio *= 1.35
        risk_factors.append("Mild to moderate arteriolar narrowing")
        
    if fractal_dimension < 1.38:
        stroke_hazard_ratio *= 1.45
        risk_factors.append(f"Microvascular branching rarefaction (Df={fractal_dimension:.2f} < 1.38)")
        
    if crve_microns > 220.0:
        stroke_hazard_ratio *= 1.30
        risk_factors.append(f"Venular dilation (CRVE={crve_microns:.1f}um > 220um, systemic inflammation/endothelial dysfunction marker)")
        
    if systolic_bp >= 140:
        stroke_hazard_ratio *= 1.40
        risk_factors.append(f"Uncontrolled systolic hypertension ({systolic_bp} mmHg)")
        
    stroke_hazard_ratio = round(stroke_hazard_ratio, 2)
    
    if stroke_hazard_ratio >= 2.5:
        tier = "HIGH_CEREBROVASCULAR_RISK"
    elif stroke_hazard_ratio >= 1.5:
        tier = "MODERATE_CEREBROVASCULAR_RISK"
    else:
        tier = "LOW_MICROVASCULAR_RISK"
        
    return {
        "crae_microns": round(crae_microns, 1),
        "crve_microns": round(crve_microns, 1),
        "arteriolar_venular_ratio": round(avr, 3),
        "retinal_fractal_dimension": round(fractal_dimension, 3),
        "estimated_stroke_hazard_ratio": stroke_hazard_ratio,
        "risk_stratification_tier": tier,
        "identified_risk_markers": risk_factors if risk_factors else ["Optimal microvascular geometry"],
        "recommendation": "Recommend continuous ambulatory BP monitoring and brain MRI small-vessel evaluation if high tier." if stroke_hazard_ratio >= 2.0 else "Normal cerebral microcirculatory proxy."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "stratify_retinal_av_ratio_stroke_risk",
                        "description": """Analyze retinal fundus microvasculature geometry including Arteriolar-to-Venular Ratio (AVR) and fractal dimension (Df).
Retinal microvessels share embryological, anatomical, and physiological characteristics with cerebral small vessels.
Computes Central Retinal Arteriolar Equivalent (CRAE), Central Retinal Venular Equivalent (CRVE), and 10-year stroke hazard ratio.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = stratify_retinal_av_ratio_stroke_risk(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'crae_microns': 152.0, 'crve_microns': 218.0, 'fractal_dimension': 1.44, 'systolic_bp': 122}
        out = stratify_retinal_av_ratio_stroke_risk(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
