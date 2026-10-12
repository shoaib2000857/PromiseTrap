'use client';
import {useEffect,useState} from 'react';
import {ArrowRight,ArrowUpRight,FileText,Search,Sparkles,ShieldCheck,Loader2} from 'lucide-react';
import {filterGallery} from '../lib/demo';
import {api,type Investigation} from '../lib/types';
export type DemoCase={id:string;title:string;domain:string;summary:string;issues:string[];capability:string;source_count:number;preview_url:string;image_available:boolean;featured?:boolean;control?:boolean};
export default function InvestigationGallery({onLoad}:{onLoad:(c:Investigation,live:boolean)=>Promise<void>}){
 const [catalog,setCatalog]=useState<DemoCase[]>([]),[error,setError]=useState(''),[loading,setLoading]=useState(true),[pending,setPending]=useState('');
 const [category,setCategory]=useState('All investigations'),[search,setSearch]=useState('');
 async function fetchCatalog(){setLoading(true);setError('');try{setCatalog(await api<DemoCase[]>('/examples/gallery'));}catch(e){setError((e as Error).message);}finally{setLoading(false);}}
 useEffect(()=>{fetchCatalog();},[]);
 async function launch(item:DemoCase,live=false){setPending(item.id+(live?'-live':''));setError('');try{const c=await api<Investigation>('/examples/advanced/'+item.id+(live?'?images=true':''),{method:'POST'});await onLoad(c,live);}catch(e){setError((e as Error).message);}finally{setPending('');}}
 const visible=filterGallery(catalog,category,search);
 return <section className="investigation-gallery" id="investigation-gallery" aria-labelledby="gallery-title">
  <div className="section-heading"><div><span className="eyebrow">DEMO MODE / NO KEY REQUIRED FOR WALKTHROUGHS</span><h2 id="gallery-title">The Investigation Gallery</h2><p className="muted">Real problems. Fictional evidence. Verifiable investigations.</p></div><span className="gallery-count">{catalog.length} CASE FILES</span></div>
  <div className="gallery-toolbar"><div className="gallery-filters" aria-label="Investigation categories">{['All investigations',...new Set(catalog.map(c=>c.domain))].map(c=><button key={c} aria-pressed={category===c} className={category===c?'active':''} onClick={()=>setCategory(c)}>{c}</button>)}</div><div className="searchbox"><Search size={16}/><input aria-label="Search investigation gallery" placeholder="Find a case or capability…" value={search} onChange={e=>setSearch(e.target.value)}/></div></div>
  {loading&&<p role="status"><Loader2 size={16} className="spin"/> Loading fictional case catalog…</p>}
  {error&&<div className="tool-error" role="alert">{error} <button className="text-button" onClick={fetchCatalog}>Retry catalog</button></div>}
  <div className="gallery-grid">{visible.map((c,i)=><article className={'gallery-card '+(c.featured?'flagship ':'')+(c.control?'control':'')} key={c.id}>
   <div className="gallery-card-head"><span className="eyebrow">{c.domain.toUpperCase()}</span><span className="fictional-badge">FICTIONAL DEMO</span></div>
   <div className="gallery-visual"><img src={c.preview_url} loading="lazy" alt={'Original fictional document preview for '+c.title}/><div className="gallery-visual-caption"><FileText size={15}/>{c.source_count} original documents<span>{String(i+1).padStart(2,'0')}</span></div>{c.featured&&<span className="gallery-ribbon">START HERE / FLAGSHIP</span>}{c.control&&<span className="gallery-ribbon"><ShieldCheck size={12}/> NEGATIVE CONTROL</span>}</div>
   <h3>{c.title}</h3><p>{c.summary}</p><div className="issue-tags">{c.issues.map(issue=><span key={issue}>{issue}</span>)}</div><div className="gallery-capability"><Sparkles size={14}/>{c.capability}</div>
   <div className="gallery-actions"><button className="primary" disabled={!!pending} onClick={()=>launch(c)}>{pending===c.id?<Loader2 size={15} className="spin"/>:null}Explore Investigation <ArrowRight size={15}/></button>{c.image_available&&<button className="text-button" disabled={!!pending} onClick={()=>launch(c,true)}>Analyze Original Images with Gemma 4 <ArrowUpRight size={14}/></button>}</div>
  </article>)}</div>
  {!loading&&!error&&!visible.length&&<p className="tool-caution">No investigations match. <button className="text-button" onClick={()=>{setSearch('');setCategory('All investigations');}}>Clear filters</button></p>}
  <p className="gallery-disclosure">Walkthroughs use authored claims and real PromiseGraph rules. Image analysis sends fictional documents to the Gemini API and requires GEMINI_API_KEY. All organizations and offers shown here are fictional.</p>
 </section>;
}
