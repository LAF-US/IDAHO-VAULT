#!/usr/bin/env python3
"""Spelunking Census — grounded synthesis from RECOVERED cosmonaut reports.

Source of truth: the 13 lore cosmonauts' final reports, recovered from subagent
transcripts on disk (census_recovered/*.md) after context compaction. Every
number printed below is computed from entity/heading/coverage data hand-coded
from those reports; the S0 entity-resolution merges are logged inline so each
alias decision is auditable. No value here is narrated from memory.

Run:  python3 census_synthesis.py   (writes census_synthesis_result.json)
"""
from __future__ import annotations
import os, sys, json, random, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_metrics as cm

random.seed(13)

# D1..D13  (index 0..12)
READERS = ["Lodestar","Sextant","Augur","Lantern","Metronome","Cog","Beacon",
           "Tally","Mummer","Stringer","Magpie","Cairn","Tabula"]
DOORS = ["!README (root touchstone)","CONSTITUTION.md","SHALL-ROME-WITNESS",
         "FABLEHAVEN-QUIET-BOX","THE-MUSIC-BOX-MODEL",".crewai/MANIFEST.md",
         "!/SIGNALS/README*","!/AGENTS.md",".abhorsen/ABHORSEN.md","William Borah.md",
         "Dario Amodei clipping","THE TRIPTYCH 0401.md","COLD ROOT DROP (control)"]
N = 13

# --- S0: entity resolution -> canonical nodes : reader-indices that named it ---
# Merges logged: "Touchstone Tree" <- {!README structure, MIND/BODY/SOUL/NEST};
# "named Swarm" <- {Abhorsen/Concierge/Lexicographer..., "the swarm", UNIFIED SWARM};
# "Lich/GEMINIAEUS" <- {Lich Problem, Undead Taxonomy, the rogue-Gemini matter};
# "Standing/Personae Engine" <- {Standing Engine, PERSONAE ENGINE, 3-word address}.
NODES = {
 "Logan (sole human authority)":             set(range(13)),
 "CONSTITUTION.md (binding law)":            set(range(13)),
 "The named multi-agent Swarm":             set(range(13)),
 "The Swarmic Nest (!/)":                    {0,1,3,4,5,6,7,11,12},
 "Dotfolder persona chambers (.*)":          {0,1,5,7,8,10,11,12},
 "Idaho journalism / legislature corpus":    {0,1,6,7,9,10,11,12},
 "The Touchstone Tree (MIND/BODY/SOUL/NEST)":{0,1,2,5,8,10},
 "The DOCKET / Courtroom":                   {3,8,9,11,12},
 "Lich Problem / GEMINIAEUS matter":         {2,3,4,6},
 "Standing / Personae Engine doctrine":      {2,3,4},
 "swarm.json (machine registry)":            {5,7},
 "Canon Core / Esto Perpetua":               {8,9},
 "Fablehaven / Fandom lore-as-doctrine":     {3,10},
 "Operational toolchain (GH/Linear/Slack)":  {7,10},
 "The Witness practice":                     {2},
 "CHAINFIRE / CHAINLINK cycle":              {4},
}
node_names = list(NODES.keys())
# reliability_data[coder][unit] in {0,1}
R = [[1 if c in NODES[nm] else 0 for nm in node_names] for c in range(N)]

# sanity: column sums == |set|
for j, nm in enumerate(node_names):
    assert sum(R[c][j] for c in range(N)) == len(NODES[nm]), nm

# --- field 4b: the single telos verb each reader chose ---
VERBS = ["govern","govern","witness","govern","govern","govern","govern",
         "chronicle","govern","document","govern","coordinate","govern"]
GOVERN_FAMILY = {"govern"}                       # governance-foregrounded
RECORD_FAMILY = {"witness","chronicle","document","coordinate"}  # record-foregrounded

