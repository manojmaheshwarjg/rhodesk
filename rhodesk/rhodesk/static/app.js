const $ = (id) => document.getElementById(id);
const money = (c) => "$" + ((c || 0) / 100).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const trim = (s, n) => { s = String(s ?? ""); if (s.length <= n) return s; const cut = s.slice(0, n); const sp = cut.lastIndexOf(" "); return (sp > n * 0.6 ? cut.slice(0, sp) : cut) + "…"; };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));

let state = { view: "counterparties", posture: "all", rows: [], status: null, callTimer: null, runId: null };

async function api(path, opts) {
  const res = await fetch(path, { headers: { "Content-Type": "application/json" }, ...opts });
  if (!res.ok) throw new Error((await res.text()).slice(0, 300));
  return res.json();
}

function toast(msg, ms = 3200) {
  const t = $("toast");
  t.textContent = msg;
  t.classList.add("on");
  setTimeout(() => t.classList.remove("on"), ms);
}

// --- status ----------------------------------------------------------------

async function loadStatus() {
  const s = await api("/api/status");
  state.status = s;
  const svc = s.services;
  $("orgName").textContent = svc.company;
  $("orgInitials").textContent = svc.company.slice(0, 2).toUpperCase();
  $("services").innerHTML = [
    ["Rho", true, svc.rho.note],
    ["Tavily", svc.tavily.live, svc.tavily.live ? "live" : "stubbed"],
    ["LLM", svc.llm.live, svc.llm.live ? svc.llm.provider : "stubbed"],
    ["Voice", svc.voice.live, svc.voice.live ? "ElevenLabs" : "simulated"],
  ].map(([n, on, note]) =>
    `<div><span class="led ${on ? "on" : "off"}"></span>${n} <span style="color:var(--gr3)">${esc(note)}</span></div>`
  ).join("");
  if (s.counts.counterparties) $("lastRun").textContent = `${s.counts.counterparties} counterparties`;
}

// --- run -------------------------------------------------------------------

async function runDesk() {
  $("runBtn").disabled = true;
  $("runbar").classList.add("on");
  try {
    await api("/api/run", { method: "POST" });
  } catch (e) { toast("Could not start: " + e.message); }
  const poll = setInterval(async () => {
    const r = await api("/api/run");
    $("runtext").textContent = r.stage === "error"
      ? "Error: " + r.detail
      : `${r.stage}${r.detail ? " · " + r.detail : ""}`;
    if (!r.running) {
      clearInterval(poll);
      $("runBtn").disabled = false;
      setTimeout(() => $("runbar").classList.remove("on"), 1200);
      state.runId = null;
      await loadStatus();
      await render();
      if (r.finished) toast(`${r.finished.companies} companies, ${r.finished.signals} signals`);
    }
  }, 700);
}

// --- views -----------------------------------------------------------------

async function render() {
  if (state.view === "counterparties") return renderCounterparties();
  if (state.view === "changes") return renderChanges();
  if (state.view === "queue") return renderQueue();
  if (state.view === "signals") return renderSignals();
  if (state.view === "settings") return renderSettings();
  return renderCalls();
}

async function renderCounterparties() {
  $("title").textContent = "Counterparties";
  const rows = await api("/api/counterparties");
  state.rows = rows;
  $("subtitle").textContent = rows.length
    ? `${rows.length} resolved companies · ${rows.reduce((a, r) => a + (r.aliases?.length || 0), 0)} ledger names`
    : "Nothing yet. Press Run desk.";

  const sum = (f) => rows.reduce((a, r) => a + (r[f] || 0), 0);
  const byP = (p) => rows.filter((r) => r.posture === p);
  $("tiles").innerHTML = [
    ["Collect", money(byP("collect").reduce((a, r) => a + r.outstanding, 0)), `${byP("collect").length} to call`, "var(--blue-t)"],
    ["Cut", money(byP("cut").reduce((a, r) => a + r.monthly_spend, 0)) + " /mo", `${byP("cut").length} found`, "var(--amber-t)"],
    ["Cover", money(byP("cover").reduce((a, r) => a + r.outstanding, 0)), `${byP("cover").length} at risk`, "var(--red-t)"],
    ["Total outstanding", money(sum("outstanding")), `${sum("open_invoices")} open invoices`, "var(--gr)"],
  ].map(([l, v, m, c]) =>
    `<div class="tile"><p class="l">${l}</p><p class="v">${v}</p><p class="m" style="color:${c}">${m}</p></div>`
  ).join("");

  const counts = { all: rows.length, collect: byP("collect").length, cut: byP("cut").length, cover: byP("cover").length, watch: byP("watch").length };
  $("filters").innerHTML = Object.entries(counts).map(([k, n]) =>
    `<button class="pill ${state.posture === k ? "on" : ""}" data-posture="${k}">${k[0].toUpperCase() + k.slice(1)} ${n}</button>`
  ).join("");

  const shown = state.posture === "all" ? rows : rows.filter((r) => r.posture === state.posture);
  if (!shown.length) {
    $("content").innerHTML = `<div class="empty">${rows.length ? "Nothing in this posture." : "Press <strong>Run desk</strong> to read the ledger and research every counterparty."}</div>`;
    return;
  }

  $("content").innerHTML = `<table><thead><tr>
      <th>Counterparty</th><th>Sector</th><th class="num">Outstanding</th><th class="num">Money out</th>
      <th class="num">Oldest</th><th class="num">% of AR</th><th>Signal</th><th>Posture</th><th>Recommended</th>
    </tr></thead><tbody>${shown.map(rowHtml).join("")}</tbody></table>`;
}

