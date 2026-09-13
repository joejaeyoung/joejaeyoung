#!/usr/bin/env python3
"""
~/.claude/projects 의 세션 전사(JSONL)를 집계해 AI 코딩 사용량 카드(SVG)를 만든다.

  python3 gen_ai_usage.py > ai-usage.svg

집계 대상은 assistant 메시지의 message.usage 다.
model 이 <synthetic> 이거나 토큰이 전부 0 인 레코드는 뺀다.
비용은 공개 API 단가로 계산한 추정치이고, 구독 요금제 실지출과는 다르다.
"""
import json, os, sys, collections

ROOT = os.path.expanduser("~/.claude/projects")

# USD / MTok : (input, output, cache write 5m, cache read)
PRICE = {
    "opus":   (15.0, 75.0, 18.75, 1.50),
    "sonnet": ( 3.0, 15.0,  3.75, 0.30),
    "haiku":  ( 1.0,  5.0,  1.25, 0.10),
}
def tier(model: str) -> str:
    m = model.lower()
    if "opus" in m: return "opus"
    if "fable" in m or "mythos" in m: return "opus"   # Mythos급은 Opus 단가로 가정
    if "sonnet" in m: return "sonnet"
    if "haiku" in m: return "haiku"
    return "sonnet"

def collect():
    sessions, days = set(), set()
    req = 0
    tk = {"in": 0, "out": 0, "cw": 0, "cr": 0}
    by_model = collections.defaultdict(lambda: {"req": 0, "in": 0, "out": 0, "cw": 0, "cr": 0})
    for dp, _, fn in os.walk(ROOT):
        for f in fn:
            if not f.endswith(".jsonl"): continue
            try: fh = open(os.path.join(dp, f), encoding="utf-8", errors="replace")
            except OSError: continue
            with fh:
                for line in fh:
                    if '"usage"' not in line: continue
                    try: d = json.loads(line)
                    except ValueError: continue
                    if d.get("type") != "assistant": continue
                    msg = d.get("message") or {}
                    u = msg.get("usage") or {}
                    model = msg.get("model") or "unknown"
                    if model == "<synthetic>": continue
                    i  = u.get("input_tokens") or 0
                    o  = u.get("output_tokens") or 0
                    cw = u.get("cache_creation_input_tokens") or 0
                    cr = u.get("cache_read_input_tokens") or 0
                    if i + o + cw + cr == 0: continue
                    ts = d.get("timestamp") or ""
                    if ts[:10]: days.add(ts[:10])
                    if d.get("sessionId"): sessions.add(d["sessionId"])
                    req += 1
                    tk["in"] += i; tk["out"] += o; tk["cw"] += cw; tk["cr"] += cr
                    bm = by_model[model]
                    bm["req"] += 1; bm["in"] += i; bm["out"] += o; bm["cw"] += cw; bm["cr"] += cr
    return sessions, days, req, tk, by_model

def human(n: int) -> str:
    for unit, div in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if n >= div:
            v = n / div
            return f"{v:.1f}{unit}" if v < 100 else f"{v:.0f}{unit}"
    return str(n)

