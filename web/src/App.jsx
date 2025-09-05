import React, { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8077";

export default function App() {
  const [trades, setTrades] = useState([]);
  const [editingId, setEditingId] = useState(null);

  // Filtres
  const [filters, setFilters] = useState({
    date_from: "", date_to: "", bias: "", tags: ""
  });

  // Formulaire (tous les champs)
  const [form, setForm] = useState({
    num_trade: "", trade_date: "", analyse_time: "",
    bias_daily: "bullish",
    mp_bull_low: false, mp_bull_ll: false, mp_bull_hl: false, mp_bull_high: false,
    mp_bear_hh: false, mp_bear_lh: false,
    fvg_cible: "", ob_bullish: false, ob_bearish: false,
    sl: "", tp: "", gains_esperes: "", pnl: "",
    rr_planned: "", rr_realized: "",
    liq_buy: false, liq_sell: false, reversal: false, trade_stoppe: false,
    setup_notes: "", emotion: "", tags: ""
  });

  function num(v){ return v===""?null:Number(v); }

  async function load() {
    const qs = new URLSearchParams();
    if (filters.date_from) qs.set("date_from", filters.date_from);
    if (filters.date_to) qs.set("date_to", filters.date_to);
    if (filters.bias) qs.set("bias", filters.bias);
    if (filters.tags) qs.set("tags", filters.tags);
    const url = `${API}/api/trades${qs.toString() ? `?${qs.toString()}` : ""}`;
    const r = await fetch(url);
    setTrades(await r.json());
  }
  useEffect(() => { load(); }, []); // 1er chargement

  async function submit(e) {
    e.preventDefault();
    const payload = {
      ...form,
      num_trade: form.num_trade===""?null:Number(form.num_trade),
      sl: num(form.sl), tp: num(form.tp), gains_esperes: num(form.gains_esperes),
      pnl: num(form.pnl), rr_planned: num(form.rr_planned), rr_realized: num(form.rr_realized)
    };
    const url = editingId ? `${API}/api/trades/${editingId}` : `${API}/api/trades`;
    const method = editingId ? "PATCH" : "POST";
    const r = await fetch(url, { method, headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload) });
    if(r.ok){ setEditingId(null); await load(); }
  }

  function startEdit(t){
    setEditingId(t.id);
    setForm({
      num_trade: t.num_trade ?? "", trade_date: t.trade_date ?? "", analyse_time: t.analyse_time ?? "",
      bias_daily: t.bias_daily ?? "bullish",
      mp_bull_low: !!t.mp_bull_low, mp_bull_ll: !!t.mp_bull_ll, mp_bull_hl: !!t.mp_bull_hl, mp_bull_high: !!t.mp_bull_high,
      mp_bear_hh: !!t.mp_bear_hh, mp_bear_lh: !!t.mp_bear_lh,
      fvg_cible: t.fvg_cible ?? "", ob_bullish: !!t.ob_bullish, ob_bearish: !!t.ob_bearish,
      sl: t.sl ?? "", tp: t.tp ?? "", gains_esperes: t.gains_esperes ?? "", pnl: t.pnl ?? "",
      rr_planned: t.rr_planned ?? "", rr_realized: t.rr_realized ?? "",
      liq_buy: !!t.liq_buy, liq_sell: !!t.liq_sell, reversal: !!t.reversal, trade_stoppe: !!t.trade_stoppe,
      setup_notes: t.setup_notes ?? "", emotion: t.emotion ?? "", tags: t.tags ?? ""
    });
  }
  function cancelEdit(){ setEditingId(null); }

  async function remove(id){
    if(!confirm("Supprimer ce trade ?")) return;
    await fetch(`${API}/api/trades/${id}`, { method:"DELETE" });
    await load();
  }

  async function upload(id, tf, file){
    const fd = new FormData(); fd.append("file", file);
    await fetch(`${API}/api/trades/${id}/screenshots/${tf}`, { method:"POST", body: fd });
    await load();
  }

  async function exportCsv(){
    const qs = new URLSearchParams();
    if (filters.date_from) qs.set("date_from", filters.date_from);
    if (filters.date_to) qs.set("date_to", filters.date_to);
    if (filters.bias) qs.set("bias", filters.bias);
    if (filters.tags) qs.set("tags", filters.tags);
    const r = await fetch(`${API}/api/trades/export.csv${qs.toString()?`?${qs.toString()}`:""}`);
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'trades.csv';
    document.body.appendChild(a); a.click();
    a.remove(); URL.revokeObjectURL(url);
  }

  return (
    <div className="container">
      <div className="h1">Journal Trading</div>
      <div className="sub">MVP — créer, modifier et supprimer des trades • champs complets comme Excel</div>

      {/* ===== FORMULAIRE ===== */}
      <form onSubmit={submit} className="card form">
        <div className="grid-4">
          <input className="input" placeholder="N° trade" value={form.num_trade} onChange={e=>setForm({...form, num_trade:e.target.value})}/>
          <input className="input" type="date" value={form.trade_date} onChange={e=>setForm({...form, trade_date:e.target.value})}/>
          <input className="input" type="time" value={form.analyse_time} onChange={e=>setForm({...form, analyse_time:e.target.value})}/>
          <select className="input" value={form.bias_daily} onChange={e=>setForm({...form, bias_daily:e.target.value})}>
            <option value="bullish">Bullish</option><option value="bearish">Bearish</option><option value="neutral">Neutral</option>
          </select>
        </div>

        <fieldset><legend>Market Profile</legend>
          <div className="grid-4">
            <label className="inline"><input type="checkbox" checked={form.mp_bull_low} onChange={e=>setForm({...form, mp_bull_low:e.target.checked})}/> Bullish: Low</label>
            <label className="inline"><input type="checkbox" checked={form.mp_bull_ll} onChange={e=>setForm({...form, mp_bull_ll:e.target.checked})}/> Bullish: LL</label>
            <label className="inline"><input type="checkbox" checked={form.mp_bull_hl} onChange={e=>setForm({...form, mp_bull_hl:e.target.checked})}/> Bullish: HL</label>
            <label className="inline"><input type="checkbox" checked={form.mp_bull_high} onChange={e=>setForm({...form, mp_bull_high:e.target.checked})}/> Bullish: High</label>
            <label className="inline"><input type="checkbox" checked={form.mp_bear_hh} onChange={e=>setForm({...form, mp_bear_hh:e.target.checked})}/> Bearish: HH</label>
            <label className="inline"><input type="checkbox" checked={form.mp_bear_lh} onChange={e=>setForm({...form, mp_bear_lh:e.target.checked})}/> Bearish: LH</label>
          </div>
        </fieldset>

        <fieldset><legend>FVG & OrderBlocks</legend>
          <div className="grid-4">
            <input className="input" placeholder="FVG cible" value={form.fvg_cible} onChange={e=>setForm({...form, fvg_cible:e.target.value})}/>
            <label className="inline"><input type="checkbox" checked={form.ob_bullish} onChange={e=>setForm({...form, ob_bullish:e.target.checked})}/> OB Bullish</label>
            <label className="inline"><input type="checkbox" checked={form.ob_bearish} onChange={e=>setForm({...form, ob_bearish:e.target.checked})}/> OB Bearish</label>
          </div>
        </fieldset>

        <fieldset><legend>Prise de position</legend>
          <div className="grid-4">
            <input className="input" placeholder="SL" value={form.sl} onChange={e=>setForm({...form, sl:e.target.value})}/>
            <input className="input" placeholder="TP" value={form.tp} onChange={e=>setForm({...form, tp:e.target.value})}/>
            <input className="input" placeholder="Gains espérés" value={form.gains_esperes} onChange={e=>setForm({...form, gains_esperes:e.target.value})}/>
            <input className="input" placeholder="P&L" value={form.pnl} onChange={e=>setForm({...form, pnl:e.target.value})}/>
          </div>
          <div className="grid-4">
            <input className="input" placeholder="R/R prévu" value={form.rr_planned} onChange={e=>setForm({...form, rr_planned:e.target.value})}/>
            <input className="input" placeholder="R/R réalisé" value={form.rr_realized} onChange={e=>setForm({...form, rr_realized:e.target.value})}/>
          </div>
        </fieldset>

        <fieldset><legend>Zone de liquidité & États</legend>
          <div className="grid-4">
            <label className="inline"><input type="checkbox" checked={form.liq_buy} onChange={e=>setForm({...form, liq_buy:e.target.checked})}/> Liquidity Buy</label>
            <label className="inline"><input type="checkbox" checked={form.liq_sell} onChange={e=>setForm({...form, liq_sell:e.target.checked})}/> Liquidity Sell</label>
            <label className="inline"><input type="checkbox" checked={form.reversal} onChange={e=>setForm({...form, reversal:e.target.checked})}/> Reversal</label>
            <label className="inline"><input type="checkbox" checked={form.trade_stoppe} onChange={e=>setForm({...form, trade_stoppe:e.target.checked})}/> Trade stoppé</label>
          </div>
        </fieldset>

        <div className="grid-4">
          <input className="input" placeholder="Émotion" value={form.emotion} onChange={e=>setForm({...form, emotion:e.target.value})}/>
          <input className="input" placeholder="Tags (csv)" value={form.tags} onChange={e=>setForm({...form, tags:e.target.value})}/>
          <input className="input" placeholder="Notes setup" value={form.setup_notes} onChange={e=>setForm({...form, setup_notes:e.target.value})}/>
        </div>

        <div style={{display:"flex", gap:12}}>
          <button className="btn" type="submit">{editingId ? "Mettre à jour" : "Enregistrer"}</button>
          {editingId && <button type="button" className="btn" style={{background:"#444"}} onClick={cancelEdit}>Annuler</button>}
        </div>
      </form>

      {/* ===== BARRE DE FILTRES + EXPORT ===== */}
      <div className="card" style={{padding:12, marginTop:12}}>
        <div className="grid-4">
          <input className="input" type="date" value={filters.date_from} onChange={e=>setFilters(f=>({...f, date_from:e.target.value}))}/>
          <input className="input" type="date" value={filters.date_to} onChange={e=>setFilters(f=>({...f, date_to:e.target.value}))}/>
          <select className="input" value={filters.bias} onChange={e=>setFilters(f=>({...f, bias:e.target.value}))}>
            <option value="">Biais (tous)</option>
            <option value="bullish">Bullish</option>
            <option value="bearish">Bearish</option>
            <option value="neutral">Neutral</option>
          </select>
          <input className="input" placeholder="Tags contient..." value={filters.tags} onChange={e=>setFilters(f=>({...f, tags:e.target.value}))}/>
        </div>
        <div style={{display:"flex", gap:12, marginTop:10, alignItems:"center"}}>
          <button className="btn" type="button" onClick={load}>Appliquer</button>
          <button className="btn" type="button" style={{background:"#444"}} onClick={()=>{
            setFilters({date_from:"", date_to:"", bias:"", tags:""}); setTimeout(load, 0);
          }}>Réinitialiser</button>
          <div style={{flex:1}} />
          <button className="btn" type="button" onClick={exportCsv}>Exporter CSV</button>
        </div>
      </div>

      {/* ===== TABLE ===== */}
      <h2 style={{marginTop:18}}>Trades</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Date</th><th>#</th><th>Biais</th>
            <th>MP (Bullish)</th><th>MP (Bearish)</th>
            <th>FVG</th><th>OBs</th>
            <th>SL</th><th>TP</th><th>Gains</th><th>P&L</th>
            <th>Liquidity</th><th>Rev</th><th>Stop</th>
            <th>Screens</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {trades.map(t=>(
            <tr key={t.id}>
              <td>{t.trade_date||""}</td>
              <td>{t.num_trade||""}</td>
              <td><span className="badge">{t.bias_daily||""}</span></td>
              <td style={{fontSize:12}}>{t.mp_bull_low&&"Low "}{t.mp_bull_ll&&"LL "}{t.mp_bull_hl&&"HL "}{t.mp_bull_high&&"High "}</td>
              <td style={{fontSize:12}}>{t.mp_bear_hh&&"HH "}{t.mp_bear_lh&&"LH "}</td>
              <td>{t.fvg_cible||""}</td>
              <td>{t.ob_bullish?"Bullish":""}{t.ob_bullish&&t.ob_bearish?" / ":""}{t.ob_bearish?"Bearish":""}</td>
              <td>{t.sl??""}</td><td>{t.tp??""}</td><td>{t.gains_esperes??""}</td>
              <td className={t.pnl>0?"pnl-pos":t.pnl<0?"pnl-neg":""}>{t.pnl??""}</td>
              <td>{t.liq_buy?"Buy":""}{t.liq_buy&&t.liq_sell?" / ":""}{t.liq_sell?"Sell":""}</td>
              <td>{t.reversal?"Oui":"Non"}</td>
              <td>{t.trade_stoppe?"Oui":"Non"}</td>
              <td>
                {["4H","1H","30M","15M"].map(tf=>(
                  <span key={tf} style={{marginRight:8, display:"inline-block"}}>
                    <label style={{fontSize:12,opacity:.8,marginRight:4}}>{tf}</label>
                    <input type="file" onChange={e=>e.target.files?.[0] && upload(t.id, tf, e.target.files[0])}/>
                  </span>
                ))}
              </td>
              <td>
                <button className="btn" style={{padding:"6px 10px", fontSize:12}} onClick={()=>startEdit(t)}>Modifier</button>{" "}
                <button className="btn" style={{padding:"6px 10px", fontSize:12, background:"#c0392b"}} onClick={()=>remove(t.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