function rowHtml(r) {
  const initials = r.display_name.split(/\s+/).slice(0, 2).map((w) => w[0]).join("").toUpperCase();
  const sig = r.top_signal;
  const extra = (r.aliases || []).filter((a) => a !== r.display_name);
  const aliasLine = extra.length ? extra.join(" · ") : "";
  return `<tr class="clickable" data-id="${esc(r.id)}">
    <td><div class="co"><div class="sq">${esc(initials)}</div><div style="min-width:0">
      <p class="nm">${esc(r.display_name)}${r.demo ? ' <span class="bd demo">demo</span>' : ""}</p>
      ${aliasLine ? `<p class="al">${esc(aliasLine)}</p>` : ""}</div></div></td>
    <td style="color:var(--gr2)">${esc(r.sector || "—")}</td>
    <td class="num" style="${r.outstanding ? "font-weight:500" : ""}">${r.outstanding ? money(r.outstanding) : '<span style="color:var(--gr3)">—</span>'}</td>
    <td class="num">${r.money_out ? money(r.money_out) : '<span style="color:var(--gr3)">—</span>'}</td>
    <td class="num" style="${r.oldest_days > 60 ? "color:var(--red-t)" : ""}">${r.oldest_days ? r.oldest_days + "d" : '<span style="color:var(--gr3)">—</span>'}</td>
    <td class="num">${r.ar_share ? Math.round(r.ar_share * 100) + "%" : '<span style="color:var(--gr3)">—</span>'}</td>
    <td>${sig ? `<span class="sig"><span class="sd ${esc(sig.severity)}"></span>${esc(trim(sig.title, 38))}</span>` : '<span style="color:var(--gr3);font-size:13px">No change</span>'}</td>
    <td><span class="bd ${esc(r.posture)}">${r.posture[0].toUpperCase() + r.posture.slice(1)}</span></td>
    <td style="color:var(--gr2)">${esc(r.recommendation || "None")}</td>
  </tr>`;
}

async function renderSignals() {
  $("title").textContent = "Signals";
  $("subtitle").textContent = "What changed about the companies that owe you money, or that you pay";
  $("tiles").innerHTML = ""; $("filters").innerHTML = "";
  const rows = await api("/api/signals");
  if (!rows.length) { $("content").innerHTML = `<div class="empty">No signals yet.</div>`; return; }
  $("content").innerHTML = `<div class="card" style="padding:4px 20px">${rows.map((s) => `
    <div class="sgrow">
      <span class="sd ${esc(s.severity)}" style="margin-top:7px"></span>
      <div style="flex-grow:1">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:3px">
          <strong style="font-weight:500">${esc(s.counterparty_name)}</strong>
          <span class="bd ${esc(s.posture)}">${esc(s.posture)}</span>
          ${s.outstanding ? `<span style="font-size:13px;color:var(--gr2)">${money(s.outstanding)} outstanding</span>` : ""}
        </div>
        <p style="margin:0;font-size:14px">${esc(s.title)}</p>
        <p style="margin:4px 0 0;font-size:14px;color:var(--gr);line-height:1.5">${esc(s.detail)}</p>
        ${s.source_url ? `<p class="src">${esc(s.source_name || s.source_url)}</p>` : ""}
      </div>
    </div>`).join("")}</div>`;
}

const AGO = (iso) => {
  if (!iso) return "";
  const secs = (Date.now() - new Date(iso).getTime()) / 1000;
  if (secs < 90) return "just now";
  if (secs < 5400) return Math.round(secs / 60) + " min ago";
  if (secs < 172800) return Math.round(secs / 3600) + " hours ago";
  return Math.round(secs / 86400) + " days ago";
};

const GROUPS = [
  ["urgent", "Needs attention today"],
  ["attention", "Worth a look"],
  ["good", "Good news"],
  ["info", "For the record"],
];