# --- field 4a: telos decomposed into induced alignment facets (binary x reader) ---
FACETS = {
 "GOVERN-SWARM (human-led AI governance)": {0,1,2,3,4,5,6,8,10,11,12},   # 11 (not Tally,Stringer)
 "JOURNALISM (serve Logan's Idaho work)":  {0,1,3,5,6,7,8,9,10,11,12},   # 11 (not Augur,Metronome)
 "DURABLE-RECORD (outlast the session)":   {0,1,2,3,4,5,6,7,9,11,12},    # 11 (not Mummer,Magpie)
 "BENEFICIARY = Logan":                    set(range(13)),               # 13 unanimous
}
facet_names = list(FACETS.keys())
A = [[1 if c in FACETS[fn] else 0 for fn in facet_names] for c in range(N)]

# --- field 6: opened-doc sets, hub tokens normalized for fair overlap ---
COV = {
 0:{"README","ROOTLIST","CONSTITUTION","WAKEUP","AGENTS","SOUL","MIND","BODY","CHARTER","DECISIONS","CLAUDE_DIR","LOGAN","VAULTCONV"},
 1:{"CONSTITUTION","ROOTLIST","README","AGENTS","CROSSFRAMING","ROSTER","DOCTRINAL","WAKEUP","NESTLIST","CIVICLAW"},
 2:{"WITNESS_ROME","ROOTLIST","README","CLASSES_CLAUDE","SEVEN_REALMS","PERSONA_PERSONA","DOCKET","CLAUDE_MD","ESTO","VFD","WITNESS_CUB"},
 3:{"FABLEHAVEN_QB","ROOTLIST","README","FABLEHAVEN_TAX","DOCKET","LICH","ESTO","CONSTITUTION","STANDING_ENGINE","KERR_AKH"},
 4:{"MUSICBOX","README","INBOX_README","CHAINLINK","PERSONAE_ENGINE","AGENTS","WAKEUP","DECISIONS","ROOTLIST","NESTLIST"},
 5:{"CREWAI_MANIFEST","ROOTLIST","README","WIZARDS","AGENTS","WAKEUP","ROSTER","DOCTRINAL","SWARMJSON","CONSTELLATION","STIGMERGIC"},
 6:{"SIGNALS_README","ROOTLIST","README","ESTO","WIZARDS","DOCKET","CONSTITUTION","SIGNALS_DIR","SIGNALS_MD","SIGNAL_CORPSE","AGENT_PROTOCOL","NESTLIST"},
 7:{"AGENTS","CONSTITUTION","WAKEUP","README","VAULTCONV","DECISIONS","ROOTLIST"},
 8:{"ABHORSEN","CLAUDE_MD","README","WAITING","DOCKET","AGENTS","ESTO","CONSTITUTION","ROOTLIST"},
 9:{"BORAH","IDAHO","README","ESTO","DOCKET","CONSTITUTION","CHARTER","AGENTS","TOUCHSTONE","AUDIT","GRIMOIRE","BORAH1924","ROOTLIST","NESTLIST"},
 10:{"AMODEI","ROOTLIST","README","WIZARDS","ESTO","DOCKET","AGENTS","BORAH1907","TVTROPER"},
 11:{"TRIPTYCH","ROOTLIST","README","WIZARDS","DOCKET","NESTLIST","AGENTS","AUDIT","WAKEUP","JOURNALIST","LOGAN"},
 12:{"README","ESTO","WIZARDS","AUDIT","DOCKET","WAKEUP","AGENTS","RA","EMERGING","ROSTER","STILLPOINT","REFLECTION","HB542","CONSTELLATION","ROOTLIST"},
}

# ============================== COHESION ===================================
alpha_full = cm.krippendorff_alpha(R, distance=cm.nominal_distance)

# core+shoulder only: drop the 6 door-local tail nodes (named by <=2 readers)
keep = [j for j,nm in enumerate(node_names) if len(NODES[nm]) >= 3]
R_core = [[R[c][j] for j in keep] for c in range(N)]
alpha_core = cm.krippendorff_alpha(R_core, distance=cm.nominal_distance)

