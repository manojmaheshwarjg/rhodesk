const $ = (id) => document.getElementById(id);
const money = (c) => "$" + ((c || 0) / 100).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const trim = (s, n) => { s = String(s ?? ""); if (s.length <= n) return s; const cut = s.slice(0, n); const sp = cut.lastIndexOf(" "); return (sp > n * 0.6 ? cut.slice(0, sp) : cut) + "…"; };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));

let state = { view: "collect", posture: "all", rows: [], status: null, callTimer: null, runId: null };

async function api(path, opts) {
  const res = await fetch(path, { headers: { "Content-Type": "application/json" }, ...opts });
  if (!res.ok) throw new Error((await res.text()).slice(0, 300));
  return res.json();
}

// Which services are connected is an operator's question, not something the
// chrome should announce on every screen. It lives in Agent settings.
function servicesHtml(svc) {
  return [
    ["Rho", true, svc.rho.note, ""],
    ["Tavily", svc.tavily.live, svc.tavily.live ? "live" : "offline mode", svc.tavily.last_error],
    ["Model", svc.llm.live, svc.llm.live ? `${svc.llm.provider} · ${svc.llm.model}` : "rules only", svc.llm.last_error],
    ["Voice", svc.voice.live, svc.voice.live ? `ElevenLabs · ${svc.voice.telephony || "browser"}` : "not configured", svc.voice.last_error],
  ].map(([n, on, note, err]) =>
    `<div title="${esc(err || "")}"><span class="led ${on ? "on" : "off"}"></span>${n}<span>${esc(err ? "failing" : note)}</span></div>`
  ).join("");
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
  // The portal builds the org monogram from word initials, so "Acme, Inc" is
  // AI. Split on spaces and on camel case so "FusionTech" is FT, not FU.
  const words = svc.company.replace(/([a-z])([A-Z])/g, "$1 $2").split(/[^A-Za-z]+/).filter(Boolean);
  $("orgInitials").textContent = (words.length > 1
    ? words[0][0] + words[1][0]
    : svc.company.slice(0, 2)).toUpperCase();
  if (s.counts.counterparties) $("lastRun").textContent = `${s.counts.counterparties} counterparties`;
}

// --- notifications ---------------------------------------------------------

async function loadNotifications() {
  const d = await api("/api/notifications");
  state.notif = d;
  const badge = $("bellCount");
  badge.textContent = d.unread;
  badge.hidden = !d.unread;
  const next = new Date(d.schedule.next_due);
  $("notifs").innerHTML = `
    <div class="nh">Research runs daily at ${String(d.schedule.hour).padStart(2, "0")}:00.
      Next ${next.toLocaleString(undefined, { weekday: "short", hour: "numeric", minute: "2-digit" })}.</div>
    ${d.notifications.length
      ? d.notifications.map((n) => `
        <div class="nrow ${n.read_at ? "" : "unread"}">
          <h5>${esc(n.title)}</h5>
          ${n.detail ? `<p>${esc(n.detail)}</p>` : ""}
          <time>${new Date(n.at).toLocaleString(undefined, { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })}</time>
        </div>`).join("")
      : `<div class="nrow"><p>Nothing yet. The next scheduled run will report here.</p></div>`}`;
  return d;
}

async function toggleNotifications() {
  const panel = $("notifs");
  const opening = !panel.classList.contains("on");
  panel.classList.toggle("on", opening);
  if (opening) {
    await loadNotifications();
    await api("/api/notifications/read", { method: "POST" });
    $("bellCount").hidden = true;
  }
}

// --- run -------------------------------------------------------------------

// "Run workflow" was CI jargon on a finance screen, and it never said how many
// people were about to be phoned. The label now states both.
function setRunButton(tab, ready) {
  const btn = $("runBtn");
  btn.hidden = false;
  btn.disabled = !ready;
  const noun = tab === "collect"
    ? (ready === 1 ? "account" : "accounts")
    : (ready === 1 ? "vendor" : "vendors");
  btn.textContent = ready ? `Call ${ready} ${noun}` : "Nobody ready to call";
}


// A live call is the product's headline moment, so it gets the middle of the
// screen rather than a progress strip. The shell is built once and then
// patched, so the orb keeps its animation instead of restarting every tick.
const CALL = { timer: null, mode: null, ids: [], cp: null, turns: -1, orbs: [], gen: 0 };

const callSecs = (call) => {
  if (!call.created_at) return 0;
  const end = call.ended_at ? new Date(call.ended_at) : new Date();
  return Math.max(0, Math.round((end - new Date(call.created_at)) / 1000));
};
const MMSS = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

// Who holds the floor. There are no audio levels to read, so the role of the
// last thing said is the only honest signal.
function speakerOf(call) {
  if (call.state === "done") return "done";
  if (call.state === "wrapping") return "wrapping";
  const t = (call.transcript || []).filter((x) => x.role !== "tool");
  if (t.length) return t[t.length - 1].role;
  // Answered but nobody transcribed yet. Ringing and connected look identical
  // without this, which is why a live call sat on "Dialing" for two minutes.
  return call.connected_at ? "connected" : "dialing";
}

// The dial animation: a rotating point cloud, drawn in the same mint to
// periwinkle to orchid gradient the "Researched by Rhonica" band already
// uses, so the agent reads as part of this product and not a borrowed widget.
const ORB_STOPS = [[10, 205, 172], [124, 152, 246], [196, 132, 240]];
const ORB_GRAY = [152, 160, 156];
const mixc = (x, y, t) => [x[0] + (y[0] - x[0]) * t, x[1] + (y[1] - x[1]) * t, x[2] + (y[2] - x[2]) * t];

function gradAt(t) {
  const n = ORB_STOPS.length - 1;
  const i = Math.min(n - 1, Math.floor(t * n));
  return mixc(ORB_STOPS[i], ORB_STOPS[i + 1], t * n - i);
}

// How alive the sphere looks per state: how hard it breathes, how fast it
// turns, how far its colour sits from grey, and how slow each breath is.
// Listening stays lit, so she reads as attentive rather than switched off.
// Resting breathes slowly, the way something asleep does.
const ORB_GAIN = { dialing: 0.22, connected: 0.6, agent: 1, human: 0.35, wrapping: 0.3, done: 0.18 };
const ORB_SPIN = { dialing: 0.0024, connected: 0.0042, agent: 0.0060, human: 0.0030, wrapping: 0.0090, done: 0.0008 };
const ORB_LIT  = { dialing: 0.45, connected: 0.85, agent: 1, human: 0.62, wrapping: 0.6, done: 0.7 };
const ORB_PACE = { dialing: 300, connected: 340, agent: 260, human: 420, wrapping: 220, done: 950 };

