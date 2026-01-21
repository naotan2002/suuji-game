
import streamlit as st
import random

# --- ページの設定 ---
st.set_page_config(page_title="数当てサバイバル", page_icon="🎮")
st.title("🎮 数当てサバイバル：Web版")

# --- 警告メッセージ（ルール説明） ---
st.warning("⚠️ 数字が近いとマイナス値が高くなる！！得点が０になるとGAME OVER！！")

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
    st.session_state.history = []

# --- サイドパネル（現在のステータス） ---
st.sidebar.header("ステータス")
st.sidebar.metric("持ち点", f"{st.session_state.score} 点")
st.sidebar.metric("正解数", f"{st.session_state.win_count} / 5")
st.sidebar.write(f"現在の難易度: **{st.session_state.difficulty[0]}**")

# --- メイン画面 ---
st.info(st.session_state.message)

# --- 入力フォーム（エンターキー対応） ---
if not st.session_state.game_over and st.session_state.win_count < 5:
    # clear_on_submit=True により、送信後に枠内が空になります
    with st.form(key='guess_form', clear_on_submit=True):
        # 文字入力として受け取り、後で数字かどうかチェックします
        user_input = st.text_input(
            "1-100の数字を入力してください（Enterで回答）", 
            placeholder="例: 50"
        )
        submit = st.form_submit_button("回答する")

    if submit:
        # --- 入力チェックロジック ---
        # 1. 空文字ではないか、2. 数字のみか、3. 1-100の範囲内か
        if not user_input or not user_input.isdigit() or not (1 <= int(user_input) <= 100):
            st.error("1～100までの半角数字を入力してください")
        else:
            guess = int(user_input)
            diff = abs(guess - st.session_state.secret_number)
            
            if diff == 0:
                st.session_state.win_count += 1
                st.session_state.score += 100
                st.session_state.history = [] # 正解で履歴リセット
                st.session_state.secret_number = random.randint(1, 100)
                st.session_state.difficulty = random.choice([("難易度大", 100), ("難易度中", 75), ("難易度小", 50)])
                st.session_state.message = "☆正解！ボーナス+100点！ 次の問題です。"
                st.balloons()
            else:
                penalty = calculate_penalty(diff, st.session_state.difficulty[1])
                st.session_state.score -= penalty
                hint = "もっと大きいよ" if guess < st.session_state.secret_number else "もっと小さいよ"
                
                # 履歴に追加
                res_text = f"【{len(st.session_state.history)+1}回目】 {guess} ⇒ {hint} （-{penalty}点）"
                st.session_state.history.append(res_text)
                st.session_state.message = f"はずれ！ {hint}"

            if st.session_state.score <= 0:
                st.session_state.game_over = True
            
            st.rerun()

# --- 履歴の表示エリア ---
if st.session_state.history:
    st.write("---")
    st.subheader("これまでのヒント")
    for h in reversed(st.session_state.history):
        st.write(h)

# ゲームオーバー・クリア判定
if st.session_state.game_over:
    st.error(f"GAME OVER... 正解は {st.session_state.secret_number} でした。")
if st.session_state.win_count >= 5:
    st.success(f"MISSION COMPLETE! 最終スコア: {st.session_state.score}点")
    st.confetti()

# リセットボタン
if st.button("最初からやり直す"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()