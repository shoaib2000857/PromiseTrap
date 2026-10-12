import type {Investigation} from './types';
export type InvestigationAction='evidence'|'journey'|'calculator'|'conditions'|'lab'|'eligibility'|'challenge'|'graph'|'clarify'|'report'|'sources';
export type GalleryEntry={id:string;title:string;domain:string;summary:string;issues:string[];capability:string};
export function filterGallery<T extends GalleryEntry>(catalog:T[],category:string,query:string):T[]{
 const search=query.trim().toLowerCase();
 return catalog.filter(c=>(category==='All investigations'||c.domain===category)&&[c.title,c.domain,c.summary,c.capability,...c.issues].join(' ').toLowerCase().includes(search));
}
export function investigationActions(c:Investigation):{id:InvestigationAction;title:string;available:boolean}[]{
 return [
  {id:'evidence',title:'Inspect evidence & ScopeGuard',available:!!c.findings.length},
  {id:'sources',title:'Open original sources',available:!!c.sources.length},
  {id:'journey',title:'Trace promise changes',available:!!c.claims.length},
  {id:'calculator',title:'Understand financial commitments',available:!!c.financial?.values.length},
  {id:'conditions',title:'Explore benefit conditions',available:!!c.conditions?.length},
  {id:'lab',title:'Test a hypothetical change',available:!!c.findings.length},
  {id:'eligibility',title:'Check documented eligibility',available:c.claims.some(claim=>!!claim.criteria?.length)},
  {id:'challenge',title:'Challenge a finding',available:!!c.findings.length},
  {id:'graph',title:'Inspect evidence network',available:!!c.claims.length},
  {id:'clarify',title:'Generate clarification questions',available:!!c.findings.length},
  {id:'report',title:'Download a report & receipt',available:!!c.claims.length},
 ];
}
export function investigationNavigation(c:Investigation,action:InvestigationAction,preferredFinding?:string){
 const finding=c.findings.find(f=>f.id===preferredFinding)||c.findings.find(f=>f.category==='financial')||c.findings[0];
 const tab={evidence:'Findings',challenge:'Findings',sources:'Sources',journey:'Promise Journey',calculator:'Reality Calculator',conditions:'Findings',lab:'PromiseLab',eligibility:'Overview',graph:'Evidence graph',clarify:'Report',report:'Report'}[action];
 const source=c.sources.find(s=>s.id===c.claims.find(claim=>claim.id===finding?.claim_a_id)?.source_id)||c.sources[0];
 return {tab,findingId:action==='evidence'||action==='challenge'?finding?.id:undefined,sourceId:action==='sources'?source?.id:undefined,labFindingId:action==='lab'?finding?.id:undefined,targetId:action==='conditions'?'condition-chain':action==='eligibility'?'personal-reality':action==='clarify'?'clarification-copilot':'workspace-content'};
}
export function changedClaimFields(original:Record<string,unknown>,edited:Record<string,unknown>){
 const format=(value:unknown):string=>value===null||value===undefined?'Unknown':Array.isArray(value)?value.map(String).join('; ')||'None':typeof value==='object'?JSON.stringify(value):String(value);
 const rows:{field:string;before:string;after:string}[]=[];
 for(const [field,value] of Object.entries(edited)){
  if(JSON.stringify(value)===JSON.stringify(original[field]))continue;
  if(field==='scope'&&value&&typeof value==='object'&&original.scope&&typeof original.scope==='object'){
   const before=original.scope as Record<string,unknown>;
   for(const [dimension,next] of Object.entries(value)){if(JSON.stringify(next)!==JSON.stringify(before[dimension]))rows.push({field:'scope · '+dimension,before:format(before[dimension]),after:format(next)});}
  }else rows.push({field,before:format(original[field]),after:format(value)});
 }
 return rows;
}
