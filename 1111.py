
import random

# --- 関数定義：ペナルティの計算 ---
def calculate_penalty(difference, difficulty_value):
    if difference == 0:
        return 0

    # 計算式: penalty_base = 難易度 // (2の「差-1」乗)
    penalty_base = difficulty_value // (2 ** (difference - 1))

    if penalty_base >= 1:
        penalty = random.randint(1, penalty_base)
    else:
        penalty = 0

    return penalty

# --- メイン処理 ---
score = 100
win_count = 0
max_wins = 5

difficulty_level = {"難易度大": 100, "難易度中": 75, "難易度小": 50}

print("【数当てサバイバル：難易度変化版】")
print(f"5回正解でクリア！ 1～100までの数字を当てよう。")
print("正解に近い時にはマイナスポイントが大きい可能性は高くなる")
print("-" * 30)

while score > 0 and win_count < max_wins:
    level_name = random.choice(list(difficulty_level.keys()))
    level_value = difficulty_level[level_name]

    secret_number = random.randint(1, 100)

    print(f"\n★第 {win_count + 1} 問目開始！")
    print(f"【現在の難易度: {level_name}】")

    while True:
        user_input = input(f"（持ち点: {score}）1-100の数字を入力: ")

        try:
            guessed_number = int(user_input)
            if not (1 <= guessed_number <= 100):
                print("1-100の範囲で入れてね。")
                continue

            # 内部では「差」を計算するが、表示はしない
            diff = abs(guessed_number - secret_number)

            if diff == 0:
                win_count += 1
                score += 100
                print(f"☆正解！ボーナス+100点！ (合計正解数: {win_count}/{max_wins})")
                break
            else:
                penalty = calculate_penalty(diff, level_value)
                score -= penalty

                # --- 修正箇所：(差:{diff}) の表示を削除 ---
                print(f"はずれ！ 減少ポイント: -{penalty}")

                if score <= 0:
                    print("-" * 30)
                    print(f"正解は {secret_number} でした。")
                    print("点数が0になりました。ゲームオーバー...")
                    break

                # ヒント（これがないとクリアが非常に困難になるため残しています）
                if guessed_number < secret_number:
                    print("もっと大きいよ。")
                else:
                    print("もっと小さいよ。")

        except ValueError:
            print("無効な入力です。数字を入力してください。")

    if win_count >= max_wins:
        print("\n" + "="*40)
        print(f"MISSION COMPLETE! 見事{max_wins}問正解しました！")
        print(f"最終残りスコア: {score}点")
        print("="*40)

print("\nゲームを終了します。")