async function renderChanges() {
  $("title").textContent = "What changed";
  const d = await api("/api/changes" + (state.runId ? `?run_id=${state.runId}` : ""));

  if (!d.run) {
    $("subtitle").textContent = "Nothing to compare yet";
    $("tiles").innerHTML = ""; $("filters").innerHTML = "";
    $("content").innerHTML = `<div class="empty">Run the desk to take a first reading. The run after that is the one that can tell you what moved.</div>`;
    return;
  }

  const runs = (await api("/api/runs")).runs;
  $("filters").innerHTML = `<div class="runsel">${runs.slice(0, 8).map((r) => `
    <button class="rp ${r.id === d.run.id ? "on" : ""}" data-run="${r.id}">
      Run ${r.id} · ${esc(AGO(r.finished_at))}${r.degraded ? ` <span class="deg">degraded</span>` : ""}
    </button>`).join("")}</div>`;

  if (!d.comparable) {
    $("subtitle").textContent = "First reading, nothing behind it to compare against";
    $("tiles").innerHTML = "";
    $("content").innerHTML = `<div class="empty">Run ${d.run.id} is the baseline: ${d.run.counterparties} counterparties and ${d.run.signals} signals. The next run is the first one that can show movement.</div>`;
    return;
  }

  const n = (w) => d.summary[w] || 0;
  $("subtitle").textContent = d.changes.length
    ? `${d.changes.length} changes since run ${d.previous.id}, ${AGO(d.previous.finished_at)}`
    : `Nothing moved since run ${d.previous.id}`;

  $("tiles").innerHTML = [
    ["Needs attention", String(n("urgent")), n("urgent") ? "act today" : "nothing urgent", n("urgent") ? "var(--red-t)" : "var(--gr)"],
    ["Worth a look", String(n("attention")), "when you have a moment", "var(--amber-t)"],
    ["Recovered", money(d.money.recovered), "paid since the last run", "var(--mint-t)"],
    ["Newly overdue", money(d.money.new_overdue), "aged or arrived owing", "var(--gr)"],
  ].map(([l, v, m, c]) =>
    `<div class="tile"><p class="l">${l}</p><p class="v">${v}</p><p class="m" style="color:${c}">${m}</p></div>`).join("");

  if (!d.changes.length) {
    $("content").innerHTML = `<div class="empty">Nothing moved between run ${d.previous.id} and run ${d.run.id}. That is a real answer, not an empty screen.</div>`;
    return;
  }

  const degraded = d.changes.find((c) => c.kind === "degraded");
  const body = GROUPS.map(([weight, label]) => {
    const rows = d.changes.filter((c) => c.weight === weight && c.kind !== "degraded");
    if (!rows.length) return "";
    return `<p class="grp">${label}</p>` + rows.map((c) => `
      <div class="chrow" ${c.counterparty_id ? `data-id="${esc(c.counterparty_id)}" style="cursor:pointer"` : ""}>
        <span class="wt ${esc(c.weight)}">${esc(c.kind)}</span>
        <div style="flex-grow:1;min-width:0">
          <span class="nm">${esc(c.display_name)}</span>
          <p class="hl">${esc(c.headline)}</p>
          ${c.detail ? `<p class="dt">${esc(trim(c.detail, 220))}</p>` : ""}
          ${c.source_url ? `<p class="src">${esc(c.source_url.replace(/^https?:\/\/(www\.)?/, "").split("/")[0])}</p>` : ""}
        </div>
        ${c.amount ? `<div class="amt"><p style="margin:0;font-size:15px;font-weight:500">${money(Math.abs(c.amount))}</p></div>` : ""}
      </div>`).join("");
  }).join("");

  $("content").innerHTML =
    (degraded ? `<div class="warnbox"><strong style="font-weight:500">${esc(degraded.headline)}.</strong> ${esc(degraded.detail)}</div>` : "") +
    `<div class="card" style="padding:0">${body}</div>`;
}

async function renderQueue() {
  $("title").textContent = "Collect queue";
  const q = await api("/api/queue");
  $("subtitle").textContent = q.items.length
    ? `${q.items.length} to work, ranked by what is likeliest to come back`
    : "Nothing owed to you right now.";
  $("filters").innerHTML = "";

  $("tiles").innerHTML = [
    ["Outstanding", money(q.total_outstanding), `${q.items.length} counterparties`, "var(--gr)"],
    ["Expected recovery", money(q.total_expected), "after age and risk", "var(--mint-t)"],
    ["Already called", String(q.already_called), `of ${q.items.length}`, "var(--gr)"],
    ["Approval needed above", money(q.needs_approval_above), "set in agent settings", "var(--amber-t)"],
  ].map(([l, v, m, c]) =>
    `<div class="tile"><p class="l">${l}</p><p class="v">${v}</p><p class="m" style="color:${c}">${m}</p></div>`).join("");

  if (!q.items.length) { $("content").innerHTML = `<div class="empty">Nothing in the queue. Run the desk first.</div>`; return; }

  $("content").innerHTML = `<div class="card" style="padding:0">${q.items.map((i, n) => {
    const sig = i.top_signal;
    const pct = Math.round(i.recoverability * 100);
    const approval = i.outstanding >= q.needs_approval_above;
    return `<div class="qrow">
      <div class="rank">${n + 1}</div>
      <div style="flex-grow:1;min-width:0">
        <div style="display:flex;align-items:center;gap:10px">
          <strong style="font-weight:500;font-size:15px">${esc(i.display_name)}</strong>
          <span class="bd ${esc(i.posture)}">${i.posture[0].toUpperCase() + i.posture.slice(1)}</span>
          ${approval ? `<span class="bd cut">needs approval</span>` : ""}
        </div>
        <p style="margin:4px 0 0;font-size:13px;color:var(--gr)">
          ${i.open_invoices} open · oldest ${i.oldest_days || 0} days · ${Math.round((i.ar_share || 0) * 100)}% of AR
          ${sig ? ` · <span class="sd ${esc(sig.severity)}" style="display:inline-block;vertical-align:1px"></span> ${esc(trim(sig.title, 40))}` : ""}
        </p>
        ${i.last_call ? `<p style="margin:4px 0 0;font-size:12px;color:var(--mint-t)">Last call ${esc((i.last_call.created_at || "").slice(0, 10))} · ${esc(i.last_call.summary || i.last_call.state)}</p>` : ""}
      </div>
      <div style="text-align:right;flex-shrink:0">
        <p style="margin:0;font-size:16px;font-weight:500">${money(i.outstanding)}</p>
        <p style="margin:3px 0 0;font-size:12px;color:var(--gr2)">${money(i.expected)} expected</p>
      </div>
      <div style="flex-shrink:0"><div class="bar"><i style="width:${pct}%"></i></div>
        <p style="margin:5px 0 0;font-size:11px;color:var(--gr2);text-align:right">${pct}% likely</p></div>
      <button class="btn" data-call="${esc(i.id)}" style="flex-shrink:0">Review call</button>
    </div>`;
  }).join("")}</div>`;
}

