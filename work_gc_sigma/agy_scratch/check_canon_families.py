import json

with open("work_gc_sigma/sigma4_20000000.json", "r", encoding="utf-8") as f:
    sig = json.load(f)

# Let's inspect canon_families or canon readings of sigma['<T4']
# Does sigma4_20000000.json contain canon_families or other classification info?
print("sig keys:", sig.keys())
print("sig['canon_families']['<T4'] len:", len(sig['canon_families']['<T4']))
print("First 20 canon_families['<T4']:", sig['canon_families']['<T4'][:20])

# What are the canon families in <T3?
print("canon_families['<T3']:", sig['canon_families']['<T3'])
# What are the canon families in <T2?
print("canon_families['<T2']:", sig['canon_families']['<T2'])
# What are the canon families in <T1?
print("canon_families['<T1']:", sig['canon_families']['<T1'])