# bootstrap CI for full alpha by resampling UNITS (nodes) with replacement
def boot_alpha(mat, ncols, B=3000):
    # Percentiles are taken over the resamples ATTEMPTED, not the ones that
    # happened to succeed. A resample that fails is a degenerate draw -- an
    # extreme one -- so silently dropping it and then indexing into the
    # survivors narrows the interval and makes the CI claim more confidence
    # than the data supports. Failures are counted and reported instead.
    vals=[]; failed=0
    for _ in range(B):
        cols=[random.randrange(ncols) for _ in range(ncols)]
        sub=[[row[j] for j in cols] for row in mat]
        try:
            vals.append(cm.krippendorff_alpha(sub, distance=cm.nominal_distance))
        except Exception:
            failed+=1
    if failed:
        print(f"  boot_alpha: {failed}/{B} resamples failed; "
              f"CI computed over the {len(vals)} that succeeded", file=sys.stderr)
    # Too few survivors to place a 95% bound. Previously this indexed a short
    # (or empty) list, returning a bogus interval and raising IndexError when
    # every resample failed.
    if len(vals) < 40:
        print(f"  boot_alpha: only {len(vals)} usable resamples; no CI",
              file=sys.stderr)
        return None, None
    vals.sort()
    lo=vals[int(0.025*len(vals))]; hi=vals[int(0.975*len(vals))]
    return lo, hi
ci_full = boot_alpha(R, len(node_names))
ci_core = boot_alpha(R_core, len(keep))

# convergence ratio + load-bearing per node
conv = {nm: cm.convergence_ratio(len(s), N) for nm,s in NODES.items()}

# centroid = nodes named by >= k of 13 ; reader -> MASI distance to centroid set
k = 7
centroid = {nm for nm,s in NODES.items() if len(s) >= k}
reader_sets = [{nm for nm in node_names if c in NODES[nm]} for c in range(N)]
masi_to_centroid = [cm.masi_distance(reader_sets[c], centroid) for c in range(N)]

# ============================== ALIGNMENT ==================================
alpha_align = cm.krippendorff_alpha(A, distance=cm.nominal_distance)
# Ties are broken by name, not by set iteration order. Every verb with the same
# count tied, and `set` ordering varies with PYTHONHASHSEED, so the committed
# census_synthesis_result.json showed a spurious diff on every run -- noise that
# hides a real change in a record whose whole value is being citable.
verb_tally = {v: VERBS.count(v) for v in sorted(set(VERBS), key=lambda x:(-VERBS.count(x), x))}
govern_n = sum(1 for v in VERBS if v in GOVERN_FAMILY)
record_n = sum(1 for v in VERBS if v in RECORD_FAMILY)

# ====================== SEPARATION (coverage-conditioned) ==================
pairs = [(a,b) for a in range(N) for b in range(a+1,N)]
jac = [cm.jaccard(COV[a],COV[b]) for a,b in pairs]
mean_jac = statistics.mean(jac)
# entity-set separation (MASI distance) on the same pairs
ent = [cm.masi_distance(reader_sets[a],reader_sets[b]) for a,b in pairs]
mean_ent = statistics.mean(ent)
# correlation: does higher coverage overlap predict lower entity separation?
def pearson(x,y):
    mx,my=statistics.mean(x),statistics.mean(y)
    num=sum((a-mx)*(b-my) for a,b in zip(x,y))
    dx=(sum((a-mx)**2 for a in x))**.5; dy=(sum((b-my)**2 for b in y))**.5
    return num/(dx*dy) if dx and dy else float("nan")
r_cov_ent = pearson(jac, ent)

# ============================== THE GRID ===================================
# alignment axis: govern-foregrounded (1) vs record-foregrounded (0)
# separation axis: MASI distance from centroid (0 = on-core, 1 = outrider)
# cohesion bubble: fraction of the centroid core nodes this reader named
grid=[]
for c in range(N):
    core_recall = len(reader_sets[c] & centroid)/len(centroid)
    grid.append({
        "reader":READERS[c],"door":DOORS[c],"verb":VERBS[c],
        "align":"GOVERN" if VERBS[c] in GOVERN_FAMILY else "RECORD",
        "sep_from_core":round(masi_to_centroid[c],3),
        "core_recall":round(core_recall,3),
    })

