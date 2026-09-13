#!/usr/bin/env python3
"""
로컬 AI 코딩 도구의 세션 기록을 집계해 사용량 카드(SVG)를 만든다.

  python3 gen_ai_usage.py > ai-usage.svg

집계 대상
  Claude Code : ~/.claude/projects/**/*.jsonl 의 assistant 메시지 message.usage
  Codex       : ~/.codex/sessions/**/*.jsonl 의 token_count 이벤트 중
                info.total_token_usage (세션 누적이므로 세션별 마지막 값을 사용)

model 이 <synthetic> 이거나 토큰이 전부 0 인 레코드는 뺀다.
비용은 공개 API 단가로 환산한 추정치이고 구독 요금제 실지출과 다르다.
"""
import json, os, sys, collections

CLAUDE_ROOT = os.path.expanduser("~/.claude/projects")
CODEX_ROOT = os.path.expanduser("~/.codex/sessions")

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


def collect_claude():
    sessions, days = set(), set()
    req = 0
    tk = {"in": 0, "out": 0, "cw": 0, "cr": 0}
    by_model = collections.defaultdict(lambda: {"req": 0, "in": 0, "out": 0, "cw": 0, "cr": 0})
    for dp, _, fn in os.walk(CLAUDE_ROOT):
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
    return {"sessions": len(sessions), "days": days, "req": req, "tk": tk, "by_model": by_model}


def collect_codex():
    sessions = 0
    turns = 0
    days = set()
    tk = {"in": 0, "cached": 0, "out": 0, "reason": 0, "total": 0}
    models = collections.Counter()
    for dp, _, fn in os.walk(CODEX_ROOT):
        for f in fn:
            if not f.endswith(".jsonl"): continue
            last, sday, smodels = None, None, set()
            try: fh = open(os.path.join(dp, f), encoding="utf-8", errors="replace")
            except OSError: continue
            with fh:
                for line in fh:
                    if '"token_count"' in line:
                        try: d = json.loads(line)
                        except ValueError: continue
                        info = (d.get("payload") or {}).get("info")
                        if info and info.get("total_token_usage"):
                            last = info["total_token_usage"]
                            if d.get("timestamp"): sday = d["timestamp"][:10]
                    elif '"turn_context"' in line:
                        try: d = json.loads(line)
                        except ValueError: continue
                        p = d.get("payload") or {}
                        m = p.get("model") or p.get("model_slug")
                        if m: smodels.add(m); turns += 1
                        if not sday and d.get("timestamp"): sday = d["timestamp"][:10]
            if last:
                sessions += 1
                tk["in"]     += last.get("input_tokens", 0)
                tk["cached"] += last.get("cached_input_tokens", 0)
                tk["out"]    += last.get("output_tokens", 0)
                tk["reason"] += last.get("reasoning_output_tokens", 0)
                tk["total"]  += last.get("total_tokens", 0)
                if sday: days.add(sday)
                for m in smodels: models[m] += 1
    return {"sessions": sessions, "turns": turns, "days": days, "tk": tk, "models": models}


def human(n: int) -> str:
    for unit, div in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if n >= div:
            v = n / div
            return f"{v:.1f}{unit}" if v < 100 else f"{v:.0f}{unit}"
    return str(n)

