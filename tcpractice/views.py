# Create your views here.
from django.core.context_processors import csrf
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from tcpractice.models import ProblemType,Problem,Round,History
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
            pids.append(((i%3)+1, (i/3)+1, pid,pname))
    except:
        return []
    return pids

def saveProblems(roundid):
    r = Round(id=roundid)
    probs = getProblems(roundid)
    if len(probs) < 6:
        raise Exception('can\'t get problems')
    for p in probs:
        probtype = ProblemType(level=p[0],division=p[1])
        probtype.save()
        problem = Problem(id=p[2],
                          name=p[3])
        problem.ptypes.add(probtype.id);
        problem.save()
        r.problems.add(problem.id)
        r.save()

def searchProblem(problems,division,level):
    for p in problems:
        for ptype in p.ptypes.all():
            if ptype.level == level and ptype.division == division:
                return p
            
@login_required
def index(request):
    rounds = Round.objects.all().order_by("-id")
    hist = History.objects.filter(user=request.user).order_by("-roundid")
    hists = {}
    for h in hist:
        rid = h.roundid.id
        if not rid in hists:
            hists[rid] = {
                "rname" : h.roundid.name,
                "div1_1" : False,
                "div1_2" : False,
                "div1_3" : False,
                "div2_1" : False,
                "div2_2" : False,
                "div2_3" : False
                }
        for ptype in h.probid.ptypes.all():
            hists[rid]["div"+str(ptype.level)+"_"+str(ptype.division)] = True
    hists2 = []
    level_str = ["Easy","Medium","Hard"]
    level_str2 = ["-Easy","-Medium","-Hard"]
    for (rid,rvals) in hists.iteritems():
        s = []
        s.append(rvals["rname"])
        for i in xrange(1,3):
            s2 = ""
            for j in xrange (1,4):
                if rvals["div"+str(i)+"_"+str(j)] == True:
                    s2 += level_str[j-1]
                else:
                    s2 += level_str2[j-1]
            s2 += " "
            s.append(s2)
        hists2.append(s)
            
    c = {
        'username' : request.user.username,
        'rounds' : rounds,
        'hists2' : hists2,
        }
    c.update(csrf(request))
    return render_to_response('./index.html', c)


@login_required
def create(request):
    r = Round(id=request.POST['round'])
    p = r.problems.all()
    if len(p) == 0:
        saveProblems(request.POST['round'])
    c = {
        'problem' : searchProblem(p,toInt(request.POST['level']),
                                  toInt(request.POST['division'])),
        'roundid' : request.POST['round'],
        }
    c.update(csrf(request))
    return render_to_response('./create.html',c)

@login_required
def create_done(request):
    rid = Round(id=request.POST['roundid'])
    prob = Problem(id=request.POST['problemid'])
    memo = request.POST['memo'];
    code = request.POST['code'];
    hist = History(user=request.user,
                   roundid=rid,
                   probid=prob,
                   memo=memo,
                   code=code,
                   ctime=datetime.now(),
                   mtime=datetime.now())
    hist.save()
    return HttpResponseRedirect('./')
                   
    

def login(requst):
    return HttpResponse("<html><body>login</body></html>")
