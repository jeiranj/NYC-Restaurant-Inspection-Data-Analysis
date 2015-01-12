import numpy as np

def check_grades(grade_list):
    """Check validity of user-supplied 'grade_list'. 
    If not any of (A, B, C), it returns False.
    Args:
        -- grade_list """
    grades = np.unique(grade_list)
    allowed_grades = ['A','B','C']
    not_shared = list(list(set(grades)-set(allowed_grades)))
    if len(not_shared)==0:
        return True
    else: 
        return False
    
    
def check_camis_id(allowed_ids,camis_id):
    """Check validity of user-supplied 'camis_id'. 
    If not in allowed_ids, it returns False.
    Args:
        -- allowed_ids: a list containing all the appropriate caims_ids
        -- camis_id: the user-supplied id corresponding to a restaurant """
    camis_id = int(camis_id)
    allowed_ids = map(int,allowed_ids)
    included = camis_id in allowed_ids
    return included
    