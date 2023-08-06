#%%
import dotenv
import os

from kf6py import KF6API


config = dotenv.dotenv_values('./singapore.env')
# config = dotenv.dotenv_values('./ikit-2.env')
# config = dotenv.dotenv_values('./.env')
kfurl = config.get("KF6_URL")
username = config.get("KF6_USERNAME")
password = config.get("KF6_PASSWORD")

#%%
kf6api = KF6API(kfurl, username, password)
kf6api.get_my_communities()
#%%
curr = {
    "community": "624d59370a5d7b90e9b37646",
    "view": "627ca1bc00117407e7313e98"
}

#%%
kf6api.get_views(curr['community'])
#%%
x = kf6api.get_notes_from_view(curr['community'], curr["view"])
x

#%%
kf6api.get_links(curr['community'], 'buildson', succinct=False)

#%%
kf6api.create_contribution(curr['community'], curr['view'], 'another code', 'hello')

# %%
