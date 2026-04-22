"""
Spare — Adaptive Save Engine Demo
==================================
A Streamlit app that simulates an intelligent, context-aware saving system.
Rule-based logic that adapts to balance, spending level, and transaction type.

Run:  streamlit run spare_engine.py
"""

import streamlit as st

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Spare · Adaptive Save Engine",
    page_icon="💚",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS — typography, hierarchy, and contrast improvements
#
# Key changes from v1:
#   1. section-label: 9px → 11px, #AEADA6 → #6B6B63 (readable labels)
#   2. result-mode:   9px → 12px, now bold (output label must be legible)
#   3. result-amount: 42px → 52px (primary output should dominate the page)
#   4. result-message: 16px → 17px, weight 400 → 500 (notification text is key)
#   5. result-reason: removed opacity:0.75, 12px → 13px, weight 300 → 400
#   6. breakdown-title: 9px → 11px, #AEADA6 → #6B6B63 (readable on grey bg)
#   7. breakdown-label: weight 300 → 400, #6B6B63 stays (now readable at 400)
#   8. breakdown-row: 13px → 14px (table body needs breathing room)
#   9. breakdown-value: 12px → 13px (monospace values were too small)
#  10. app-sub: weight 300 → 400 (subtitle was too faint)
#  11. how-text: 13px → 14px, weight 300 → 400 (body text minimum 14px)
#  12. scenario cards: desc text 12px → 13px, weight 300 → 400
#  13. Input section: added a visible container background to separate from result
#  14. Result card: added left accent border for stronger visual anchor
#  15. how-num circle: 22px → 26px for better touch target and proportion
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Mulish:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Mulish', sans-serif;
    background-color: #F8F7F3;
    color: #0E0E0C;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; padding-bottom: 4rem; max-width: 760px; }

/* ── App header ── */
.app-header {
    border-bottom: 2px solid #0E0E0C;
    padding-bottom: 1.25rem;
    margin-bottom: 2rem;
}

.app-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;          /* was 10px — slightly larger for legibility */
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4A4A42;           /* was #6B6B63 — darker for better contrast */
    margin-bottom: 0.5rem;
}

.app-title {
    font-family: 'Lora', Georgia, serif;
    font-size: 34px;
    font-weight: 400;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}

.app-title em { font-style: italic; color: #2E7A4A; }

/* FIX: was weight 300 and #6B6B63 — too faint for a subtitle */
.app-sub {
    font-size: 15px;
    color: #3C3C35;           /* was #6B6B63 — significantly darker */
    font-weight: 400;         /* was 300 — thin weight + mid-grey = low contrast */
    line-height: 1.65;
}

/* ── Section labels ── */
/* FIX: was 9px #AEADA6 — nearly invisible, especially on coloured backgrounds */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;          /* was 9px */
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6B6B63;           /* was #AEADA6 */
    margin-bottom: 0.9rem;
    margin-top: 0.25rem;
}

/* ── Input section container ── */
/* NEW: wraps inputs in a subtle background to visually separate them from result */
.input-container {
    background: #F0EFE9;
    border: 0.5px solid #D8D7CE;
    border-radius: 4px;
    padding: 1.25rem 1.5rem 1rem;
    margin-bottom: 1.5rem;
}

/* ── Result card ── */
/* FIX: added left accent border (4px) for a stronger visual anchor on the output */
.result-card {
    border-radius: 4px;
    padding: 1.75rem 1.75rem 1.5rem;
    margin: 0.5rem 0 1.25rem;
}