async function renderCalls() {
  $("title").textContent = "Calls";
  $("subtitle").textContent = "Every call the desk has placed";
  $("filters").innerHTML = "";
  const [rows, stats] = await Promise.all([api("/api/calls"), api("/api/call-stats")]);

  $("tiles").innerHTML = [
    ["Placed", String(stats.placed), `${stats.simulated} simulated`, "var(--gr)"],
    ["Completed", String(stats.completed), "reached a person", "var(--gr)"],
    ["Commitments", String(stats.commitments), "dates or terms agreed", "var(--mint-t)"],
    ["Value secured", money(stats.value_secured), "against open invoices", "var(--mint-t)"],
  ].map(([l, v, m, c]) =>
    `<div class="tile"><p class="l">${l}</p><p class="v">${v}</p><p class="m" style="color:${c}">${m}</p></div>`).join("");

  if (!rows.length) { $("content").innerHTML = `<div class="empty">No calls yet. Work the collect queue.</div>`; return; }

  $("content").innerHTML = `<div class="card" style="padding:0">${rows.map((c) => {
    const oc = c.outcome || {};
    const good = ["commitment", "agreed"].includes(oc.result);
    return `<div style="border-bottom:1px solid var(--ln-s)">
      <div class="qrow" style="border-bottom:0;cursor:pointer" data-expand="${esc(c.id)}">
        <div style="flex-grow:1;min-width:0">
          <div style="display:flex;align-items:center;gap:10px">
            <strong style="font-weight:500;font-size:15px">${esc(c.counterparty_name)}</strong>
            <span class="bd ${esc(c.posture || "watch")}">${esc(c.posture || "—")}</span>
            ${c.simulated ? `<span class="bd demo">simulated</span>` : ""}
          </div>
          <p style="margin:4px 0 0;font-size:13px;color:var(--gr)">${esc(oc.summary || (c.state === "live" ? "In progress" : "No outcome recorded"))}</p>
        </div>
        <span style="font-size:13px;color:${good ? "var(--mint-t)" : "var(--gr2)"};flex-shrink:0">${good ? "Commitment" : esc(c.state)}</span>
        <span style="font-size:13px;color:var(--gr2);flex-shrink:0;width:130px;text-align:right">${esc((c.created_at || "").slice(0, 16).replace("T", " "))}</span>
      </div>
      <div id="tx-${esc(c.id)}" style="display:none;padding:0 20px 18px">
        ${(oc.commitments || []).length ? `<div style="margin-bottom:10px">${(oc.commitments || []).map((x) =>
          `<div class="kv"><span>${esc(x.label)}</span><span>${esc(x.value)}</span></div>`).join("")}</div>` : ""}
        <div class="tx">${(c.transcript || []).map((tn) => tn.role === "tool"
          ? `<div class="tool">${esc(tn.text)}</div>`
          : `<div class="turn"><div class="tav ${tn.role}">${tn.role === "agent" ? "RD" : "··"}</div>
             <div><p class="who">${tn.role === "agent" ? "Rho Desk" : esc(c.counterparty_name)}</p>
             <p class="say">${esc(tn.text)}</p></div></div>`).join("") || '<p style="color:var(--gr2);margin:0">No transcript.</p>'}</div>
      </div>
    </div>`;
  }).join("")}</div>`;
}

