
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../../../../../../../var/folders/6c/12zttfmj58d_3_yqjbdtcn6h0000gn/T/5e4c7bde-a896-41ad-8b28-f06754799481'))
	print(os.getcwd())
except:
	pass
cwd = os.getcwd()
import random
import pandas as pd 
import numpy as np 
from schrutepy import schrutepy
import json
import tensorflow as tf
import gpt_2_simple as gpt2



sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess,
              checkpoint='latest',
              run_name=f"{cwd}/run1",
              checkpoint_dir=cwd,
              model_name=None,
              model_dir='models',
              multi_gpu=False)






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
    real_lines = real_lines.loc[real_lines['index'] <= end_real]

    season = real_lines.iat[0,1]
    episode = real_lines.iat[0,2]
    episode_name = real_lines.iat[0,3]
    real_script = pd.DataFrame()
    ml_input = []
    for i in range(0, len(real_lines)):
        character = real_lines.iat[i,6]
        text = real_lines.iat[i,7]
        
        real_script = real_script.append({'Character': character, 'Lines': text}, ignore_index=True)
        ml_line = f"{character}: {text}"
        ml_input.append(ml_line)


    # random_game = random.randrange(0,2)
    random_game = 1
    quiz_script = pd.DataFrame()

    if random_game == 0:
        quiz_lines = df.copy()
        quiz_lines = quiz_lines.loc[quiz_lines['index'] >= start_quiz]
        quiz_lines = quiz_lines.loc[quiz_lines['index'] <= end_quiz]
        for i in range(0, len(quiz_lines)):
            character = quiz_lines.iat[i,6]
            text = quiz_lines.iat[i,7]
            
            

            quiz_script = quiz_script.append({'Character': character, 'Lines': text}, ignore_index=True)
        
        real_or_fake = 'Real'
    else:
        ### MACHINE LEARNING GOES HERE ###
        ml_script = gpt2.generate(sess,
                run_name='run1',
                checkpoint_dir=f"{cwd}",
                model_name=None,
                model_dir='models',
                sample_dir='samples',
                return_as_list=True,
                truncate=None,
                destination_path=None,
                sample_delim='=' * 20 + '\n',
                prefix=str(ml_input),
                seed=None,
                nsamples=1,
                batch_size=1,
                length=256,
                temperature=0.7,
                top_k=0,
                top_p=0.0,
                include_prefix=False)[0]
        
        splits = []
        for line in ml_script.splitlines():
            line = line.split(":")
            splits.append(line)
        splits.pop(0)
        splits.pop(0)    

        characters = []
        lines = []
        for i in range(0, len(splits)):
            if i%3 == 0:
                character = splits[i]
                character = character[0]
                characters.append(character)
            elif i%3 == 1: 
                line = splits[i][0]

                lines.append(line)


        for i in range(0, len(characters)):
            character = characters[i]
            text = lines[i]
            quiz_script = quiz_script.append({'Character': character, 'Lines': text}, ignore_index=True)
        real_or_fake = "Fake"


    real_script = real_script.to_dict('records')
    quiz_script = quiz_script.to_dict('records')

    quiz = {'User_Selected':user_selection, 'Real_dialouge':real_script, 'Quiz_Script':quiz_script, 'Real_or_Fake':real_or_fake }

    return quiz 
