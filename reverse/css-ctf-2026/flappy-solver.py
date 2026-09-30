import urllib.request, urllib.parse, sys, time
BASE="http://34.116.80.78:8765"
M32=0xffffffff
def rng_next(s):
    x=s
    x^=(x<<13)&M32
    x^=(x>>17)
    x^=(x<<5)&M32
    return x&M32
class Pipe:
    __slots__=('x','gap','passed')
def init_state(seed):
    st={'y':0xf000,'vel':0,'score':0,'tick':0,'dead':False,'rng':seed&M32,'pipes':[]}
    for i in range(5):
        p=Pipe(); p.x=((i*270+1040)<<8)
        st['rng']=rng_next(st['rng']); p.gap=(st['rng']%231)+125
        p.passed=False
        st['pipes'].append(p)
    return st
def clone(st):
    n=dict(st); n['pipes']=[]
    for p in st['pipes']:
        q=Pipe(); q.x=p.x; q.gap=p.gap; q.passed=p.passed; n['pipes'].append(q)
    return n
def step(st, flap):
    if st['dead'] or st['tick']>0x8c9f:
        st['dead']=True; return
    v=st['vel']
    if flap: v=-1724
    v+=67
    if v>2048: v=2048
    st['vel']=v
    st['y']+=v
    st['tick']+=1
    for p in st['pipes']: p.x-=717
    y=st['y']
    if y<=0xc00 or y>0x1d3ff: st['dead']=True
    # collision
    for p in st['pipes']:
        x=p.x
        if x>0xd3ff: continue
        if x<=0x7800:
            pass
        else:
            if (y-3071) <= ((p.gap-87)<<8): st['dead']=True
            elif (y+3071) >= ((p.gap+87)<<8): st['dead']=True
        if not p.passed and x<=0x77ff:
            p.passed=True
            if not st['dead']: st['score']+=1
    # recycle
    for p in st['pipes']:
        if p.x < -17408 & M32 if False else (p.x if p.x< (1<<31) else p.x-(1<<32)) < -17408:
            mx=max(q.x for q in st['pipes'])
            p.x=mx+0x10e00
            st['rng']=rng_next(st['rng']); p.gap=(st['rng']%231)+125
            p.passed=False

def solve(seed, target, beam=400, maxticks=36000):
    start=init_state(seed)
    # beam entries: (state, flaps_list)
    beams=[(start,[])]
    for t in range(maxticks):
        nxt=[]
        for st,fl in beams:
            if st['score']>=target:
                return fl, st['tick'], st['score']
            for flap in (False,True):
                ns=clone(st); step(ns,flap)
                if ns['dead']: continue
                nfl=fl+[t] if flap else fl
                nxt.append((ns,nfl))
        if not nxt:
            return None
        # score beams: prefer higher score, then bird centered on nearest upcoming pipe gap
        def key(item):
            st=item[0]
            # nearest pipe with x in front (x> ~ -something) and not passed
            cand=[p for p in st['pipes'] if p.x>0x7800 and not p.passed]
            if cand:
                p=min(cand,key=lambda p:p.x)
                dist=abs(st['y']-(p.gap<<8))
            else:
                dist=abs(st['y']-(240<<8))
            return (-st['score'], dist)
        nxt.sort(key=key)
        beams=nxt[:beam]
        # early success check
        for st,fl in beams:
            if st['score']>=target:
                return fl, st['tick'], st['score']
    return None

def post(path, data, token=None):
    body=urllib.parse.urlencode(data).encode() if isinstance(data,dict) else data.encode()
    req=urllib.request.Request(BASE+path, data=body, method='POST')
    req.add_header('Content-Type','application/x-www-form-urlencoded')
    if token: req.add_header('Authorization','Bearer '+token)
    try:
        r=urllib.request.urlopen(req,timeout=15); return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def parse(qs):
    return dict(urllib.parse.parse_qsl(qs))

if __name__=='__main__':
    st,r=post('/api/attempt',{})
    print('attempt',st,r)
    d=parse(r); token=d['token']; seed=int(d['seed']); target=int(d['target']); rnd=int(d['round'])
    print(f'round={rnd} seed={seed} target={target}')
    res=solve(seed,target)
    if not res: print('SOLVE FAILED'); sys.exit(1)
    flaps,ticks,score=res
    print(f'solved: ticks={ticks} score={score} nflaps={len(flaps)}')
    flapstr=','.join(str(x) for x in flaps)
    # validate via practice
    body=f'sequence=1&ticks={ticks}&final={score}&score={score}&flaps={flapstr}'
    st,r=post('/api/practice',body,token); print('practice',st,r[:200])
    st,r=post('/api/practice/check',f'sequence=1',token); print('check',st,r[:200])