def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    cl = collect_claude()
    cx = collect_codex()
    cl_total = sum(cl["tk"].values())
    cx_total = cx["tk"]["total"]
    if cl_total == 0 and cx_total == 0:
        sys.exit("집계할 사용량 레코드가 없습니다.")

    days = sorted(cl["days"] | cx["days"])
    period = f"{days[0].replace('-', '.')} – {days[-1].replace('-', '.')}" if days else "-"

    cost = 0.0
    rows = []
    for m, v in cl["by_model"].items():
        pi, po, pw, pr = PRICE[tier(m)]
        c = v["in"]/1e6*pi + v["out"]/1e6*po + v["cw"]/1e6*pw + v["cr"]/1e6*pr
        cost += c
        rows.append((m.replace("claude-", ""), v["req"], v["in"]+v["out"]+v["cw"]+v["cr"], "claude"))
    for m, cnt in cx["models"].items():
        rows.append((m, cnt, 0, "codex"))
    rows = [r for r in rows if r[3] == "claude"]
    rows.sort(key=lambda r: -r[2])
    rows = rows[:4]

    pct = {k: cl["tk"][k] / cl_total * 100 for k in cl["tk"]}
    reuse = cl["tk"]["cr"] / max(1, cl["tk"]["cw"])
    grand = cl_total + cx_total
    cx_share = cx_total / grand * 100 if grand else 0

    W, H = 860, 492
    BG, FG, DIM, AC, AC2, GRID = "#0d1117", "#e6edf3", "#8b949e", "#58a6ff", "#3fb950", "#21262d"
    o = []; a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">')
    a(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{GRID}"/>')
    a(f'<text x="28" y="40" fill="{AC}" font-size="13" font-weight="700">&gt;_ AI PAIR — 쓴 것과 맡긴 범위</text>')
    a(f'<text x="28" y="61" fill="{DIM}" font-size="11">{esc(period)}  ·  로컬 세션 기록 집계</text>')
    a(f'<text x="{W-28}" y="40" fill="{DIM}" font-size="11" text-anchor="end">≈ ${cost:,.0f} 추정 (공개 API 단가)</text>')
    a(f'<line x1="28" y1="76" x2="{W-28}" y2="76" stroke="{GRID}"/>')

    # 두 도구 블록
    colw = (W - 56 - 24) / 2
    blocks = [
        ("CLAUDE CODE", "초안 · 구현", AC,
         [(f"{cl['sessions']:,}", "sessions"), (human(cl["req"]), "requests"), (human(cl_total), "tokens")]),
        ("CODEX", "리뷰 · 반증", AC2,
         [(f"{cx['sessions']:,}", "sessions"), (f"{cx['turns']:,}", "turns"), (human(cx_total), "tokens")]),
    ]
    for bi, (name, role, col, kpis) in enumerate(blocks):
        bx = 28 + bi * (colw + 24)
        a(f'<rect x="{bx:.0f}" y="92" width="{colw:.0f}" height="96" rx="7" fill="#11161d" stroke="{GRID}"/>')
        a(f'<rect x="{bx:.0f}" y="92" width="3" height="96" rx="2" fill="{col}"/>')
        a(f'<text x="{bx+16:.0f}" y="114" fill="{col}" font-size="12" font-weight="700">{name}</text>')
        a(f'<text x="{bx+colw-16:.0f}" y="114" fill="{DIM}" font-size="11" text-anchor="end">{role}</text>')
        for ki, (val, lab) in enumerate(kpis):
            kx = bx + 16 + ki * ((colw - 32) / 3)
            a(f'<text x="{kx:.0f}" y="152" fill="{FG}" font-size="21" font-weight="700">{val}</text>')
            a(f'<text x="{kx:.0f}" y="171" fill="{DIM}" font-size="10">{lab}</text>')

    # 토큰 배분
    a(f'<text x="28" y="216" fill="{DIM}" font-size="10" letter-spacing="1">토큰 배분 — 쓰는 데 몰리고, 검토는 적은 횟수로 정확히</text>')
    bx, bw, by, bh = 28, W - 56, 226, 13
    wcl = bw * (cl_total / grand); wcx = max(2.0, bw - wcl)
    a(f'<rect x="{bx}" y="{by}" width="{wcl:.1f}" height="{bh}" rx="2" fill="{AC}"/>')
    a(f'<rect x="{bx+wcl:.1f}" y="{by}" width="{wcx:.1f}" height="{bh}" rx="2" fill="{AC2}"/>')
    a(f'<text x="28" y="258" fill="{DIM}" font-size="10">Claude {100-cx_share:.1f}%  ·  Codex {cx_share:.1f}%  '
      f'— 리뷰는 토큰을 적게 쓰지만 되돌린 판단은 여기서 나온다</text>')

    # Claude 토큰 구성
    a(f'<text x="28" y="294" fill="{DIM}" font-size="10" letter-spacing="1">CLAUDE 토큰 구성</text>')
    SEG = [("read", pct["cr"], AC), ("write", pct["cw"], AC2), ("out", pct["out"], "#d29922"), ("in", pct["in"], "#f85149")]
    by2 = 304; cur = bx
    for _, p, c in SEG:
        w = max(1.2, bw * p / 100)
        a(f'<rect x="{cur:.1f}" y="{by2}" width="{w:.1f}" height="{bh}" fill="{c}"/>')
        cur += w
    a(f'<rect x="{bx}" y="{by2}" width="{bw}" height="{bh}" rx="2" fill="none" stroke="{GRID}"/>')
    lx = bx
    for nm, p, c in SEG:
        a(f'<rect x="{lx}" y="333" width="8" height="8" rx="2" fill="{c}"/>')
        a(f'<text x="{lx+12}" y="341" fill="{DIM}" font-size="10">{nm} {p:.2f}%</text>')
        lx += 112
    a(f'<text x="{W-28}" y="341" fill="{FG}" font-size="10" text-anchor="end">'
      f'캐시 재사용 {reuse:.1f}× — 맥락을 다시 올리지 않게 작업을 잘라 둔 결과</text>')

    # 모델별
    a(f'<text x="28" y="378" fill="{DIM}" font-size="10" letter-spacing="1">CLAUDE 모델별</text>')
    top = rows[0][2] if rows else 1
    for i, (m, r, t, _) in enumerate(rows):
        y = 398 + i * 20
        a(f'<text x="28" y="{y}" fill="{FG}" font-size="11">{esc(m)}</text>')
        w = (W - 460) * (t / top)
        a(f'<rect x="190" y="{y-9}" width="{max(2,w):.0f}" height="10" rx="2" fill="{AC}" opacity="{1-i*0.2:.2f}"/>')
        a(f'<text x="{W-140}" y="{y}" fill="{DIM}" font-size="10" text-anchor="end">{human(t)} tok</text>')
        a(f'<text x="{W-28}" y="{y}" fill="{DIM}" font-size="10" text-anchor="end">{r:,} req</text>')
    cxm = " · ".join(m for m, _ in cx["models"].most_common(3))
    a(f'<text x="{W-28}" y="378" fill="{DIM}" font-size="10" text-anchor="end">CODEX: {esc(cxm)}</text>')
    a(f'<text x="28" y="{H-14}" fill="{DIM}" font-size="9" opacity="0.7">'
      f'비용은 공개 API 단가 기준 추정이며 구독 실지출과 다릅니다 · gen_ai_usage.py 로 재생성</text>')
    a('</svg>')
    sys.stdout.write("\n".join(o))


if __name__ == "__main__":
    main()
