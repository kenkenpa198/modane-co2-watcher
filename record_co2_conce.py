import csv
from datetime import datetime as dt
import os
import mh_z19

'''
■ CO2 濃度を検証する関数
メインプログラム側のメモリサイズ超過などの対策用。

▼引数
int co2_conce : 検証する CO2 濃度

▼戻り値
int 0         : 正常値である
int 1         : 4桁を超える異常値
int 2         : マイナスである異常値

'''
def verify_co2_conce(co2_conce: int) -> int:
    if co2_conce > 9999:
        return 1
    if co2_conce < 0:
        return 2
    return 0


'''
■ メイン処理

'''
# 現在日時を取得（YYYY-MM-DD hh:mm:ss）
now = dt.now().strftime('%Y-%m-%d %H:%M:%S')

# CO2 濃度の値を取得
co2_conce = mh_z19.read_all()["co2"]
# co2_conce = 1

# 取得した値の検証と格納
if verify_co2_conce(co2_conce) == 1:
    # 4桁を超える場合は -1 に変更
    verified_co2_conce = -1
if verify_co2_conce(co2_conce) == 2:
    # 負の数値の場合は -2 に変更
    verified_co2_conce = -2
else:
    verified_co2_conce = co2_conce

# logs ディレクトリが無ければ作成
dir_path = './logs/'
os.makedirs(dir_path, exist_ok=True)

# CSV ファイルへ書き込み
filename = 'co2_conces.csv'
with open(dir_path + filename, 'a') as f:
    writer = csv.writer(f)
    writer.writerow([verified_co2_conce, now])