
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../../../../../../../var/folders/6c/12zttfmj58d_3_yqjbdtcn6h0000gn/T/5e4c7bde-a896-41ad-8b28-f06754799481'))
	print(os.getcwd())
except:
	pass

import random
import pandas as pd 
import numpy as np 
from schrutepy import schrutepy

def get_quiz(user_selection):
    df = schrutepy.load_schrute()
    user_selection = user_selection.title()

    user_df = df.copy()
    user_df = user_df.loc[user_df['character']==user_selection]
    user_df['Random_Selector'] = np.arange(user_df.shape[0])

    random_line = random.randrange(len(user_df['Random_Selector']))

    start_line = user_df.loc[user_df['Random_Selector']== random_line]
    start_real = start_line.iat[0,0]

    end_real = start_real+5
    start_quiz = start_real+6
    end_quiz = start_real+10

    real_lines = df.copy()
    real_lines = real_lines.loc[real_lines['index'] >= start_real]
    real_lines = real_lines.loc[real_lines['index'] <=end_real]

    season = real_lines.iat[0,1]
    episode = real_lines.iat[0,2]
    episode_name = real_lines.iat[0,3]
    real_script = pd.DataFrame()

    for i in range(0, len(real_lines)):
        character = real_lines.iat[i,6]
        text = real_lines.iat[i,7]
        
        

        real_script = real_script.append({'Character': character, 'Lines': text}, ignore_index=True)



    real_or_fake = random.randrange(2)
    quiz_script = pd.DataFrame()
    if real_or_fake == 0:
        quiz_lines = df.copy()
        quiz_lines = quiz_lines.loc[quiz_lines['index'] >= start_quiz]
        quiz_lines = quiz_lines.loc[quiz_lines['index'] <= end_quiz]
        for i in range(0, len(quiz_lines)):
            character = quiz_lines.iat[i,6]
            text = quiz_lines.iat[i,7]
            
            

            quiz_script = quiz_script.append({'Character': character, 'Lines': text}, ignore_index=True)
        
        real_or_fake = 'Real'
    else:
        character = 'Machine Learning'
        text = 'I made up some lines to go with the above text'
        quiz_script = quiz_script.append({'Character': character, 'Lines': text}
        real_or_fake = "Fake"

    
    real_script = real_script.to_dict('records')
    quiz_script = quiz_script.to_dict('records')

    quiz = {'User_Selected':user_selection, 'Real_dialouge':real_script, 'Quiz_Script':quiz_script, 'Real_or_Fake':real_or_fake }

    return quiz 


