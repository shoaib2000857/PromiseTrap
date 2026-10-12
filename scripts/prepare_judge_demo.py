"""Prepare fictional sources, then run genuine Gemma inference for judging."""
import json
import time
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'judge-demo'
OUT.mkdir(parents=True, exist_ok=True)

with httpx.Client(base_url='http://127.0.0.1:8000/api/v1', timeout=40, trust_env=False) as api:
    def request(method, path, **kwargs):
        r = api.request(method, path, **kwargs)
        r.raise_for_status()
        return r.json()

    case = request('POST', '/investigations', json={
        'title': 'JUDGES · Nova Internship — the promise vs the commitment',
        'description': 'Fictional judge demonstration. Real Gemma extraction from original PNGs and text. Publication dates are authored scenario metadata, not independently authenticated.'})
    cid = case['id']
    print('Judge investigation:', cid, flush=True)
    image_docs = [('internship-advertisement','advertisement','2026-10-01'), ('internship-registration','registration','2026-10-03'), ('internship-offer','offer','2026-10-05')]
    for name, stage, date in image_docs:
        source = request('POST', f'/investigations/{cid}/sources', files={'files': (name+'.png', (ROOT/'examples'/'advanced'/(name+'.png')).read_bytes(), 'image/png')})[0]
        request('PATCH', '/sources/'+source['id'], json={'document_stage':stage,'published_at':date,'effective_at':date})

    texts = [
        ('nova-eligibility.txt','selection','2026-10-04',None,
         'FICTIONAL DEMO SOURCE — Nova Internship, 2026 intake. Applies to all registered applicants.\nApplicants must be in year 4 of their degree.\nApplicants must have an academic score of at least 75 percent.\nParticipation requires successful selection.\n'),
        ('nova-payment-and-refunds.txt','agreement','2026-10-05',None,
         'FICTIONAL DEMO SOURCE — Nova Internship, 2026 intake. Applies to all registered applicants.\nRegistration requires a mandatory processing fee of INR 499 paid upfront.\nAn optional printed certificate costs INR 200; it is a separate optional service and is not required for registration or a digital certificate.\nThe registration processing fee is non-refundable once the application is submitted.\n'),
        ('nova-deadline-v1.txt','advertisement','2026-10-01','nova-application-deadline',
         'FICTIONAL DEMO SOURCE — Nova Internship, 2026 intake. Applies to all registered applicants.\nNotice published October 1, 2026.\nApplication deadline is October 15, 2026.\n'),
        ('nova-deadline-v2.txt','advertisement','2026-10-06','nova-application-deadline',
         'FICTIONAL DEMO SOURCE — Nova Internship, 2026 intake. Applies to all registered applicants.\nUpdated notice published October 6, 2026, superseding the October 1 notice.\nApplication deadline is October 20, 2026.\n')]
    for filename,stage,date,group,text in texts:
        (OUT/filename).write_text(text,encoding='utf-8')
        request('POST',f'/investigations/{cid}/sources/text',json={'filename':filename,'text':text,'document_stage':stage,'published_at':date,'effective_at':date,'version_group':group})
    request('POST',f'/investigations/{cid}/analyze',json={'provider':'gemma'})
    manifest={'primary_id':cid,'primary_url':f'http://127.0.0.1:3000/?investigation={cid}&provider=gemma','controls':{}}
    for scenario, title in [('internship','JUDGES · Authored internship fallback'),('scholarship','JUDGES · Eligibility and scholarship cap'),('deadline','JUDGES · Dated deadline revisions'),('optional','JUDGES · Optional-service negative control'),('consistent','JUDGES · Consistent-offer negative control')]:
        fixture=request('POST','/examples/advanced/'+scenario)
        request('PATCH','/investigations/'+fixture['id'],json={'title':title,'description':fixture['description']+' Authored fictional claims; not model inference.'})
        manifest['controls'][scenario]={'id':fixture['id'],'url':f'http://127.0.0.1:3000/?investigation={fixture["id"]}','claims':len(fixture['claims']),'findings':len(fixture['findings'])}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('Direct demo:',manifest['primary_url'],flush=True)
    end=time.monotonic()+600
    previous=None
    while time.monotonic()<end:
        case=request('GET','/investigations/'+cid)
        if case['stage']!=previous:
            previous=case['stage'];print(case['stage'],flush=True)
        if case['status']!='processing':break
        time.sleep(2)
    (OUT/'actual-gemma-result.json').write_text(json.dumps(case,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':case['status'],'claims':len(case['claims']),'findings':len(case['findings']),'model':case.get('model_identifier'),'error':case.get('error_message')}),flush=True)
    if case['status']!='completed':raise RuntimeError('Genuine extraction did not complete. Use the explicitly authored fallback.')