async function renderSettings() {
  $("title").textContent = "Agent settings";
  $("subtitle").textContent = "These are not decoration: the agent reads them before every call";
  $("tiles").innerHTML = ""; $("filters").innerHTML = "";
  const s = await api("/api/settings");
  const cps = await api("/api/counterparties");

  $("content").innerHTML = `
    <div class="cols2">
      <div class="card">
        <p class="lbl">Identity</p>
        <div class="fld"><label>Calling on behalf of</label>
          <input type="text" id="s-company" value="${esc(s.company_name)}"></div>
        <div class="fld"><label>Voice</label>
          <select id="s-voice">${["Quinn", "Aria", "Nova", "Rowan"].map((v) =>
            `<option ${v === s.voice_name ? "selected" : ""}>${v}</option>`).join("")}</select></div>
        <div class="fld"><label>Tone</label>
          <select id="s-tone">${["measured", "warm", "direct"].map((v) =>
            `<option ${v === s.tone ? "selected" : ""}>${v}</option>`).join("")}</select></div>
        <div class="sw"><input type="checkbox" id="s-disclose" ${s.disclose_ai ? "checked" : ""}>
          <label for="s-disclose" style="margin:0">Say it is an AI in the first sentence</label></div>
        <div class="sw"><input type="checkbox" id="s-record" ${s.announce_recording ? "checked" : ""}>
          <label for="s-record" style="margin:0">Announce that the call is recorded</label></div>
        <p class="hint">Turning either off may be unlawful where you or the other party are. Both stay on unless you have checked.</p>
      </div>

      <div class="card">
        <p class="lbl">Limits</p>
        <div class="fld"><label>A human must approve calls above</label>
          <input type="number" id="s-threshold" value="${Math.round(s.approval_threshold_cents / 100)}" min="0" step="500">
          <p class="hint">In dollars. Anything at or above this refuses to dial until someone approves it.</p></div>
        <div class="fld"><label>Payment window the agent may offer</label>
          <input type="number" id="s-window" value="${s.payment_window_days}" min="1" max="120">
          <p class="hint">Days.</p></div>
        <div class="fld"><label>Most instalments it may agree to</label>
          <input type="number" id="s-instal" value="${s.max_instalments}" min="1" max="6"></div>
        <div class="fld"><label>Calls per run</label>
          <input type="number" id="s-calls" value="${s.calls_per_run}" min="1" max="50"></div>
      </div>
    </div>

    <div class="cols2">
      <div class="card">
        <p class="lbl">Authorised to agree</p>
        <div class="fld"><textarea id="s-may">${esc((s.may_agree || []).join("\n"))}</textarea>
          <p class="hint">One per line. Handed to the agent verbatim. The phrases "the window below" and "the limit below" are replaced with the numbers you set.</p></div>
      </div>
      <div class="card">
        <p class="lbl">Must not</p>
        <div class="fld"><textarea id="s-must">${esc((s.must_not || []).join("\n"))}</textarea>
          <p class="hint">One per line. Keep the last line: it stops the agent repeating back anything it read online, which is what makes the research feel like judgement rather than surveillance.</p></div>
      </div>
    </div>

    <div class="card">
      <p class="lbl">Safety</p>
      <div class="fld"><label>Always dial this number instead of the counterparty's</label>
        <input type="text" id="s-override" value="${esc(s.demo_override_number || "")}" placeholder="+1 555 000 0000">
        <p class="hint">Set this before any live demo. Leave blank in production.</p></div>
      <div class="fld"><label>Never call</label>
        <select id="s-dnc" multiple size="6">${cps.map((c) =>
          `<option value="${esc(c.id)}" ${(s.do_not_call || []).includes(c.id) ? "selected" : ""}>${esc(c.display_name)}</option>`).join("")}</select>
        <p class="hint">Hold cmd to select several. A call to anyone here is refused by the API, not just hidden in the UI.</p></div>
    </div>

    <div class="savebar">
      <button class="btn" id="s-save">Save settings</button>
      <button class="btn2" id="s-reset">Reset to defaults</button>
      <span style="font-size:13px;color:var(--gr2)" id="s-status"></span>
    </div>`;

  $("s-save").onclick = async () => {
    const lines = (id) => $(id).value.split("\n").map((x) => x.trim()).filter(Boolean);
    const patch = {
      company_name: $("s-company").value.trim() || "your company",
      voice_name: $("s-voice").value, tone: $("s-tone").value,
      disclose_ai: $("s-disclose").checked,
      announce_recording: $("s-record").checked,
      approval_threshold_cents: Math.round(Number($("s-threshold").value || 0) * 100),
      payment_window_days: Number($("s-window").value || 21),
      max_instalments: Number($("s-instal").value || 2),
      calls_per_run: Number($("s-calls").value || 5),
      may_agree: lines("s-may"), must_not: lines("s-must"),
      demo_override_number: $("s-override").value.trim(),
      do_not_call: [...$("s-dnc").selectedOptions].map((o) => o.value),
    };
    try {
      await api("/api/settings", { method: "PUT", body: JSON.stringify(patch) });
      $("s-status").textContent = "Saved. The next brief uses these.";
      await loadStatus();
      toast("Settings saved");
    } catch (e) { toast("Could not save: " + e.message); }
  };
  $("s-reset").onclick = async () => {
    await api("/api/settings/reset", { method: "POST" });
    toast("Reset to defaults"); renderSettings();
  };
}

// --- drawer ----------------------------------------------------------------

function closeDrawer() {
  $("drawer").classList.remove("on");
  $("scrim").classList.remove("on");
  if (state.callTimer) { clearInterval(state.callTimer); state.callTimer = null; }
}

