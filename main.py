
import streamlit as st
import random

# --- ページの設定 ---
st.set_page_config(page_title="数当てサバイバル", page_icon="🎮")
st.title("🎮 数当てサバイバル：Web版")

# --- ペナルティ計算の関数 ---
def calculate_penalty(difference, difficulty_value):
    if difference == 0: return 0
    penalty_base = difficulty_value // (2 ** (difference - 1))
    return random.randint(1, max(1, penalty_base)) if penalty_base >= 1 else 0

# --- ゲーム状態の初期化 ---
if 'score' not in st.session_state:
    st.session_state.score = 100
    st.session_state.win_count = 0
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.difficulty = random.choice([("難易度大", 100), ("難易度中", 75), ("難易度小", 50)])
    st.session_state.message = "1～100までの数字を当てよう！5回正解でクリア。"
    st.session_state.game_over = False
    st.session_state.history = [] # ★履歴を保存するリストを追加

# --- サイドパネル（現在のステータス） ---
st.sidebar.header("ステータス")
st.sidebar.metric("持ち点", f"{st.session_state.score} 点")
st.sidebar.metric("正解数", f"{st.session_state.win_count} / 5")
st.sidebar.write(f"現在の難易度: **{st.session_state.difficulty[0]}**")

# --- メイン画面 ---
st.info(st.session_state.message)

# --- 入力フォーム ---
if not st.session_state.game_over and st.session_state.win_count < 5:
    with st.form(key='guess_form', clear_on_submit=True):
        guess = st.number_input("1-100の数字を入力してください", min_value=1, max_value=100)
        submit = st.form_submit_button("回答する")

    if submit:
        diff = abs(guess - st.session_state.secret_number)
        
        if diff == 0:
            st.session_state.win_count += 1
            st.session_state.score += 100
            st.session_state.history = [] # 正解したら履歴をリセット
            st.session_state.secret_number = random.randint(1, 100)
            st.session_state.difficulty = random.choice([("難易度大", 100), ("難易度中", 75), ("難易度小", 50)])
            st.session_state.message = f"☆正解！ボーナス+100点！ 次の問題です。"
            st.balloons()
        else:
            penalty = calculate_penalty(diff, st.session_state.difficulty[1])
            st.session_state.score -= penalty
            hint = "もっと大きいよ" if guess < st.session_state.secret_number else "もっと小さいよ"
            
            # ★履歴に今回の結果を追加する
            res_text = f"【{len(st.session_state.history)+1}回目】 {guess} ⇒ {hint} （-{penalty}点）"
            st.session_state.history.append(res_text)
            st.session_state.message = f"はずれ！ {hint}"

        if st.session_state.score <= 0:
            st.session_state.game_over = True
        
        st.rerun()

# --- ★履歴の表示エリア ---
if st.session_state.history:
    st.write("---")
    st.subheader("これまでのヒント")
    # 新しい履歴が上にくるように表示
    for h in reversed(st.session_state.history):
        st.write(h)

# ゲームオーバー・クリア判定
if st.session_state.game_over:
    st.error(f"ゲームオーバー... 正解は {st.session_state.secret_number} でした。")
if st.session_state.win_count >= 5:
    st.success(f"MISSION COMPLETE! 最終スコア: {st.session_state.score}点")
    st.confetti()

# リセットボタン
if st.button("ゲームをリセット"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()