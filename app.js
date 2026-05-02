/* ============================================================
   BOOST Training Registration — frontend
   Posts JSON to Google Apps Script Web App, which appends a row
   to the linked Google Sheet. No backend on GitHub Pages side.
   ============================================================ */

// REPLACE_ME: paste the Apps Script Web App /exec URL after deploy
const APPS_SCRIPT_URL = "https://script.google.com/macros/s/REPLACE_ME_DEPLOYMENT_ID/exec";

const form     = document.getElementById("regForm");
const status   = document.getElementById("formStatus");
const submit   = form.querySelector(".submit-btn");

// ---------- helpers ----------
function setStatus(msg, kind) {
  status.textContent = msg;
  status.className = "form-status" + (kind ? " " + kind : "");
}

function markInvalid(field, on) {
  if (on) field.classList.add("invalid");
  else    field.classList.remove("invalid");
}

function collect() {
  const data = {};
  const fd = new FormData(form);
  for (const [k, v] of fd.entries()) {
    if (k === "instruments") {
      data.instruments = data.instruments || [];
      data.instruments.push(v);
    } else {
      data[k] = v;
    }
  }
  data.instruments = (data.instruments || []).join(", ");
  data.submitted_at = new Date().toISOString();
  data.user_agent = navigator.userAgent;
  return data;
}

function validate(data) {
  const errs = [];
  // required text/select fields
  ["name","email","phone","role","institution","city","experience"].forEach(k => {
    const el = form.elements[k];
    if (!data[k] || !data[k].trim()) {
      errs.push(k);
      markInvalid(el, true);
    } else {
      markInvalid(el, false);
    }
  });

  // email shape
  if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errs.push("email-format");
    markInvalid(form.elements["email"], true);
  }

  // at least one instrument
  if (!data.instruments) {
    errs.push("instruments");
  }

  // consent checkbox
  if (!form.elements["consent"].checked) errs.push("consent");

  return errs;
}

// ---------- submit ----------
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  setStatus("");

  const data = collect();
  const errs = validate(data);

  if (errs.length) {
    setStatus("Please fix the highlighted fields and tick the consent box.", "err");
    return;
  }

  if (APPS_SCRIPT_URL.includes("REPLACE_ME")) {
    setStatus("Backend URL not configured yet. (See README → Deploy step 3.)", "err");
    return;
  }

  submit.classList.add("loading");
  submit.disabled = true;
  setStatus("Submitting…");

  try {
    // Apps Script doPost: use text/plain to avoid CORS preflight (works for anonymous web apps)
    const res = await fetch(APPS_SCRIPT_URL, {
      method: "POST",
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(data),
    });

    if (!res.ok) throw new Error("HTTP " + res.status);
    const out = await res.json().catch(() => ({ ok: true }));

    if (out.ok === false) throw new Error(out.error || "Server rejected submission");

    // success — replace card with thank-you panel
    showThanks(data);
  } catch (err) {
    console.error(err);
    setStatus("Submission failed: " + err.message + ". Please try again or email the organisers.", "err");
    submit.classList.remove("loading");
    submit.disabled = false;
  }
});

function showThanks(data) {
  const card = document.querySelector(".reg-card");
  card.innerHTML = `
    <h2>Registration received</h2>
    <p class="reg-sub">Thank you, <strong>${escapeHtml(data.name)}</strong>.</p>
    <div class="thanks-box">
      <p>Your registration for the hands-on training on Kjeldahl, Soxhlet and
         Dietary Fibre Estimation has been logged.</p>
      <p>A confirmation email will follow at
         <strong>${escapeHtml(data.email)}</strong> within 24 hours.</p>
      <p>Save these dates: <strong>12&ndash;13 May 2026</strong>.
         Bring a lab coat and a notebook.</p>
    </div>
    <button type="button" class="submit-btn" onclick="location.reload()">Register another participant</button>
  `;
  // inject minimal styling for thanks-box
  const s = document.createElement("style");
  s.textContent = `
    .thanks-box { background:#faf2e7; border-radius:10px; padding:18px;
                  border-left:3px solid var(--accent); margin:14px 0 18px;
                  font-size:14.5px; color:var(--ink); }
    .thanks-box p { margin: 0 0 10px; }
    .thanks-box code { background:#fff; padding:2px 6px; border-radius:4px; }
  `;
  document.head.appendChild(s);
  card.scrollIntoView({ behavior: "smooth", block: "start" });
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => (
    { "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]
  ));
}