function makeOrb(canvas, size) {
  const ctx = canvas.getContext("2d");
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = size * dpr;
  canvas.height = size * dpr;

  // Fibonacci lattice, so points sit evenly instead of bunching at the poles.
  const n = Math.round(size * 9);
  const pts = [];
  const golden = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < n; i++) {
    const y = 1 - (i / (n - 1)) * 2;
    const r = Math.sqrt(Math.max(0, 1 - y * y));
    pts.push([Math.cos(golden * i) * r, y, Math.sin(golden * i) * r]);
  }

  const orb = { mode: "dialing", rot: 0, lit: 0.45, gain: 0.22, spin: 0.0024, phase: 0, last: 0, raf: 0 };
  const frame = (ms) => {
    // Every quality eases toward its target, so a change of state glides
    // instead of snapping, and the breath keeps its place when its pace changes.
    const m = orb.mode;
    const dt = orb.last ? Math.min(ms - orb.last, 64) : 16;
    orb.last = ms;
    orb.spin += (ORB_SPIN[m] - orb.spin) * 0.05;
    orb.gain += (ORB_GAIN[m] - orb.gain) * 0.05;
    orb.lit += (ORB_LIT[m] - orb.lit) * 0.05;
    orb.rot += orb.spin;
    orb.phase += dt / ORB_PACE[m];
    const breathe = (Math.sin(orb.phase) * 0.5 + 0.5) * orb.gain;
    const R = canvas.width * 0.37 * (1 + breathe * 0.09);
    const cx = canvas.width / 2, cy = canvas.height / 2;
    const cos = Math.cos(orb.rot), sin = Math.sin(orb.rot);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i];
      const x = p[0] * cos - p[2] * sin;
      const z = p[0] * sin + p[2] * cos;
      const depth = (z + 1) / 2;                  // 0 at the back, 1 at the front
      const c = mixc(ORB_GRAY, gradAt((x + 1) / 2), orb.lit);
      ctx.globalAlpha = 0.2 + depth * 0.78;
      ctx.fillStyle = `rgb(${c[0] | 0},${c[1] | 0},${c[2] | 0})`;
      ctx.beginPath();
      ctx.arc(cx + x * R, cy + p[1] * R, (0.4 + depth * 1.15) * dpr, 0, 6.283185);
      ctx.fill();
    }
    orb.raf = requestAnimationFrame(frame);
  };
  orb.raf = requestAnimationFrame(frame);
  canvas._orb = orb;
  CALL.orbs.push(orb);
  return orb;
}

function stopOrbs() {
  CALL.orbs.forEach((o) => cancelAnimationFrame(o.raf));
  CALL.orbs = [];
}

// What Rhonica is doing, in her own words, under the orb. "busy" marks the
// states that take a moment, which get animated dots.
function captionOf(call) {
  switch (speakerOf(call)) {
    case "agent": return { text: "Rhonica is talking" };
    case "human": return { text: "Rhonica is listening" };
    case "connected": return { text: "Rhonica is on the line" };
    case "wrapping": return { text: "Rhonica is writing the summary", busy: true };
    case "done": return { text: "Rhonica is resting" };
    default: return { text: "Rhonica is dialing", busy: true };
  }
}

// A batch tile has no outcome banner, so a finished tile shows the result.
function statusOf(call) {
  if (call.state === "done") return (RESULT[(call.outcome || {}).result] || { label: "Call complete" }).label;
  const { text, busy } = captionOf(call);
  return busy ? `${text}\u2026` : text;
}

// Crossfades the caption only when it actually changes, since the poll
// rewrites it every second.
function setCaption(el, call) {
  const { text, busy } = captionOf(call);
  const key = busy ? `${text}\u2026` : text;
  if (el.dataset.key === key) return;
  el.dataset.key = key;
  const html = esc(text) + (busy ? '<span class="cmdots"><i>.</i><i>.</i><i>.</i></span>' : "");
  el.classList.add("swap");
  setTimeout(() => { el.innerHTML = html; el.classList.remove("swap"); }, 160);
}

function paintOrb(el, call) {
  if (el && el._orb) el._orb.mode = speakerOf(call);
}

// --- review, before anything dials ----------------------------------------
// Nothing rings until it is confirmed here. The modal opens on this stage, the
// operator sees who is about to be called and why, and only then does it dial.

function openModal(wide) {
  stopOrbs();
  $("cmodal").classList.toggle("wide", !!wide);
  $("cmodal").classList.add("on");
  $("cscrim").classList.add("on");
  $("cdock").hidden = true;
}

const ruleList = (arr, colour) => (arr || []).map((x) =>
  `<div class="rule"><span class="sd ${colour}" style="margin-top:7px"></span><span>${esc(x)}</span></div>`).join("");

// What this call is for, composed from the row rather than written by a model,
// so the review can never say something the board does not. The opening line
// lives in the brief the agent gets; the operator needs the objective.
function callFocus(cp) {
  const owed = cp.outstanding || 0;
  if (owed > 0) {
    const n = cp.open_invoices || 0;
    const out = [`Agree a payment date for ${money(owed)}${n > 1 ? ` across ${n} invoices` : ""}.`];
    if (cp.oldest_days) out.push(`The oldest is ${cp.oldest_days} days past due.`);
    if (cp.verdict === "escalate") out.push("Settle terms before the other creditors do.");
    return out.join(" ");
  }
  const per = money(cp.monthly_spend || 0);
  if (cp.duplicate) return `Cancel the duplicate subscription and recover ${per} a month.`;
  return `Move ${per} a month onto better terms, or cancel it.`;
}

async function reviewCall(cp) {
  openModal(false);
  $("cmodal").innerHTML = `
    <div class="chd"><div><h2 class="ctitle">${esc(cp.display_name)}</h2>
      <p class="creason">Writing the brief\u2026</p></div></div>
    <div class="cbody"><p class="empty">One moment.</p></div>`;

  let brief, cfg;
  try {
    [brief, cfg] = await Promise.all([
      api(`/api/counterparties/${cp.id}/brief`, { method: "POST" }),
      api("/api/settings"),
    ]);
  } catch (e) { toast("Could not write the brief: " + e.message); closeCallModal(); return; }

  // Same precedence _place_call uses, so the review shows the number that
  // will actually ring rather than the one on the counterparty record.
  const dialing = cfg.demo_override_number || cp.contact_phone || "";

  $("cmodal").innerHTML = `
    <div class="chd">
      <div>
        <h2 class="ctitle">Call ${esc(cp.display_name)}?</h2>
        <p class="creason">${esc(cp.verdict_reason || cp.rationale || "")}</p>
      </div>
      <button class="btn2" id="cmCancel" style="flex-shrink:0">Cancel</button>
    </div>
    <div class="cbody">
      ${brief.needs_approval ? `<div class="warnbox">
        <strong style="font-weight:500">Above your approval threshold.</strong> Calling from here is the approval.</div>` : ""}
      <div class="card"><p class="lbl">Objective</p>
        <p style="margin:0;font-size:15px;line-height:1.6">${esc(callFocus(cp))}</p></div>
      <div class="cols2">
        <div class="card"><p class="lbl">May agree to</p>${ruleList(brief.may_agree, "positive")}</div>
        <div class="card"><p class="lbl">Must not</p>${ruleList(brief.must_not, "severe")}</div>
      </div>
      <div class="cfoot">
        <span class="cnum">${dialing ? "Dials " + esc(dialing) : "No number on file"}</span>
        <div style="flex-grow:1"></div>
        <button class="btn2" id="cmTalk">Talk to the agent</button>
        <button class="btn" id="cmDial">Call now</button>
      </div>
    </div>`;
  $("cmCancel").onclick = closeCallModal;
  $("cmDial").onclick = () => startCall(cp, brief);
  // Browser voice still paints into the drawer, so hand the screen over to it.
  $("cmTalk").onclick = () => { closeCallModal(); startVoice(cp, brief); };
}

