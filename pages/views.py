from django.shortcuts import render

# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
import pickle
import pandas as pd

def homePageView(request):
    # return request object and specify page.

    return render(request, 'home.html', {
        'genders': ["Male", "Female"],
        'job_types': ["Employed", "Self employed"],
        'educational_status': ["High school", "Bachelor", "Master", "PhD"]})


def homePost(request):
    # Create variable to store choice that is recognized through entire function.
    age = 30
    gender = "Male"
    appearance_score = 50
    job_type = "Employed"
    educational_status = "Bachelor"

    try:
        # Extract value from request object by control name.
        current_age = request.POST['age']
        gender = request.POST['gender']
        current_appearance_score = request.POST['appearance_score']
        job_type = request.POST['job_type']
        educational_status = request.POST['educational_status']

        # Crude debugging effort.
        age = int(current_age)
        appearance_score = int(current_appearance_score)

        print("User choice!")
        print(age)
        print(gender)
        print(appearance_score)
        print(job_type)
        print(educational_status)

    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage': '*** The choice was missing please try again',
            'genders': ["Male", "Female"],
            'job_types': ["Employed", "Self employed"],
            'educational_status': ["High school", "Bachelor", "Master", "PhD"]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'age': age,
                                                               'gender': gender,
                                                               'appearance_score': appearance_score,
                                                               'job_type': job_type,
                                                               'educational_status': educational_status},))


def results(request, age, gender, appearance_score, job_type, educational_status):
    print("*** Inside results()")
    # load saved model
    with open('./model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['Age', 'Gender', 'Appearance_Score', 'Job_Type', 'Educational_Status_Bsc',
                 'Educational_Status_High School', 'Educational_Status_Master', 'Educational_Status_PhD'])

    singleSampleDf = singleSampleDf._append({'Age': int(age),
                                             'Gender': 1 if gender == "Male" else 0,
                                             'Appearance_Score': int(appearance_score),
                                             'Job_Type': 1 if job_type == "Employed" else 0,
                                             'Educational_Status_Bsc': 1 if educational_status == "Bachelor" else 0,
                                             'Educational_Status_High School': 1 if educational_status == "High school" else 0,
                                             'Educational_Status_Master': 1 if educational_status == "Master" else 0,
                                             'Educational_Status_PhD': 1 if educational_status == "PhD" else 0},
                                            ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))
    print(singlePrediction[0])
    string_prediction = "You will have Valentine Date :)" if singlePrediction[0] == 1 \
        else "You will not have Valentine date :'("

    return render(request, 'results.html', {'age': age, 'gender': gender, 'appearance_score': appearance_score,
                                            'job_type': job_type, 'educational_status': educational_status,
                                            'prediction': singlePrediction, 'string_prediction': string_prediction})


def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')
