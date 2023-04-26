# -*- coding: utf-8 -*-
import os
import threading
from django.http import JsonResponse
from Spider.NewsUrlSpider import begincollect
from Spider.NewsDetailSpider import begindetailcollect
from Spider import NewsUrlSpider, NewsDetailSpider
from news_api.models import spiderstate, urlcollect


def beginUrlSpider(request):
    '''
        @Description：启动新闻URL采集系统
        @:param time  --> 系统运行间隔时间
        @:param oritime  --> 系统运行间隔时间（原始记录用于前端读取显示）
    '''
    if request.method == "GET":
        time = request.GET.get('time')
        oritime = request.GET.get('oritime')
        t = threading.Thread(target=begincollect, kwargs={'time': time})
        t.setDaemon(True)
        t.start()
        spiderstate.objects.filter(spiderid=1).update(status=1, interval=oritime)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def beginDetailSpider(request):
    '''
        @Description：启动新闻详情页内容采集系统
        @:param time  --> 系统运行间隔时间
        @:param oritime  --> 系统运行间隔时间（原始记录用于前端读取显示）
    '''
    if request.method == "GET":
        time = request.GET.get('time')
        oritime = request.GET.get('oritime')
        t = threading.Thread(target=begindetailcollect, kwargs={'time': time})
        t.setDaemon(True)
        t.start()
        # begindetailcollect(time)
        spiderstate.objects.filter(spiderid=2).update(status=1, interval=oritime)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def closeSpiderThread(request):
    '''
        @Description：关闭爬虫系统
        @:param None
    '''
    if request.method == "GET":
        servename = request.GET.get('servename')
        if servename == 'url':
            spiderstate.objects.filter(spiderid=1).update(status=0, interval='')
            NewsUrlSpider.endsched()
        elif servename == 'detail':
            spiderstate.objects.filter(spiderid=2).update(status=0, interval='')
            NewsDetailSpider.endsched()
        # getpidandkill(servename)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def getSpiderPageData(request):
    '''
        @Description：获取爬虫系统管理页数据
        @:param None
    '''

    if request.method == "GET":
        statelist = spiderstate.objects.all()
        urllist = urlcollect.objects.all()
        urlloglist = dict()
        detaillist = dict()
        files = os.listdir('./Spider/Detaillogs')
        for file in files:
            if str(file) in ('log.log', '.keep'):
                pass
            time = file[8:].replace("_", ' ')
            time = time[:13] + ':' + time[14:16] + ':' + time[17:]
            filepath = os.path.join('./Spider/Detaillogs', file)
            urlloglist[file] = {
                'time': time,
                'filepath': filepath
            }
        files = os.listdir('./Spider/Urllogs/')
        for file in files:
            if str(file) in ('log.log', '.keep'):
                pass
            time = file[8:].replace("_", ' ')
            time = time[:13] + ':' + time[14:16] + ':' + time[17:]
            filepath = os.path.join('./Spider/Urllogs/', file)
            detaillist[file] = {
                'time': time,
                'filepath': filepath
            }
        statistical = dict()
        for url in urllist:
            if statistical.get(url.time) == None:
                statistical[url.time] = 1
            else:
                statistical[url.time] = statistical[url.time] + 1
        spiderstatelist = dict()
        for state in statelist:
            spiderstatelist[state.spiderid] = [state.status, state.interval]
        data = {
            'spiderstatelist': spiderstatelist,
            'statistical': statistical,
            'urlloglist': urlloglist,
            'detaillist': detaillist,

        }
        return JsonResponse({"status": "200", 'message': data})
