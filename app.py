from time import sleep
import random
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import streamlit as st

def scrapying_1(total_pages):
    # スクレイピング実行中メッセージを表示
    progress_text = st.empty()
    # スクレイピングの進捗バーを表示
    progress_bar = st.progress(0)

    d_list = []
    # ページごとにurlを変え、スクレイピングしてリストへ保存までの一連の作業を繰り返す

    for i in range(total_pages//2):
        url = f'https://www.cardrush-pokemon.jp/product-list?page=2&fpc=11446.2159.60.65e0419bb9e7e60v.1697681557000&page={i+1}'

        # urlへアクセスしHTMLをBeautifulSoupで解析する
        r = requests.get(url)
        r.raise_for_status() #アクセス失敗したときに直ちにプログラムを停止させる
        sec = random.uniform(3, 5)
        sleep(sec)
        soup = BeautifulSoup(r.content, 'lxml')
        sec = random.uniform(1, 3)
        sleep(sec)
        
        progress_text.text(f'現在{total_pages}ページ中{i+1}ページ目をスクレイピングしています。')
        # 解析したHTMLから各商品情報を取得
        card_infos = soup.select('ul.layout160 > li')

        # 取得した商品情報から各カード情報を取得
        for card_info in card_infos:
            # カードかそれ以外(パックやカード以外の商品)を判断する
            stock = card_info.select_one('p.stock').text
            if stock.endswith('枚'):
                # 在庫数が枚で終わる＝カードと判断し、各情報を取得する
                card_name_tag = card_info.select_one('p.item_name')
                card_name = card_name_tag.get_text(strip=True)
                pattern = r'^(.*?)\s*\【(.*?)\】\s*\{(.*?)\]$'
                matches = re.match(pattern, card_name)
                card_name = matches.group(1)
                rarity = '【' + matches.group(2) + '】' 
                card_number = '{' + matches.group(3) + ']'
                price = card_info.select_one('p.selling_price > span:first-of-type').text
                stock = stock.replace("在庫数 ", "")
                img_url = card_info.select_one('div.global_photo > img').get('src')
                card_url = card_info.select_one('div.item_data > a').get('href')

                d={
                    '商品名':card_name,
                    'レアリティ':rarity,
                    'カードリスト番号':card_number,
                    '価格':price,
                    '在庫数':stock,
                    '画像URL':img_url,
                    '商品URL':card_url        
                }
                d_list.append(d)

        # プログレスバーを更新
        progress_bar.progress((i+1) / total_pages)

    df = pd.DataFrame(d_list)
    progress_text.empty()
    return df



def scrapying_2(total_pages):
    # スクレイピング実行中メッセージを表示
    progress_text = st.empty()
    # スクレイピングの進捗バーを表示
    progress_bar = st.progress(0)

    d_list = []
    # ページごとにurlを変え、スクレイピングしてリストへ保存までの一連の作業を繰り返す

    for i in range(total_pages//2, total_pages+1):
        url = f'https://www.cardrush-pokemon.jp/product-list?page=2&fpc=11446.2159.60.65e0419bb9e7e60v.1697681557000&page={i}'

        # urlへアクセスしHTMLをBeautifulSoupで解析する
        r = requests.get(url)
        r.raise_for_status() #アクセス失敗したときに直ちにプログラムを停止させる
        sec = random.uniform(3, 5)
        sleep(sec)
        soup = BeautifulSoup(r.content, 'lxml')
        sec = random.uniform(1, 3)
        sleep(sec)
        
        progress_text.text(f'現在{total_pages}ページ中{i}ページ目をスクレイピングしています。')
        # 解析したHTMLから各商品情報を取得
        card_infos = soup.select('ul.layout160 > li')

        # 取得した商品情報から各カード情報を取得
        for card_info in card_infos:
            # カードかそれ以外(パックやカード以外の商品)を判断する
            stock = card_info.select_one('p.stock').text
            if stock.endswith('枚'):
                # 在庫数が枚で終わる＝カードと判断し、各情報を取得する
                card_name_tag = card_info.select_one('p.item_name')
                card_name = card_name_tag.get_text(strip=True)
                pattern = r'^(.*?)\s*\【(.*?)\】\s*\{(.*?)\]$'
                matches = re.match(pattern, card_name)
                card_name = matches.group(1)
                rarity = '【' + matches.group(2) + '】' 
                card_number = '{' + matches.group(3) + ']'
                price = card_info.select_one('p.selling_price > span:first-of-type').text
                stock = stock.replace("在庫数 ", "")
                img_url = card_info.select_one('div.global_photo > img').get('src')
                card_url = card_info.select_one('div.item_data > a').get('href')

                d={
                    '商品名':card_name,
                    'レアリティ':rarity,
                    'カードリスト番号':card_number,
                    '価格':price,
                    '在庫数':stock,
                    '画像URL':img_url,
                    '商品URL':card_url        
                }
                d_list.append(d)

        # プログレスバーを更新
        progress_bar.progress(i / total_pages)

    df = pd.DataFrame(d_list)
    progress_text.empty()
    return df




st.title('Webスクレイピングアプリ')

# # urlへアクセスしHTMLをBeautifulSoupで解析する
# r = requests.get('https://www.cardrush-pokemon.jp/product-list?page=2&fpc=11446.2159.60.65e0419bb9e7e60v.1697681557000&page=1')
# r.raise_for_status() #アクセス失敗したときに直ちにプログラムを停止させる
# sleep(1)
# soup = BeautifulSoup(r.content, 'lxml')
#　総ページ数を取得
# total_pages = int(soup.select_one('a.to_last_page').text)
total_pages = 10

if st.button('## スクレイピング開始'):
    # スクレイピングを実行
    message = st.text("スクレイピング実行中です。しばらくお待ちください。(所要時間約１時間)")
    df_scrapying_1 = scrapying_1(total_pages)
    df_scrapying_2 = scrapying_2(total_pages)
    message.empty()
    df_scrapying = pd.concat(df_scrapying_1, df_scrapying_2)

# スクレイピングの結果を表示
if 'df_scrapying' in locals():
    st.write('## スクレイピング結果', df_scrapying)

# df.to_csv(f'{d}.csv', index=None, encoding='utf-8-sig')

