import streamlit as st
import pandas as pd
from scipy.stats import kendalltau
from PIL import Image
import random
import csv
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from scipy.stats import spearmanr
st.set_page_config(layout="wide")
pagelist = ["stepA","stepB","stepC"]
selector=st.sidebar.selectbox("ページ選択",pagelist,key="page-select")

if 'current_time' not in st.session_state:
    st.session_state["current_time"] = datetime.now().strftime("%Y%m%d_%H%M%S")

columns = [
    ['name', 'evaluation']
]
df = pd.DataFrame(data=columns)
if 'df' not in st.session_state:    
    st.session_state["df"] = df

def display_items(start_index, items, num_items=8):
    """ 指定されたインデックスから始まる項目を表示する """
    end_index = start_index + num_items
    selected_items = items[start_index:end_index]
    
    if 'selected_items' not in st.session_state:
        st.session_state["selected_items"] = selected_items
    selected_items = st.session_state["selected_items"]
        
    if 'text_list' not in st.session_state:
        st.session_state["text_list"] = []
    if 'image_done' not in st.session_state:
        st.session_state["image_done"] = []
    
    try:
        num_items2 = len(selected_items)
        lcol=[]
        col= st.columns(4)
        def syasinhyouzi():
            if st.button("図{}".format(i+1), key=i+1):
                st.session_state["image_done"].append(selected_items[i])
                st.session_state["text_list"].append("{}".format(i+1))
                text_result = ' '.join(st.session_state["text_list"])
                new_row = [''.join(selected_items[i]), "stepA"]
                st.session_state["df"] = st.session_state["df"].append(pd.Series(new_row, index=st.session_state["df"].columns), ignore_index=True)
                selected_items[i] = "d-"+selected_items[i]
            st.image(selected_items[i], use_column_width=True)
        for i in list(range(0,num_items2,4)):
            with col[0]:
                syasinhyouzi()            
        for i in list(range(1,num_items2,4)):
            with col[1]:
                syasinhyouzi()             
        for i in list(range(2,num_items2,4)):
            with col[2]:
                syasinhyouzi() 
        for i in list(range(3,num_items2,4)):
            with col[3]:
                syasinhyouzi()
        
        def modoru():    
            selected_items[int(st.session_state["text_list"][-1])-1] = st.session_state["image_done"][-1]
            st.session_state["image_done"] = st.session_state["image_done"][:-1]
            st.session_state["text_list"] = st.session_state["text_list"][:-1]
            text_result = ' '.join(st.session_state["text_list"])
            st.session_state["df"] = st.session_state["df"].drop(st.session_state["df"].index[-1])
        if len(st.session_state["text_list"])>0:
            st.button("評価1個戻る", on_click=modoru)
    
    except FileNotFoundError:
        st.subheader("下の「評価1個戻る」のボタンを押してください")
        def modoru():    
            selected_items[int(st.session_state["text_list"][-1])-1] = st.session_state["image_done"][-1]
            st.session_state["image_done"] = st.session_state["image_done"][:-1]
            st.session_state["text_list"] = st.session_state["text_list"][:-1]
            text_result = ' '.join(st.session_state["text_list"])
            st.session_state["df"] = st.session_state["df"].drop(st.session_state["df"].index[-1])
        if len(st.session_state["text_list"])>0:
            st.button("評価1個戻る", on_click=modoru)

def main():    
    st.title("サンプルアプリ（ミニトマト20個の評価）")
    st.write("---")
    st.subheader("品質が良いと思う順に選択してください")
    
    image_list = ['2.jpg', '3.jpg', '4.jpg', '6.jpg', '7.jpg', '9.jpg', '12.jpg', '13.jpg', '15.jpg', '16.jpg', '17.jpg', '18.jpg', '31.jpg', '33.jpg', '34.jpg', '37.jpg', '49.jpg', '56.jpg', '62.jpg', '86.jpg']
    random.shuffle(image_list)
    if 'image_list' not in st.session_state:
        st.session_state['image_list'] = image_list
    image_list = st.session_state['image_list']

    # セッションステートでインデックスを管理
    if 'start_index' not in st.session_state:
        st.session_state['start_index'] = 0  

    # アイテムを表示
    display_items(st.session_state['start_index'], image_list)
    
    if len(st.session_state["text_list"]) == len(st.session_state["selected_items"]):
        if st.session_state['start_index'] >= len(image_list) - 8:
            def change_page2():
                st.session_state["グループ"+"{}".format(st.session_state['count']+1)].extend(st.session_state["image_done"])
                st.session_state["page-select"] = "stepB"
                del st.session_state["selected_items"]
                del st.session_state["text_list"]
                del st.session_state["image_done"]
                del st.session_state['count']
            st.write("") 
            st.subheader("下の「次の段階へ」のボタンを押してください")    
            st.button("次の段階へ", on_click=change_page2)            
            
        else:     
            def change_page():
                for i in range(3):
                    if 'グループ'+'{}'.format(i+1) not in st.session_state:
                        st.session_state["グループ"+"{}".format(i+1)] = []
                if 'count' not in st.session_state:
                    st.session_state['count'] = 0    
                st.session_state["グループ"+"{}".format(st.session_state['count']+1)].extend(st.session_state["image_done"])
                st.session_state['count'] += 1
                del st.session_state["selected_items"]
                del st.session_state["text_list"]
                del st.session_state["image_done"]
                st.session_state['start_index'] += 8
            st.write("")     
            st.subheader("下の「次へ」のボタンを押してください")     
            st.button("次へ", on_click=change_page)

