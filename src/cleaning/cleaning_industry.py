#clean_industry.py

def get_industry_mapping():
    return {
        "人力仲介代徵": "服務與專業顧問業",
        "其他專業／科學及技術業": "服務與專業顧問業",
        "百貨相關業": "批發與零售業",
        "IC設計相關業": "資訊科技業",
        "電腦軟體服務業": "資訊科技業",
        "旅館業": "觀光與餐飲業",
        "銀行業": "金融與保險業",
        "會計服務業": "服務與專業顧問業",
        "網際網路相關業": "資訊科技業",
        "藥品／化妝品及清潔用品零售業": "批發與零售業",
        "其它軟體及網路相關業": "資訊科技業",
        "運動服務業": "服務與專業顧問業",
        "汽車及其零件製造業": "製造業",
        "藥品製造業": "醫療與健康照護",
        "醫院": "醫療與健康照護",
        "半導體製造業": "製造業",
        "產物保險業": "金融與保險業",
        "電腦及其週邊設備製造業": "製造業",
        "其他投資理財相關業": "金融與保險業",
        "工商顧問服務業": "服務與專業顧問業",
        "自動控制相關業": "資訊科技業",
        "量販流通相關業": "批發與零售業",
        "廣告行銷公關業": "服務與專業顧問業",
        "旅遊服務業": "觀光與餐飲業",
        "乳品製造業": "製造業",
        "數位內容產業": "資訊科技業",
        "不動產經營業": "服務與專業顧問業",
        "雜誌／期刊出版業": "服務與專業顧問業",
        "金屬表面處理及熱處理業": "製造業",
        "綜合商品批發代理業": "批發與零售業",
        "其他金融及輔助業": "金融與保險業",
        "電信相關業": "資訊科技業",
        "印刷電路板製造業(PCB)": "製造業",
        "電腦系統整合服務業": "資訊科技業",
        "其他零售業": "批發與零售業",
        "生化科技研發業": "醫療與健康照護",
        "精密儀器相關製造業": "製造業",
        "光電產業": "製造業",
        "消費性電子產品製造業": "製造業",
        "其他相關製造業": "製造業",
        "化學原料製造業": "製造業",
        "金融控股業": "金融與保險業",
        "環境衛生及污染防治服務業": "服務與專業顧問業",
        "航空運輸輔助業": "運輸與物流業",
        "其他半導體相關業": "製造業",
        "其他出版業": "服務與專業顧問業",
        "自行車及其零件製造業": "製造業",
        "大專校院教育事業": "服務與專業顧問業",
        "船舶及其零件製造修配業": "製造業",
        "診所": "醫療與健康照護",
        "人身保險業": "金融與保險業",
        "其他電子零組件相關業": "製造業",
        "印刷業": "服務與專業顧問業",
        "醫療器材製造業": "醫療與健康照護",
        "其他食品製造業": "製造業",
        "建材／傢俱零售業": "批發與零售業",
        "食品什貨批發業": "批發與零售業",
        "停車場業": "運輸與物流業",
        "家用電器製造業": "製造業",
        "電視業": "服務與專業顧問業",
        "證券及期貨業": "金融與保險業",
        "電池製造業": "製造業",
        "運輸工具設備租賃業": "運輸與物流業",
        "其他餐飲業": "觀光與餐飲業",
        "藥品／化妝品及清潔用品批發業": "批發與零售業",
        "其他醫療保健服務業": "醫療與健康照護",
        "食品什貨零售業": "批發與零售業",
        "其他化學相關製造業": "製造業",
        "儲配／運輸物流業": "運輸與物流業",
        "其他機械製造修配業": "製造業",
        "電子通訊／電腦週邊零售業": "批發與零售業",
        "機車及其零件製造業": "製造業",
        "其他教育服務業": "服務與專業顧問業",
        "鞋類／布類／服飾品零售業": "批發與零售業",
        "專用生產機械製造修配業": "製造業",
        "多媒體傳播相關業": "服務與專業顧問業",
        "鐘錶／眼鏡零售業": "批發與零售業",
        "其他運輸工具及零件製造修配業": "製造業",
        "餐館業": "觀光與餐飲業",
        "社會福利服務業": "服務與專業顧問業",
        "其他不動產業": "服務與專業顧問業"
    }
def clean_industry_column(df,column_name="產業"):
    mapping=get_industry_mapping()
    df["八大產業"]=df[column_name].map(mapping).fillna("其他")
    return df
if __name__== "__main__":
    import pandas as pd
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))  # 取得目前這支 .py 檔案所在資料夾的絕對路徑
    file_path=os.path.abspath(os.path.join(current_dir,"../../data/104_cleaned_0714.csv"))
    df=pd.read_csv(file_path, encoding="utf-8-sig",quoting=1,sep=",",header=0)
    df=clean_industry_column(df)
    print(df.head())
