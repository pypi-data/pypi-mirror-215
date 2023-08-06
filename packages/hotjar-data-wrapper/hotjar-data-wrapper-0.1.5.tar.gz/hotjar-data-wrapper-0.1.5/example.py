# %%
import os

from dotenv import load_env

import hotjar_data_wrapper.hotjar_api as hot

# %%
load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
site_id = os.getenv("account")
survey_id = os.getenv("survey_id")
# %%
status = hot.login_hotjar(username=username, password=password)
status.content
# %%
questions = hot.get_survey_questions(
    survey_id=survey_id, site_id=site_id, username=username, password=password
)
questions.content
# %%
meta = hot.get_survey_metadata(
    survey_id=survey_id, site_id=site_id, username=username, password=password
)
meta.status_code  # 200
meta.content  # prints content
# %%
all_surveys = hot.get_list_all_surveys(
    site_id=site_id, username=username, password=password
)
all_surveys.content
# %%
hot.get_all_surveys_metadata(
    path="data/hotjar surveys",
    surveys_list=ids,
    site_id=site_id,
    username=username,
    password=password,
)
