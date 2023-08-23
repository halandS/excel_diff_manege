import pandas as pd
import numpy as np
import os

# 小さい行を大きい行に合わせる関数
def match_datasize(data1,data2):
    # 両方のデータフレームの行数と列数を確認
    num_rows_df1, num_cols_df1 = data1.shape
    num_rows_df2, num_cols_df2 = data2.shape

    # 行数が小さいデータフレームを大きい方に合わせる
    if num_rows_df1 < num_rows_df2:
        data1 = data1.reindex(index=range(num_rows_df2), 
                              fill_value=np.nan)
    elif num_rows_df1 == num_rows_df2:
        pass
    else:
        data2 = data2.reindex(index=range(num_rows_df1), 
                              fill_value=np.nan)


    # 列に対しても同様の処理
    if num_cols_df1 < num_cols_df2:
        data1 = data1.reindex(columns=range(num_cols_df2), 
                              fill_value=np.nan)
    elif num_cols_df1 == num_cols_df2:
        pass
    else:
        data2 = data2.reindex(columns=range(num_cols_df1), 
                              fill_value=np.nan)
    
    return data1, data2


# ファイル書き込みに関する関数
def make_file(type='csv'):
    base_filename = f'check.{type}'
    name, ext = os.path.splitext(base_filename)
    filename = base_filename
    counter = 1
    # ファイル名の重複を避けるために、カウンターを作成
    while os.path.exists(filename):
        filename = f"{name}_{counter}{ext}"
        counter += 1
    return filename


# 差分を取得し格納する関数
def get_diff(data1,data2,file_type='csv'):
    # 差分の確認
    diff_data = pd.DataFrame(columns=
                             ["行", "列", "変更前", "変更後"])
    for i in range(max(data1.shape[0],data2.shape[0])):
        for k in range(max(data1.shape[1],data2.shape[1])):
            if data1.iloc[i,k] == data2.iloc[i,k]:
                pass
            else:
                # 値が異なる場合に、その変更内容をデータフレームに保存
                diff = pd.DataFrame({"行":[i+1],"列":[k+1],
                "変更前":[data1.iloc[i,k]],
                "変更後":[data2.iloc[i,k]]})
                diff_data = pd.concat([diff_data, diff], 
                                      ignore_index=True)
                
    # ファイルの書き込み処理
    if file_type == 'csv':
        filename = make_file('csv')
        diff_data.to_csv(filename, index=False)
        print(f'{filename}として出力')
    elif file_type == 'txt':
        filename = make_file('txt')
        with open(filename, "w") as file:
            for _, col in diff_data.iterrows():
                file.write(
                    f"行:{col['行']},列:{col['列']},変更前:{col['変更前']},変更後:{col['変更後']} \n")
        print(f'{filename}として出力')


# 実行関数
def check_diff(data1,data2,file_type='csv'):
    data1_,data2_ = match_datasize(data1,data2)
    get_diff(data1_,data2_,file_type)