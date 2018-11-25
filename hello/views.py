from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
import json
import requests
import os
import threading
from pprint import pprint
from .models import Greeting
from scrapyd_api import ScrapydAPI
from time import sleep

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request,'formpage.html')

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})

def crawl(request):
	if request.method == 'POST':
		#-----------------pending test -----------------
		data = {
		'result' : 'pending'
		}
		return JsonResponse(data)
		#----------------Get Values from From Submit--------------------------
		company = request.POST.get('name', None)
		url = request.POST.get('url', None)
		address = request.POST.get('address', None)
		city = request.POST.get('city', None)
		state = request.POST.get('state', None)
		zipcode = request.POST.get('zipcode', None)
		telephone = request.POST.get('telephone', None)

		#-----------------Make Shared Storage when report captured on Server(for ajax and scray and django)-----------
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		#dirname = 'store_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S') #2010.08.09.12.08.45 
		#os.mkdir(os.path.join(BASE_DIR+'/sharedstorage', dirname))
		Scrapy_DIR = BASE_DIR+'/scrapy_app/'

		#------------Create JSON file to scrapy app path and save JSON data to file-------------------------------------
		basename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		iname = 'image_'+basename
		os.mkdir(os.path.join(BASE_DIR+'/hello/static', iname))

		jdata = {
		'company':company,
		'url':url,
		'address':address,
		'city':city,
		'state':state,
		'zipcode':zipcode,
		'telephone':telephone,
		'BASE_DIR':BASE_DIR,
		'Scrapy_DIR':Scrapy_DIR,
		'Image_DIR':iname
		}

		with open(Scrapy_DIR+'/data.json', 'w') as outfile:
			json.dump(jdata, outfile)

		#-------------Check Flag and Start Scrapy with Scrapyd--------------------------------
		data = {
		'project': 'scrapy_app',
		'spider': 'autoreport'
		}

		try:
			with open('flag.json') as f:
				fl_json = json.load(f)
			pass
		except Exception as e:
			try:
				scrapy_respon = requests.post('http://localhost:6800/schedule.json', data=data)
				pass
			except Exception as e:
				datas = {
				'result' : 'error',
				'errors' : {'key':'Server Error','val':'Scrapy not working!!!'}
				}
				return JsonResponse(datas)
		else:
			pass

		sleep(10)
		while True:
			sleep(5)
			with open(BASE_DIR+'/hello/static/'+iname+'/data.json') as f:
				respon_json = json.load(f)
			respon_status = respon_json['status']
			pprint(respon_status)
			if respon_status == 'finished':
				break
			else:
				datas = {
				'result' : 'pending',
				'errors' : {'key':'pending Error','val':'pending now!!!'}
				}
				#jflag = {
				# 'flag' : 'started'
				#}
				#with open('flag.json','w') as ofile:
				#	json.dump(jflag, ofile)
				return JsonResponse(datas)
			pass

		with open(BASE_DIR+'/hello/static/'+iname+'/data.json') as f:
			json_data = json.load(f)

		pinggrade = json_data['pinggrade']
		pingsize = json_data['pingsize']
		pingtime =  json_data['pingtime']
		pingreq = json_data['pingreq']
		loreview = json_data['loreview']
		lopercent = json_data['lopercent']
		mobspeed = json_data['gispeedm']
		deskspeed = json_data['gispeedd']
		gtspeed = json_data['gtspeed']
		gtyslow = json_data['gtyslow']
		gtloadtime = json_data['gtloadtime']
		gtpagesize = json_data['gtpagesize']
		gtreqcount = json_data['gtrequest']

		pprint(str(pinggrade))

		#-----------------Making HTML Content Message--------------------------
		message = """<html>
		<head>
			<meta content='text/html; charset=UTF-8' http-equiv='content-type'>
    		<link href="/static/report.css" rel='stylesheet' />
		</head>
		<body class="c10">
			<div class="c10">
			<table class="c13">
		        <tbody>
		            <tr class="c0">
		                <td class="c19" colspan="1" rowspan="1">
		                    <p class="c5"><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 96.45px; height: 86.50px;"><img alt="" src="/static/logo.jpg" style="width: 96.45px; height: 86.50px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p>
		                </td>
		                <td class="c6" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c3"><br>Monopoly Digital<br></span><span>Monopolydigital.com</span><span class="c3"><br></span><span class="c9 c3"><a class="c12" href="mailto:info@monopolydigital.com">info@monopolydigital.com</a></span><span class="c1"><br>(800) 677-0269</span></p>
		                </td>
		            </tr>
		        </tbody>
		    </table>
		    <table class="c13">
		        <tbody>
		            <tr class="c0">
		                <td class="c20" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c4">"""+company+"""<br>"""+address+"""</span></p>
		                    <p class="c5"><span class="c4">"""+city+""", """+state+""" """+zipcode+"""</span></p>
		                    <p class="c5"><span class="c4">"""+telephone+"""<br>"""+url+"""</span></p>
		                </td>
		            </tr>
		        </tbody>
		    </table>
		    <p class="c5"><span class="c1"><br>Snapshot: """+datetime.now().date().strftime('%m/%d/%Y')+"""<br></span></p>
		    <p class="c5"><span class="c4">We use internal tools in addition to well respected, 3rd party independent testing to generate this report that identifies the top metrics that affect your digital presence:</span></p>
		    <p class="c5"><span class="c3">Website performance</span><span class="c4">&nbsp;- If your site is running slow, the user experience will be poor and Google is much less likely to rank your site for any competitive terms.</span></p>
		    <p class="c5"><span class="c3">Name search results:</span><span class="c4">&nbsp;What does it look like when a potential customer searches your name on Google? &nbsp;You should have accurate info, great reviews and hopefully your competition isn&rsquo;t ranking on top of your name.</span></p>
		    <p class="c5"><span class="c3">Review results: &nbsp;</span><span>When someone searches for your name or industry + reviews, what do they see? &nbsp;Is this an accurate depiction of your business?<br></span><span class="c3">Comprehensive local results: &nbsp;</span><span class="c4">Does your business information have congruence across the web? If not, your customers are likely to get confused, but most importantly Google gets confused and is likely to not rank you in the top local listings. &nbsp;This can dramatically affect your web traffic.</span></p>
		    <p class="c5"><span class="c18">Major issues are highlighted in red. If these items are not addressed and corrected, it is likely your site will not rank for your industry keywords.</span></p>
		    <p class="c5"><span class="c4">Screenshots for all metrics taken on the date of this report are attached below.</span></p>
		    <p class="c5 c7"><span class="c1"></span></p>
		    <p class="c5"><span>Questions about this report? Email us: </span><span class="c9"><a class="c12" href="mailto:info@monopolydigital.com">info@monopolydigital.com</a></span><span>&nbsp; Please include the report date and if you have multiple locations, please include the location address.</span></p>
		    <table class="c13">
		        <tbody>
		            <tr class="c0">
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">Pagespeed:</a></span><span><br></span><span class="c2">Mobile: """+str(mobspeed)+"""/100<br>Desktop: """+str(deskspeed)+"""/100</span></p>
		                </td>
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">Pingdom:</a></span><span><br></span><span class="c2">Grade: D """+str(pinggrade)+"""%<br>Page size: """+str(pingsize)+"""<br>Load time: """+str(pingtime)+"""<br>Requests: """+str(pingreq)+"""</span></p>
		                </td>
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">GTmetrix:</a></span><span class="c3"><br></span><span class="c2">Grade: F """+str(gtspeed)+"""<br>YSlow: E """+str(gtyslow)+"""<br>Load time: """+str(gtloadtime)+"""s<br>Page size: """+str(gtpagesize)+"""<br>Requests: """+str(gtreqcount)+"""</span></p>
		                </td>
		            </tr>
		            <tr class="c0">
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">Think With Google:</a></span><span><br></span><span class="c2">Test results: Poor<br>Customer loss: 33%</span></p>
		                </td>
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">Comprehensive Local Search:</a></span><span><br></span><span class="c2">"""+str(lopercent)+"""% Listing Inaccuracy<br>"""+str(loreview)+"""</span></p>
		                </td>
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c7 c8"><span class="c1"></span></p>
		                </td>
		            </tr>
		        </tbody>
		    </table>
		    <p class="c5"><span class="c3 c9"><a class="c12">Name search results:</a></span><span><br>Organic Rank for name: #1<br>Paid rank for name: None. </span><span class="c2">Competition is advertising on top</span><span class="c4"><br>Competing sites not ranking organically for name search<br>Ratings in name search:</span></p>
    		<p class="c5 c16"><span>Google: 1 review, 5 stars<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="c2">Yelp: 1 review, 1 star</span><span class="c4"><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Others: Yellow pages 3 reviews, 5 stars</span></p>
    		<p class="c5"><span class="c3">Local results:</span><span><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sidebar showing in organic search<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="c14 c2">Missing information<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Address incorrect<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shows residential location in outside pics</span></p>
    		<p class="c5"><span class="c9 c3"><a class="c12">Reviews results:</a></span><span><br>Google: 1 review, 5 star<br>Yelp: 11 reviews, 3.5 Stars<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="c2">1 review, 1 star</span><span><br></span><span class="c2">Two Yelp pages for a single location</span><span class="c4"><br>Yellow pages 3 reviews, 5 stars</span></p>
    		<p class="c5"><span class="c3">Screenshots:</span><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 960.00px; height: 840.00px;"><img alt="" src="/static/"""+str(iname)+"""/screenshot1.png" style="width: 960.00px; height: 840.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 960.00px; height: 840.00px;"><img alt="" src="/static/"""+str(iname)+"""/screenshot0.png" style="width: 960.00px; height: 840.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span><span><br></span><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 960.00px; height: 840.00px;"><img alt="" src="/static/"""+str(iname)+"""/screenshot2.png" style="width: 960.00px; height: 840.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p>
    		<p class="c17"><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 960.00px; height: 840.00px;"><img alt="" src="/static/"""+str(iname)+"""/screenshot3.png" style="width: 960.00px; height: 840.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p>
    		<p class="c17"><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 960.00px; height: 840.00px;"><img alt="" src="/static/"""+str(iname)+"""/screenshot4.png" style="width: 960.00px; height: 840.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 960.00px; height: 840.00px;"><img alt="" src="/static/"""+str(iname)+"""/screenshot5.png" style="width: 960.00px; height: 840.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p>
		    </div>
		</body>
		</html>"""

		#--------------------Save to Local message---------------------
		hname = 'report_'+basename+'.html'
		f = open('hello/static/'+hname,'w')

		message1 = """<html>
		<head>
			<meta content='text/html; charset=UTF-8' http-equiv='content-type'>
    		<link href="report.css" rel='stylesheet' />
		</head>
		<body class="c10">
			<div class="c10">
			<table class="c13">
		        <tbody>
		            <tr class="c0">
		                <td class="c19" colspan="1" rowspan="1">
		                    <p class="c5"><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 96.45px; height: 86.50px;"><img alt="" src="logo.jpg" style="width: 96.45px; height: 86.50px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p>
		                </td>
		                <td class="c6" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c3"><br>Monopoly Digital<br></span><span>Monopolydigital.com</span><span class="c3"><br></span><span class="c9 c3"><a class="c12" href="mailto:info@monopolydigital.com">info@monopolydigital.com</a></span><span class="c1"><br>(800) 677-0269</span></p>
		                </td>
		            </tr>
		        </tbody>
		    </table>
		    <table class="c13">
		        <tbody>
		            <tr class="c0">
		                <td class="c20" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c4">"""+company+"""<br>"""+address+"""</span></p>
		                    <p class="c5"><span class="c4">"""+city+""", """+state+""" """+zipcode+"""</span></p>
		                    <p class="c5"><span class="c4">"""+telephone+"""<br>"""+url+"""</span></p>
		                </td>
		            </tr>
		        </tbody>
		    </table>
		    <p class="c5"><span class="c1"><br>Snapshot: """+datetime.now().date().strftime('%m/%d/%Y')+"""<br></span></p>
		    <p class="c5"><span class="c4">We use internal tools in addition to well respected, 3rd party independent testing to generate this report that identifies the top metrics that affect your digital presence:</span></p>
		    <p class="c5"><span class="c3">Website performance</span><span class="c4">&nbsp;- If your site is running slow, the user experience will be poor and Google is much less likely to rank your site for any competitive terms.</span></p>
		    <p class="c5"><span class="c3">Name search results:</span><span class="c4">&nbsp;What does it look like when a potential customer searches your name on Google? &nbsp;You should have accurate info, great reviews and hopefully your competition isn&rsquo;t ranking on top of your name.</span></p>
		    <p class="c5"><span class="c3">Review results: &nbsp;</span><span>When someone searches for your name or industry + reviews, what do they see? &nbsp;Is this an accurate depiction of your business?<br></span><span class="c3">Comprehensive local results: &nbsp;</span><span class="c4">Does your business information have congruence across the web? If not, your customers are likely to get confused, but most importantly Google gets confused and is likely to not rank you in the top local listings. &nbsp;This can dramatically affect your web traffic.</span></p>
		    <p class="c5"><span class="c18">Major issues are highlighted in red. If these items are not addressed and corrected, it is likely your site will not rank for your industry keywords.</span></p>
		    <p class="c5"><span class="c4">Screenshots for all metrics taken on the date of this report are attached below.</span></p>
		    <p class="c5 c7"><span class="c1"></span></p>
		    <p class="c5"><span>Questions about this report? Email us: </span><span class="c9"><a class="c12" href="mailto:info@monopolydigital.com">info@monopolydigital.com</a></span><span>&nbsp; Please include the report date and if you have multiple locations, please include the location address.</span></p>
		    <table class="c13">
		        <tbody>
		            <tr class="c0">
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">Pagespeed:</a></span><span><br></span><span class="c2">Mobile: """+str(mobspeed)+"""/100<br>Desktop: """+str(deskspeed)+"""/100</span></p>
		                </td>
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">Pingdom:</a></span><span><br></span><span class="c2">Grade: D """+str(pinggrade)+"""%<br>Page size: """+str(pingsize)+"""<br>Load time: """+str(pingtime)+"""<br>Requests: """+str(pingreq)+"""</span></p>
		                </td>
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">GTmetrix:</a></span><span class="c3"><br></span><span class="c2">Grade: F """+str(gtspeed)+"""<br>YSlow: E """+str(gtyslow)+"""<br>Load time: """+str(gtloadtime)+"""s<br>Page size: """+str(gtpagesize)+"""MB<br>Requests: """+str(gtreqcount)+"""</span></p>
		                </td>
		            </tr>
		            <tr class="c0">
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">Think With Google:</a></span><span><br></span><span class="c2">Test results: Poor<br>Customer loss: 33%</span></p>
		                </td>
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c5"><span class="c9 c3"><a class="c12">Comprehensive Local Search:</a></span><span><br></span><span class="c2">"""+str(lopercent)+"""% Listing Inaccuracy<br>"""+str(loreview)+"""</span></p>
		                </td>
		                <td class="c15" colspan="1" rowspan="1">
		                    <p class="c7 c8"><span class="c1"></span></p>
		                </td>
		            </tr>
		        </tbody>
		    </table>
		    <p class="c5"><span class="c3 c9"><a class="c12">Name search results:</a></span><span><br>Organic Rank for name: #1<br>Paid rank for name: None. </span><span class="c2">Competition is advertising on top</span><span class="c4"><br>Competing sites not ranking organically for name search<br>Ratings in name search:</span></p>
    		<p class="c5 c16"><span>Google: 1 review, 5 stars<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="c2">Yelp: 1 review, 1 star</span><span class="c4"><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Others: Yellow pages 3 reviews, 5 stars</span></p>
    		<p class="c5"><span class="c3">Local results:</span><span><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sidebar showing in organic search<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="c14 c2">Missing information<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Address incorrect<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shows residential location in outside pics</span></p>
    		<p class="c5"><span class="c9 c3"><a class="c12">Reviews results:</a></span><span><br>Google: 1 review, 5 star<br>Yelp: 11 reviews, 3.5 Stars<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="c2">1 review, 1 star</span><span><br></span><span class="c2">Two Yelp pages for a single location</span><span class="c4"><br>Yellow pages 3 reviews, 5 stars</span></p>
    		<p class="c5"><span class="c3">Screenshots:</span><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 768.00px; height: 697.33px;"><img alt="" src='"""+str(iname)+"""/screenshot1.png' style="width: 768.00px; height: 697.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 768.00px; height: 672.00px;"><img alt="" src='"""+str(iname)+"""/screenshot0.png' style="width: 768.00px; height: 672.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span><span><br></span><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 768.00px; height: 732.00px;"><img alt="" src='"""+str(iname)+"""/screenshot2.png' style="width: 768.00px; height: 732.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p>
    		<p class="c17"><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 781.05px; height: 680.50px;"><img alt="" src='"""+str(iname)+"""/screenshot3.png' style="width: 781.05px; height: 680.50px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p>
    		<p class="c17"><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 763.00px; height: 367.00px;"><img alt="" src='"""+str(iname)+"""/screenshot4.png' style="width: 763.00px; height: 949.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span><span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 698.50px; height: 1040.66px;"><img alt="" src='"""+str(iname)+"""/screenshot5.png' style="width: 698.50px; height: 1040.66px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" title=""></span></p>
		    </div>
		</body>
		</html>"""

		f.write(message1)
		f.close()

		data = {
	        'result': 'success',
	        'htmlcontent': message
        }

		return JsonResponse(data)