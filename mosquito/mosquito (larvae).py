from go_utils import get_api_data

mhm_df = get_api_data("mosquito_habitat_mapper")

from go_utils.mhm import qa_filter
import pandas as pd

filtered_mhm_df = qa_filter(mhm_df,has_genus=True, min_larvae_count=-1,has_photos=False)

df = pd.DataFrame(filtered_mhm_df)
selected_columns = df[["mhm_MGRSLongitude","mhm_MGRSLatitude","mhm_measuredDate", "mhm_LarvaeCount"]]

new_df = selected_columns.copy()

new_df['mhm_LarvaeCount'] = new_df['mhm_LarvaeCount'].astype(str)

print(new_df)

new_df.to_csv ("C:/Users/aviba/PycharmProjects/colors/Mosquito/outputmosquitoNEW2.csv")

new_df=new_df[new_df.mhm_LarvaeCount != 'nan']

for x, row in new_df.iterrows():
    if int (row.mhm_LarvaeCount)>25:
        new_df.at [x, 'mhm_LarvaeCount']="1"
    else:
        new_df.at [x, 'mhm_LarvaeCount']="0"

print (new_df)

print ("done")
