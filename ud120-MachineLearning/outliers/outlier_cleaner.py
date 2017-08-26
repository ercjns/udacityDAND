#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    ### your code goes here
    for i in range(len(predictions)):
        sq_error = (net_worths[i] - predictions[i])**2
        new = (ages[i], net_worths[i], sq_error)
        cleaned_data.append(new)

    cleaned_data.sort(key=lambda x: x[2])

    n = int(round(len(cleaned_data)*.9))
    cleaned_data = cleaned_data[:n]
    return cleaned_data