if selector == "stepA":
    main()
    
elif selector == "stepB":
    lst_step1_first = []
    def display_items2(start_index, items, num_items=8):
        """ 指定されたインデックスから始まる項目を表示する """
        end_index = start_index + num_items
        selected_items = items[start_index:end_index]

        if 'selected_items' not in st.session_state:
            st.session_state["selected_items"] = selected_items
        selected_items = st.session_state["selected_items"]
        
        lst_step1_first = []
        for i in range(len(selected_items)):
            if len(selected_items[i])>0:
                lst_step1_first.append(selected_items[i][0]) 
                
            
        if 'text_list' not in st.session_state:
            st.session_state["text_list"] = []
        if 'image_done' not in st.session_state:
            st.session_state["image_done"] = []
            
        num_items = len(lst_step1_first)
        lcol=[]
        col= st.columns(4)
        def syasinhyouzi(i):
            def list_first(i):
                st.session_state["image_done"].append(lst_step1_first[i])
                new_row = [''.join(lst_step1_first[i]) ,"stepB"]
                st.session_state["df"] = st.session_state["df"].append(pd.Series(new_row, index=st.session_state["df"].columns), ignore_index=True)
                if len(st.session_state["グループ1"])>0:
                    if lst_step1_first[i] == st.session_state["グループ1"][0]:
                        del st.session_state["グループ1"][0]
                if len(st.session_state["グループ2"])>0:
                    if lst_step1_first[i] == st.session_state["グループ2"][0]:
                        del st.session_state["グループ2"][0]
                if len(st.session_state["グループ3"])>0:
                    if lst_step1_first[i] == st.session_state["グループ3"][0]:
                        del st.session_state["グループ3"][0]                    
            if st.button("図{}".format(i+1), key=i+1, on_click=list_first, args=(i,)):
                pass
            st.image(lst_step1_first[i], use_column_width=True)
            
        for i in list(range(0,num_items,4)):
            with col[0]:
                syasinhyouzi(i)            
        for i in list(range(1,num_items,4)):
            with col[1]:
                syasinhyouzi(i)             
        for i in list(range(2,num_items,4)):
            with col[2]:
                syasinhyouzi(i) 
        for i in list(range(3,num_items,4)):
            with col[3]:
                syasinhyouzi(i)    
                
        if len(lst_step1_first) == 0:
            if st.session_state['start_index_step2'] >= len(stepB_list) - 8 :
                def change_page3():
                    for i in range(1):
                        if 'step2_グループ'+'{}'.format(i+1) not in st.session_state:
                            st.session_state["step2_グループ"+"{}".format(i+1)] = []                
                    if 'count' not in st.session_state:
                        st.session_state['count'] = 0                      
                    st.session_state["step2_グループ"+"{}".format(st.session_state['count']+1)].extend(st.session_state["image_done"])
                    st.session_state["page-select"] = "stepC"
                    del st.session_state["selected_items"]
                    del st.session_state["text_list"]
                    del st.session_state["image_done"]
                    del st.session_state['count']
                st.write("")     
                st.subheader("下の「結果を見る」のボタンを押してください")     
                st.button("結果を見る", on_click=change_page3)
            else:     
                def change_page4():
                    for i in range(1):
                        if 'step2_グループ'+'{}'.format(i+1) not in st.session_state:
                            st.session_state["step2_グループ"+"{}".format(i+1)] = []
                    if 'count' not in st.session_state:
                        st.session_state['count'] = 0    
                    st.session_state["step2_グループ"+"{}".format(st.session_state['count']+1)].extend(st.session_state["image_done"])
                    st.session_state['count'] += 1
                    del st.session_state["selected_items"]
                    del st.session_state["text_list"]
                    del st.session_state["image_done"]
                    st.session_state['start_index_step2'] += 8
                st.write("") 
                st.subheader("下の「次へ」のボタンを押してください")     
                st.button("次へ", on_click=change_page4)
        
    st.title("サンプルアプリ（ミニトマト20個の評価）")
    st.subheader("一番品質が良いと思うものを選び続けてください")
    
    stepB_list = []
    for i in range(3):
        stepB_list.append(st.session_state["グループ"+"{}".format(i+1)])

    if 'start_index_step2' not in st.session_state:
        st.session_state['start_index_step2'] = 0

    display_items2(st.session_state['start_index_step2'], stepB_list) 
            
    
