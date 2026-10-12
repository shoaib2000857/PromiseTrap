'use client';
import {useState} from 'react';
import {ArrowRight,Check,Compass,X,Play,RotateCcw} from 'lucide-react';
import {type Investigation} from '../lib/types';
import {investigationActions,type InvestigationAction} from '../lib/demo';
const tourSteps:{action:InvestigationAction;title:string;detail:string}[]=[
 {action:'evidence',title:'Choose a finding',detail:'Open a finding card to see the matched claims and their ScopeGuard reasoning.'},
 {action:'sources',title:'Open original evidence',detail:'Inspect the original source bytes and exact quotation. Image location is approximate unless reviewed.'},
 {action:'journey',title:'Trace the promise',detail:'Follow document stages and qualifications. Undated documents are a sequence, not a chronology.'},
 {action:'calculator',title:'Understand the commitment',detail:'Review real financial values. Conditional compensation is separate from guarantees.'},
 {action:'lab',title:'Change a hypothetical condition',detail:'Edit claim B or apply an available preset, then rerun PromiseGraph. Originals stay untouched.'},
 {action:'lab',title:'Inspect the hypothetical result',detail:'Compare the original classification, hypothetical classification and exact changed fields. Use Reset to restore the sandbox.'},
 {action:'graph',title:'Inspect the evidence network',detail:'Select a source, claim or finding to highlight connected evidence. Open its details or fit the graph.'},
 {action:'report',title:'Export the dossier',detail:'Download an actual PDF, Markdown or JSON report. The report carries provenance, evidence and limitations.'},
];
export default function InvestigationExperience({caseData,onAction,onRestart,onGallery,busy}:{caseData:Investigation;onAction:(a:InvestigationAction)=>void;onRestart:()=>void;onGallery:()=>void;busy:boolean}){
 const [tour,setTour]=useState<number|null>(null),[visited,setVisited]=useState<InvestigationAction[]>([]),[expanded,setExpanded]=useState(true);
 const actions=investigationActions(caseData);
 function go(action:InvestigationAction){setVisited(v=>v.includes(action)?v:[...v,action]);onAction(action);}
 const steps=tourSteps.filter(s=>actions.find(a=>a.id===s.action)?.available);
 function move(i:number){setTour(i);go(steps[i].action);}
 return <section className="explore-investigation" aria-label="Explore this investigation">
  <div className="explore-heading"><div><span className="eyebrow">{caseData.is_example?'DEMO CONTROL CENTER':'SUGGESTED INVESTIGATION PATH'}</span><h2><Compass size={20}/> Explore This Investigation</h2></div><div className="tool-actions"><button className="text-button" onClick={()=>setExpanded(!expanded)} aria-expanded={expanded}>{expanded?'Collapse':'Expand'} actions</button>{steps.length>0&&<button className="secondary" onClick={()=>move(0)}><Play size={13}/> Guided tour</button>}{caseData.demo_scenario&&<><button className="text-button" onClick={onGallery}>Choose another case</button><button className="text-button" disabled={busy||caseData.status==='processing'} onClick={onRestart}><RotateCcw size={13}/> Restart safely</button></>}</div></div>
  {expanded&&<><div className="explore-actions">{actions.filter(a=>a.available).map(a=><button key={a.id} onClick={()=>go(a.id)}>{visited.includes(a.id)?<Check size={13}/>:<ArrowRight size={13}/>} {a.title}</button>)}</div><p className="muted">{!caseData.findings.length&&caseData.claims.length?'No discrepancies established; inspect the documents, graph and report to review the aligned evidence. ':''}Checkmarks mean opened in this session, not independently verified. {caseData.claims_provenance?.startsWith('model:')?'Live extraction: '+caseData.claims_provenance.slice(6):caseData.example_mode==='fictional_images'?'Original images loaded; model extraction has not completed.':caseData.is_example?'Fictional sample · Authored claims · Verified with PromiseGraph rules':'Findings apply to the supplied evidence only.'}</p></>}
  {tour!==null&&steps[tour]&&<div className="guided-tour" role="region" aria-label="Guided investigation tour"><div><span className="eyebrow">GUIDED TOUR / {tour+1} OF {steps.length}</span><h3>{steps[tour].title}</h3><p>{steps[tour].detail}</p></div><div className="tour-controls"><button className="secondary" disabled={tour===0} onClick={()=>move(tour-1)}>Back</button><button className="primary" onClick={()=>tour===steps.length-1?setTour(null):move(tour+1)}>{tour===steps.length-1?'Finish':'Next'}</button><button className="text-button" onClick={()=>tour===steps.length-1?setTour(null):move(tour+1)}>Skip</button><button className="icon-button" aria-label="Exit guided tour" onClick={()=>setTour(null)}><X size={18}/></button></div></div>}
 </section>;
}