.result-card.green  { background: #E4F2E9; border: 1px solid #8DC4A0; border-left: 4px solid #2E7A4A; }
.result-card.amber  { background: #F8EFDC; border: 1px solid #D4A84B; border-left: 4px solid #8A5500; }
.result-card.red    { background: #F5E5E2; border: 1px solid #D49490; border-left: 4px solid #9C3020; }
.result-card.blue   { background: #E3EEF8; border: 1px solid #7EB4D8; border-left: 4px solid #0C3A6A; }

/* FIX: was 9px — mode label must be legible, it names the decision */
.result-mode {
    font-family: 'DM Mono', monospace;
    font-size: 12px;          /* was 9px */
    font-weight: 600;         /* was 500 — bolder so it reads as a label, not a caption */
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.result-card.green  .result-mode { color: #1A4A2A; }
.result-card.amber  .result-mode { color: #5C3800; }
.result-card.red    .result-mode { color: #7A1810; }
.result-card.blue   .result-mode { color: #0A3060; }

/* FIX: increased from 42px → 52px — this is the primary output, it should dominate */
.result-amount {
    font-family: 'Lora', Georgia, serif;
    font-size: 56px;          /* was 42px */
    font-weight: 500;         /* was 400 — heavier for a number at this size */
    line-height: 1;
    letter-spacing: -0.02em;
    margin-bottom: 0.6rem;
}

.result-card.green  .result-amount { color: #1A4A2A; }
.result-card.amber  .result-amount { color: #5C3800; }
.result-card.red    .result-amount { color: #7A1810; }
.result-card.blue   .result-amount { color: #0A3060; }

/* FIX: was 16px weight 300 — the notification message should be prominent */
.result-message {
    font-family: 'Lora', Georgia, serif;
    font-style: italic;
    font-size: 18px;          /* was 16px */
    font-weight: 400;
    line-height: 1.6;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(0,0,0,0.1);  /* NEW: visual separator before reason */
}

.result-card.green  .result-message { color: #1A4A2A; }
.result-card.amber  .result-message { color: #5C3800; }
.result-card.red    .result-message { color: #7A1810; }
.result-card.blue   .result-message { color: #0A3060; }

/* FIX: was 12px weight 300 opacity 0.75 — triple-faded, unreadable */
.result-reason {
    font-size: 13px;          /* was 12px */
    font-weight: 400;         /* was 300 */
    line-height: 1.65;
    color: inherit;           /* inherits card text color */
    opacity: 0.80;            /* was 0.75 — slightly more legible */
}

/* ── Breakdown table ── */
.breakdown {
    background: #ECECE6;
    border: 0.5px solid #CCCCC4;
    border-radius: 3px;
    padding: 1.1rem 1.25rem;
    margin-top: 1rem;
}

/* FIX: was 9px #AEADA6 on a grey background — completely illegible */
.breakdown-title {
    font-family: 'DM Mono', monospace;
    font-size: 11px;          /* was 9px */
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4A4A42;           /* was #AEADA6 — much darker */
    margin-bottom: 0.85rem;
}

/* FIX: was weight 300 #6B6B63 — low contrast on grey; bumped weight */
.breakdown-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 7px 0;           /* was 5px — more breathing room */
    border-bottom: 0.5px solid #D0CFC8;
    font-size: 14px;          /* was 13px */
}

.breakdown-row:last-child { border-bottom: none; }

.breakdown-label {
    color: #4A4A42;           /* was #6B6B63 */
    font-weight: 400;         /* was 300 */
}

/* FIX: was 12px — monospace values at 12px are hard to read quickly */
.breakdown-value {
    font-weight: 600;
    color: #0E0E0C;
    font-family: 'DM Mono', monospace;
    font-size: 13px;          /* was 12px */
}

.breakdown-value.green { color: #1E5C30; }
.breakdown-value.amber { color: #5C3800; }
.breakdown-value.red   { color: #7A1810; }

/* ── Streamlit widget overrides ── */
/* FIX: bumped all labels to 14px and weight 600 for better form hierarchy */
div[data-testid="stSlider"] > label,
div[data-testid="stRadio"] > label,
div[data-testid="stNumberInput"] > label {
    font-size: 14px;          /* was 13px */
    font-weight: 600;         /* was 500 */
    color: #1E1E18;           /* was #35352F — slightly darker */
}

.stSlider [data-baseweb="slider"] { margin-top: 0.25rem; }
div[data-testid="stHorizontalBlock"] { gap: 1.5rem; }

/* ── Divider ── */
.divider { height: 1px; background: #D0CFC8; margin: 2rem 0; }  /* was 0.5px — thicker is more visible */

/* ── How it works ── */
.how-step {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    margin-bottom: 14px;      /* was 12px — more breathing room */
}

/* FIX: was 22px — slightly too small; now 26px for better proportion */
.how-num {
    font-family: 'DM Mono', monospace;
    font-size: 11px;          /* was 10px */
    background: #0E0E0C;
    color: #F8F7F3;
    width: 26px;              /* was 22px */
    height: 26px;             /* was 22px */
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}

/* FIX: was 13px weight 300 — main body text should be at least 14px/400 */
.how-text {
    font-size: 14px;          /* was 13px */
    color: #2A2A22;           /* was #35352F — darker */
    font-weight: 400;         /* was 300 */
    line-height: 1.65;
}

.how-text strong { font-weight: 600; color: #0E0E0C; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# ENGINE LOGIC
# ──────────────────────────────────────────────

def compute_context_score(balance: float, spending_level: str, transaction_amount: float) -> int:
    """
    Compute a context score from 0–100 that represents how comfortable
    the user's financial situation is right now.

    Higher score  → save more aggressively
    Lower score   → save conservatively or skip

    Inputs:
      balance           - current account balance (₹)
      spending_level    - 'Low', 'Medium', or 'High' (user's recent pattern)
      transaction_amount - size of the triggering transaction (₹)
    """
    score = 50  # start from neutral

    # ── Balance signal (most important — range: ±35 points) ──
    if balance >= 10_000:
        score += 35   # very healthy — can save confidently
    elif balance >= 5_000:
        score += 20   # comfortable
    elif balance >= 2_000:
        score += 5    # adequate but modest
    elif balance >= 1_000:
        score -= 15   # getting tight
    elif balance >= 500:
        score -= 30   # low — save minimally
    else:
        score = 0     # below floor — skip entirely (return early)
        return score

    # ── Spending level signal (range: ±20 points) ──
    if spending_level == "Low":
        score += 20   # user is being careful — reward with more saving
    elif spending_level == "Medium":
        score += 0    # neutral
    elif spending_level == "High":
        score -= 20   # high spending week — pull back on saving

    # ── Transaction size relative to balance (range: ±10 points) ──
    # If this transaction is a large chunk of remaining balance, be more careful
    spend_ratio = transaction_amount / max(balance, 1)
    if spend_ratio > 0.5:
        score -= 10   # large relative spend — be conservative
    elif spend_ratio < 0.1:
        score += 10   # small relative spend — can comfortably save more

    # Clamp to valid range
    return max(0, min(100, score))


def compute_save_amount(
    transaction_amount: float,
    balance: float,
    spending_level: str,
) -> dict:
    """
    Main decision function. Returns a dict with:
      - save_amount: ₹ to move into savings (0 if skip)
      - mode: 'Safe', 'Normal', 'Boost', or 'Skip'
      - base_rate: percentage applied before adjustment
      - context_score: 0–100 scoring
      - notification: user-facing message
      - reason: plain-language explanation of the decision
    """

    MIN_BALANCE_FLOOR = 500    # never save if balance is at or below this
    MIN_SAVE_AMOUNT   = 5      # saves below ₹5 are skipped (feel trivial)
    MAX_SAVE_AMOUNT   = 50     # hard cap — never save more than this

    # ── Hard rule 1: balance floor ──────────────────────────────
    if balance <= MIN_BALANCE_FLOOR:
        return {
            "save_amount":    0,
            "mode":           "Skip",
            "base_rate":      0,
            "context_score":  0,
            "notification":   None,   # no notification on a silent skip
            "reason":         f"Balance is ₹{balance:,.0f} — below the ₹{MIN_BALANCE_FLOOR:,} safety floor. Saving is paused until the account recovers.",
        }

    # ── Compute context score ────────────────────────────────────
    score = compute_context_score(balance, spending_level, transaction_amount)

    # ── Hard rule 2: score-based skip ───────────────────────────
    if score < 20:
        return {
            "save_amount":    0,
            "mode":           "Skip",
            "base_rate":      0,
            "context_score":  score,
            "notification":   None,
            "reason":         "Context score is very low — multiple stress signals present (low balance + high spending). Skipping this save silently.",
        }

    # ── Base rate selection based on context score ───────────────
    # Score 80–100 → Boost mode (8–10%)
    # Score 50–79  → Normal mode (5–7%)
    # Score 20–49  → Safe mode (3–5%)
    if score >= 80:
        base_rate = 0.10
        mode = "Boost"
    elif score >= 50:
        base_rate = 0.07
        mode = "Normal"
    else:
        base_rate = 0.04
        mode = "Safe"

    # ── Calculate raw save amount ────────────────────────────────
    raw_save = transaction_amount * base_rate

    # ── Apply score modifier (fine-grained adjustment within mode) ──
    # Map score within each band to a 0.7–1.0 multiplier
    score_multiplier = 0.7 + (score / 100) * 0.3
    adjusted_save = raw_save * score_multiplier

    # ── Hard cap ─────────────────────────────────────────────────
    save_amount = min(adjusted_save, MAX_SAVE_AMOUNT)

    # ── Hard rule 3: balance protection ──────────────────────────
    # Never let a save push the user below their floor
    max_allowed = max(0, balance - MIN_BALANCE_FLOOR)
    save_amount = min(save_amount, max_allowed)

    # ── Hard rule 4: minimum meaningful save ─────────────────────
    if save_amount < MIN_SAVE_AMOUNT:
        return {
            "save_amount":    0,
            "mode":           "Skip",
            "base_rate":      round(base_rate * 100, 1),
            "context_score":  score,
            "notification":   None,
            "reason":         f"Calculated save of ₹{save_amount:.0f} is below the ₹{MIN_SAVE_AMOUNT} minimum. Skipping — will accumulate into next transaction.",
        }

    # Round to nearest rupee
    save_amount = round(save_amount)

    # ── Build user-facing notification and reason ─────────────────
    notifications = {
        "Boost": f"A good week to save a little more — ₹{save_amount} set aside.",
        "Normal": f"₹{save_amount} quietly saved. Running total keeps growing.",
        "Safe": f"Saved just ₹{save_amount} this time — keeping it small while your balance is lower.",
    }

    reasons = {
        "Boost": (
            f"Balance is healthy (₹{balance:,.0f}) and recent spending is {spending_level.lower()}. "
            f"Context score: {score}/100 — conditions are good, saving at a higher rate ({base_rate*100:.0f}%)."
        ),
        "Normal": (
            f"Balance (₹{balance:,.0f}) is stable and spending is {spending_level.lower()}. "
            f"Context score: {score}/100 — standard save rate ({base_rate*100:.0f}%) applied."
        ),
        "Safe": (
            f"Balance (₹{balance:,.0f}) or recent spending ({spending_level.lower()}) signals some pressure. "
            f"Context score: {score}/100 — saving conservatively ({base_rate*100:.0f}%) to avoid strain."
        ),
    }

    return {
        "save_amount":   save_amount,
        "mode":          mode,
        "base_rate":     round(base_rate * 100, 1),
        "context_score": score,
        "notification":  notifications[mode],
        "reason":        reasons[mode],
    }


# ──────────────────────────────────────────────
# HELPER: map mode to card colour class
# ──────────────────────────────────────────────
MODE_COLOURS = {
    "Boost":  "blue",
    "Normal": "green",
    "Safe":   "amber",
    "Skip":   "red",
}

MODE_LABELS = {
    "Boost":  "⬆ Boost Mode — saving more",
    "Normal": "● Normal Mode — standard save",
    "Safe":   "▼ Safe Mode — saving less",
    "Skip":   "○ Skipped — no save this time",
}


# ──────────────────────────────────────────────
# APP LAYOUT
# ──────────────────────────────────────────────

# Header
st.markdown("""
<div class="app-header">
  <div class="app-eyebrow">Spare · Product Demo · Adaptive Save Engine</div>
  <div class="app-title">How much should <em>Spare</em> save<br>right now?</div>
  <div class="app-sub">
    Enter a transaction and account context. The engine decides how much to save —
    adapting to your balance, recent spending, and the size of this transaction.
  </div>
</div>
""", unsafe_allow_html=True)


# ── INPUT SECTION ────────────────────────────────────────────────
# Wrapped in .input-container to visually separate inputs from the result output
st.markdown('<p class="section-label">Inputs — transaction context</p>', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    transaction_amount = st.number_input(
        "Transaction amount (₹)",
        min_value=10,
        max_value=50_000,
        value=450,
        step=50,
        help="The amount just spent — e.g. a restaurant bill, a cab fare, a grocery run.",
    )

with col2:
    balance = st.number_input(
        "Current account balance (₹)",
        min_value=0,
        max_value=1_000_000,
        value=4_200,
        step=100,
        help="Your account balance at the moment of the transaction.",
    )

spending_level = st.radio(
    "Recent spending pattern (last 7 days)",
    options=["Low", "Medium", "High"],
    index=1,
    horizontal=True,
    help="Low = you've been careful this week. High = lots of transactions, large amounts.",
)

# Close input container
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── COMPUTE ─────────────────────────────────────────────────────
result = compute_save_amount(transaction_amount, balance, spending_level)

mode   = result["mode"]
colour = MODE_COLOURS[mode]
label  = MODE_LABELS[mode]


# ── RESULT CARD ──────────────────────────────────────────────────
st.markdown('<p class="section-label">Result — engine decision</p>', unsafe_allow_html=True)

if mode == "Skip":
    amount_display = "₹0"
    message_display = "No save this time."
else:
    amount_display  = f"₹{result['save_amount']}"
    message_display = result["notification"]

st.markdown(f"""
<div class="result-card {colour}">
  <div class="result-mode">{label}</div>
  <div class="result-amount">{amount_display}</div>
  <div class="result-message">"{message_display}"</div>
  <div class="result-reason">{result['reason']}</div>
</div>
""", unsafe_allow_html=True)


# ── DECISION BREAKDOWN ───────────────────────────────────────────
with st.expander("See the decision breakdown"):

    score       = result["context_score"]
    base_rate   = result["base_rate"]
    save_amount = result["save_amount"]

    # Score bar colour
    if score >= 70:
        score_cls = "green"
    elif score >= 40:
        score_cls = "amber"
    else:
        score_cls = "red"

    # Rate display
    rate_display = f"{base_rate}%" if base_rate > 0 else "—"
    raw_calc     = round(transaction_amount * base_rate / 100, 2) if base_rate > 0 else 0

    st.markdown(f"""
    <div class="breakdown">
      <div class="breakdown-title">How the engine reached this number</div>

      <div class="breakdown-row">
        <span class="breakdown-label">Transaction amount</span>
        <span class="breakdown-value">₹{transaction_amount:,}</span>
      </div>
      <div class="breakdown-row">
        <span class="breakdown-label">Account balance</span>
        <span class="breakdown-value">₹{balance:,}</span>
      </div>
      <div class="breakdown-row">
        <span class="breakdown-label">Spending pattern</span>
        <span class="breakdown-value">{spending_level}</span>
      </div>
      <div class="breakdown-row">
        <span class="breakdown-label">Context score</span>
        <span class="breakdown-value {score_cls}">{score} / 100</span>
      </div>
      <div class="breakdown-row">
        <span class="breakdown-label">Mode selected</span>
        <span class="breakdown-value">{mode}</span>
      </div>
      <div class="breakdown-row">
        <span class="breakdown-label">Save rate applied</span>
        <span class="breakdown-value">{rate_display}</span>
      </div>
      <div class="breakdown-row">
        <span class="breakdown-label">Raw calculation (₹{transaction_amount} × {rate_display})</span>
        <span class="breakdown-value">₹{raw_calc:,.2f}</span>
      </div>
      <div class="breakdown-row">
        <span class="breakdown-label">After caps and safety rules</span>
        <span class="breakdown-value green">₹{save_amount}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── DIVIDER ──────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── SCENARIO EXPLORER ────────────────────────────────────────────
st.markdown('<p class="section-label">Try these scenarios</p>', unsafe_allow_html=True)

# FIX: was 13px weight 300 #6B6B63 — too faint for instructional text
st.markdown("""
<p style="font-size:14px; color:#3C3C35; font-weight:400; margin-bottom:1rem; line-height:1.65;">
  Adjust the inputs above to see how the engine responds to different situations.
</p>
""", unsafe_allow_html=True)

scenarios = [
    ("Post-salary, healthy balance",  "₹800 restaurant dinner · ₹18,000 balance · Low spending",  "Boost"),
    ("Normal Tuesday",                "₹250 Swiggy order · ₹4,500 balance · Medium spending",     "Normal"),
    ("Month-end squeeze",             "₹300 groceries · ₹1,200 balance · High spending",          "Safe"),
    ("Nearly empty",                  "Any transaction · ₹400 balance",                           "Skip"),
]

cols = st.columns(2)
for i, (title, desc, expected_mode) in enumerate(scenarios):
    colour_map = {"Boost": "#E3EEF8", "Normal": "#E4F2E9", "Safe": "#F8EFDC", "Skip": "#F5E5E2"}
    border_map = {"Boost": "#7EB4D8", "Normal": "#8DC4A0", "Safe": "#D4A84B", "Skip": "#D49490"}
    text_map   = {"Boost": "#0A3060", "Normal": "#1A4A2A", "Safe": "#5C3800", "Skip": "#7A1810"}
    with cols[i % 2]:
        # FIX: desc text was 12px weight 300 — bumped to 13px weight 400
        st.markdown(f"""
        <div style="
            background:{colour_map[expected_mode]};
            border:0.5px solid {border_map[expected_mode]};
            border-left:3px solid {border_map[expected_mode]};
            border-radius:3px;
            padding:0.9rem 1rem;
            margin-bottom:8px;
        ">
            <div style="font-family:'DM Mono',monospace;font-size:10px;font-weight:600;
                        letter-spacing:0.1em;text-transform:uppercase;
                        color:{text_map[expected_mode]};margin-bottom:5px;">
                → {expected_mode} mode
            </div>
            <div style="font-size:14px;font-weight:600;color:#0E0E0C;margin-bottom:4px;">{title}</div>
            <div style="font-size:13px;color:#3C3C35;font-weight:400;line-height:1.55;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ── HOW IT WORKS ─────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-label">How the engine works</p>', unsafe_allow_html=True)

steps = [
    ("Transaction detected",    "A UPI spend triggers the engine. Amount and context are read."),
    ("Context scored (0–100)",  "Balance, spending pattern, and transaction size produce a score. Higher = more capacity to save."),
    ("Mode selected",           "<strong>Boost</strong> (80+), <strong>Normal</strong> (50–79), <strong>Safe</strong> (20–49), or <strong>Skip</strong> (&lt;20)."),
    ("Hard rules applied",      "Floor checks, caps, and category exclusions run last. They cannot be overridden."),
    ("User notified",           "A warm, human notification explains what happened — and why, if the amount changed."),
]

for n, (title, body) in enumerate(steps, 1):
    st.markdown(f"""
    <div class="how-step">
        <div class="how-num">{n}</div>
        <div class="how-text"><strong>{title}</strong> — {body}</div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────────────────────────
st.markdown("""
<div style="
    border-top: 0.5px solid #D8D7CE;
    padding-top: 1.25rem;
    margin-top: 2.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.06em;
    color: #AEADA6;
    display: flex;
    justify-content: space-between;
">
    <span>Spare · Adaptive Save Engine · Demo v1.0</span>
    <span>Rule-based · No external APIs · April 2026</span>
</div>
""", unsafe_allow_html=True)