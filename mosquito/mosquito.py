import pandas as pd
from go_utils.mhm import qa_filter
from go_utils import get_api_data

mhm_df = get_api_data("mosquito_habitat_mapper")


filtered_mhm_df = qa_filter(mhm_df, has_genus=True,
                            min_larvae_count=1, has_photos=False)

df = pd.DataFrame(filtered_mhm_df)
selected_columns = df[["mhm_MGRSLongitude",
                       "mhm_MGRSLatitude", "mhm_MosquitoPupae"]]

new_df = selected_columns.copy()

new_df['mhm_MosquitoPupae'] = new_df['mhm_MosquitoPupae'].astype(str)
val = new_df['mhm_MosquitoPupae'].values[0]
print(type(val))

new_df["mhm_MosquitoPupae"] = new_df["mhm_MosquitoPupae"].str.replace(
    "False", "0")
new_df["mhm_MosquitoPupae"] = new_df["mhm_MosquitoPupae"].str.replace(
    "True", "1")

print(new_df)

new_df = new_df[new_df.mhm_MosquitoPupae != 'nan']

new_df.to_csv("outputmosquito32.csv", index=False)