elif selector == "stepC":     
    st.subheader("官能評価終了")
    def last(i):
        st.image(st.session_state["step2_グループ1"][i], use_column_width=True)
    num_items = 20
    col= st.columns(4)
    for i in list(range(0,num_items,4)):
        with col[0]:
            last(i)            
    for i in list(range(1,num_items,4)):
        with col[1]:
            last(i)             
    for i in list(range(2,num_items,4)):
        with col[2]:
            last(i)
    for i in list(range(3,num_items,4)):
        with col[3]:
            last(i)
    
    st.write("---")
    st.subheader('')
        
    st.subheader("統計解析結果")
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import os
    from scipy.stats import spearmanr
    list1 = st.session_state["step2_グループ1"]
    list2 = ['13.jpg', '3.jpg', '31.jpg', '62.jpg', '18.jpg', '9.jpg', '37.jpg', '86.jpg', '16.jpg', '56.jpg', '6.jpg', '4.jpg', '15.jpg', '34.jpg', '49.jpg', '7.jpg', '33.jpg', '12.jpg', '2.jpg', '17.jpg']
    list3 = ['13.jpg', '3.jpg', '31.jpg', '62.jpg', '18.jpg', '9.jpg', '37.jpg', '16.jpg', '6.jpg', '34.jpg', '49.jpg', '56.jpg', '15.jpg', '4.jpg', '86.jpg', '2.jpg', '7.jpg', '12.jpg', '33.jpg', '17.jpg'] 
    
    # ファイル名をインデックスにマッピングする辞書を作成
    rank_dict = {name: i for i, name in enumerate(list1)}

    # 新しいリストでの各要素の順位を抽出
    ranks1 = [rank_dict[name] for name in list1]
    ranks2 = [rank_dict[name] for name in list2]
    ranks3 = [rank_dict[name] for name in list3]

    correlation, pvalue = spearmanr(ranks1, ranks2)
    correlation2, pvalue = spearmanr(ranks1, ranks3)
    new_row = [correlation ,correlation2]
    st.session_state["df"] = st.session_state["df"].append(pd.Series(new_row, index=st.session_state["df"].columns), ignore_index=True)
    
    # フォントファイルのパスを設定
    font_path = 'NotoSansCJKjp-Regular.otf'  # プロジェクトディレクトリ内のフォントファイルを指定

    # フォントのプロパティを設定
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    
    # グラフのデータ
    labels = ['傷面積', '傷面積/大きさ']
    values = [correlation, correlation2]
    colors = ['mediumblue', 'crimson']
    bar_width = 0.35

    # 棒グラフを作成
    fig, ax = plt.subplots(figsize=(5, 5))
    bars = ax.bar(labels, values, width=bar_width, color=colors)
    
    for i in range(len(bars) - 1):
        bar1 = bars[i]
        bar2 = bars[i + 1]
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax.plot([bar1.get_x() + bar1.get_width()/2, bar2.get_x() + bar2.get_width()/2], 
                [height1, height2], linestyle='--', color='black')

    # グラフのタイトルとラベル
    ax.set_title('官能評価順位との相関', fontproperties=font_prop, fontsize=20)
    #ax.set_xlabel('Variables', fontproperties=font_prop)
    ax.set_ylabel('スピアマンの順位相関係数', fontproperties=font_prop, fontsize=20)
    plt.ylim(0, 1)
    ax.set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0], fontproperties=font_prop, fontsize=20)
    ax.set_xticklabels(labels, fontproperties=font_prop, fontsize=20)

    # Streamlitでグラフを表示
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig)
    with col2:
        if correlation < correlation2:
            st.header("")
            st.write("---")
            st.subheader("あなたの評価は")
            st.subheader("「傷面積」＜「傷面積/大きさ」")
            st.write("")
            st.write("評価時の着目点を質問された時に、「傷の大きさ」と答えられても、「ミニトマト自体の大きさ」と答えることは難しいと思います。ランキング手法を用いることで、言語化しにくい感覚も可視化することが可能になります。")
            st.write("---")
        else:
            st.header("")
            st.write("---")
            st.subheader("あなたの評価は")
            st.subheader("「傷面積」＞「傷面積/大きさ」")
            st.write("")
            st.write("評価時の着目点を質問された時に、「傷の大きさ」と答えられても、「ミニトマト自体の大きさ」と答えることは難しいと思います。ランキング手法を用いることで、言語化しにくい感覚も可視化することが可能になります。")
            st.write("---")
    if st.checkbox("解析結果の詳細を見る"):
        ranks1_ranking = [rank + 1 for rank in ranks1]
        ranks2_ranking = [rank + 1 for rank in ranks2]
        ranks3_ranking = [rank + 1 for rank in ranks3]
        rounded_correlation = round(correlation, 3)
        rounded_correlation2 = round(correlation2, 3)

        col1, col2, cil3 = st.columns(3)
        with col1:
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.scatter(ranks1_ranking, ranks2_ranking, marker='o', facecolors='none', edgecolors='black', s=100)
            ax.set_xlabel('官能評価結果の順位', fontproperties=font_prop, fontsize=20)
            ax.set_ylabel('傷面積の順位', fontproperties=font_prop, fontsize=20)
            plt.ylim([-1, 21])
            plt.xlim([-1, 21])
            plt.xticks(range(0, 21, 5), fontsize=20)
            plt.yticks(range(0, 21, 5), fontsize=20)
            ax.plot(range(0, 21), range(0, 21), linestyle='--', color='gray')         
            ax.set_title('相関係数　'+'{}'.format(rounded_correlation), fontsize=20)
            st.pyplot(fig)
        with col2:    
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.scatter(ranks1_ranking, ranks3_ranking, marker='o', facecolors='none', edgecolors='black', s=100)
            ax.set_xlabel('官能評価結果の順位', fontproperties=font_prop, fontsize=20)
            ax.set_ylabel('傷面積/大きさの順位', fontproperties=font_prop, fontsize=20)
            plt.ylim([-1, 21])
            plt.xlim([-1, 21])
            plt.xticks(range(0, 21, 5), fontsize=20)
            plt.yticks(range(0, 21, 5), fontsize=20)
            ax.plot(range(0, 21), range(0, 21), linestyle='--', color='gray')         
            ax.set_title('相関係数　'+'{}'.format(rounded_correlation2), fontsize=20)
            #ax.text(1, 19, '相関係数：'+ '{}'.format(rounded_correlation2), fontsize=20, color='red')
            st.pyplot(fig)

    st.write("---")
    st.subheader('')
    st.subheader('「質問への回答」と「結果の収集」にご協力お願い致します')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        question1 = st.radio("性別", ("男性", "女性"))
    with col2:
        question2 = st.radio("年齢", ("10代", "20代", "30代", "40代", "50代", "60代", "70代", "80代"))
    with col3:
        question3 = st.radio("6月7日の口頭発表に、あなたの結果を利用することを", ("承諾する", "承諾しない"))
        
    st.subheader('')
    
    if question1 == "男性":
      answer1 = "_male"
    else:
      answer1 = "_female"
    if question2 == "10代":
      answer2 = "_10"
    elif question2 == "20代":
      answer2 = "_20"
    elif question2 == "30代":
      answer2 = "_30"
    elif question2 == "40代":
      answer2 = "_40"  
    elif question2 == "50代":
      answer2 = "_50"
    elif question2 == "60代":
      answer2 = "_60"
    elif question2 == "70代":
      answer2 = "_70"      
    else:
      answer2 = "_80"
    if question3 == "承諾する":
      answer3 = "_yes"
    else:
      answer3 = "_no"    
    
    
    filename = "Fooma_tomato_"+"{}".format(st.session_state["current_time"])+answer1+answer2+answer3+".csv"
    #st.write(filename)
    st.session_state["df"].to_csv(filename, index=False, encoding='cp932')
    

    # ダウンロードボタンを表示
    csv = st.session_state["df"].to_csv(index=False).encode('cp932')
    #st.download_button(label='結果ダウンロード', data=csv, file_name=filename)   
    

    def send_email(to_email, subject, body, attachment_path):
        from_email = 'yuk8965@gmail.com'  # ここにあなたのGmailアドレスを入力
        from_password = 'yndzolulnzbskfqy'  # ここにGoogleアプリパスワードを入力

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(attachment_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

    # メール送信のためのUI
    recipient_email = "yuk8965@gmail.com"  # 固定の受信者のメールアドレスをここに記述

    # ユーザーが件名と本文を入力
    subject = "Fooma_tomato_result"
    body = "添付ファイルとしてCSVファイルを送信します。"

    if 'email_sent' not in st.session_state:
        st.session_state['email_sent'] = False

    # メール送信ボタン
    if not st.session_state['email_sent']:
        if st.button("結果を送信"):
            send_email(recipient_email, subject, body, filename)
            st.session_state['email_sent'] = True
            st.success("結果を送信しました")
            st.write("---")
            st.subheader("アプリは以上になります。ありがとうございました。")
    else:
        st.subheader("結果はすでに送信されました。")
        st.write("---")
        st.subheader("アプリは以上になります。ありがとうございました。")