async function reviewBatch(tab) {
  openModal(true);
  const noun = tab === "cut" ? "vendors" : "accounts";
  $("cmodal").innerHTML = `<div class="chd"><div><h2 class="ctitle">Reading the queue\u2026</h2></div></div>
    <div class="cbody"><p class="empty">One moment.</p></div>`;

  let rows;
  try {
    const d = await api("/api/board");
    rows = (tab === "cut" ? d.cut : d.collect).filter((r) => r.ready);
  } catch (e) { toast("Could not read the queue: " + e.message); closeCallModal(); return; }

  if (!rows.length) { toast("Nothing on this tab is ready to call."); closeCallModal(); return; }

  $("cmodal").innerHTML = `
    <div class="chd">
      <div>
        <h2 class="ctitle">Call ${rows.length} ${rows.length === 1 ? noun.slice(0, -1) : noun}?</h2>
        <p class="creason">Nothing rings until you confirm. Rhonica works them in this order.</p>
      </div>
      <button class="btn2" id="cmCancel" style="flex-shrink:0">Cancel</button>
    </div>
    <div class="cbody">
      <div class="qlist">${rows.map((r, i) => `
        <div class="qitem">
          <span class="qnum">${i + 1}</span>
          <div>
            <p class="qname">${esc(r.display_name)}
              <span class="qamt">${esc(tab === "cut" ? money(r.monthly_spend) + " a month" : money(r.outstanding) + " outstanding")}</span></p>
            <p class="qwhy">${esc(r.verdict_reason || r.note || "")}</p>
          </div>
        </div>`).join("")}</div>
      <div class="cfoot">
        <div style="flex-grow:1"></div>
        <button class="btn" id="cmDial">Call ${rows.length} ${rows.length === 1 ? noun.slice(0, -1) : noun}</button>
      </div>
    </div>`;
  $("cmCancel").onclick = closeCallModal;
  $("cmDial").onclick = () => dialBatch(tab);
}

async function dialBatch(tab) {
  const btn = $("cmDial");
  btn.disabled = true;
  btn.textContent = "Placing calls\u2026";
  let started;
  try { started = await api("/api/workflow", { method: "POST", body: JSON.stringify({ tab }) }); }
  catch (e) { toast("Could not start: " + e.message); closeCallModal(); return; }
  if (!started.started) { toast("Nothing on this tab is ready to call."); closeCallModal(); return; }

  const seeds = started.calls.map((c) => ({ id: c.call_id, counterparty_name: c.display_name }));
  batchShell(seeds, tab === "cut" ? "vendors" : "accounts");
  watchCalls(started.calls.map((c) => c.call_id), "batch");
}

// --- timeline --------------------------------------------------------------
// Every real call to one counterparty, newest first. The same history is what
// Rhonica is given before her next call, so the note under it is literal.

async function openTimeline(cpId) {
  // The modal is shared, so opening this over a watched call would tear it down.
  if (CALL.timer) { toast("Rhonica is on a call. The timeline opens once it ends."); return; }
  openModal(false);
  $("cmodal").innerHTML = `
    <div class="chd"><div><h2 class="ctitle">Timeline</h2>
      <p class="creason">Reading the call history\u2026</p></div></div>
    <div class="cbody"><p class="empty">One moment.</p></div>`;

  let d;
  try { d = await api(`/api/counterparties/${cpId}/calls`); }
  catch (e) { toast("Could not load the timeline: " + e.message); closeCallModal(); return; }

  const calls = d.calls || [];
  $("cmodal").innerHTML = `
    <div class="chd">
      <div>
        <h2 class="ctitle">${esc(d.display_name)}</h2>
        <p class="creason">${calls.length
          ? `${calls.length} call${calls.length === 1 ? "" : "s"} \u00b7 the last one ${esc(AGO(calls[0].at))}`
          : "No calls yet"}</p>
      </div>
      <button class="btn2" id="cmCancel" style="flex-shrink:0">Close</button>
    </div>
    <div class="cbody">
      ${calls.length
        ? `<ol class="tlist">${calls.map(timelineItem).join("")}</ol>`
        : '<p class="empty">Rhonica has not called them yet.</p>'}
      <p class="tlnote">Rhonica reads this history before every call, so a follow-up picks up where the last one left off.</p>
    </div>`;
  $("cmCancel").onclick = closeCallModal;
}

