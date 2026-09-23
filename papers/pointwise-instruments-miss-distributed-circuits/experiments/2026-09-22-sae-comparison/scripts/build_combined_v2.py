import json
import os
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
# v2 scope (gpt2/gemma2/qwen15); only include those whose _v2 summary exists
MODELS = [m for m in ["gpt2", "gemma2", "qwen15"] if os.path.exists(f"{RES}/summary_{m}_v2.json")]

def gg(d, *ks):
    for k in ks:
        if not isinstance(d, dict): return None
        d = d.get(k)
    return d
def ci(node):
    if not isinstance(node, dict): return None
    if "median" in node: return {"median": node.get("median"), "lo": node.get("lo"), "hi": node.get("hi"), "n": node.get("n")}
    if "rate" in node: return {"rate": node.get("rate"), "lo": node.get("lo"), "hi": node.get("hi"), "n": node.get("n")}
    return None
def med(node):
    c = ci(node);
    return c.get("median") if c and "median" in c else (c.get("rate") if c else None)

combined = {"experiment": "sae-comparison", "version": "v2", "models": {}}
for m in MODELS:
    d = json.load(open(f"{RES}/summary_{m}_v2.json"))
    prov = d.get("provenance", {})
    mm = {"n_layers": d["n_layers"], "hf_id": prov.get("hf_id"), "commit": prov.get("commit"),
          "elapsed_s": d.get("elapsed_s"), "behaviors": {}}
    for b, s in d["summary"].items():
        gates = gg(d, "gates", b) or {}
        cell = {
            "n_items": s["n_items"], "n_admitted": s["n_admitted"], "usable_for_rules": s["usable_for_rules"],
            "noop_gates": {"cache_parity": max(gates.get("cache_parity") or [0]),
                           "kv_noop": gates.get("kv_noop_max"),
                           "kv_isolated_split_noop": gates.get("kv_isolated_split_noop_max"),
                           "resid_noop": max((gates.get("resid_noop_max") or {"x":0}).values()),
                           "sae_noop": max((gates.get("sae_noop_max") or {"x":0}).values())},
            "kv1_inforward_best": {"layer": gg(s,"kv1","best_layer"), "fraction": ci(gg(s,"kv1","best","fraction")), "flip": ci(gg(s,"kv1","best","flip"))},
            "kv1_isolated_best": {"layer": gg(s,"kv1_iso","best_layer"), "fraction": ci(gg(s,"kv1_iso","best","fraction")), "flip": ci(gg(s,"kv1_iso","best","flip"))},
            "kv_range_inforward": {k: {"fraction": ci(gg(s,"kv_range",k,"fraction")), "flip": ci(gg(s,"kv_range",k,"flip"))} for k in ("first","second","all") if gg(s,"kv_range",k)},
            "kv_range_isolated": {k: {"fraction": ci(gg(s,"kv_range_iso",k,"fraction")), "flip": ci(gg(s,"kv_range_iso",k,"flip"))} for k in ("first","second","all") if gg(s,"kv_range_iso",k)},
            "resid1_best": {"layer": gg(s,"resid1","best_layer"), "fraction": ci(gg(s,"resid1","best","fraction")), "early": gg(s,"resid1","first_early_layer_ge_0.5")},
            "sae_global_diag_N200": gates.get("sae_global_diag_N200"),
            "rules": s.get("rules", {}),
        }
        if "sae_k" in s:
            cell["sae_k_best"] = {k: {"layer": gg(s,"sae_k","best",k,"best_layer"),
                                      "fraction": ci(gg(s,"sae_k","best",k,"best","fraction")),
                                      "flip": ci(gg(s,"sae_k","best",k,"best","flip"))} for k in ("k1","k5","k20")}
            cell["sae_swap_best"] = {"layer": gg(s,"sae_swap","best_layer"), "fraction": ci(gg(s,"sae_swap","best","fraction"))}
            cell["sae_global"] = {N: {"fraction": ci(gg(s,"sae_global",N,"fraction")), "flip": ci(gg(s,"sae_global",N,"flip")),
                                      "random_fraction": ci(gg(s,"sae_global_random",N,"fraction"))} for N in ("N10","N50","N200")}
            cell["steering_best"] = {"layer": gg(s,"steering","best_layer"), "norm_gain": ci(gg(s,"steering","best"))}
            cell["kv_suff_all"] = ci(s.get("kv_suff_all"))
        mm["behaviors"][b] = cell
    combined["models"][m] = mm

