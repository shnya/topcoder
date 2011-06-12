# Create your views here.
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from tcpractice.models import Problem,Round,History
from django.db import transaction
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from datetime import datetime
import urllib2
import re

def getProblems(roundid):
    pids = []
    try:
        html = urllib2.urlopen('http://www.topcoder.com/stat?c=round_overview&er=0&rd=%s' % roundid).read()
        reg = re.compile("problem_statement\&pm\=(\d+)\&[^<>]*>([^<>]*)<");
        start = 0
        for i in xrange(0,6):
            m = reg.search(html,start)
            if m == None:
                return []
            start = m.end()+1
            pid = int(m.group(1))
            pname = m.group(2)
            pids.append(((i%3)+1, (i/3)+1, pid, pname))
    except:
        return []
    return pids

@transaction.commit_on_success
def saveProblems(roundid):
    probs = getProblems(roundid)
    if len(probs) < 6:
        raise Exception("can't get problems")
    for p in probs:
        prob,created = Problem.objects.get_or_create(problemid=p[2],
                                             level=p[0],
                                             division=p[1],
                                             round=Round.objects.get(id=roundid))
        prob.name = p[3]
        prob.save()

@login_required
def index(request):
    rounds = Round.objects.all().order_by("-id")
    hist = History.objects.filter(user=request.user).order_by("-round")
    hists = {}
    for h in hist:
        rid = h.round.id
        p = h.problem
        if not rid in hists:
            hists[rid] = [
                h.round.name,
                h.round.id,
                [False,False,False],
                [False,False,False]
                ]
        hists[rid][1+p.division][p.level-1] = True
    hists2 = hists.values()
    hists2.sort(lambda x,y : int(y[1] - x[1]))
    c = {
        'username' : request.user.username,
        'rounds' : rounds,
        'hist' : hists2
        }
    c.update(csrf(request))
    return render_to_response('./index.html', c)


@login_required
def create(request):
    p = Problem()
    r = Round.objects.get(id=request.POST['roundid'])
    try:
        p = Problem.objects.get(division=request.POST['division'],
                                level=request.POST['level'],
                                round=r)
    except Problem.DoesNotExist:
        saveProblems(r.id)
        p = Problem.objects.get(division=request.POST['division'],
                                level=request.POST['level'],
                                round=r)
    memo = ""
    code = ""
    try:
        hist = History.objects.get(user=request.user,
                                   round=r,
                                   problem=p)
        memo = hist.memo
        code = hist.code
        if 'delete' in request.POST:
            if request.POST['delete'] == 'delete':
                hist.delete()
                return HttpResponseRedirect('./')
    except History.DoesNotExist:
        pass
    

    c = {
        'problem' : p,
        'round' : r,
        'memo' : memo,
        'code' : code,
        'level' : ['Easy','Medium','Hard'][p.level-1]
        }
    c.update(csrf(request))
    return render_to_response('./create.html',c)

@login_required
def create_done(request):
    round = Round(id=request.POST['roundid'])
    prob = Problem.objects.get(id=request.POST['problemid'])
    memo = request.POST['memo'];
    code = request.POST['code'];
    hist,created = History.objects.get_or_create(user=request.user,
                                                 round=round,
                                                 problem=prob,
                                                 defaults={
                                                     'ctime': datetime.now(),
                                                     'mtime': datetime.now()
                                                     })
    hist.memo = memo;
    hist.code = code;
    hist.mtime = datetime.now()
    hist.save()
    return HttpResponseRedirect('./')

@login_required
def detail(request):
    r = Round.objects.get(id=request.GET['roundid'])
    prob = Problem.objects.get(level=request.GET['level'],
                               division=request.GET['division'],
                               round=r)
    hist = History.objects.get(user=request.user,
                               round=r,
                               problem=prob)
    c = {
        'hist' : hist,
        'problem' : prob,
        'round' : r,
        'level' : ['Easy','Medium','Hard'][prob.level-1]
        }
    c.update(csrf(request))
    return render_to_response('./detail.html',c)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('./')

def login_view(request):
    if 'username' in request.POST:
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user == None:
            c = {"error_message": "Failed Login"}
            c.update(csrf(request))
            return render_to_response('./login.html',c)
        else:
            login(request,user)
            return HttpResponseRedirect('./')
    else:
        c = {"error_message":False}
        c.update(csrf(request))
        return render_to_response('./login.html',c)

def create_new_user(request):
    try:
        User.objects.get(username=request.POST['username'])
        c = {"error_message":"This account already exists."}
        c.update(csrf(request))
        return render_to_response('./login.html',c)
    except User.DoesNotExist:
        User.objects.create_user(request.POST['username'],
                                 "",
                                 request.POST['password'])
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        login(request,user)
    return HttpResponseRedirect('./')
    


    