function timelineItem(c) {
  const res = RESULT[c.result];
  const label = c.state === "wrapping" ? "Writing the summary\u2026"
    : c.state !== "done" ? "On a call now"
    : res ? res.label : (c.result ? humanKey(c.result) : "Completed");
  const tone = c.state !== "done" ? "live" : (res && res.tone) || "plain";
  const when = new Date(c.at).toLocaleString(undefined,
    { weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" });
  const took = c.state === "done" && c.duration_secs != null ? ` \u00b7 ${MMSS(c.duration_secs)}` : "";
  const agreed = (c.commitments || []).filter((x) => x && x.label);
  return `<li class="tlitem">
    <span class="tldot ${esc(tone)}"></span>
    <p class="tlwhen"><span>${esc(when)}${took}</span><span class="tlago">${esc(AGO(c.at))}</span></p>
    <p class="tlres">${esc(label)}</p>
    ${c.summary ? `<p class="tlsum">${esc(c.summary)}</p>` : ""}
    ${agreed.length ? `<p class="tlkv">${agreed.map((x) =>
      `<span>${esc(humanKey(x.label))}: <b>${esc(String(x.value))}</b></span>`).join("")}</p>` : ""}
  </li>`;
}

// --- shells ---------------------------------------------------------------

function singleShell(cp) {
  $("cmodal").classList.remove("wide");
  $("cmodal").innerHTML = `
    <div class="chd">
      <div>
        <h2 class="ctitle">${esc(cp.display_name)}</h2>
        <p class="creason">${esc(cp.verdict_reason || cp.rationale || cp.note || "")}</p>
      </div>
      <div style="display:flex;gap:10px;flex-shrink:0" id="cmActs"></div>
    </div>
    <div class="cbody">
      <div class="orbwrap">
        <canvas class="corb" id="cmOrb"></canvas>
        <p class="cstate"><span class="cmcap" id="cmStatus" data-key="Rhonica is dialing\u2026">Rhonica is dialing<span class="cmdots"><i>.</i><i>.</i><i>.</i></span></span><span class="t" id="cmTime">0:00</span></p>
      </div>
      <div id="cmOutcome"></div>
      <p class="lbl">Transcript</p>
      <div class="tx" id="cmTx"><p style="color:var(--gr2);margin:0">Connecting\u2026</p></div>
    </div>`;
  stopOrbs();
  makeOrb($("cmOrb"), 132);
}

function batchShell(calls, noun) {
  $("cmodal").classList.add("wide");
  $("cmodal").innerHTML = `
    <div class="chd">
      <div>
        <h2 class="ctitle">Working ${calls.length} ${noun}</h2>
        <p class="creason" id="cmProgress">Placing calls\u2026</p>
      </div>
      <div style="display:flex;gap:10px;flex-shrink:0" id="cmActs"></div>
    </div>
    <div class="cbody">
      <div class="ctiles" id="cmTiles">${calls.map((c) => `
        <div class="ctile" data-tile="${esc(c.id)}">
          <canvas class="corb"></canvas>
          <p class="cname">${esc(c.counterparty_name)}</p>
          <p class="cstat">Rhonica is dialing\u2026</p>
          <p class="ctime">0:00</p>
        </div>`).join("")}</div>
    </div>`;
  stopOrbs();
  $("cmTiles").querySelectorAll("canvas.corb").forEach((c) => makeOrb(c, 74));
}

// --- patches --------------------------------------------------------------

function paintSingle(call, cp) {
  paintOrb($("cmOrb"), call);
  setCaption($("cmStatus"), call);
  $("cmTime").textContent = MMSS(callSecs(call));
  const done = call.state === "done";

  const turns = (call.transcript || []).length;
  if (turns !== CALL.turns) {
    CALL.turns = turns;
    const tx = $("cmTx");
    tx.innerHTML = (call.transcript || []).map((t) => t.role === "tool"
      ? `<div class="tool">${esc(t.text)}</div>`
      : `<div class="turn"><div class="tav ${esc(t.role)}">${t.role === "agent" ? "R" : "\u00b7\u00b7"}</div>
         <div><p class="who">${t.role === "agent" ? "Rhonica" : esc(cp.display_name)}</p>
         <p class="say">${esc(t.text)}</p></div></div>`).join("")
      || '<p style="color:var(--gr2);margin:0">Connecting\u2026</p>';
    tx.scrollTop = tx.scrollHeight;
  }

  const oc = call.outcome || {};
  $("cmOutcome").innerHTML = done && oc.summary
    ? `<div class="banner" style="margin-bottom:16px"><p style="margin:0;font-size:12px;color:var(--mint-t);letter-spacing:.05em;text-transform:uppercase">Outcome${RESULT[oc.result] ? ` \u00b7 ${esc(RESULT[oc.result].label)}` : ""}</p>
       <p style="margin:6px 0 0;font-size:16px">${esc(oc.summary)}</p>
       ${(oc.commitments || []).length ? `<div style="margin-top:10px">${(oc.commitments || []).map((c) =>
         `<div class="kv" style="border-color:rgba(8,166,138,.2)"><span>${esc(humanKey(c.label))}</span><span>${esc(String(c.value))}</span></div>`).join("")}</div>` : ""}
       </div>`
    : "";
  paintActions(done);
}

function paintBatch(calls) {
  const done = calls.filter((c) => c.state === "done").length;
  $("cmProgress").textContent = done === calls.length
    ? `${calls.length} calls complete`
    : `${done} done \u00b7 ${calls.length - done} on a call`;
  calls.forEach((c) => {
    const tile = document.querySelector(`[data-tile="${c.id}"]`);
    if (!tile) return;
    tile.classList.toggle("done", c.state === "done");
    paintOrb(tile.querySelector("canvas"), c);
    tile.querySelector(".cstat").textContent = statusOf(c);
    tile.querySelector(".ctime").textContent = MMSS(callSecs(c));
  });
  paintActions(done === calls.length);
}

function paintActions(done) {
  const acts = $("cmActs");
  const want = done ? "close" : "min";
  if (acts.dataset.mode === want) return;
  acts.dataset.mode = want;
  acts.innerHTML = done
    ? `<button class="btn2" id="cmClose">Close</button>`
    : `<button class="btn2" id="cmMin">Minimize</button>`;
  if (done) $("cmClose").onclick = closeCallModal;
  else $("cmMin").onclick = minimizeCall;
}

// --- open, minimize, close ------------------------------------------------

// One poll a second, and each waits for the previous one to come back, so a
// slow response can never stack requests behind it.
const POLL_MS = 1000;

function watchCalls(ids, mode, cp, noun) {
  closeDrawer();
  CALL.ids = ids; CALL.mode = mode; CALL.cp = cp; CALL.turns = -1;
  if (CALL.timer) clearTimeout(CALL.timer);
  const gen = CALL.gen = CALL.gen + 1;

  const tick = async () => {
    let calls = null;
    try { calls = await Promise.all(ids.map((id) => api(`/api/calls/${id}`))); }
    catch { /* try again next second */ }
    if (CALL.gen !== gen) return;            // closed, or a newer call took over
    if (calls) {
      if (mode === "single") paintSingle(calls[0], cp); else paintBatch(calls);
      paintDock(calls);
      // Stop once every call is written up and ElevenLabs has finished with it
      // too, so a transcript that lands after an early summary gets it redone.
      if (calls.every((c) => c.state === "done" && c.provider_status !== "processing")) {
        CALL.timer = null; render(); return;
      }
    }
    CALL.timer = setTimeout(tick, POLL_MS);
  };

  if (mode === "single") singleShell(cp);
  $("cmodal").classList.add("on");
  $("cscrim").classList.add("on");
  $("cdock").hidden = true;
  tick();
}

function paintDock(calls) {
  if ($("cdock").hidden) return;
  const live = calls.filter((c) => c.state !== "done").length;
  $("cdock").innerHTML = live
    ? `<span class="rec"></span>${live} call${live === 1 ? "" : "s"} in progress`
    : `<span class="rec" style="animation:none;background:var(--mint-d)"></span>Calls complete`;
}

function minimizeCall() {
  $("cmodal").classList.remove("on");
  $("cscrim").classList.remove("on");
  $("cdock").hidden = false;
  $("cdock").innerHTML = `<span class="rec"></span>Call in progress`;
}

function restoreCall() {
  $("cdock").hidden = true;
  $("cmodal").classList.add("on");
  $("cscrim").classList.add("on");
}

function closeCallModal() {
  CALL.gen += 1;
  if (CALL.timer) { clearTimeout(CALL.timer); CALL.timer = null; }
  stopOrbs();
  $("cmodal").classList.remove("on");
  $("cscrim").classList.remove("on");
  $("cdock").hidden = true;
  render();
}

function runWorkflow() {
  reviewBatch(state.view === "cut" ? "cut" : "collect");
}

// --- views -----------------------------------------------------------------

async function render() {
  if (state.view === "collect") return renderBoard("collect");
  if (state.view === "cut") return renderBoard("cut");
  if (state.view === "counterparties") return renderCounterparties();
  if (state.view === "changes") return renderChanges();
  if (state.view === "queue") return renderQueue();
  if (state.view === "signals") return renderSignals();
  if (state.view === "settings") return renderSettings();
  return renderCalls();
}

const CLOCK = (iso) => {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

async function renderToday() {
  $("title").textContent = "Today";
  $("subtitle").textContent = "Reading the desk";
  $("filters").innerHTML = "";
  $("tiles").innerHTML = "";
  $("content").innerHTML = `<div class="empty">Reading the desk…</div>`;

  const d = await api("/api/today");
  $("title").textContent = `${d.greeting}`;
  $("subtitle").textContent = d.headline;

  const w = d.week;
  $("tiles").innerHTML = [
    ["Recovered this week", money(w.recovered), "invoices paid off", "var(--mint-t)"],
    ["Calls made", String(w.calls), `${w.real_calls} on a real line`, "var(--gr)"],
    ["Answered", String(w.answered), w.calls ? `of ${w.calls}` : "none yet", "var(--gr)"],
    ["In the queue", String(d.queue_total), "ranked by expected recovery", "var(--gr)"],
  ].map(([l, v, m, c]) =>
    `<div class="tile"><p class="l">${l}</p><p class="v">${v}</p><p class="m" style="color:${c}">${m}</p></div>`).join("");

  const needs = d.needs_you.length
    ? `<div class="card" style="padding:0">${d.needs_you.map((n) => `
        <div class="ny" ${n.counterparty_id ? `data-call="${esc(n.counterparty_id)}" style="cursor:pointer"` : ""}>
          <span class="flag ${esc(n.weight)}"></span>
          <div style="flex-grow:1;min-width:0">
            <h4>${esc(n.title)}</h4>
            <p>${esc(n.detail)}</p>
          </div>
          ${n.amount ? `<div class="amt">${money(n.amount)}</div>` : ""}
        </div>`).join("")}</div>`
    : `<div class="card"><p class="allgood">Nothing needs a decision from you. The desk has the rest.</p></div>`;

  const handled = d.handled.length
    ? `<div class="card" style="padding:0">${d.handled.map((h) => `
        <div class="tl" ${h.counterparty_id ? `data-open="${esc(h.counterparty_id)}" style="cursor:pointer"` : ""}>
          <span class="pip ${esc(h.kind === "call" ? "made" : h.weight || "")}"></span>
          <div style="flex-grow:1;min-width:0">
            <h5>${esc(h.title)}</h5>
            ${h.detail ? `<p>${esc(trim(h.detail, 180))}</p>` : ""}
          </div>
          <time>${CLOCK(h.at)}</time>
        </div>`).join("")}</div>`
    : `<div class="card"><p class="allgood">Nothing since the last run.</p></div>`;

  const queued = d.queued.length
    ? `<div class="card" style="padding:0">${d.queued.map((q) => `
        <div class="qd" data-call="${esc(q.id)}" style="cursor:pointer">
          <span class="bd ${esc(q.posture)}">${esc(q.posture)}</span>
          <span class="nm">${esc(q.display_name)}</span>
          <span class="v">${money(q.outstanding)}</span>
        </div>`).join("")}</div>`
    : `<div class="card"><p class="allgood">Queue is empty.</p></div>`;

  $("content").innerHTML = `
    <p class="sect">Needs you</p>
    ${needs}
    <div class="two" style="margin-top:22px">
      <div><p class="sect">Handled since the last run</p>${handled}</div>
      <div><p class="sect">Queued next</p>${queued}</div>
    </div>`;
}

const VERDICT_LABEL = { call: "Call", escalate: "Escalate", email: "Email", none: "Leave" };

function citeHtml(r) {
  if (!r.note_source) return "";
  const when = r.note_date ? " · " + new Date(r.note_date).toLocaleDateString(undefined, { day: "numeric", month: "short" }) : "";
  const src = r.note_url
    ? `<a href="${esc(r.note_url)}" target="_blank" rel="noopener">${esc(r.note_source)}</a>`
    : esc(r.note_source);
  return `<p class="cite">${src}${when}</p>`;
}

function outcomeHtml(r) {
  if (!r.last_call) return `<span class="nocall">Not called yet</span>`;
  const c = r.last_call;
  const timeline = `<button class="tlink" data-timeline="${esc(r.id)}">Timeline</button>`;
  if (c.state === "wrapping") return `<span class="outcome"><span class="res" style="color:var(--gr)">Writing the summary\u2026</span>${timeline}</span>`;
  if (c.state !== "done") return `<span class="outcome"><span class="res" style="color:var(--mint-t)">On a call now</span>${timeline}</span>`;
  const label = (RESULT[c.result] || {}).label || c.result || "Completed";
  return `<span class="outcome"><span class="res">${esc(label)}</span>
    ${c.summary ? `<p>${esc(trim(c.summary, 110))}</p>` : ""}${timeline}</span>`;
}

async function renderBoard(which) {
  const collect = which === "collect";
  $("title").textContent = collect ? "AR Collections" : "Spend Recovery";
  $("filters").innerHTML = "";
  $("tiles").innerHTML = "";
  $("content").innerHTML = `<div class="empty">Reading the ledger…</div>`;

  const d = await api("/api/board");
  const rows = collect ? d.collect : d.cut;
  const t = d.totals;

  $("subtitle").innerHTML = collect
    ? `${rows.length} owing you ${money(t.outstanding)}. ${t.ready} queued for this run, ${t.callable} qualified.`
    : `${rows.length} recurring vendors worth ${money(t.monthly_spend)} a month.`;

  // The button names its own blast radius: how many, and what they are.
  // Counted off this tab's own rows. totals.ready only covers collect, so
  // reading it here would have made the vendor button quote the AR number.
  setRunButton(collect ? "collect" : "cut", rows.filter((r) => r.ready).length);

  if (!rows.length) { $("content").innerHTML = `<div class="empty">Nothing here.</div>`; return; }

  // Widths are sized to their own headers. With table-layout:fixed a header
  // wider than its column spills into the next one, which is what made the
  // band look like it overlapped "Days overdue".
  const cols = collect
    ? `<colgroup><col style="width:172px"><col style="width:112px"><col style="width:126px">
        <col><col style="width:180px"><col style="width:132px"><col style="width:98px"></colgroup>`
    : `<colgroup><col style="width:214px"><col style="width:116px">
        <col><col style="width:188px"><col style="width:134px"><col style="width:132px"></colgroup>`;

  const head = collect
    ? `<tr><th colspan="3"></th><th colspan="2" class="ai-head">Researched by Rhonica</th><th colspan="2"></th></tr>
       <tr><th>Counterparty</th><th class="num">Outstanding</th>
           <th class="num">Days overdue</th><th class="ai ai-start">What we found</th><th class="ai ai-end">Action</th>
           <th>Outcome</th><th></th></tr>`
    : `<tr><th colspan="2"></th><th colspan="2" class="ai-head">Researched by Rhonica</th><th colspan="2"></th></tr>
       <tr><th class="">Vendor</th><th class="num">Monthly</th>
           <th class="ai ai-start">What we found</th><th class="ai ai-end">Action</th>
           <th class="">Outcome</th><th class=""></th></tr>`;

  const body = rows.map((r) => {
    const v = r.verdict || "none";
    const verdict = `<span class="verdict v-${esc(v)}">${esc(VERDICT_LABEL[v] || v)}</span>
       ${r.verdict_reason ? `<p class="why">${esc(r.verdict_reason)}</p>` : ""}`;
    const found = `<p class="note">${esc(r.note || "Nothing found.")}</p>${citeHtml(r)}`;
    const act = collect
      ? (r.ready ? `<button class="btn" data-call="${esc(r.id)}">Call</button>`
                 : r.callable ? `<span class="queued">In queue</span>` : "")
      : (v === "email"
          ? `<button class="btn2" data-draft="${esc(r.id)}">Draft email</button>`
          : r.ready ? `<button class="btn" data-call="${esc(r.id)}">Call</button>`
          : r.callable ? `<span class="queued">In queue</span>` : "");

    return collect
      ? `<tr data-id="${esc(r.id)}">
          <td><div class="namecell"><strong style="font-weight:500">${esc(r.display_name)}</strong></div>
              <p class="why" style="margin-top:5px">${r.open_invoices} open · ${Math.round(r.ar_share * 100)}% of AR</p></td>
          <td class="num" style="font-weight:500">${money(r.outstanding)}</td>
          <td class="num" style="${r.oldest_days > 60 ? "color:var(--red-t);font-weight:500" : ""}">${r.oldest_days}</td>
          <td class="ai ai-start">${found}</td>
          <td class="ai ai-end">${verdict}</td>
          <td>${outcomeHtml(r)}</td>
          <td style="text-align:right">${act}</td></tr>`
      : `<tr data-id="${esc(r.id)}">
          <td><div class="namecell"><strong style="font-weight:500">${esc(r.display_name)}</strong>
              ${r.duplicate ? `<span class="bd cut">duplicate</span>` : ""}</div></td>
          <td class="num" style="font-weight:500">${money(r.monthly_spend)}</td>
          <td class="ai ai-start">${found}</td>
          <td class="ai ai-end">${verdict}</td>
          <td>${outcomeHtml(r)}</td>
          <td style="text-align:right">${act}</td></tr>`;
  }).join("");

  $("content").innerHTML = `<table class="board">${cols}<thead>${head}</thead><tbody>${body}</tbody></table>`;
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
    <td style="color:var(--gr2)">${esc(r.sector || "-")}</td>
    <td class="num" style="${r.outstanding ? "font-weight:500" : ""}">${r.outstanding ? money(r.outstanding) : '<span style="color:var(--gr3)">-</span>'}</td>
    <td class="num">${r.money_out ? money(r.money_out) : '<span style="color:var(--gr3)">-</span>'}</td>
    <td class="num" style="${r.oldest_days > 60 ? "color:var(--red-t)" : ""}">${r.oldest_days ? r.oldest_days + "d" : '<span style="color:var(--gr3)">-</span>'}</td>
    <td class="num">${r.ar_share ? Math.round(r.ar_share * 100) + "%" : '<span style="color:var(--gr3)">-</span>'}</td>
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
  if (secs < 172800) { const h = Math.round(secs / 3600); return h === 1 ? "1 hour ago" : h + " hours ago"; }
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
    return `<div class="qitem">
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

// Commitment keys come back from the model as snake_case field names.
const humanKey = (k) => String(k).replace(/[_-]+/g, " ").replace(/^./, (c) => c.toUpperCase());

// Every result the outcome extractor can emit. An unmapped one used to render
// raw and lowercase next to properly labelled ones.
const RESULT = {
  commitment:        { label: "Payment date agreed",  tone: "good" },
  partial:           { label: "Part payment agreed",  tone: "good" },
  agreed:            { label: "New terms agreed",     tone: "good" },
  cancelled:         { label: "Cancelled",            tone: "good" },
  retention_offered: { label: "Retention offer made", tone: "good" },
  callback:          { label: "Call back arranged",   tone: "" },
  deferred:          { label: "Call back arranged",   tone: "" },
  voicemail:         { label: "Reached voicemail",    tone: "" },
  none:              { label: "No agreement",         tone: "" },
  dispute:           { label: "Disputed",             tone: "bad" },
  refused:           { label: "Refused",              tone: "bad" },
  escalated:         { label: "Escalated to a human", tone: "bad" },
};

async function renderCalls() {
  $("runBtn").hidden = true;
  $("title").textContent = "Calls";
  $("subtitle").textContent = "Every call the desk has placed, and what came of it";
  $("filters").innerHTML = "";
  const [rows, stats] = await Promise.all([api("/api/calls"), api("/api/call-stats")]);

  $("tiles").innerHTML = [
    ["Placed", String(stats.placed), "since the desk started", "var(--gr)"],
    ["Reached a person", String(stats.answered), stats.placed ? `of ${stats.placed}` : "none yet", "var(--gr)"],
    ["Commitments", String(stats.commitments), "dates or terms agreed", "var(--mint-t)"],
    ["Value secured", money(stats.value_secured), "against open invoices", "var(--mint-t)"],
  ].map(([l, v, m, c]) =>
    `<div class="tile"><p class="l">${l}</p><p class="v">${v}</p><p class="m" style="color:${c}">${m}</p></div>`).join("");

  if (!rows.length) {
    $("content").innerHTML = `<div class="empty">No calls yet. Run the workflow from AR Collections.</div>`;
    return;
  }

  const body = rows.map((c) => {
    const oc = c.outcome || {};
    const r = RESULT[oc.result] || {
      label: c.state === "live" ? "On the call now"
           : c.state === "wrapping" ? "Writing the summary\u2026" : "Completed", tone: "" };
    const commitments = (oc.commitments || []).filter((x) => x && x.label);
    const turns = (c.transcript || []).filter((t) => t.role !== "tool").length;
    return `<tr class="callrow" data-callrow="${esc(c.id)}">
        <td><div class="namecell"><strong style="font-weight:500">${esc(c.counterparty_name)}</strong></div>
            <p class="why" style="margin-top:5px">${esc(c.to_number || "no number")}</p></td>
        <td class="when">${esc(new Date(c.created_at).toLocaleString(undefined,
            { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" }))}</td>
        <td><span class="res ${esc(r.tone)}">${esc(r.label)}</span>
            ${commitments.length ? `<p class="why" style="margin-top:5px">${commitments.map((x) =>
              `${esc(humanKey(x.label))}: ${esc(String(x.value))}`).join(" · ")}</p>` : ""}</td>
        <td class="said">${esc(oc.summary || (c.state === "done" ? "Nothing recorded" : "In progress"))}</td>
        <td style="text-align:right"><button class="btn2 small">${turns ? `Transcript (${turns})` : "No transcript"}</button></td>
      </tr>
`;
  }).join("");

  $("content").innerHTML = `<table class="board calls">
    <colgroup><col style="width:220px"><col style="width:150px"><col style="width:210px"><col><col style="width:150px"></colgroup>
    <thead><tr><th>Counterparty</th><th>Called</th><th>Result</th><th>What was agreed</th><th></th></tr></thead>
    <tbody>${body}</tbody></table>`;
}

async function renderSettings() {
  $("runBtn").hidden = true;
  $("title").textContent = "Agent settings";
  $("subtitle").textContent = "What the agent may say, how far it may go, and what stops it";
  $("tiles").innerHTML = ""; $("filters").innerHTML = "";
  const s = await api("/api/settings");
  const cps = await api("/api/counterparties");

  const sched = (state.notif && state.notif.schedule) || {};
  const nextRun = sched.next_due ? new Date(sched.next_due) : null;

  $("content").innerHTML = `
    <div class="sech"><h3>On the phone</h3><p>Who the counterparty hears, and what it has to tell them.</p></div>
    <div class="cols2">
      <div class="card">
        <div class="fld"><label>Calling on behalf of</label>
          <input type="text" id="s-company" value="${esc(s.company_name)}"></div>
        <div class="cols2" style="gap:14px">
          <div class="fld"><label>Voice</label>
            <select id="s-voice">${["Quinn", "Aria", "Nova", "Rowan"].map((v) =>
              `<option ${v === s.voice_name ? "selected" : ""}>${v}</option>`).join("")}</select></div>
          <div class="fld"><label>Tone</label>
            <select id="s-tone">${["measured", "warm", "direct"].map((v) =>
              `<option ${v === s.tone ? "selected" : ""}>${v}</option>`).join("")}</select></div>
        </div>
      </div>
      <div class="card">
        <p class="lbl">Disclosure</p>
        <label class="sw"><input type="checkbox" id="s-disclose" ${s.disclose_ai ? "checked" : ""}>
          <span>Say it is an AI in the first sentence
            <span>Before anything else is said, including the company name.</span></span></label>
        <label class="sw"><input type="checkbox" id="s-record" ${s.announce_recording ? "checked" : ""}>
          <span>Announce that the call is recorded
            <span>Required in two party consent states.</span></span></label>
        <p class="hint">Turning either off may be unlawful where you or the other party are. Both stay on unless you have checked.</p>
      </div>
    </div>

    <div class="sech"><h3>Negotiating authority</h3><p>The furthest the agent may go without coming back to you.</p></div>
    <div class="cols2">
      <div class="card">
        <div class="cols2" style="gap:14px">
          <div class="fld"><label>Payment window</label>
            <input type="number" id="s-window" value="${s.payment_window_days}" min="1" max="120">
            <p class="hint">Days it may offer.</p></div>
          <div class="fld"><label>Most instalments</label>
            <input type="number" id="s-instal" value="${s.max_instalments}" min="1" max="6"></div>
        </div>
        <div class="fld" style="margin-bottom:0"><label>Authorised to agree</label>
          <textarea id="s-may">${esc((s.may_agree || []).join("\n"))}</textarea>
          <p class="hint">One per line, handed to the agent verbatim.</p></div>
      </div>
      <div class="card">
        <div class="fld" style="margin-bottom:0"><label>Must never do</label>
          <textarea id="s-must" style="min-height:188px">${esc((s.must_not || []).join("\n"))}</textarea>
          <p class="hint">Keep the last line. It stops the agent repeating back what it read online, which is what makes the research feel like judgement rather than surveillance.</p></div>
      </div>
    </div>

    <div class="sech"><h3>Guardrails</h3><p>Enforced at the API, not just hidden in this screen.</p></div>
    <div class="cols2">
      <div class="card">
        <div class="fld"><label>A human must approve calls above</label>
          <input type="number" id="s-threshold" value="${Math.round(s.approval_threshold_cents / 100)}" min="0" step="500">
          <p class="hint">Dollars. At or above this, the API refuses to dial without an approver (412).</p></div>
        <div class="fld" style="margin-bottom:0"><label>Always dial this number instead</label>
          <input type="text" id="s-override" value="${esc(s.demo_override_number || "")}" placeholder="+1 555 000 0000">
          <p class="hint">While this is set the agent cannot reach a real counterparty.</p></div>
      </div>
      <div class="card">
        <div class="fld"><label>Calls per run</label>
          <input type="number" id="s-calls" value="${s.calls_per_run}" min="1" max="50"></div>
        <div class="fld" style="margin-bottom:0"><label>Never call</label>
          <div class="dnc">${cps.map((c) =>
            `<label class="dnc-item"><input type="checkbox" value="${esc(c.id)}" ${(s.do_not_call || []).includes(c.id) ? "checked" : ""}>
               <span>${esc(c.display_name)}</span>
               ${c.outstanding ? `<em>${money(c.outstanding)}</em>` : ""}</label>`).join("")}</div>
          <p class="hint">A call to anyone ticked here is refused by the API with a 403, not merely hidden.</p></div>
      </div>
    </div>

    <div class="sech"><h3>Research and connections</h3><p>Where the board's findings come from.</p></div>
    <div class="cols2">
      <div class="card">
        <p class="lbl">Schedule</p>
        <p style="margin:0 0 14px;font-size:14px">Runs every day at ${String(sched.hour ?? 17).padStart(2, "0")}:00${
          nextRun ? `, next ${esc(nextRun.toLocaleString(undefined, { weekday: "long", hour: "numeric", minute: "2-digit" }))}` : ""}.</p>
        <button class="btn2" id="researchBtn">Run research now</button>
        <p class="hint">Only if you need it sooner than the schedule.</p>
      </div>
      <div class="card">
        <p class="lbl">Connections</p>
        <div class="svc">${servicesHtml((state.status || {}).services || {})}</div>
        <p class="hint">Each degrades on its own. Anything not connected falls back rather than failing, so a run always completes.</p>
      </div>
    </div>

    <div class="savebar">
      <button class="btn" id="s-save">Save settings</button>
      <button class="btn2" id="s-reset">Reset to defaults</button>
      <span style="font-size:13px;color:var(--gr2)" id="s-status"></span>
    </div>`;

  $("researchBtn").onclick = async (e) => {
    e.target.disabled = true;
    e.target.textContent = "Researching…";
    try {
      const r = await api("/api/research", { method: "POST" });
      toast(r.ran ? `${r.qualified} qualified to call` : "Could not run: " + r.reason);
      await loadNotifications();
    } catch (err) { toast(err.message); }
    e.target.disabled = false;
    e.target.textContent = "Run research now";
  };

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
      do_not_call: [...document.querySelectorAll(".dnc-item input:checked")].map((i) => i.value),
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

async function openCall(id) {
  const rows = await api("/api/calls");
  const c = rows.find((x) => x.id === id);
  if (!c) return;
  const oc = c.outcome || {};
  const r = RESULT[oc.result] || {
      label: c.state === "live" ? "On the call now"
           : c.state === "wrapping" ? "Writing the summary\u2026" : "Completed", tone: "" };
  const commitments = (oc.commitments || []).filter((x) => x && x.label);

  $("drawer").classList.add("on");
  $("scrim").classList.add("on");
  $("drawer").innerHTML = `
    <div class="dhd">
      <div>
        <h2 style="margin:0;font-size:22px;font-weight:500;letter-spacing:-.027em">${esc(c.counterparty_name)}</h2>
        <p class="sub">${esc(new Date(c.created_at).toLocaleString(undefined,
          { weekday: "long", day: "numeric", month: "long", hour: "numeric", minute: "2-digit" }))}
          · ${esc(c.to_number || "no number")}</p>
      </div>
      <button class="btn2" id="closeDrawer">Close</button>
    </div>
    <div class="dbody one">
      <div>
        <p class="lbl">Result</p>
        <div class="card" style="margin-bottom:22px">
          <p class="res ${esc(r.tone)}" style="margin:0 0 9px;font-size:17px">${esc(r.label)}</p>
          <p style="margin:0;font-size:14px;line-height:1.6">${esc(oc.summary || "Nothing recorded.")}</p>
          ${commitments.length ? `<div style="margin-top:15px">${commitments.map((x) =>
            `<div class="kv"><span>${esc(humanKey(x.label))}</span><span>${esc(String(x.value))}</span></div>`).join("")}</div>` : ""}
        </div>
        <p class="lbl">Transcript</p>
        <div class="tx">${(c.transcript || []).map((t) => t.role === "tool"
          ? `<div class="tool">${esc(t.text)}</div>`
          : `<div class="turn"><div class="tav ${esc(t.role)}">${t.role === "agent" ? "R" : "··"}</div>
             <div><p class="who">${t.role === "agent" ? "Rhonica" : esc(c.counterparty_name)}</p>
             <p class="say">${esc(t.text)}</p></div></div>`).join("")
          || '<p style="color:var(--gr2);margin:0">Nothing was recorded for this call.</p>'}</div>
      </div>
    </div>`;
  $("closeDrawer").onclick = closeDrawer;
}

async function openDraft(id) {
  $("drawer").classList.add("on");
  $("scrim").classList.add("on");
  $("drawer").innerHTML = `<div class="dhd"><h2 style="margin:0;font-size:22px;font-weight:500">Drafting</h2></div>
    <div class="dbody one"><p class="empty">Writing the email…</p></div>`;
  const d = await api(`/api/counterparties/${id}/draft`, { method: "POST" });
  $("drawer").innerHTML = `
    <div class="dhd">
      <div><h2 style="margin:0;font-size:22px;font-weight:500;letter-spacing:-.027em">${esc(d.vendor)}</h2>
        <p class="sub">Renegotiation email, drafted from this run's research</p></div>
      <button class="btn2" id="closeDrawer">Close</button>
    </div>
    <div class="dbody one">
      <div class="card">
        <p class="lbl">To</p>
        <p style="margin:0 0 16px;font-size:14px">${esc(d.to || "no address on file")}</p>
        <p class="lbl">Subject</p>
        <p style="margin:0 0 16px;font-size:15px;font-weight:500">${esc(d.subject)}</p>
        <p class="lbl">Body</p>
        <p style="margin:0;font-size:14px;line-height:1.65;white-space:pre-wrap">${esc(d.body)}</p>
      </div>
      <p class="hint">Drafted, not sent. Copy it into your mail client when you are happy with it.</p>
    </div>`;
  $("closeDrawer").onclick = closeDrawer;
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
        <div class="kv"><span>Oldest</span><span${cp.oldest_days > 60 ? ' style="color:var(--red-t)"' : ""}>${cp.oldest_days ? cp.oldest_days + " days" : "-"}</span></div>
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
        <span style="font-size:13px;color:var(--gr2)">${state.status?.services.voice.live ? "Dials through ElevenLabs" : "Voice is not configured yet"}</span>
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
        <button class="btn" id="simInstead">Continue without voice</button>
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
      : `<div class="turn"><div class="tav ${t.role}">${t.role === "agent" ? "R" : "··"}</div>
         <div><p class="who">${t.role === "agent" ? "Rhonica" : esc(cp.display_name)}</p>
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
          // A rehearsal returns no outcome by design, so do not imply one.
          toast(r.rehearsal ? "Test call ended. Nothing was recorded against the counterparty."
                            : (r.outcome?.summary || "Call logged"));
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
  watchCalls([callId], "single", cp);
}

// --- wiring ----------------------------------------------------------------

document.addEventListener("click", (e) => {
  // The portal's own nav is present so the shape is right, but inert. Only the
  // Desk's own screens are wired.
  const nav = e.target.closest("[data-view]");
  if (nav) {
    document.querySelectorAll("[data-view]").forEach((b) => b.classList.remove("on"));
    nav.classList.add("on");
    state.view = nav.dataset.view;
    render();
    return;
  }
  const timelineBtn = e.target.closest("[data-timeline]");
  if (timelineBtn) { e.stopPropagation(); openTimeline(timelineBtn.dataset.timeline); return; }
  const callRow = e.target.closest("[data-callrow]");
  if (callRow) { openCall(callRow.dataset.callrow); return; }
  const draftBtn = e.target.closest("[data-draft]");
  if (draftBtn) { e.stopPropagation(); openDraft(draftBtn.dataset.draft); return; }
  const openRow = e.target.closest("[data-open]");
  if (openRow) { openDossier(openRow.dataset.open); return; }
  const runPill = e.target.closest("[data-run]");
  if (runPill) { state.runId = Number(runPill.dataset.run); renderChanges(); return; }
  const chRow = e.target.closest(".chrow[data-id]");
  if (chRow) { openDossier(chRow.dataset.id); return; }
  const pill = e.target.closest("[data-posture]");
  if (pill) { state.posture = pill.dataset.posture; renderCounterparties(); return; }
  const callBtn = e.target.closest("[data-call]");
  if (callBtn) {
    e.stopPropagation();
    api(`/api/counterparties/${callBtn.dataset.call}`).then(reviewCall);
    return;
  }
  const row = e.target.closest("tr[data-id]");
  if (row) openDossier(row.dataset.id);
});

$("scrim").onclick = closeDrawer;
$("cdock").onclick = restoreCall;
$("runBtn").onclick = runWorkflow;
$("bellBtn").onclick = (e) => { e.stopPropagation(); toggleNotifications(); };
document.addEventListener("click", (e) => {
  if (!e.target.closest(".bellwrap")) $("notifs").classList.remove("on");
});
setInterval(() => loadNotifications().catch(() => {}), 60000);

loadStatus().then(render);
loadNotifications().catch(() => {});