# same-layer SAE specificity from raw
import numpy as np
for m in [x for x in ["gpt2","gemma2"] if x in MODELS]:
    d = json.load(open(f"{RES}/raw_{m}_v2.json"))
    for b in ["identity","color"]:
        raw = d["behaviors"][b]; wp = raw["whole_path_dlp"]; adm=[it["admitted"] for it in raw["items"]]
        cell = combined["models"][m]["behaviors"][b]; spec={}
        for k in ["k1","k5","k20"]:
            L = cell["sae_k_best"][k]["layer"]
            if L is None: continue
            a = raw["arms"]["sae_k_by_k"][k][L]["dlp"]; r = raw["arms"]["sae_k_random_by_k"][k][L]["dlp"]
            fa=[x/w for x,w,aa in zip(a,wp,adm) if aa and abs(w)>1e-6]; fr=[x/w for x,w,aa in zip(r,wp,adm) if aa and abs(w)>1e-6]
            spec[k]={"layer":L,"attributed":float(np.median(fa)) if fa else None,"random_same_layer":float(np.median(fr)) if fr else None}
        cell["sae_k_same_layer_specificity"]=spec

combined["notes"]=[
 "v2 fixes: (1) SAE-global is now a PROPAGATING ablation (encode current residual, subtract selected feature contributions per position, error kept); (2) KV arms add ISOLATED variants (prefix/suffix split, subject stream intact) as PRIMARY for rule 1.",
 "isolated KV fractions normalized by the isolated whole-path; in-forward fractions by the in-forward whole-path.",
 "kv_isolated_split_noop is the max-abs logit diff of the split-with-no-overwrite vs the unsplit clean forward; the split no-op is the baseline for the isolated arms.",
 "sae_global_diag_N200 shows how top-200 attributed (layer,pos,latent) distribute over positions and layers.",
]
json.dump(combined, open(f"{RES}/combined_summary_v2.json","w"), indent=1)
print("wrote combined_summary_v2.json")

# comparison print
v1 = {m: json.load(open(f"{RES}/summary_{m}.json"))["summary"] for m in MODELS}
def f(x): return "%.3f"%x if isinstance(x,(int,float)) else " n/a"
print("\n== KV single-layer: v1(in-forward) vs v2 in-forward vs v2 ISOLATED (primary) ==")
print("%-9s %-8s %4s | %-18s | %-18s | %-18s" % ("model","behav","adm","v1 KV1best","v2 KV1 inforward","v2 KV1 ISOLATED"))
for m in MODELS:
    for b,c in combined["models"][m]["behaviors"].items():
        v1c=v1[m][b]
        print("%-9s %-8s %3d  | %-4s %-13s | %-4s %-13s | %-4s %-13s" % (
            m,b,c["n_admitted"],
            gg(v1c,"kv1","best_layer"), f(med(gg(v1c,"kv1","best","fraction"))),
            c["kv1_inforward_best"]["layer"], f(med(c["kv1_inforward_best"]["fraction"])),
            c["kv1_isolated_best"]["layer"], f(med(c["kv1_isolated_best"]["fraction"]))))
print("\n== SAE-global: v1(buggy) vs v2(propagating) N200 frac, + random, + diag ==")
for m in [x for x in ["gpt2","gemma2"] if x in MODELS]:
    for b,c in combined["models"][m]["behaviors"].items():
        v1c=v1[m][b]; sg=c.get("sae_global",{})
        diag=c.get("sae_global_diag_N200") or {}
        pc=diag.get("by_position_class",{})
        print("%-9s %-8s | v1 N200=%s | v2 N200=%s (rand %s) N10=%s(rand %s) | pos subj/last/other=%s/%s/%s" % (
            m,b, f(med(gg(v1c,"sae_global","N200","fraction"))),
            f(med(sg.get("N200",{}).get("fraction"))), f(med(sg.get("N200",{}).get("random_fraction"))),
            f(med(sg.get("N10",{}).get("fraction"))), f(med(sg.get("N10",{}).get("random_fraction"))),
            pc.get("subject"),pc.get("answer_last"),pc.get("other")))
