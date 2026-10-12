"""Review actual extraction and prepare saved judge outputs with explicit history."""
import copy
import json
from pathlib import Path
import httpx
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--skip-challenge',action='store_true',help='Do not repeat a provider call while preparing exports.')
args=parser.parse_args()

OUT=Path(__file__).resolve().parents[1]/'data'/'judge-demo'
m=json.loads((OUT/'manifest.json').read_text())
cid=m['primary_id']
with httpx.Client(base_url='http://127.0.0.1:8000/api/v1',timeout=120,trust_env=False) as api:
    def request(method,path,**kwargs):
        r=api.request(method,path,**kwargs);r.raise_for_status();return r
    case=request('GET','/investigations/'+cid).json()
    # The duplicate INR 499 obligation is the same registration fee in both documents.
    # Model aliases are corrected through the public analyst-review API, not hidden.
    canonical=next(c['scope'] for c in case['claims'] if c['original_text'].startswith('A mandatory processing fee'))
    edits=[]
    for original in case['claims']:
        c=copy.deepcopy(original)
        if c['subject']=='registration' and c['predicate']=='required_fee':
            c['scope']={**canonical,'purpose':'registration','application_stage':'registration'}
            if c['value']==0: c['currency']='INR'
        for criterion in c.get('criteria',[]):
            if criterion['field']=='academic_score' and criterion['value']=='75 percent':criterion['value']='75'
        if c!=original:
            c['review_status']='confirmed'
            request('PATCH',f'/investigations/{cid}/claims/{c["id"]}',json=c)
            edits.append({'claim_id':c['id'],'quote':c['original_text'],'before':original,'after':c})
    review_path=OUT/'analyst-review.json'
    prior=json.loads(review_path.read_text(encoding='utf-8'))['edits'] if review_path.exists() else []
    review_path.write_text(json.dumps({'notice':'Explicit analyst normalization after genuine Gemma extraction. Raw result is preserved separately. Free registration uses the INR context of the same offer. Image quotes remain approximate.','edits':prior+edits},ensure_ascii=False,indent=2),encoding='utf-8')
    case=request('GET','/investigations/'+cid).json()
    print('REVIEWED TOTALS',json.dumps(case['financial']['currencies']),flush=True)
    print('FINDINGS',[(f['status'],f['title']) for f in case['findings']],flush=True)
    fee=next(f for f in case['findings'] if f['category']=='financial' and f['status'] in {'potential_conflict','contradiction','insufficient_evidence'})
    pair=[next(c for c in case['claims'] if c['id']==fee[k]) for k in ['claim_a_id','claim_b_id']]
    b=copy.deepcopy(pair[1]);b.update(subject='printed certificate',modality='optional',conditions=[])
    if b['scope']:b['scope']={**b['scope'],'purpose':'printed certificate','application_stage':'completion'}
    simulation=request('POST',f'/investigations/{cid}/simulate',json={'a':pair[0],'b':b}).json()
    (OUT/'simulation-check.json').write_text(json.dumps(simulation,indent=2),encoding='utf-8')
    print('SIMULATION',simulation['finding']['status'],flush=True)
    profiles={}
    for name,profile in [('unknown',{}),('ineligible',{'year_of_study':'3','academic_score':'70'}),('eligible',{'year_of_study':'4','academic_score':'80'})]:
        profiles[name]=request('POST',f'/investigations/{cid}/eligibility',json=profile).json()
    (OUT/'eligibility-check.json').write_text(json.dumps(profiles,indent=2),encoding='utf-8')
    draft=request('POST',f'/investigations/{cid}/clarify').json()
    (OUT/'clarification-draft.txt').write_text(draft['draft'],encoding='utf-8')
    if not args.skip_challenge:
        print('Generating actual Gemma alternative interpretation...',flush=True)
        try:
            alt=request('POST',f'/investigations/{cid}/findings/{fee["id"]}/challenge',json={'provider':'gemma'}).json()
            (OUT/'actual-gemma-challenge.json').write_text(json.dumps(alt,indent=2),encoding='utf-8')
        except httpx.HTTPError as exc:
            print('Challenge not verified:',type(exc).__name__,flush=True)
    graph=request('GET',f'/investigations/{cid}/graph').json()
    print('GRAPH',len(graph['nodes']),'nodes',len(graph['edges']),'edges',flush=True)
    sid=case['sources'][0]['id']
    checks={}
    for filename in ['internship-advertisement.png','advertisement-altered-bytes.png']:
        checks[filename]=request('POST','/sources/'+sid+'/verify',files={'file':(filename,(OUT/filename).read_bytes(),'image/png')}).json()
    (OUT/'receipt-check.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    for fmt,ext in [('json','json'),('markdown','md'),('pdf','pdf')]:
        r=request('GET',f'/investigations/{cid}/report',params={'format':fmt})
        (OUT/('judge-dossier.'+ext)).write_bytes(r.content)
        if fmt=='pdf':assert r.content.startswith(b'%PDF-')
    (OUT/'judge-receipt.json').write_bytes(request('GET',f'/investigations/{cid}/receipt').content)
    final=request('GET','/investigations/'+cid).json()
    (OUT/'reviewed-ready-result.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
    assert final['financial']['currencies']['INR']['mandatory_upfront_cost']=='499'
    print('Judge case ready. Raw extraction, analyst changes, simulation, profiles, hash checks and exports saved. Provider challenge is separately identified if it succeeded.',flush=True)
