/* ============================================================
   BOOST Training Registration — Google Apps Script backend
   Deploy as Web App (Execute as: Me, Access: Anyone).
   Paste the resulting /exec URL into app.js APPS_SCRIPT_URL.
   ============================================================ */

// ---- CONFIG (edit these) ----
const SHEET_ID = "REPLACE_ME_SPREADSHEET_ID";   // open Sheet → URL → /d/<this>/edit
const SHEET_TAB = "Registrations";
const NOTIFY_EMAIL = "REPLACE_ME_ORGANISER_EMAIL@example.com"; // gets a copy on each registration; "" to disable
const SEND_USER_CONFIRMATION = true;            // email registrant a "received" note
const TRAINING_DATES = "12-13 May 2026";        // shown in confirmation mail
const TRAINING_VENUE = "Belda College, Paschim Medinipur";

const HEADERS = [
  "submitted_at","name","email","phone","role","institution","city",
  "instruments","experience","diet","notes",
  "consent","status",
  "user_agent"
];

// ---- Entry point ----
function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);

    // basic guard
    if (!body || !body.name || !body.email) {
      return jsonOut({ ok: false, error: "Missing required fields" });
    }

    const sheet = openSheet_();
    const row = HEADERS.map(h => {
      if (h === "status") return "REGISTERED";
      return body[h] !== undefined ? body[h] : "";
    });
    sheet.appendRow(row);

    if (SEND_USER_CONFIRMATION) sendUserMail_(body);
    if (NOTIFY_EMAIL && !NOTIFY_EMAIL.startsWith("REPLACE_ME")) sendOrganiserMail_(body);

    return jsonOut({ ok: true });
  } catch (err) {
    return jsonOut({ ok: false, error: String(err) });
  }
}

function doGet() {
  // health check; visiting the URL in browser shows status
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true, service: "boost-training-reg", time: new Date() }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ---- Helpers ----
function openSheet_() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sh = ss.getSheetByName(SHEET_TAB);
  if (!sh) {
    sh = ss.insertSheet(SHEET_TAB);
    sh.appendRow(HEADERS);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold").setBackground("#f4d8b6");
    sh.setFrozenRows(1);
  } else if (sh.getLastRow() === 0) {
    sh.appendRow(HEADERS);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold").setBackground("#f4d8b6");
    sh.setFrozenRows(1);
  }
  return sh;
}

function jsonOut(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function sendUserMail_(body) {
  const subject = "Registration received — Belda College / Borosil Instrument Training";
  const text =
`Dear ${body.name},

Thank you for registering for the hands-on training on Kjeldahl, Soxhlet
and Dietary Fibre Estimation, organised by the Department of Nutrition,
Belda College, in collaboration with Borosil Scientific. The instruments
are supported through the WBDSTBT BOOST grant.

A final confirmation with seat number and joining details will be sent
within 24 hours.

Dates: ${TRAINING_DATES}
Venue: ${TRAINING_VENUE}
Instruments selected: ${body.instruments}

Please bring a lab coat, safety goggles and a notebook.

If you did not initiate this registration, reply to this mail.

Warm regards,
Training Coordination Team`;

  try {
    MailApp.sendEmail({ to: body.email, subject: subject, body: text });
  } catch (err) {
    Logger.log("user mail failed: " + err);
  }
}

function sendOrganiserMail_(body) {
  const subject = "[BOOST training] New registration — " + body.name;
  const text =
`New registration received.

Name:         ${body.name}
Role:         ${body.role}
Institution:  ${body.institution}
City:         ${body.city}
Email:        ${body.email}
Phone:        ${body.phone}
Instruments:  ${body.instruments}
Experience:   ${body.experience}
Diet:         ${body.diet}
Notes:        ${body.notes || "(none)"}
Submitted:    ${body.submitted_at}

Open the Sheet to confirm the seat or mark as waitlist.`;

  try {
    MailApp.sendEmail({ to: NOTIFY_EMAIL, subject: subject, body: text });
  } catch (err) {
    Logger.log("organiser mail failed: " + err);
  }
}

/* Optional one-time setup helper:
   Run setup_() manually from the Apps Script editor to create the sheet
   with headers if it does not exist. */
function setup_() {
  const sh = openSheet_();
  Logger.log("Sheet ready with " + sh.getLastRow() + " rows.");
}
