def depression_level(score):

    if score > 5:
        return "High"
    elif score > 2:
        return "Medium"
    else:
        return "Low"


def suicide_level(score):

    if score >= 7:
        return "High Risk"
    elif score >= 4:
        return "Moderate Risk"
    elif score > 0:
        return "Low Signal"
    else:
        return "No Risk"