print("\n== Decision rules v2 ==")
for m in MODELS:
    for b,c in combined["models"][m]["behaviors"].items():
        r=c["rules"]
        if "rule1_single_layer_kv_null_isolated_PRIMARY" in r:
            ri=r["rule1_single_layer_kv_null_isolated_PRIMARY"]; rf=r["rule1_single_layer_kv_null_inforward"]
            ex=""
            if "rule2_sae_single_layer_necessary" in r:
                ex=" R2=%s(f%s) R3=%s(f%s)"%(r["rule2_sae_single_layer_necessary"]["holds"], f(r["rule2_sae_single_layer_necessary"]["best_k20_median_fraction"]),
                    r["rule3_sae_global_faithful"]["holds"], f(r["rule3_sae_global_faithful"]["N200_median_fraction"]))
            print("  %-9s %-8s: R1_ISO(primary)=%s(f%s) R1_inforward=%s(f%s) R4=%s%s"%(m,b,
                ri["holds"],f(ri["best_median_fraction"]),rf["holds"],f(rf["best_median_fraction"]),
                r["rule4_residual_bus"].get("predicted_holds"),ex))
        else:
            print("  %-9s %-8s: rules not applied (n=%d)"%(m,b,c["n_admitted"]))

# ---- TransformerLens cross-check tables ----
def f(x): return "%.3f" % x if isinstance(x, (int, float)) else "n/a"
tl_all = {}
for m in MODELS:
    d = json.load(open(f"{RES}/summary_{m}_v2.json"))
    tl = d.get("tl")
    if tl and "behaviors" in tl:
        tl_all[m] = tl
        combined["models"][m]["tl"] = tl
json.dump(combined, open(f"{RES}/combined_summary_v2.json", "w"), indent=1)

print("\n== TransformerLens agreement: max|Delta_lp(TL) - Delta_lp(HF)| per arm ==")
print("%-9s %-8s %-9s | %-10s %-12s %-12s %-10s | verdict agree (R1iso/R2)" % (
    "model","behav","clean_gt","resid1","kv1_inforward","kv1_isolated","sae_k20"))
for m in MODELS:
    tl = tl_all.get(m)
    if not tl: 
        print(f"  {m}: TL missing"); continue
    for b, bd in tl["behaviors"].items():
        a = bd["arm_agreement"]; v = bd.get("verdict_agreement", {})
        def am(k): 
            n = a.get(k); return f(n["max_abs_dlp_diff"]) if n else "n/a"
        r1 = v.get("rule1_isolated", {}); r2 = v.get("rule2_sae20", {})
        print("%-9s %-8s %-9s | %-10s %-12s %-12s %-10s | R1iso:%s R2:%s" % (
            m, b, f(bd["clean_logit_gate"]),
            am("resid1"), am("kv1_inforward"), am("kv1_isolated"), am("sae_k20"),
            r1.get("agree"), r2.get("agree")))

print("\n== Timing (per item per intervention, ms; full-recompute vs cached-prefix) ==")
print("%-9s | %-22s | %-22s | tl_ver" % ("model","HF full / cached","TL full / cached"))
for m in MODELS:
    tl = tl_all.get(m)
    if not tl: continue
    t = tl.get("timing", {})
    print("%-9s | %8s / %-10s | %8s / %-10s | %s" % (
        m, f(t.get("hf_full_per_item_per_interv_ms")), f(t.get("hf_cached_per_item_per_interv_ms")),
        f(t.get("tl_full_per_item_per_interv_ms")), f(t.get("tl_cached_per_item_per_interv_ms")),
        tl.get("tl_version")))
print("wrote combined_summary_v2.json (with tl section)")
