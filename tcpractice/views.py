# Create your views here.
from django.core.context_processors import csrf
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from tcpractice.models import Problem,Round,History
from django.db import transaction

from datetime import datetime
import urllib2
import re

def toInt(str):
    try:
        return int(str)
    except:
        return None

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
        raise Exception('can\'t get problems')
    for p in probs:
        Problem(problemid=p[2],
                name=p[3],
                level=p[0],
                division=p[1],
                round=Round.objects.get(id=roundid)).save()

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
    try:
        p = Problem.objects.get(division=request.POST['division'],
                                level=request.POST['level'],
                                round=request.POST['round'])
    except:
        saveProblems(request.POST['round'])
        p = Problem.objects.get(division=request.POST['division'],
                                level=request.POST['level'],
                                round=request.POST['round'])
    c = {
        'problem' : p,
        'roundid' : request.POST['round'],
        }
    c.update(csrf(request))
    return render_to_response('./create.html',c)

@login_required
def create_done(request):
    round = Round(id=request.POST['roundid'])
    prob = Problem(id=request.POST['problemid'])
    memo = request.POST['memo'];
    code = request.POST['code'];
    hist = History(user=request.user,
                   round=round,
                   problem=prob,
                   memo=memo,
                   code=code,
                   ctime=datetime.now(),
                   mtime=datetime.now())
    hist.save()
    return HttpResponseRedirect('./')



def login(requst):
    return HttpResponse("<html><body>login</body></html>")
