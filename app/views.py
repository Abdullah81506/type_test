from django.shortcuts import render
import random
from django.shortcuts import render, redirect
from .models import Paragraph, TypingResult
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def home(request):
    return render(request, 'app/home.html')

@login_required
def typing_test(request):
    difficulty = request.GET.get('difficulty') # Get the difficulty level from the query parameters 

    if difficulty not in ['easy', 'beginner', 'hard']: 
        return redirect('home') # if invalid, redirect to home page

    paragraphs = Paragraph.objects.filter(difficulty=difficulty)  # Filter paragraphs based on the selected difficulty level 

    paragraph = random.choice(paragraphs).text if paragraphs.exists() else "No paragraphs available for this difficulty" # Randomly select a paragraph from the filtered list if it exists, otherwise return a default message

    context = {'paragraph': paragraph,'difficulty': difficulty}

    return render(request, 'app/typing_test.html', context )

@csrf_exempt
@login_required
def save_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # Parse the JSON data sent by JavaScript
            
            # Validate data
            difficulty = data.get('difficulty')
            if difficulty not in ['easy', 'beginner', 'hard']:
                raise ValueError("Invalid difficulty level")
                
            wpm = float(data.get('wpm', 0))
            accuracy = float(data.get('accuracy', 0))
            typos = int(data.get('typos', 0))
            
            # Create and save the result
            result = TypingResult.objects.create(
                user=request.user,
                difficulty=difficulty,
                wpm=wpm,
                accuracy=accuracy,
                typos=typos
            )
            
            return JsonResponse({  # 
                'status': 'success',
                'id': result.id
            })

        except Exception as e: # Handle any exceptions that occur during processing
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid method'
    }, status=405)


@login_required
def results(request):
    # Get historical results for chart
    results = TypingResult.objects.filter(user=request.user).order_by('-timestamp') 

    labels = [result.timestamp.strftime('%b %d, %Y') for result in results] # prepare labels for the chart using the timestamp of each result
    net_wpm_data = [round(result.wpm * (result.accuracy / 100.0)) for result in results]  # Calculate net WPM based on accuracy

    # Get latest test results from query params
    gross_wpm = request.GET.get('wpm', 0)
    accuracy = request.GET.get('accuracy', 0)
    net_wpm = request.GET.get('netSpeed', 0)
    typos = request.GET.get('typos', 0)

    return render(request, 'app/results.html', {
        'labels': labels,
        'wpm_data': net_wpm_data,  
        'max_wpm': max(net_wpm_data) if net_wpm_data else 0,
        'gross_wpm': gross_wpm,
        'accuracy': accuracy,
        'net_wpm': net_wpm,
        'typos': typos
    })



@login_required
def get_paragraph(request):
    difficulty = request.GET.get('difficulty') # Get the difficulty level from the query parameters
    if difficulty not in ['easy', 'beginner', 'hard']: 
        return JsonResponse({'paragraph': 'Invalid difficulty level.'}, status=400)
    
    paragraphs = list(Paragraph.objects.filter(difficulty=difficulty)) # Filter paragraphs based on the selected difficulty level
    
    if paragraphs: 
        paragraph = random.choice(paragraphs) 
        return JsonResponse({'paragraph': paragraph.text}) # Return the text of the randomly selected paragraph json response is used by JavaScript to display the paragraph in the typing test page without reloading the page 
    
    return JsonResponse({
        'paragraph': 'No paragraphs available for this difficulty level.'
    }, status=404)
