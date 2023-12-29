import numpy as np


def merge(subset, min_num_body_parts=4, min_score=0.4):
    """
    Estimates the skeletons.
    :param connections: valid connections
    :param min_num_body_parts: minimum number of body parts for a skeleton
    :param min_score: minimum score value for the skeleton
    :return: list of skeletons. Each skeleton has a list of identifiers of body parts:
        [
            [id1, id2,...,idN, score, parts_num],
            [id1, id2,...,idN, score, parts_num]
            ...
        ]

    position meaning:
        [   [nose       , neck           , right_shoulder , right_elbow      , right_wrist  , left_shoulder
             left_elbow , left_wrist     , right_hip      , right_knee       , right_ankle  , left_hip
             left_knee  , left_ankle     , right_eye      , left_eye         , right_ear    , left_ear
             score, parts_num],
        ]
    """

    # 2 step :
    #---merge----
    # Merge the limbs in the subset
    # score : score
    # parts_num : How many limbs are in the subset 
    ###############################
    
    cat_subset = np.zeros(20) #用來合併的矩陣
    cat_subset = cat_subset.reshape(1,len(subset.T))
    while(len(subset)!=0):
        #取出subset的第一筆和後面的subset比較
        temp=subset[0].copy()
        finish=[] #紀錄等等那些subset合併完成可以刪掉

        for i in range(1,len(subset)):
            for j in range(18):
                #如果有和subset相同的就要merge
                if(subset[i][j]==temp[j] and temp[j]!= -1):
                    #要更新到temp的部位
                    update_index=[k for k in range(18) if subset[i][k]!=-1 and subset[i][k]!=temp[k]]
                    temp[update_index]=subset[i][update_index]
                    #加score
                    temp[18]+=subset[i][18]
                    finish.append(i)
        #計算part_num
        temp[19]=0
        for i in range(18):
            if(temp[i]!=-1):
                temp[19]+=1
        temp = temp.reshape(1,len(subset.T))
        cat_subset=np.concatenate([cat_subset,temp]) #完成一個人的合併
        #刪掉合併過的subset
                #delete已經merge的index    
        delete_idx = []
        delete_idx.append(0)
        for i in range(len(finish)): 
            delete_idx.append(finish[i])
        subset = np.delete(subset, delete_idx, axis=0)

    # after merge
    #---delete---
    # Delete the non-compliant subset
    # 1. parts_num < 4
    # 2. Average score(score / parts_num) < 0.4 
    ############################################
    print(cat_subset.shape)
    
    delete_idx = []
    for i in range(len(cat_subset)): 
        if cat_subset[i][19]<4 or (cat_subset[i][18]/cat_subset[i][19])<0.4:  # revise here
            delete_idx.append(i)
    cat_subset = np.delete(cat_subset, delete_idx, axis=0)
    print(cat_subset)
    return cat_subset
