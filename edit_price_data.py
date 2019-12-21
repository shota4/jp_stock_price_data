import pandas as pd
import datetime as dt
from dateutil import relativedelta
import codecs
from glob import glob

def read_csv(file_name: str) -> pd.core.frame.DataFrame:
    '''
    kabuoji3.comからダウンロードしたcsvをファイル名[file_name]を指定して読み込み、整形してDataFrame[df]として返します。
    '''
    with codecs.open(file_name, 'r', 'Shift_JIS', 'ignore') as f:
        df = pd.read_csv(f)
    df.columns = df.iloc[0]
    df.drop(df.index[[0,1]],inplace=True)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    df.index.name = "日付"
    return df

def get_price_data_by_year(year: int) -> pd.core.frame.DataFrame:
    '''
    フォルダ内のファイルリスト[FILES_DICT]から指定年[year]の株価csvのファイル名を参照し、読み込んでDataFrame[df]として返します。
    '''
    file_name = FILES_DICT[str(year)]
    df = read_csv(file_name)
    return df

def create_historical_data(open: int,last: int) -> pd.core.frame.DataFrame:
    '''
    指定年[open]から指定年[last]までの株価データを読み込み、結合して1つのDataFrame[df]として返します。
    '''
    df = get_price_data_by_year(open)
    for i in range(int(open) + 1,int(last) + 1):
        df = pd.concat([df, get_price_data_by_year(i)])
    return df

def create_historical_data_by_date(years: int) -> pd.core.frame.DataFrame:
    '''
    実行日から遡ってちょうど指定年数[years]分の株価データを作成し、1つのDataFrame[df]として返します。
    '''
    this_year = int(dt.datetime.now().year)
    df = create_historical_data(this_year - years,this_year)
    open = dt.datetime.now() - relativedelta.relativedelta(years=years)
    df = df[df.index >= open]
    return df

if __name__ == "__main__":
    
    #ダウンロードしたCSVが入っているフォルダのディレクトリを指定（相対パスでも絶対パスでも可、フォルダ名の後に/*を忘れずに）
    CSV_FOLDER_DIRECTORY = './csv/*'

    #上記のCSV_FOLDER_DIRECTORYを元にCSVファイルの辞書FILES_DICTを自動で作成する部分（編集不要）
    FILES_DICT = {}
    files = glob(CSV_FOLDER_DIRECTORY)
    files.sort()
    for file_name in files:
        FILES_DICT[file_name[-8:-4]] = file_name

    '''
    #指定年から指定年までの株価データを保存したい場合
    df = create_historical_data(開始年,終了年)
    df.to_csv("保存名")

    （例）
    df = create_historical_data(2015,2019)
    df.to_csv("2015-2019.csv")
    '''

    '''
    #実行日から遡ってちょうど指定年数分の株価データを保存したい場合
    df = create_historical_data_by_date(年数)
    df.to_csv("保存名")

    （例）
    df = create_historical_data_by_date(5)
    df.to_csv("5years_price.csv")
    ''' 