def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def main():
    sessions, days, req, tk, by_model = collect()
    total = sum(tk.values())
    if total == 0:
        sys.exit("집계할 사용량 레코드가 없습니다.")
    ds = sorted(days)
    period = f"{ds[0].replace('-', '.')} – {ds[-1].replace('-', '.')}"

    cost, rows = 0.0, []
    for m, v in by_model.items():
        pi, po, pw, pr = PRICE[tier(m)]
        c = v["in"]/1e6*pi + v["out"]/1e6*po + v["cw"]/1e6*pw + v["cr"]/1e6*pr
        cost += c
        rows.append((m.replace("claude-", ""), v["req"], v["in"]+v["out"]+v["cw"]+v["cr"], c))
    rows.sort(key=lambda r: -r[2])
    rows = rows[:4]

    pct = {k: tk[k] / total * 100 for k in tk}
    reuse = tk["cr"] / max(1, tk["cw"])

    W, H = 820, 418
    BG, FG, DIM, AC, GRID = "#0d1117", "#e6edf3", "#8b949e", "#58a6ff", "#21262d"
    SEG = [("read",  pct["cr"], "#58a6ff"),
           ("write", pct["cw"], "#3fb950"),
           ("out",   pct["out"], "#d29922"),
           ("in",    pct["in"],  "#f85149")]

    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">')
    a(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{GRID}"/>')
    # 헤더
    a(f'<text x="28" y="42" fill="{AC}" font-size="13" font-weight="700">&gt;_ AI CODING USAGE</text>')
    a(f'<text x="28" y="64" fill="{DIM}" font-size="12">{esc(period)}  ·  Claude Code 세션 전사 집계</text>')
    a(f'<text x="{W-28}" y="42" fill="{DIM}" font-size="12" text-anchor="end">≈ ${cost:,.0f} (공개 단가 추정)</text>')
    a(f'<line x1="28" y1="80" x2="{W-28}" y2="80" stroke="{GRID}"/>')
    # KPI 4칸
    kpis = [(f"{len(sessions):,}", "SESSIONS"), (human(req), "REQUESTS"),
            (f"{len(days)}", "ACTIVE DAYS"), (human(total), "TOKENS")]
    for i, (val, lab) in enumerate(kpis):
        x = 28 + i * ((W - 56) / 4)
        a(f'<text x="{x:.0f}" y="122" fill="{FG}" font-size="28" font-weight="700">{val}</text>')
        a(f'<text x="{x:.0f}" y="142" fill="{DIM}" font-size="11" letter-spacing="1">{lab}</text>')
    # 토큰 구성 막대
    a(f'<text x="28" y="182" fill="{DIM}" font-size="11" letter-spacing="1">TOKEN MIX</text>')
    bx, bw, by, bh = 28, W - 56, 192, 16
    cur = bx
    for name, p, col in SEG:
        w = max(1.2, bw * p / 100)
        a(f'<rect x="{cur:.1f}" y="{by}" width="{w:.1f}" height="{bh}" fill="{col}"/>')
        cur += w
    a(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3" fill="none" stroke="{GRID}"/>')
    lx = bx
    for name, p, col in SEG:
        a(f'<rect x="{lx}" y="228" width="9" height="9" rx="2" fill="{col}"/>')
        a(f'<text x="{lx+14}" y="237" fill="{DIM}" font-size="11">{name} {p:.2f}%</text>')
        lx += 130
    a(f'<text x="{W-28}" y="237" fill="{FG}" font-size="11" text-anchor="end">캐시 재사용 {reuse:.1f}× — 새로 만든 토큰 1당 다시 읽은 토큰</text>')
    # 모델별
    a(f'<text x="28" y="278" fill="{DIM}" font-size="11" letter-spacing="1">BY MODEL</text>')
    top = rows[0][2] if rows else 1
    for i, (m, r, t, c) in enumerate(rows):
        y = 300 + i * 24
        a(f'<text x="28" y="{y}" fill="{FG}" font-size="12">{esc(m)}</text>')
        w = (W - 430) * (t / top)
        a(f'<rect x="200" y="{y-10}" width="{max(2,w):.0f}" height="11" rx="2" fill="{AC}" opacity="{1 - i*0.2:.2f}"/>')
        a(f'<text x="{W-150}" y="{y}" fill="{DIM}" font-size="11" text-anchor="end">{human(t)} tok</text>')
        a(f'<text x="{W-28}" y="{y}" fill="{DIM}" font-size="11" text-anchor="end">{r:,} req</text>')
    a(f'<text x="28" y="{H-14}" fill="{DIM}" font-size="10" opacity="0.75">비용은 공개 API 단가 기준 추정이며 구독 실지출과 다릅니다 · gen_ai_usage.py 로 재생성</text>')
    a('</svg>')
    sys.stdout.write("\n".join(o))

if __name__ == "__main__":
    main()