# ============================== REPORT ======================================
def bar(x,w=22): return "#"*int(round(x*w))+"."*(w-int(round(x*w)))
print("="*72)
print("SPELUNKING CENSUS — grounded synthesis (n=13 lore cosmonauts)")
print("source: recovered subagent transcripts; metrics via census_metrics.py")
print("="*72)
print("\n--- S1 COHESION : convergence profile (named by / 13) ---")
for nm,s in sorted(NODES.items(), key=lambda kv:-len(kv[1])):
    c=len(s); print(f"  {bar(c/N)}  {c:2d}/13 {conv[nm]*100:5.1f}%  "
                    f"{'LOAD-BEARING' if cm.is_load_bearing_door(conv[nm]) else 'door-local ':12s} {nm}")
def fmt_ci(ci):
    """Render a bootstrap CI, or say plainly that there wasn't one."""
    lo, hi = ci
    return "not computable" if lo is None else f"[{lo:+.3f},{hi:+.3f}]"
print(f"\n  Cohesion alpha (all 16 nodes)      = {alpha_full:+.3f}  95% CI {fmt_ci(ci_full)}")
print(f"  Cohesion alpha (10 core+shoulder)  = {alpha_core:+.3f}  95% CI {fmt_ci(ci_core)}")
print(f"  centroid (named by >= {k}): {len(centroid)} nodes -> {sorted(centroid)}")
print(f"  mean reader MASI distance to centroid = {statistics.mean(masi_to_centroid):.3f}")

print("\n--- S2 ALIGNMENT : telos heading ---")
print(f"  verb tally: {verb_tally}")
print(f"  GOVERN-family {govern_n}/13   RECORD-family {record_n}/13   beneficiary=Logan 13/13")
for fn in facet_names:
    print(f"    facet {len(FACETS[fn]):2d}/13  {fn}")
print(f"  Alignment alpha (4-facet x 13)     = {alpha_align:+.3f}  (few units; read as descriptive)")

print("\n--- S3 SEPARATION (coverage-conditioned) ---")
print(f"  mean pairwise coverage Jaccard       = {mean_jac:.3f}")
print(f"  mean pairwise entity MASI separation = {mean_ent:.3f}")
print(f"  Pearson r(coverage overlap, entity sep) = {r_cov_ent:+.3f}")
print("  shared hubs opened by >=10/13 readers:",
      sorted([t for t in set().union(*COV.values())
              if sum(t in COV[c] for c in range(N))>=10],
             key=lambda t:-sum(t in COV[c] for c in range(N))))

print("\n--- S4 THE GRID (reader x alignment x separation, bubble=core recall) ---")
print(f"  {'reader':10s} {'door':26s} {'verb':10s} {'align':7s} sep  core")
for g in grid:
    print(f"  {g['reader']:10s} {g['door'][:26]:26s} {g['verb']:10s} {g['align']:7s} "
          f"{g['sep_from_core']:.2f} {g['core_recall']:.2f}")

out={"alpha_cohesion_full":alpha_full,"alpha_cohesion_full_CI":ci_full,
     "alpha_cohesion_core":alpha_core,"alpha_cohesion_core_CI":ci_core,
     "alpha_alignment":alpha_align,"verb_tally":verb_tally,
     "govern_n":govern_n,"record_n":record_n,
     "convergence":{nm:len(s) for nm,s in NODES.items()},
     "centroid":sorted(centroid),"mean_masi_to_centroid":statistics.mean(masi_to_centroid),
     "mean_coverage_jaccard":mean_jac,"mean_entity_separation":mean_ent,
     "r_coverage_vs_separation":r_cov_ent,"grid":grid}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "census_synthesis_result.json"),"w") as f:
    json.dump(out,f,indent=2)
print("\n[written] census_synthesis_result.json")
