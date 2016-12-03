from django.http import HttpResponse
from django.shortcuts import render
import requests,json

# Create your views here.
def index(request):
    return render(request , 'index.html')

def navigator(request):
    context = {
        'search_term': request.GET['search_term'],
    }
    param = { 'q': request.GET['search_term'] }
    response = requests.get('https://api.github.com/search/repositories', params=param)
    if response.status_code == 200 and response.json():
        data = json.loads(response.text)
        repos = (data['items'])

       # sorted_repos= sorted(l, key=itemgetter('created_at'), reverse=True)
        sorted_repos = sorted(repos, key=lambda k: k['created_at'], reverse=True)
        count = 1
        for each in sorted_repos:
            if count > 5:
                break
            url = each['url'] + '/commits'
            response = requests.get(url)
            if response.status_code == 200 and response.json():
                data = response.json()
                for commit in data:
                    each['last_commit'] = {
                        'sha': commit['sha'],
                        'message': commit['commit']['message'],
                        'author': commit['commit']['author']['name']
                    }
                    break
            count += 1
        context['repos'] = sorted_repos
    else:
        print('not json')
    return render(request, 'template.html', context=context)