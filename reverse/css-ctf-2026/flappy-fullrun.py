import flappy as F
def solve2(seed,target,beam=2500):
    start=F.init_state(seed); beams=[(start,[])]
    for t in range(6000):
        nxt=[]; seen=set()
        for st,fl in beams:
            if st['score']>=target: return fl,st['tick'],st['score']
            for flap in (True,False):
                ns=F.clone(st); F.step(ns,flap)
                if ns['dead']: continue
                k=(ns['y']>>7,ns['vel'],ns['score'],min(p.x for p in ns['pipes'])>>9)
                if k in seen: continue
                seen.add(k)
                nxt.append((ns, fl+[t] if flap else fl))
        if not nxt: return None
        def key(it):
            st=it[0]
            cand=[p for p in st['pipes'] if p.x>0x6000 and not p.passed]
            d=abs(st['y']-(min(cand,key=lambda p:p.x).gap<<8)) if cand else 0
            return (-st['score'],d)
        nxt.sort(key=key); beams=nxt[:beam]
        for st,fl in beams:
            if st['score']>=target: return fl,st['tick'],st['score']
    return None

st,r=F.post('/api/attempt',{}); d=F.parse(r)
token=d['token']; seed=int(d['seed']); target=int(d['target']); rnd=int(d['round']); waits=int(d['wait_seconds'])
print("START round",rnd,"seed",seed,"target",target)
while True:
    res=solve2(seed,target)
    if not res:
        print("solve failed r",rnd); break
    fl,ticks,score=res
    print(f"round {rnd}: solved ticks={ticks} score={score} flaps={len(fl)}")
    flapstr=','.join(map(str,fl))
    body=f'round={rnd}&wait_ms={waits*1000+1500}&ticks={ticks}&score={score}&flaps={flapstr}'
    st,r=F.post('/api/complete',body,token)
    print(f"  complete r{rnd}: {st} {r[:220]}")
    d=F.parse(r)
    if 'flag' in d:
        print("\n=== FLAG ===", d['flag']); break
    if 'flag' in r and 'CSSCTF' in r:
        print("\nRAW:",r); break
    if 'round' not in d:
        print("no next round; full response:",r); break
    rnd=int(d['round']); seed=int(d['seed']); target=int(d['target']); waits=int(d.get('wait_seconds',0))
    if rnd>3: break
