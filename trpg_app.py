import streamlit as st
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.objec_factory import start_game, create_enemy
from system.save_log import save_log
from system.dice import roll_dice, get_outcome_label
from llm.call_llm import call_llm
from llm.event_prompt import build_event_prompt_before, build_event_prompt_after
from llm.combat_prompt import attack_kind, build_combat_prompt, start_combat_prompt
from llm.ending_prompt import build_ending_prompt
from model.player import STAT_KO

st.set_page_config(
    page_title="LLM TRPG",
    page_icon="⚔",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600&family=Noto+Sans+KR:wght@400;500&display=swap');
.stApp { background-color: #1a1410; font-family: 'Noto Sans KR', sans-serif; }
[data-testid="stHeader"] { display: none; }

/* 메인 영역 */
.main .block-container { padding: 0 !important; max-width: 800px !important; margin: 0 auto; }

/* 사이드바 스타일 */
[data-testid="stSidebar"] {
    background: #120f0b !important;
    border-right: 1px solid #3a2e22 !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

/* 사이드바 내부 커스텀 */
.sb-title {
    font-family: 'Noto Serif KR', serif;
    font-size: 14px; font-weight: 600; color: #c9a84c;
    padding: 16px 16px 10px; border-bottom: 1px solid #3a2e22;
    display: flex; align-items: center; gap: 6px;
}
.sb-gem { width: 7px; height: 7px; border-radius: 50%; background: #c9a84c; display: inline-block; }
.sb-section { padding: 12px 16px; border-bottom: 1px solid #2a2018; }
.sb-section-title { font-size: 10px; color: #5a4e38; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px; }
.sb-stat-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.sb-stat-label { font-size: 12px; color: #8a7a60; }
.sb-stat-val { font-size: 13px; font-weight: 500; color: #e8d5a3; }
.sb-bar-wrap { width: 100%; height: 5px; background: #2a2018; border-radius: 3px; overflow: hidden; margin-top: 3px; margin-bottom: 8px; }
.sb-bar-inner { height: 100%; border-radius: 3px; transition: width 0.3s; }
.sb-ability-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
.sb-ability-item { background: #1e1a12; border: 1px solid #3a2e22; border-radius: 6px; padding: 6px 10px; }
.sb-ability-name { font-size: 10px; color: #5a4e38; }
.sb-ability-val { font-size: 16px; font-weight: 600; color: #c9a84c; }
.sb-enemy-box { background: #1e1010; border: 1px solid #6a2020; border-radius: 8px; padding: 10px 12px; }
.sb-enemy-name { font-size: 13px; font-weight: 500; color: #d4a0a0; margin-bottom: 6px; }
.sb-enemy-hp-label { font-size: 10px; color: #8a4040; margin-bottom: 3px; }
.sb-turn-box { background: #1e1a12; border: 1px solid #3a2e22; border-radius: 8px; padding: 10px 12px; text-align: center; }
.sb-turn-num { font-size: 28px; font-weight: 600; color: #c9a84c; line-height: 1; }
.sb-turn-label { font-size: 10px; color: #5a4e38; margin-top: 2px; }
.sb-phase-badge { background: #2a2018; border: 1px solid #3a2e22; border-radius: 6px; padding: 6px 10px; font-size: 11px; color: #8a7a60; text-align: center; margin-top: 8px; }

/* 헤더 */
.trpg-header { background: #120f0b; border-bottom: 1px solid #3a2e22; padding: 10px 20px; position: sticky; top: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; }
.trpg-title { font-family: 'Noto Serif KR', serif; font-size: 15px; font-weight: 600; color: #c9a84c; letter-spacing: 0.05em; display: flex; align-items: center; gap: 6px; }
.trpg-gem { width: 7px; height: 7px; border-radius: 50%; background: #c9a84c; display: inline-block; }
.trpg-header-stats { display: flex; gap: 16px; align-items: center; }
.trpg-header-stat { font-size: 11px; color: #8a7a60; display: flex; align-items: center; gap: 5px; }
.trpg-header-stat span { color: #e8d5a3; font-weight: 500; }
.stat-bar-wrap { width: 44px; height: 3px; background: #2a2018; border-radius: 2px; overflow: hidden; }
.stat-bar-inner { height: 100%; border-radius: 2px; }
.turn-badge { font-size: 11px; color: #8a7a60; }
.turn-badge span { color: #e8d5a3; font-weight: 500; }

/* 말풍선 */
.gm-bubble { background: #211c14; border: 1px solid #3a2e22; border-radius: 12px; border-top-left-radius: 2px; padding: 12px 16px; color: #d4c4a0; font-family: 'Noto Serif KR', serif; font-size: 14px; line-height: 1.8; }
.player-bubble { background: #1a2535; border: 1px solid #2a3a4a; border-radius: 12px; border-top-right-radius: 2px; padding: 10px 14px; color: #a8c8e0; font-size: 13px; line-height: 1.7; }
.system-msg { background: #1a1a10; border: 1px solid #2a2a18; border-radius: 6px; padding: 8px 14px; color: #8a8a60; font-size: 12px; font-style: italic; text-align: center; margin: 6px 0; }
.combat-banner { background: #2a1010; border: 1px solid #6a2020; border-radius: 8px; padding: 10px 16px; color: #d4a0a0; font-family: 'Noto Serif KR', serif; font-size: 13px; text-align: center; margin: 6px 0; }
.dice-block { display: flex; align-items: center; gap: 10px; background: #1a1a10; border: 1px solid #2a2a18; border-radius: 8px; padding: 8px 12px; margin-top: 10px; font-size: 12px; }
.dice-val { font-size: 20px; font-weight: 600; color: #c9a84c; min-width: 28px; text-align: center; }
.dice-label { color: #c9a84c; font-weight: 500; }
.stat-change-inline { margin-top: 8px; padding-top: 8px; border-top: 1px solid #2a2a18; font-size: 12px; }
.stat-change-title { color: #5a4e38; font-size: 11px; margin-bottom: 4px; }
.stat-change-row { display: flex; gap: 8px; flex-wrap: wrap; }
.stat-up { color: #4a9a6a; font-weight: 500; }
.stat-down { color: #c0392b; font-weight: 500; }
.stat-card-enemy { background: #1e1010; border: 1px solid #6a2020; border-radius: 8px; padding: 8px 12px; margin: 4px 0; font-size: 12px; color: #d4a0a0; line-height: 1.8; }
.combat-state { display: flex; gap: 8px; margin: 6px 0; }
.combat-state-player { flex: 1; background: #1e1a12; border: 1px solid #3a2e22; border-radius: 8px; padding: 8px 12px; font-size: 12px; color: #c9a84c; }
.combat-state-enemy { flex: 1; background: #1e1010; border: 1px solid #6a2020; border-radius: 8px; padding: 8px 12px; font-size: 12px; color: #d4a0a0; }
.phase-label { font-size: 11px; color: #5a4e38; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; padding: 0 4px; }
[data-testid="stChatMessage"] { background: transparent !important; padding: 4px 0 !important; }
[data-testid="stChatInputTextArea"] { background: #1e1a12 !important; border: 1px solid #3a2e22 !important; color: #d4c4a0 !important; font-family: 'Noto Sans KR', sans-serif !important; border-radius: 8px !important; }
[data-testid="stChatInputSubmitButton"] { background: #c9a84c !important; border-radius: 8px !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3a2e22; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ── 세션 상태 초기화 ─────────────────────────────────
def init_session():
    defaults = {
        "phase": "init",
        "messages": [],
        "player": None,
        "enemy": None,
        "play_log": "",
        "timing": 0,
        "MAX_TURNS": 3,
        "event_explain": "",
        "combat_turn": 0,
        "pending_combat": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── 헬퍼 함수 ───────────────────────────────────────
def add_message(role, content, msg_type="normal"):
    st.session_state.messages.append({"role": role, "content": content, "type": msg_type})

def render_bar(value, max_val, color):
    pct = int(value / max_val * 100) if max_val > 0 else 0
    return f'<div class="stat-bar-wrap"><div class="stat-bar-inner" style="width:{pct}%;background:{color};"></div></div>'

def get_phase_label():
    p = st.session_state.phase
    t = st.session_state.timing
    m = st.session_state.MAX_TURNS
    labels = {
        "init":         "세계관과 캐릭터를 설정하세요",
        "event_before": f"이벤트 [{t}/{m}턴] — 행동을 입력하세요",
        "event_after":  f"이벤트 [{t}/{m}턴] — 계속하려면 입력하세요",
        "combat":       f"전투 중 [{t}/{m}턴] — 전투 행동을 입력하세요",
        "ending":       "여정이 끝났습니다",
    }
    return labels.get(p, "")

def event_dice_html(roll_val, roll_label):
    if roll_label == "대성공":
        color, desc = "#4a9a6a", "행운이 깃든 최상의 결과"
    elif roll_label == "대실패":
        color, desc = "#c0392b", "최악의 상황이 펼쳐진다"
    elif int(roll_val) >= 10:
        color, desc = "#4a9a6a", "훌륭한 판정"
    elif int(roll_val) >= 7:
        color, desc = "#c9a84c", "무난한 판정"
    elif int(roll_val) >= 4:
        color, desc = "#c9a84c", "아슬아슬한 판정"
    else:
        color, desc = "#c0392b", "좋지 않은 판정"
    return (
        f'<div class="dice-block"><div class="dice-val">{roll_val}</div>'
        f'<div><div class="dice-label" style="color:{color};">{roll_label}</div>'
        f'<div style="color:#5a4e38;font-size:11px;">{desc}</div></div></div>'
    )

def combat_dice_html(roll_val, roll_label, acc, dmg_cf):
    acc_color = "#4a9a6a" if acc >= 80 else "#c9a84c" if acc >= 50 else "#c0392b"
    return (
        f'<div class="dice-block"><div class="dice-val">{roll_val}</div>'
        f'<div><div class="dice-label">{roll_label}</div>'
        f'<div style="color:{acc_color};font-size:11px;">명중률 {acc}% · 공격배율 {dmg_cf}x</div></div></div>'
    )

def stat_change_inline_html(changes_before_after):
    items = []
    for name, before, after in changes_before_after:
        diff = after - before
        cls = "stat-up" if diff > 0 else "stat-down"
        prefix = "+" if diff > 0 else ""
        items.append(f'<span class="{cls}">{name} {before} → {after} ({prefix}{diff})</span>')
    return (
        f'<div class="stat-change-inline">'
        f'<div class="stat-change-title">능력치 변화</div>'
        f'<div class="stat-change-row">{"".join(items)}</div></div>'
    )

def enemy_stat_card(enemy):
    patterns = " / ".join([p["name"] for p in enemy.special_patterns])
    return (
        f'<div class="stat-card-enemy"><b>[ 적 정보 — {enemy.name} ]</b><br>'
        f'종류: {enemy.species} &nbsp;|&nbsp; ❤ 체력 {enemy.hp} &nbsp;|&nbsp; ⚔ 공격력 {enemy.atk}<br>'
        f'설명: {enemy.description}<br>특수 행동: {patterns}</div>'
    )

def combat_state_html(player, enemy):
    return (
        f'<div class="combat-state">'
        f'<div class="combat-state-player"><b>{player.name}</b><br>'
        f'❤ {player.hp} &nbsp;|&nbsp; 💙 {player.wp}</div>'
        f'<div class="combat-state-enemy"><b>{enemy.name}</b><br>'
        f'❤ 체력 {enemy.hp}</div></div>'
    )

def _do_ending():
    with st.spinner("엔딩을 생성하는 중..."):
        end = call_llm(build_ending_prompt(st.session_state.play_log))
    title   = end["ending"]["title"]
    summary = end["ending"]["summary"]
    add_message("system", f"— {title} —")
    add_message("gm", summary)
    st.session_state.play_log += f"\n[엔딩]\n{title}\n{summary}"
    save_log(st.session_state.play_log)
    st.session_state.phase = "ending"


# ── 사이드바 ─────────────────────────────────────────
def render_sidebar():
    p = st.session_state.player
    e = st.session_state.enemy

    with st.sidebar:
        st.markdown('<div class="sb-title"><span class="sb-gem"></span> 캐릭터 상태</div>', unsafe_allow_html=True)

        if p is None:
            st.markdown('<div style="padding:16px;color:#5a4e38;font-size:12px;">게임 시작 후 표시됩니다.</div>', unsafe_allow_html=True)
            return

        # 턴 + 페이즈
        t = st.session_state.timing
        m = st.session_state.MAX_TURNS
        phase_map = {
            "init": "준비", "event_before": "이벤트",
            "event_after": "이벤트", "combat": "⚔ 전투", "ending": "엔딩"
        }
        phase_ko = phase_map.get(st.session_state.phase, "")

        st.markdown(f"""
        <div class="sb-section">
            <div class="sb-turn-box">
                <div class="sb-turn-num">{t} / {m}</div>
                <div class="sb-turn-label">현재 턴</div>
            </div>
            <div class="sb-phase-badge">{phase_ko}</div>
        </div>
        """, unsafe_allow_html=True)

        # 체력 / 정신력 바
        hp_pct = int(p.hp / 100 * 100)
        wp_pct = int(p.wp / 100 * 100)
        hp_color = "#c0392b" if p.hp <= 20 else "#e67e22" if p.hp <= 40 else "#c0392b"
        st.markdown(f"""
        <div class="sb-section">
            <div class="sb-section-title">생존 수치</div>
            <div class="sb-stat-row">
                <span class="sb-stat-label">❤ 체력</span>
                <span class="sb-stat-val">{p.hp}</span>
            </div>
            <div class="sb-bar-wrap"><div class="sb-bar-inner" style="width:{hp_pct}%;background:#c0392b;"></div></div>
            <div class="sb-stat-row">
                <span class="sb-stat-label">💙 정신력</span>
                <span class="sb-stat-val">{p.wp}</span>
            </div>
            <div class="sb-bar-wrap"><div class="sb-bar-inner" style="width:{wp_pct}%;background:#2980b9;"></div></div>
        </div>
        """, unsafe_allow_html=True)

        # 능력치 그리드
        st.markdown(f"""
        <div class="sb-section">
            <div class="sb-section-title">능력치</div>
            <div class="sb-ability-grid">
                <div class="sb-ability-item">
                    <div class="sb-ability-name">힘</div>
                    <div class="sb-ability-val">{p.str_}</div>
                </div>
                <div class="sb-ability-item">
                    <div class="sb-ability-name">민첩</div>
                    <div class="sb-ability-val">{p.dex_}</div>
                </div>
                <div class="sb-ability-item">
                    <div class="sb-ability-name">지능</div>
                    <div class="sb-ability-val">{p.int_}</div>
                </div>
                <div class="sb-ability-item">
                    <div class="sb-ability-name">화술</div>
                    <div class="sb-ability-val">{p.char_}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 전투 중일 때 적 상태
        if e is not None:
            en_pct = int(e.hp / 30 * 100)
            st.markdown(f"""
            <div class="sb-section">
                <div class="sb-section-title">교전 중인 적</div>
                <div class="sb-enemy-box">
                    <div class="sb-enemy-name">⚔ {e.name}</div>
                    <div class="sb-enemy-hp-label">❤ 체력 {e.hp}</div>
                    <div class="sb-bar-wrap"><div class="sb-bar-inner" style="width:{min(en_pct,100)}%;background:#8a2020;"></div></div>
                    <div style="font-size:11px;color:#5a4e38;margin-top:4px;">공격력 {e.atk} | {e.species}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 캐릭터 기본 정보
        st.markdown(f"""
        <div class="sb-section">
            <div class="sb-section-title">캐릭터 정보</div>
            <div style="font-size:13px;color:#c9a84c;font-weight:500;">{p.name}</div>
            <div style="font-size:11px;color:#8a7a60;margin-top:2px;">{p.role}</div>
            <div style="font-size:11px;color:#5a4e38;margin-top:6px;line-height:1.6;">{p.explain}</div>
        </div>
        """, unsafe_allow_html=True)

render_sidebar()


# ── 상단 헤더 (간소화) ───────────────────────────────
p = st.session_state.player
hp_val = p.hp if p else 0
wp_val = p.wp if p else 0

hp_bar = render_bar(hp_val, 100, "#c0392b")
wp_bar = render_bar(wp_val, 100, "#2980b9")

st.markdown(f"""
<div class="trpg-header">
    <div class="trpg-title"><span class="trpg-gem"></span> LLM TRPG</div>
    <div class="trpg-header-stats">
        <div class="trpg-header-stat">❤ {hp_bar} <span>{hp_val}</span></div>
        <div class="trpg-header-stat">💙 {wp_bar} <span>{wp_val}</span></div>
        <div class="turn-badge">턴 <span>{st.session_state.timing}/{st.session_state.MAX_TURNS}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── 메시지 렌더링 ────────────────────────────────────
for msg in st.session_state.messages:
    if msg["type"] == "system":
        st.markdown(f'<div class="system-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["type"] == "stat":
        st.markdown(msg["content"], unsafe_allow_html=True)
    elif msg["type"] == "combat":
        st.markdown(f'<div class="combat-banner">⚔ {msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "gm":
        with st.chat_message("assistant", avatar="⚔"):
            st.markdown(f'<div class="gm-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "player":
        with st.chat_message("user", avatar="🧙"):
            st.markdown(f'<div class="player-bubble">{msg["content"]}</div>', unsafe_allow_html=True)


# ── PHASE: init ──────────────────────────────────────
if st.session_state.phase == "init":
    st.markdown(f'<div class="phase-label">{get_phase_label()}</div>', unsafe_allow_html=True)
    with st.form("init_form"):
        bg = st.text_input("세계관(배경 설정)", placeholder="예) 증기기관이 지배하는 스팀펑크 도시...")
        ch = st.text_input("캐릭터 정보", placeholder="예) 기억을 잃은 전직 기사, 이름은 카엘...")
        submitted = st.form_submit_button("모험 시작", use_container_width=True)

    if submitted and bg and ch:
        with st.spinner("세계관을 생성하는 중..."):
            background, player = start_game(bg, ch)
        st.session_state.player = player
        st.session_state.play_log = f"세계관: {background}\n플레이어 정보: {player.get_stats()}"
        add_message("system", f"⚔ 세계관: {background}")

        with st.spinner("첫 번째 이벤트를 생성하는 중..."):
            event_data = call_llm(build_event_prompt_before(st.session_state.play_log))
        st.session_state.event_explain = event_data["event"]["explain"]
        add_message("gm", st.session_state.event_explain)
        st.session_state.phase = "event_before"
        st.rerun()


# ── PHASE: event_before ──────────────────────────────
elif st.session_state.phase == "event_before":
    st.markdown(f'<div class="phase-label">{get_phase_label()}</div>', unsafe_allow_html=True)
    user_input = st.chat_input("행동을 입력하세요...")

    if user_input:
        add_message("player", user_input)
        roll       = get_outcome_label(roll_dice())
        roll_val   = roll["roll_result"]
        roll_label = roll["label"]

        with st.spinner("결과를 처리하는 중..."):
            event_result = call_llm(
                build_event_prompt_after(st.session_state.event_explain, user_input, roll_label)
            )

        explain      = event_result["event"]["explain"]
        stat_changes = event_result["event"].get("type", {})
        player       = st.session_state.player

        stat_snapshot = {
            "hp": player.hp, "wp": player.wp,
            "str_": player.str_, "dex_": player.dex_,
            "int_": player.int_, "char_": player.char_,
        }
        for stat, val in stat_changes.items():
            player.update_stat(stat, val)

        changes_before_after = []
        for stat in stat_changes:
            name   = STAT_KO.get(stat, stat)
            before = stat_snapshot.get(stat, 0)
            after  = getattr(player, stat, 0)
            if before != after:
                changes_before_after.append((name, before, after))

        gm_msg = explain
        gm_msg += f'<br>{event_dice_html(roll_val, roll_label)}'
        if changes_before_after:
            gm_msg += stat_change_inline_html(changes_before_after)
        add_message("gm", gm_msg)

        st.session_state.play_log += f"\n[이벤트]\n{st.session_state.event_explain}\n[플레이어]: {user_input}\n[결과]: {explain}"
        st.session_state.timing += 1

        dead, dead_log = player.is_dead()
        if dead:
            add_message("system", f"— {dead_log} —")
            add_message("system", "— 게임 오버 —")
            _do_ending()
            st.rerun()
            st.stop()

        if random.random() < 0.6 and st.session_state.timing <= st.session_state.MAX_TURNS:
            st.session_state.pending_combat = True
        elif st.session_state.timing >= st.session_state.MAX_TURNS:
            _do_ending()
            st.rerun()
            st.stop()
        else:
            st.session_state.pending_combat = False

        st.session_state.phase = "event_after"
        st.rerun()


# ── PHASE: event_after ───────────────────────────────
elif st.session_state.phase == "event_after":
    st.markdown(f'<div class="phase-label">{get_phase_label()}</div>', unsafe_allow_html=True)
    user_input = st.chat_input("계속하기...")

    if user_input:
        player = st.session_state.player
        add_message("player", user_input)

        if st.session_state.pending_combat:
            with st.spinner("적을 생성하는 중..."):
                enemy = create_enemy(st.session_state.play_log)
            st.session_state.enemy = enemy
            add_message("combat", f"적이 등장했습니다 — {enemy.name}")
            add_message("", enemy_stat_card(enemy), msg_type="stat")

            with st.spinner("전투를 시작하는 중..."):
                combat_intro = call_llm(start_combat_prompt(f"{player.get_stats()}\n{enemy.get_stats()}"))["explain"]
            st.session_state.combat_turn = 0
            add_message("gm", combat_intro)
            st.session_state.phase = "combat"
        else:
            with st.spinner("다음 이벤트를 생성하는 중..."):
                event_data = call_llm(build_event_prompt_before(st.session_state.play_log))
            st.session_state.event_explain = event_data["event"]["explain"]
            add_message("gm", st.session_state.event_explain)
            st.session_state.phase = "event_before"

        st.rerun()


# ── PHASE: combat ────────────────────────────────────
elif st.session_state.phase == "combat":
    st.markdown(f'<div class="phase-label">{get_phase_label()}</div>', unsafe_allow_html=True)
    user_input = st.chat_input("전투 행동을 입력하세요...")

    if user_input:
        player = st.session_state.player
        enemy  = st.session_state.enemy
        add_message("player", user_input)
        combat_log = ""
        roll_str = ""
        enemy_roll_str = ""

        with st.spinner("행동을 처리하는 중..."):
            action = call_llm(attack_kind(user_input))

        if action["action"]["type"] == "attack":
            attack_info = player.attack(user_input, action["action"]["stat"])
            damage_log  = enemy.apply_damage(
                player.name, user_input,
                attack_info["dmg"], attack_info["acc"],
                attack_info["roll"]["roll_result"]
            )
            combat_log += f"[플레이어 공격]\n{damage_log}"
            roll_str = combat_dice_html(
                attack_info["roll"]["roll_result"], attack_info["roll"]["label"],
                attack_info["roll"]["acc"], attack_info["roll"]["dmgCf"]
            )
        else:
            combat_log += f"[플레이어 강화]\n{player.strength(user_input, action['action']['stat'])}"

        enemy_dead, dead_log = enemy.is_dead()
        if enemy_dead:
            combat_log += f"\n{dead_log}"
            with st.spinner("전투 결과를 묘사하는 중..."):
                combat_desc = call_llm(build_combat_prompt(combat_log))["explain"]
            add_message("gm", f'{combat_desc}<br>{roll_str}')
            add_message("combat", f"{enemy.name} 쓰러짐 — 전투 승리!")
            st.session_state.play_log += f"\n[전투 승리]\n{combat_log}"
            st.session_state.enemy = None

            if st.session_state.timing >= st.session_state.MAX_TURNS:
                _do_ending()
            else:
                st.session_state.pending_combat = False
                st.session_state.phase = "event_after"
            st.rerun()
            st.stop()

        pattern = random.choice(enemy.special_patterns)
        if pattern["type"]["kind"] == "attack":
            attack_info    = enemy.attack(pattern)
            player_dmg_log = player.apply_damage(
                enemy.name, pattern["name"],
                attack_info["dmg"], attack_info["acc"],
                pattern["type"]["stat"], attack_info["roll"]["roll_result"]
            )
            combat_log    += f"\n[적 공격]\n{player_dmg_log}"
            enemy_roll_str = combat_dice_html(
                attack_info["roll"]["roll_result"], attack_info["roll"]["label"],
                attack_info["roll"]["acc"], attack_info["roll"]["dmgCf"]
            )
        else:
            combat_log += f"\n[적 강화]\n{enemy.strength(pattern)}"

        with st.spinner("전투를 묘사하는 중..."):
            combat_desc = call_llm(build_combat_prompt(combat_log))["explain"]
        add_message("gm", f'{combat_desc}<br>{roll_str}{enemy_roll_str}')
        add_message("", combat_state_html(player, enemy), msg_type="stat")

        player_dead, dead_log = player.is_dead()
        if player_dead:
            add_message("system", f"— {dead_log} —")
            add_message("system", "— 게임 오버 —")
            st.session_state.play_log += f"\n[전투 패배]\n{combat_log}"
            _do_ending()
            st.rerun()
            st.stop()

        st.session_state.play_log += f"\n[전투]\n{combat_log}"
        st.session_state.combat_turn += 1
        st.rerun()


# ── PHASE: ending ────────────────────────────────────
elif st.session_state.phase == "ending":
    st.markdown('<div class="system-msg">— 여정이 끝났습니다. 새로운 모험을 시작하려면 새로고침하세요 —</div>', unsafe_allow_html=True)