async function openDossier(id) {
  const cp = await api(`/api/counterparties/${id}`);
  const initials = cp.display_name.split(/\s+/).slice(0, 2).map((w) => w[0]).join("").toUpperCase();
  const open = (cp.invoices || []).filter((i) => i.open);

  $("drawer").innerHTML = `
    <div class="dhd">
      <div style="display:flex;gap:15px">
        <div class="sq" style="width:46px;height:46px;border-radius:11px;background:var(--mint-l);color:var(--mint-t);font-size:15px">${esc(initials)}</div>
        <div>
          <div style="display:flex;align-items:center;gap:11px">
            <h2 style="margin:0;font-size:22px;font-weight:500;letter-spacing:-.027em">${esc(cp.display_name)}</h2>
            <span class="bd ${esc(cp.posture)}">${cp.posture[0].toUpperCase() + cp.posture.slice(1)}</span>
          </div>
          <p class="sub">${esc([cp.domain, cp.sector].filter(Boolean).join(" · ") || "no public profile resolved")}</p>
        </div>
      </div>
      <div style="display:flex;gap:10px">
        <button class="btn2" id="closeDrawer">Close</button>
        ${cp.posture !== "watch" ? `<button class="btn" id="briefBtn">Review call</button>` : ""}
      </div>
    </div>
    <div class="dbody">
      <div>
        <p class="lbl">Signals</p>
        ${(cp.signals || []).length ? cp.signals.map((s) => `
          <div class="sgrow">
            <span class="sd ${esc(s.severity)}" style="margin-top:7px"></span>
            <div><p style="margin:0 0 3px;font-size:15px">${esc(s.title)}</p>
            <p style="margin:0;font-size:14px;color:var(--gr);line-height:1.5">${esc(s.detail)}</p>
            ${s.source_url ? `<p class="src">${esc(s.source_url)}</p>` : ""}</div>
          </div>`).join("")
          : `<p style="color:var(--gr2);font-size:14px">Nothing surfaced. ${state.status?.services.tavily.live ? "" : "Tavily is stubbed, so this is expected."}</p>`}
        <p class="lbl" style="margin-top:22px">Ledger names merged</p>
        <p style="margin:0;font-size:14px;color:var(--gr);line-height:1.6">${esc((cp.aliases || []).join(" · "))}</p>
        ${cp.resolution_note ? `<p style="margin:8px 0 0;font-size:13px;color:var(--gr2)">${esc(cp.resolution_note)}</p>` : ""}
      </div>
      <div>
        <p class="lbl">Exposure</p>
        <div class="kv"><span>Open invoices</span><span>${cp.open_invoices}</span></div>
        <div class="kv"><span>Outstanding</span><span style="font-weight:500">${money(cp.outstanding)}</span></div>
        <div class="kv"><span>Oldest</span><span${cp.oldest_days > 60 ? ' style="color:var(--red-t)"' : ""}>${cp.oldest_days ? cp.oldest_days + " days" : "—"}</span></div>
        <div class="kv"><span>Share of all AR</span><span>${Math.round((cp.ar_share || 0) * 100)}%</span></div>
        <div class="kv"><span>Money in</span><span>${money(cp.money_in)}</span></div>
        <div class="kv"><span>Money out</span><span>${money(cp.money_out)}</span></div>
        ${cp.recurring ? `<div class="kv"><span>Looks recurring</span><span>${money(cp.monthly_spend)} /mo</span></div>` : ""}
        ${open.length ? `<p class="lbl" style="margin-top:22px">Open invoices</p>${open.map((i) => `
          <div class="card" style="padding:13px 15px;margin-bottom:9px">
            <div style="display:flex;justify-content:space-between"><span>${esc(i.number)}</span><span style="font-weight:500">${money(i.total)}</span></div>
            <p style="margin:5px 0 0;font-size:12px;color:${i.days_overdue > 0 ? "var(--red-t)" : "var(--gr2)"}">${i.days_overdue > 0 ? i.days_overdue + " days overdue" : "due " + esc(i.due_date)}</p>
          </div>`).join("")}` : ""}
        ${cp.contact_email ? `<p class="lbl" style="margin-top:22px">Contact</p><p style="margin:0;font-size:14px">${esc(cp.contact_email)}</p>` : ""}
      </div>
    </div>`;

  $("drawer").classList.add("on");
  $("scrim").classList.add("on");
  $("closeDrawer").onclick = closeDrawer;
  const bb = $("briefBtn");
  if (bb) bb.onclick = () => openBrief(cp);
}

async function openBrief(cp) {
  $("drawer").innerHTML = `<div class="dhd"><div>
      <h2 style="margin:0;font-size:22px;font-weight:500;letter-spacing:-.027em">Call briefing</h2>
      <p class="sub">${esc(cp.display_name)}</p></div>
      <button class="btn2" id="closeDrawer">Close</button></div>
    <div style="padding:40px;text-align:center;color:var(--gr2)">Writing the brief…</div>`;
  $("closeDrawer").onclick = closeDrawer;

  const brief = await api(`/api/counterparties/${cp.id}/brief`, { method: "POST" });
  const list = (arr, colour) => (arr || []).map((x) =>
    `<div class="rule"><span class="sd ${colour}" style="margin-top:7px"></span><span>${esc(x)}</span></div>`).join("");

  $("drawer").innerHTML = `
    <div class="dhd">
      <div><h2 style="margin:0;font-size:22px;font-weight:500;letter-spacing:-.027em">Call briefing</h2>
      <p class="sub">${esc(cp.display_name)} · ${money(cp.outstanding)} outstanding</p></div>
      <button class="btn2" id="closeDrawer">Close</button>
    </div>
    <div style="padding:22px 30px">
      ${brief.needs_approval ? `<div class="warnbox"><strong style="font-weight:500">Above your approval threshold.</strong> A human has to approve this one before it dials.</div>` : ""}
      <div class="card"><p class="lbl">Opening line</p>
        <p style="margin:0;font-size:15px;line-height:1.6">${esc(brief.opening_line)}</p></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
        <div class="card"><p class="lbl">Authorised to agree</p>${list(brief.may_agree, "positive")}</div>
        <div class="card"><p class="lbl">Must not</p>${list(brief.must_not, "severe")}</div>
      </div>
      <div class="card"><p class="lbl">Context the agent may rely on</p>${list(brief.context, "info")}</div>
      <div style="display:flex;align-items:center;gap:12px;margin-top:6px">
        <span style="font-size:13px;color:var(--gr2)">${state.status?.services.voice.live ? "Will dial through ElevenLabs" : "Voice is not configured, so this will run as a simulated call"}</span>
        <div style="flex-grow:1"></div>
        <button class="btn2" id="dialBtn">${brief.needs_approval ? "Approve and simulate" : "Simulate call"}</button>
        <button class="btn" id="talkBtn">Talk to the agent</button>
      </div>
    </div>`;
  $("closeDrawer").onclick = closeDrawer;
  $("dialBtn").onclick = () => startCall(cp, brief);
  $("talkBtn").onclick = () => startVoice(cp, brief);
}

// --- browser voice ---------------------------------------------------------
// The judge talks to the agent through the laptop. No phone number involved.

let voiceConv = null;

