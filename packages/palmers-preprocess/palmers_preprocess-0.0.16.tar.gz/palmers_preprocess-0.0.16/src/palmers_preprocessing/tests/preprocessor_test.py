import sys
import catboost

from src.palmers_preprocessing.regular_data_handler import RegularDataLoader
import pandas as pd
sys.path.append('../..')
from src.palmers_preprocessing.preprocessor import Preprocessor
from src.palmers_preprocessing.utils import convert_df_with_sku_to_df_with_item, daily_sales_to_weekly_mean_sales
from clearml import Model, InputModel, Task
import pickle
from src.palmers_preprocessing import config as global_config
import numpy as np

def test_prepreocessor():
    preprocessor = Preprocessor()
    stores = ['3']
    print("Loading data...")
    df = RegularDataLoader().load()
    print(df['store'].unique().tolist())
    print("Data loaded")
    df = df[df['store'].isin(stores)]
    print("Data filtered")
    print(df.head())
    print("Convert df with sku to df with item")
    # df = convert_df_with_sku_to_df_with_item(df)
    print(df.info())

  #  items_1 = df[df['store'] == '100']['item'].unique()
  #  items_2 = df[df['store'] == '3']['item'].unique()
  #  df = df[df['item'].isin(items_1) | df['item'].isin(items_2)]
  #   print(df["item, store"].unique())
    print("Daily Sales to weekly mean sales")
    # df = daily_sales_to_weekly_mean_sales(df)

    # stores_list: list[int] = global_config.OUTLETS_SDATTA, marketing_plan: pd.DataFrame = None,
    # item_encoders = None, store_encoders = None, store_location_df: pd.DataFrame = None,
    # begin_predict_dates: str = global_config.tomorrow_date, event_encoders: dict = None,
    # regular_data_df: pd.DataFrame = None, event_df: pd.DataFrame = None,
    # holiday_df: pd.DataFrame = None

    data_path_marketing_plan = r"C:\Users\yotam\SDatta\palmers\new\for_roy\marketing_plan.csv"
    marketing_plan = pd.read_csv(data_path_marketing_plan)
    data_path_item_encoders = r"C:\Users\yotam\SDatta\palmers\new\for_roy\item_encoders.csv"
    item_encoders = pd.read_csv(data_path_item_encoders)
    data_path_store_encoders = r"C:\Users\yotam\SDatta\palmers\new\for_roy\store_encoders.csv"
    store_encoders = pd.read_csv(data_path_store_encoders)
    data_path_store_location_df = r"C:\Users\yotam\SDatta\palmers\new\for_roy\store_location_df.csv"
    store_location_df = pd.read_csv(data_path_store_location_df)
    data_path_event_encoders = r"C:\Users\yotam\SDatta\palmers\new\for_roy\event_encoders.pkl"
    with open(data_path_event_encoders, 'rb') as f:
        event_encoders = pickle.load(f)

    data_path_event_df = r"C:\Users\yotam\SDatta\palmers\new\for_roy\event_df.csv"
    event_df = pd.read_csv(data_path_event_df)
    data_path_holiday_df = r"C:\Users\yotam\SDatta\palmers\new\for_roy\holiday_df.csv"
    holiday_df = pd.read_csv(data_path_holiday_df)

    df,df_roll = preprocessor.preprocess(stores_list=[3],marketing_plan=marketing_plan,item_encoders=item_encoders,store_encoders=store_encoders,store_location_df=store_location_df, begin_predict_dates='2023-05-23',event_encoders=event_encoders, regular_data_df=df,event_df=event_df,holiday_df=holiday_df)
    pd.set_option('display.max_rows', None)
    print(df.isnull().sum())
    print(df)
    print(df.columns.tolist())
    return df,df_roll
# def test_cumulative_features():
#     preprocessor = Preprocessor()
#     df = preprocessor.get_regular_data_of_store(store_id='109', predict_date='2023-05-23')
#     cum_feat = preprocessor.get_cumulative_features(df)
#     print(cum_feat)


task = Task.init(project_name='test_predict_store_3', task_name='test_predict_store_3')
model_id = '3e2ac457fc644f39b4eb6d5a68e84dfb'  # Replace with your actual model ID
print("111")
models_store_3_path = Model(model_id).get_local_copy()
print("222")
with open(models_store_3_path, 'rb') as f:
     model_3 = pickle.load(f)['3']
print(model_3)
print("333")
df,df_roll = test_prepreocessor()
for item_store in model_3.keys():
    model = model_3[item_store]['model']
    prediction = np.ceil(model.predict(df[df[global_config.ITEM_STORE_COLUMN_NAME] == item_store][model.feature_names_])[0]*0.2 + df_roll[df_roll[global_config.ITEM_STORE_COLUMN_NAME] == item_store]['roll_3'].values[0]*0.8)
    print("Item store: ", item_store, "prediction: ", prediction)


