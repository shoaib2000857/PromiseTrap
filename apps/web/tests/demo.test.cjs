const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const ts=require('typescript');
// Test the same pure decisions used by the gallery and real workspace handlers.
// TypeScript is an existing dev dependency; no browser or new test dependency required.
const source=fs.readFileSync(path.join(__dirname,'../lib/demo.ts'),'utf8');
const compiled=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2020}});
const helpers={};new Function('exports',compiled.outputText)(helpers);
const {filterGallery,investigationActions,investigationNavigation}=helpers;
const entries=[{id:'fee',title:'Hidden fee',domain:'Recruitment',summary:'Free registration',issues:['Mandatory payment'],capability:'ScopeGuard'}, {id:'control',title:'Aligned offer',domain:'Control cases',summary:'Consistent documents',issues:['Optional fee'],capability:'PromiseGraph'}];
const empty={sources:[],claims:[],findings:[],conditions:[]};
const populated={sources:[{id:'ad'},{id:'form'}],claims:[{id:'ca',source_id:'ad',criteria:[]},{id:'cb',source_id:'form',criteria:[{field:'year_of_study'}]}],findings:[{id:'f',category:'financial',claim_a_id:'ca',claim_b_id:'cb'}],financial:{values:[{claim_id:'ca'}]},conditions:[{claim_id:'cb'}]};
test('gallery filters industry and searches real metadata case-insensitively',()=>{
 assert.deepEqual(filterGallery(entries,'Recruitment',' scopeguard ').map(c=>c.id),['fee']);
 assert.deepEqual(filterGallery(entries,'All investigations','optional').map(c=>c.id),['control']);
 assert.deepEqual(filterGallery(entries,'Control cases','free'),[]);
 assert.equal(filterGallery(entries,'All investigations','').length,2);
});
test('empty or unanalyzed images do not advertise unsupported feature launches',()=>{
 assert.deepEqual(investigationActions(empty).filter(a=>a.available),[]);
 assert.deepEqual(investigationActions({...empty,sources:[{id:'image'}]}).filter(a=>a.available).map(a=>a.id),['sources']);
});
test('consistent control remains inspectable without inventing findings or a lab pair',()=>{
 const actions=investigationActions({...populated,findings:[],conditions:[]}).filter(a=>a.available).map(a=>a.id);
 assert.ok(actions.includes('sources')&&actions.includes('graph')&&actions.includes('report'));
 assert.ok(!actions.includes('evidence')&&!actions.includes('lab')&&!actions.includes('challenge'));
});
test('documented eligibility and financial values determine applicable actions',()=>{
 const actions=investigationActions(populated).filter(a=>a.available).map(a=>a.id);
 assert.ok(actions.includes('eligibility')&&actions.includes('calculator')&&actions.includes('conditions'));
 const stripped=investigationActions({...populated,financial:undefined,conditions:[],claims:populated.claims.map(c=>({...c,criteria:[]}))});
 assert.ok(stripped.filter(a=>['eligibility','calculator','conditions'].includes(a.id)).every(a=>!a.available));
});
test('evidence and sandbox navigation select actual linked finding IDs',()=>{
 assert.equal(investigationNavigation(populated,'evidence').findingId,'f');
 assert.equal(investigationNavigation(populated,'lab').labFindingId,'f');
 assert.equal(investigationNavigation(populated,'sources').sourceId,'ad');
 assert.equal(investigationNavigation(empty,'evidence').findingId,undefined);
});
test('all actions resolve to existing workspace tabs and contextual targets',()=>{
 const tabs=['Overview','Sources','Findings','Reality Calculator','Evidence graph','Promise Journey','PromiseLab','Report'];
 for(const a of investigationActions(populated)){assert.ok(tabs.includes(investigationNavigation(populated,a.id).tab));}
 assert.equal(investigationNavigation(populated,'eligibility').targetId,'personal-reality');
 assert.equal(investigationNavigation(populated,'conditions').targetId,'condition-chain');
 assert.equal(investigationNavigation(populated,'clarify').targetId,'clarification-copilot');
});
test('a deliberately selected finding takes precedence over the flagship default',()=>{
 const c={...populated,findings:[...populated.findings,{id:'certificate',category:'certification',claim_a_id:'cb',claim_b_id:'ca'}]};
 assert.equal(investigationNavigation(c,'lab','certificate').labFindingId,'certificate');
 assert.equal(investigationNavigation(c,'sources','certificate').sourceId,'form');
 assert.equal(investigationNavigation(c,'evidence','stale-id').findingId,'f');
});

test('sandbox field differences explain changed scope dimensions without hiding the before value',()=>{
 const original={subject:'registration',modality:'required',value:'499',scope:{purpose:'registration',period:'2026',application_stage:'registration'},conditions:[]};
 const edited={...original,subject:'printed certificate',modality:'optional',scope:{...original.scope,purpose:'printed certificate',application_stage:'completion'}};
 const changes=helpers.changedClaimFields(original,edited);
 assert.equal(changes.length,4);
 assert.deepEqual(changes.find(c=>c.field==='scope · purpose'),{field:'scope · purpose',before:'registration',after:'printed certificate'});
 assert.ok(!changes.some(c=>c.field.includes('period')||c.field==='value'));
 assert.deepEqual(helpers.changedClaimFields(original,original),[]);
});