async function startVoice(cp, brief) {
  let session;
  try {
    session = await api("/api/voice/session", {
      method: "POST",
      body: JSON.stringify({ counterparty_id: cp.id, brief, approved_by: "Mike Spara" }),
    });
  } catch (e) { toast("Could not start: " + e.message); return; }

  if (!session.available) {
    $("drawer").innerHTML = `
      <div class="dhd"><div><h2 style="margin:0;font-size:22px;font-weight:500;letter-spacing:-.027em">Voice not configured</h2>
        <p class="sub">${esc(cp.display_name)}</p></div>
        <button class="btn2" id="closeDrawer">Close</button></div>
      <div style="padding:22px 30px">
        <div class="card"><p style="margin:0 0 10px;font-size:15px">Set these two, restart, and this button opens a real conversation:</p>
          <div class="tx" style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px">ELEVENLABS_API_KEY=…<br>ELEVENLABS_AGENT_ID=…</div>
          <p class="hint" style="margin-top:12px">Nothing else is needed. No phone number, no Twilio, no public URL.</p></div>
        <button class="btn" id="simInstead">Run the simulated call instead</button>
      </div>`;
    $("closeDrawer").onclick = closeDrawer;
    $("simInstead").onclick = () => startCall(cp, brief);
    return;
  }

  const turns = [];
  let mode = "connecting";

  const paint = (status, ended) => {
    const body = turns.map((t) => t.role === "tool"
      ? `<div class="tool">${esc(t.text)}</div>`
      : `<div class="turn"><div class="tav ${t.role}">${t.role === "agent" ? "RD" : "··"}</div>
         <div><p class="who">${t.role === "agent" ? "Rho Desk" : esc(cp.display_name)}</p>
         <p class="say">${esc(t.text)}</p></div></div>`).join("");
    $("drawer").innerHTML = `
      <div class="dhd">
        <div><h2 style="margin:0;font-size:22px;font-weight:500;letter-spacing:-.027em">${ended ? "Conversation ended" : "Talking to"} ${esc(cp.display_name)}</h2>
        <p class="sub">Browser voice · speak into your microphone</p></div>
        ${ended ? `<button class="btn2" id="closeDrawer">Close</button>` : ""}
      </div>
      <div style="padding:22px 30px">
        <div class="card" style="display:flex;align-items:center;gap:14px">
          <div class="orb ${mode}"><div class="wave"><i></i><i></i><i></i><i></i></div></div>
          <div style="flex-grow:1"><p style="margin:0;font-size:15px">${esc(status)}</p>
            <p class="vstat">${turns.length} turn${turns.length === 1 ? "" : "s"}</p></div>
          ${ended ? "" : `<button class="btn2" id="endBtn">End conversation</button>`}
        </div>
        <div class="tx">${body || '<p style="color:var(--gr2);margin:0">Waiting for the agent to speak…</p>'}</div>
        ${ended ? `<div style="display:flex;gap:10px;margin-top:14px"><div style="flex-grow:1"></div>
          <button class="btn2" id="backBtn">Back to counterparty</button></div>` : ""}
      </div>`;
    if (ended) {
      $("closeDrawer").onclick = closeDrawer;
      $("backBtn").onclick = () => openDossier(cp.id);
    } else {
      $("endBtn").onclick = () => voiceConv && voiceConv.endSession();
    }
  };

  $("drawer").classList.add("on");
  $("scrim").classList.add("on");
  paint("Connecting…", false);

  try {
    await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch {
    paint("Microphone blocked. Allow access and try again.", true);
    return;
  }

  let Conversation;
  try {
    ({ Conversation } = await import("https://cdn.jsdelivr.net/npm/@elevenlabs/client/+esm"));
  } catch (e) {
    paint("Could not load the ElevenLabs SDK: " + e.message, true);
    return;
  }

  const push = (role, text) => {
    if (!text) return;
    turns.push({ role, text });
    paint(mode === "speaking" ? "Agent speaking" : "Listening", false);
    api(`/api/calls/${session.call_id}/transcript`, {
      method: "POST", body: JSON.stringify({ transcript: turns }),
    }).catch(() => {});
  };

  try {
    voiceConv = await Conversation.startSession({
      ...(session.signed_url ? { signedUrl: session.signed_url }
                             : { agentId: session.agent_id }),
      dynamicVariables: session.dynamic_variables,
      // A CLIENT tool, run here in the page rather than on ElevenLabs'
      // servers. That matters: a server tool would need this app reachable
      // from the public internet (ngrok, a tunnel, a deploy), and a client
      // tool needs none of that. It also means counterparty_id comes from
      // the session we opened rather than from the model, so the agent
      // cannot look up somebody else's invoice.
      clientTools: {
        get_invoice_details: async ({ invoice_number }) => {
          const label = invoice_number || "open invoices";
          turns.push({ role: "tool", text: `get_invoice_details · ${label}` });
          paint(mode === "speaking" ? "Agent speaking" : "Looking up " + label, false);
          try {
            const r = await api("/api/tools/invoice", {
              method: "POST",
              body: JSON.stringify({ counterparty_id: cp.id, invoice_number }),
            });
            return JSON.stringify(r);
          } catch (e) {
            return JSON.stringify({ found: false, error: "lookup failed" });
          }
        },
      },
      onConnect: () => { mode = "listening"; paint("Connected. Say hello.", false); },
      onModeChange: ({ mode: m }) => {
        mode = m === "speaking" ? "speaking" : "listening";
        paint(mode === "speaking" ? "Agent speaking" : "Listening", false);
      },
      onMessage: ({ message, source }) => push(source === "user" ? "human" : "agent", message),
      onError: (err) => paint("Error: " + (err?.message || err), true),
      onDisconnect: async () => {
        mode = "connecting";
        paint("Writing up the conversation…", true);
        try {
          const r = await api(`/api/calls/${session.call_id}/finish`, {
            method: "POST", body: JSON.stringify({ transcript: turns }),
          });
          toast(r.outcome?.summary || "Call logged");
        } catch { toast("Call ended, but the write-up failed"); }
        paint("Conversation ended", true);
        voiceConv = null;
      },
    });
  } catch (e) {
    paint("Could not start the conversation: " + e.message, true);
  }
}

async function startCall(cp, brief) {
  let res;
  try {
    res = await api("/api/calls", {
      method: "POST",
      body: JSON.stringify({ counterparty_id: cp.id, brief, approved_by: "Mike Spara" }),
    });
  } catch (e) { toast("Could not start the call: " + e.message); return; }
  if (res.provider_error) toast("ElevenLabs refused, falling back to simulation");
  pollCall(res.call_id, cp);
}

function pollCall(callId, cp) {
  const draw = (call) => {
    const turns = (call.transcript || []).map((t) => t.role === "tool"
      ? `<div class="tool">${esc(t.text)}</div>`
      : `<div class="turn"><div class="tav ${t.role}">${t.role === "agent" ? "RD" : "··"}</div>
         <div><p class="who">${t.role === "agent" ? "Rho Desk" : esc(cp.display_name)}</p>
         <p class="say">${esc(t.text)}</p></div></div>`).join("");
    const done = call.state === "done";
    const oc = call.outcome || {};
    $("drawer").innerHTML = `
      <div class="dhd">
        <div><h2 style="margin:0;font-size:22px;font-weight:500;letter-spacing:-.027em">${done ? "Call complete" : "Calling"} ${esc(cp.display_name)}</h2>
        <p class="sub">${esc(call.to_number || "no number on file")} ${call.simulated ? "· simulated" : "· ElevenLabs"}</p></div>
        ${done ? `<button class="btn2" id="closeDrawer">Close</button>`
               : `<div class="live"><span class="rec"></span>Live ${call.elapsed_seconds || 0}s</div>`}
      </div>
      <div style="padding:22px 30px">
        ${done && oc.summary ? `<div class="banner"><p style="margin:0;font-size:12px;color:var(--mint-t);letter-spacing:.05em;text-transform:uppercase">Outcome</p>
          <p style="margin:6px 0 0;font-size:16px">${esc(oc.summary)}</p>
          ${(oc.commitments || []).length ? `<div style="margin-top:10px">${(oc.commitments || []).map((c) =>
            `<div class="kv" style="border-color:rgba(8,166,138,.2)"><span>${esc(c.label)}</span><span>${esc(c.value)}</span></div>`).join("")}</div>` : ""}
        </div>` : ""}
        <div class="call">${turns || '<p style="color:var(--gr2);margin:0">Connecting…</p>'}</div>
        ${done ? `<div style="display:flex;gap:10px;margin-top:14px"><div style="flex-grow:1"></div>
          <button class="btn2" id="backBtn">Back to counterparty</button></div>` : ""}
      </div>`;
    if (done) {
      clearInterval(state.callTimer); state.callTimer = null;
      $("closeDrawer").onclick = closeDrawer;
      $("backBtn").onclick = () => openDossier(cp.id);
    }
  };

  $("drawer").classList.add("on");
  $("scrim").classList.add("on");
  if (state.callTimer) clearInterval(state.callTimer);
  const tick = async () => { try { draw(await api(`/api/calls/${callId}`)); } catch (e) { /* keep polling */ } };
  tick();
  state.callTimer = setInterval(tick, 1200);
}

// --- wiring ----------------------------------------------------------------

document.addEventListener("click", (e) => {
  const nav = e.target.closest(".nv");
  if (nav) {
    document.querySelectorAll(".nv").forEach((b) => b.classList.remove("on"));
    nav.classList.add("on");
    state.view = nav.dataset.view;
    render();
    return;
  }
  const runPill = e.target.closest("[data-run]");
  if (runPill) { state.runId = Number(runPill.dataset.run); renderChanges(); return; }
  const chRow = e.target.closest(".chrow[data-id]");
  if (chRow) { openDossier(chRow.dataset.id); return; }
  const pill = e.target.closest("[data-posture]");
  if (pill) { state.posture = pill.dataset.posture; renderCounterparties(); return; }
  const callBtn = e.target.closest("[data-call]");
  if (callBtn) {
    e.stopPropagation();
    api(`/api/counterparties/${callBtn.dataset.call}`).then(openBrief);
    return;
  }
  const exp = e.target.closest("[data-expand]");
  if (exp) {
    const box = $("tx-" + exp.dataset.expand);
    if (box) box.style.display = box.style.display === "none" ? "block" : "none";
    return;
  }
  const row = e.target.closest("tr[data-id]");
  if (row) openDossier(row.dataset.id);
});

$("scrim").onclick = closeDrawer;
$("runBtn").onclick = runDesk;
$("pingBtn").onclick = async () => {
  try {
    const p = await api("/api/rho/ping");
    toast(`Rho reachable: ${p.accounts} accounts, ${money(p.total_balance_cents)} total`);
  } catch (e) { toast("Rho unreachable: " + e.message); }
};

loadStatus().then(render);
