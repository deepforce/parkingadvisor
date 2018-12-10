#%%
import pandas as pd

TEST_STREET_NAME = '10TH AVE BETWEEN E MADISON ST AND E SENECA ST'

test_data = pd.DataFrame(index=[0], data={'UNITDESC': TEST_STREET_NAME, 'WKD_RATE3': 2}, columns=['UNIDESC', 'WKD_RATE3'])
#%%
test_data.WKD_RATE3.values[0]
