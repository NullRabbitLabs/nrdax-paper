import json, collections
d=json.load(open('all.json')); T={t['id']:t for t in d['techniques']}
# Hand-assigned mechanism class from each technique's own mechanism text.
# M1 memory/storage retention, M2 CPU, M3 admission slot, M4 egress amplification,
# M5 fault-induced termination, M6 guard bypass, OOS outside declared class, MIX genuinely dual
A = {
'NRDAX-T0023':'M1','NRDAX-T0025':'M1','NRDAX-T0038':'MIX','NRDAX-T0042':'M1','NRDAX-T0046':'M1',
'NRDAX-T0059':'M1','NRDAX-T0061':'M1','NRDAX-T0071':'M1','NRDAX-T0095':'MIX','NRDAX-T0097':'M1',
'NRDAX-T0106':'M1','NRDAX-T0112':'M1','NRDAX-T0124':'M4','NRDAX-T0131':'M1','NRDAX-T0156':'M1',
'NRDAX-T0182':'M4','NRDAX-T0185':'M1','NRDAX-T0187':'M1','NRDAX-T0195':'M1','NRDAX-T0196':'M1',
'NRDAX-T0203':'M1','NRDAX-T0280':'M4','NRDAX-T0292':'OOS','NRDAX-T0321':'M1','NRDAX-T0327':'M1',
'NRDAX-T0351':'M1','NRDAX-T0353':'M1','NRDAX-T0354':'M1','NRDAX-T0355':'M1','NRDAX-T0369':'MIX',
'NRDAX-T0382':'M1','NRDAX-T0383':'M1','NRDAX-T0386':'M1','NRDAX-T0387':'M1','NRDAX-T0388':'M1',
'NRDAX-T0408':'M2',
'NRDAX-T0005':'M5','NRDAX-T0006':'M2','NRDAX-T0013':'M5','NRDAX-T0076':'M2','NRDAX-T0101':'M5',
'NRDAX-T0122':'M5','NRDAX-T0129':'M5','NRDAX-T0139':'M2','NRDAX-T0148':'M2','NRDAX-T0166':'M2',
'NRDAX-T0171':'M5','NRDAX-T0184':'M2','NRDAX-T0198':'M2','NRDAX-T0205':'M2','NRDAX-T0249':'M5',
'NRDAX-T0254':'MIX','NRDAX-T0328':'M1','NRDAX-T0342':'M2','NRDAX-T0349':'M2','NRDAX-T0384':'M2',
'NRDAX-T0389':'M2','NRDAX-T0394':'M2','NRDAX-T0399':'M5','NRDAX-T0400':'M5','NRDAX-T0401':'M5',
'NRDAX-T0407':'M5','NRDAX-T0417':'M5',
'NRDAX-T0041':'M3','NRDAX-T0064':'M3','NRDAX-T0088':'MIX','NRDAX-T0099':'MIX','NRDAX-T0100':'M2',
'NRDAX-T0145':'M5','NRDAX-T0206':'M2','NRDAX-T0214':'MIX','NRDAX-T0225':'M3','NRDAX-T0246':'M6',
'NRDAX-T0261':'MIX','NRDAX-T0275':'OOS','NRDAX-T0291':'M3','NRDAX-T0320':'M3','NRDAX-T0331':'MIX',
'NRDAX-T0333':'M3',
'NRDAX-T0024':'M5','NRDAX-T0056':'M5','NRDAX-T0143':'M2','NRDAX-T0165':'M5','NRDAX-T0202':'OOS',
'NRDAX-T0207':'M2','NRDAX-T0211':'M5','NRDAX-T0298':'OOS','NRDAX-T0307':'OOS','NRDAX-T0350':'OOS',
'NRDAX-T0409':'OOS','NRDAX-T0411':'OOS','NRDAX-T0414':'OOS',
'NRDAX-T0001':'M5','NRDAX-T0050':'OOS','NRDAX-T0120':'M5','NRDAX-T0188':'M2','NRDAX-T0192':'MIX',
'NRDAX-T0199':'M1','NRDAX-T0295':'OOS','NRDAX-T0312':'OOS','NRDAX-T0326':'M3','NRDAX-T0403':'OOS',
'NRDAX-T0329':'M4','NRDAX-T0345':'M4','NRDAX-T0142':'M5','NRDAX-T0248':'M2','NRDAX-T0317':'OOS',
'NRDAX-T0352':'M5','NRDAX-T0392':'M5','NRDAX-T0396':'M6','NRDAX-T0398':'M6',
}
FINE=['memory_amp','compute_amp','connection_exhaustion','consensus_abuse','gossip_abuse','response_amp',
'rpc_handler_cpu','subscription_cpu_amp','auth_bypass','state_import_abuse','protocol_logic_exploit',
'rate_limiter_bypass','service_misconfig']
repro=[t for t in d['techniques'] if t['family'] in FINE]
assert len(A)==len(repro), (len(A), len(repro))
NAT={'memory_amp':'M1','compute_amp':'M2','connection_exhaustion':'M3','response_amp':'M4',
'rpc_handler_cpu':'M2','subscription_cpu_amp':'M2','auth_bypass':'M6','rate_limiter_bypass':'M6',
'service_misconfig':'M6'}  # families that DO name a mechanism
SURF={'gossip_abuse','consensus_abuse','state_import_abuse'}      # surface-defined
RESID={'protocol_logic_exploit'}                                   # residual
print('=== mechanism class over the 111 reproduced ===')
for k,v in collections.Counter(A.values()).most_common(): print(f'  {k}  {v}')
print()
print('=== family x mechanism ===')
for f in FINE:
    ids=[t['id'] for t in repro if t['family']==f]
    c=collections.Counter(A[i] for i in ids)
    kind = 'mechanism' if f in NAT else ('surface' if f in SURF else 'residual/control')
    print(f'  {f:24} n={len(ids):3} [{kind:17}] {dict(c)}')
print()
print('=== conformance: mechanism-named families whose members contradict the label ===')
bad=[]
for f,exp in NAT.items():
    for t in repro:
        if t['family']==f and A[t['id']] not in (exp,'MIX'):
            bad.append((f,exp,A[t['id']],t['id'],t['name']))
for b in sorted(bad): print(f'  {b[0]:22} says {b[1]} but is {b[2]}: {b[3]} {b[4]}')
print(f'  -> {len(bad)} contradictions')
print()
print('=== M5 (fault-induced termination) has no family: where its members live ===')
m5=[(t['family'],t['id'],t['name']) for t in repro if A[t['id']]=='M5']
for f,c in collections.Counter(x[0] for x in m5).most_common(): print(f'  {f:24} {c}')
print(f'  -> {len(m5)} techniques across {len(set(x[0] for x in m5))} families')
print()
print('=== OOS: outside the declared network/node-resource class ===')
oos=[(t['family'],t['id'],t['name']) for t in repro if A[t['id']]=='OOS']
for f,i,n in sorted(oos): print(f'  {f:22} {i} {n}')
print(f'  -> {len(oos)} techniques')
