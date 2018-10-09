import datetime, json, openpyxl, os, pythonwhois, re, requests, socket, time, tweepy


twitterAuthData = {
    'consumer_key': 'GET YOUR OWN',
    'consumer_secret': 'GET YOUR OWN',
    'access_token': 'GET YOUR OWN',
    'access_token_secret': 'GET YOUR OWN'
    }


class Disinformation:


    # Initialize object
    # import os
    def __init__(self):

        # Get current directory
        self.appPath = os.path.dirname(os.path.realpath(__file__))

        # Set data directory
        self.dataPath = os.path.join(self.appPath, 'Disinformation')
        if not os.path.exists(self.dataPath): os.makedirs(self.dataPath)

        # Set log path
        self.logPath = os.path.join(self.dataPath, 'Disinformation.log')
        if os.path.exists(self.logPath): os.remove(self.logPath)

        # Set output files
        self.rawOutputPath = os.path.join(self.dataPath, 'Disinformation.json')
        self.excelOutputPath = os.path.join(self.dataPath, 'Disinformation.xlsx')

        # Initialize APIs
        self.InitializeTwitter()
        self.InitializeReddit()

        self.Log('Starting', True)

        domains = [
            {"name": "consortiumnews.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "lifezette.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "presstv.com", "type": "Iran", "sub_type": ""},
            {"name": "blacklistednews.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "rense.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "collective-evolution.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "rt.com", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "presstv.ir", "type": "Iran", "sub_type": ""},
            {"name": "thegatewaypundit.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "sputniknews.com", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "timesofisrael.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "tass.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "globalresearch.ca", "type": "Useful Idiot", "sub_type": ""},
            {"name": "rferl.org", "type": "American", "sub_type": ""},
            {"name": "ria.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "russia-insider.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "100percentfedup.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "tass.com", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "veteranstoday.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "theoccidentalobserver.net", "type": "Useful Idiot", "sub_type": ""},
            {"name": "svoboda.org", "type": "American", "sub_type": ""},
            {"name": "newobserveronline.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "rian.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "southfront.org", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "veteransnewsnow.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "voiceofrussia.com", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "thetruthseeker.co.uk", "type": "Useful Idiot", "sub_type": ""},
            {"name": "journal-neo.org", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "ruvr.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "humansarefree.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "freedomoutpost.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "tjournal.ru", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "mynewsguru.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "fellowshipoftheminds.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "defyccc.com", "type": "Climate Denial", "sub_type": ""},
            {"name": "eutimes.net", "type": "Useful Idiot", "sub_type": ""},
            {"name": "radiosvoboda.org", "type": "American", "sub_type": ""},
            {"name": "pi-news.net", "type": "Useful Idiot", "sub_type": ""},
            {"name": "rtlnieuws.nl", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "savemysweden.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "brutalist.press", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "khamenei.ir", "type": "Iran", "sub_type": ""},
            {"name": "news-front.info", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "std3.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "vestnikkavkaza.net", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "fort-russ.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "greanvillepost.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "darkmoon.me", "type": "Useful Idiot", "sub_type": ""},
            {"name": "hangthebankers.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "azatutyun.am", "type": "American", "sub_type": ""},
            {"name": "eaglerising.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "progressivestoday.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "katehon.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "radiofarda.com", "type": "American", "sub_type": ""},
            {"name": "godfatherpolitics.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "hispantv.com", "type": "Iran", "sub_type": ""},
            {"name": "pontiactribune.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "thefifthcolumnnews.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "darkpolitricks.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "4thmedia.org", "type": "Chinese", "sub_type": ""},
            {"name": "rtlz.nl", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "dirty.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "regnum.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "politicaloutcast.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "svaboda.org", "type": "American", "sub_type": ""},
            {"name": "geopolmonitor.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "davidharrisjr.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "armenialiberty.org", "type": "American", "sub_type": ""},
            {"name": "sptnkne.ws", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "lastresistance.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "dailystormer.name", "type": "Nazi", "sub_type": ""},
            {"name": "usasupreme.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "dninews.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "europalibera.org", "type": "American", "sub_type": ""},
            {"name": "d3.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "hempforfuture.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "azadliq.org", "type": "American", "sub_type": ""},
            {"name": "azadliqradiosu.az", "type": "American", "sub_type": ""},
            {"name": "riafan.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "slobodnaevropa.org", "type": "American", "sub_type": ""},
            {"name": "visiontoamerica.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "whatfinger.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "syriareport.net", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "geopolitica.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "fenixx.org", "type": "Useful Idiot", "sub_type": ""},
            {"name": "alt-right.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "greedmedia.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "geotus.army", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "azattyq.org", "type": "American", "sub_type": ""},
            {"name": "mondialisation.ca", "type": "Useful Idiot", "sub_type": ""},
            {"name": "presstv.us", "type": "Iran", "sub_type": ""},
            {"name": "ozodi.org", "type": "American", "sub_type": ""},
            {"name": "grtv.ca", "type": "Useful Idiot", "sub_type": ""},
            {"name": "hispantv.ir", "type": "Iran", "sub_type": ""},
            {"name": "svobodanews.ru", "type": "American", "sub_type": ""},
            {"name": "leprosorium.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "sentrybugle.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "azattyk.org", "type": "American", "sub_type": ""},
            {"name": "hectorreban.wordpress.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "bighealthreport.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "vesti.lv", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "rubaltic.ru", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "dnipress.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "ozodlik.org", "type": "American", "sub_type": ""},
            {"name": "fightwhitegenocide.com", "type": "Nazi", "sub_type": ""},
            {"name": "rianovosti.com", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "usareally.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "shoebat.org", "type": "Useful Idiot", "sub_type": ""},
            {"name": "libertybuzznews.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "whatreallyhappened.org", "type": "Useful Idiot", "sub_type": ""},
            {"name": "voicerussia.com", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "baltnews.lt", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "presstv.in", "type": "Iran", "sub_type": ""},
            {"name": "azathabar.com", "type": "American", "sub_type": ""},
            {"name": "radiotavisupleba.ge", "type": "American", "sub_type": ""},
            {"name": "geotus.band", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "azathabar.org", "type": "American", "sub_type": ""},
            {"name": "evropaelire.org", "type": "American", "sub_type": ""},
            {"name": "ekhokavkaza.com", "type": "American", "sub_type": ""},
            {"name": "globalresearch.org", "type": "Useful Idiot", "sub_type": ""},
            {"name": "vestikavkaza.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "jovan.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "baltnews.lv", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "no2nato.org", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "hireveterans.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "veteranstodaynetwork.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "veteranstodayjobs.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "mashaalradio.com", "type": "American", "sub_type": ""},
            {"name": "radiosvoboda.ua", "type": "American", "sub_type": ""},
            {"name": "radioazadlyg.org", "type": "American", "sub_type": ""},
            {"name": "ussrfall.com", "type": "American", "sub_type": ""},
            {"name": "azatliq.org", "type": "American", "sub_type": ""},
            {"name": "slobodnaevropa.mk", "type": "American", "sub_type": ""},
            {"name": "radiomarsho.com", "type": "American", "sub_type": ""},
            {"name": "kremlintroll.nl", "type": "Useful Idiot", "sub_type": ""},
            {"name": "thechinawatch.com", "type": "Chinese", "sub_type": ""},
            {"name": "biztass.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "telegraf.lv", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "rtlboulevard.nl", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "hispantv.net", "type": "Iran", "sub_type": ""},
            {"name": "savedonbasspeople.info", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "empoderasalud.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "vahomeloannews.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "veteranstodayforum.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "legalhelp4veterans.info", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "veteranstodaybusinessdirectory.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "militaryveteranjobnews.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "fbipajamas.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "celebritycolumns.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "bridgeagents.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "fitcolumns.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "justinking.org", "type": "Useful Idiot", "sub_type": ""},
            {"name": "nonfictionsection.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "sleepercells.us", "type": "Useful Idiot", "sub_type": ""},
            {"name": "azattyk.kg", "type": "American", "sub_type": ""},
            {"name": "khutynygharadio.com", "type": "American", "sub_type": ""},
            {"name": "radioerkenli.com", "type": "American", "sub_type": ""},
            {"name": "mashaalradio.org", "type": "American", "sub_type": ""},
            {"name": "regionalanalysis.org", "type": "American", "sub_type": ""},
            {"name": "europaelire.org", "type": "American", "sub_type": ""},
            {"name": "iraqhurr.org", "type": "American", "sub_type": ""},
            {"name": "azatradio.org", "type": "American", "sub_type": ""},
            {"name": "makdenes.org", "type": "American", "sub_type": ""},
            {"name": "danas.org", "type": "American", "sub_type": ""},
            {"name": "ozodi.tj", "type": "American", "sub_type": ""},
            {"name": "oxuzali.az", "type": "American", "sub_type": ""},
            {"name": "radioazadlyg.ru", "type": "American", "sub_type": ""},
            {"name": "tavisupleba.org", "type": "American", "sub_type": ""},
            {"name": "ekhokavkaza.org", "type": "American", "sub_type": ""},
            {"name": "rferl.net", "type": "American", "sub_type": ""},
            {"name": "radioazattyk.org", "type": "American", "sub_type": ""},
            {"name": "freedomfulfillment.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "vestnikkavkaza.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "sharpelbows.net", "type": "Useful Idiot", "sub_type": ""},
            {"name": "islamismus.net", "type": "Useful Idiot", "sub_type": ""},
            {"name": "globalresearchtv.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "geopolitika.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "rusnews.cn", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "radiovr.com.cn", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "sputniknews.cn", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "риановости.рф", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "futurico.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "enze.net", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "goohoo.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "conspiracy.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "lepra.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "tasstelecom.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "rttv.ru", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "russiatoday.net", "type": "Russian", "sub_type": "Mainstream"},
            {"name": "the.tj", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "stihi.lv", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "lublu.lv", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "subbota.com", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "baltnews.ee", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "hispantv.mx", "type": "Iran", "sub_type": ""},
            {"name": "hispan.tv", "type": "Iran", "sub_type": ""},
            {"name": "stalkerzone.org", "type": "Russian", "sub_type": "Deceptive"},
            {"name": "stream.org", "type": "Useful Idiot", "sub_type": ""},
            {"name": "thestream.org", "type": "Useful Idiot", "sub_type": ""},
            {"name": "alwaght.com", "type": "Iran", "sub_type": ""},
            {"name": "judicialwatch.org", "type": "Useful Idiot", "sub_type": ""},
            {"name": "corruptionchronicles.com", "type": "Useful Idiot", "sub_type": ""},
            {"name": "obamairsscandal.com", "type": "Useful Idiot", "sub_type": ""}
            ]

        for domain in domains:

            domain['data'] = self.CheckDomain(domain['name'])

        self.ExportJson(domains)

        self.ExportSpreadsheet(domains)

        self.Log('Complete', True)


        return


    def CheckDomain(self, domainName):

        self.Log('CheckDomain : Starting '+domainName, True)

        domainInfo = {
            'name': domainName
            }

        domainInfo['redirect'] = self.DirectLink(domainName)

        domainInfo['domain'] = self.GetDomain(domainName)

        whois = self.GetWhois(domainInfo['domain'])

        if 'whois_server' in whois.keys():

            domainInfo['registrar'] = self.GetDomain(whois['whois_server'][0])

        else:

            domainInfo['registrar'] = domainInfo['domain']

        nameservers = []

        if 'nameservers' in whois.keys():

            for nameserver in whois['nameservers']:

                nameservers.append(self.GetDomain(nameserver))

        domainInfo['nameservers'] = nameservers

        dateInfo = [
            {'key': 'created', 'whois_key': 'creation_date'},
            {'key': 'updated', 'whois_key': 'updated_date'},
            {'key': 'expires', 'whois_key': 'expiration_date'}
            ]

        for dI in dateInfo:

            if dI['whois_key'] in whois.keys():

                domainInfo[dI['key']] = whois[dI['whois_key']][0].timestamp()

            else:

                domainInfo[dI['key']] = 0.0

        domainInfo['search'] = self.GetSearchLinks(domainInfo['domain'])

        domainInfo['twitter_data'] = self.SearchTwitter(domainInfo['domain'])

        domainInfo['reddit_data'] = self.SearchReddit(domainInfo['domain'])

        tracking = self.GetTracking(domainInfo['domain'])

        domainInfo['google_analytics'] = tracking['google_analytics']
        domainInfo['google_adsense'] = tracking['google_adsense']

        self.Log('CheckDomain : Completed '+domainName, True)


        return domainInfo


    # Export domain data as spreadsheet
    # import openpyxl, os
    def ExportSpreadsheet(self, domains):

        self.Log('ExportSpreadsheet : Starting')

        wb = openpyxl.Workbook()

        overviewSheet = wb.active
        overviewSheet.title = 'Overview'

        overviewKeys = [
            {'column': 'A', 'title': 'Domain', 'key': 'name', 'object': 'self'},
            {'column': 'B', 'title': 'Type', 'key': 'type', 'object': 'self'},
            {'column': 'C', 'title': 'Sub Type', 'key': 'sub_type', 'object': 'self'},
            {'column': 'D', 'title': 'Analytics ID', 'key': 'google_analytics', 'object': 'data'},
            {'column': 'E', 'title': 'Adsense ID', 'key': 'google_adsense', 'object': 'data'},
            {'column': 'F', 'title': 'Redirect', 'key': 'redirect', 'object': 'data'},
            {'column': 'G', 'title': 'IP', 'key': 'ip', 'object': 'data.domain'},
            {'column': 'H', 'title': 'Country', 'key': 'country', 'object': 'data.domain'},
            {'column': 'I', 'title': 'City', 'key': 'city', 'object': 'data.domain'},
            {'column': 'J', 'title': 'Registrar', 'key': 'domain', 'object': 'data.registrar'},
            {'column': 'K', 'title': 'Registrar IP', 'key': 'ip', 'object': 'data.registrar'},
            {'column': 'L', 'title': 'Registrar Country', 'key': 'country', 'object': 'data.registrar'},
            {'column': 'M', 'title': 'Registrar City', 'key': 'city', 'object': 'data.registrar'}
            ]

        for overviewKey in overviewKeys:

            overviewSheet[overviewKey['column']+'1'] = overviewKey['title']

        overviewFormulas = [
            {'column': 'N', 'title': 'Reddit Count', 'value': '=IFERROR(INDEX(\'reddit communities\'!D:D,MATCH(A{0},\'reddit communities\'!A:A,0)),0)'},
            {'column': 'O', 'title': 'T_D Count', 'value': '=SUMIFS(\'reddit communities\'!C:C,\'reddit communities\'!B:B,"The_Donald",\'reddit communities\'!A:A,A{0})'},
            {'column': 'P', 'title': 'T_D %', 'value': '=IFERROR(ROUND((O{0}/N{0})*100,2),0)'},
            {'column': 'Q', 'title': 'Twitter Count', 'value': '=IFERROR(INDEX(\'twitter users\'!D:D,MATCH(A{0},\'twitter users\'!A:A,0)),0)'}
            ]

        for overviewFormula in overviewFormulas:

            overviewSheet[overviewFormula['column']+'1'] = overviewFormula['title']

        overviewRow = 2

        overviews = [
            {'title': 'twitter users', 'name': 'User', 'data': 'twitter_data.users', 'key': 'user', 'unique': [], 'row': 2},
            {'title': 'twitter hashtags', 'name': 'Hashtag', 'data': 'twitter_data.hashtags', 'key': 'hashtag', 'unique': [], 'row': 2},
            {'title': 'reddit users', 'name': 'User', 'data': 'reddit_data.users', 'key': 'user', 'unique': [], 'row': 2},
            {'title': 'reddit communities', 'name': 'Community', 'data': 'reddit_data.communities', 'key': 'community', 'unique': [], 'row': 2}
            ]

        for overview in overviews:

            overview['sheet'] = wb.create_sheet(overview['title'])

            overview['sheet']['A1'] = 'Domain'
            overview['sheet']['B1'] = overview['name']
            overview['sheet']['C1'] = overview['name']+' Count'
            overview['sheet']['D1'] = 'Domain Total'
            overview['sheet']['E1'] = overview['name']+' %'

        for domain in domains:

            #
            for overviewKey in overviewKeys:

                if overviewKey['object'] == 'self':

                    overviewSheet[overviewKey['column']+str(overviewRow)] = domain[overviewKey['key']]

                elif overviewKey['object'] == 'data':

                    overviewSheet[overviewKey['column']+str(overviewRow)] = domain['data'][overviewKey['key']]

                elif '.' in overviewKey['object']:

                    objectKeys = overviewKey['object'].split('.')

                    obj = domain.copy()

                    for objectKey in objectKeys:

                        obj = obj[objectKey]

                    overviewSheet[overviewKey['column']+str(overviewRow)] = obj[overviewKey['key']]

            #
            for overviewFormula in overviewFormulas:

                overviewSheet[overviewFormula['column']+str(overviewRow)] = overviewFormula['value'].format(str(overviewRow))
            
            overviewSheet.auto_filter.ref = 'A:Q'

            overviewRow = overviewRow+1

            for overview in overviews:

                for item in domain['data'][overview['data'].split('.')[0]][overview['data'].split('.')[1]]:

                    if not item[overview['key']] in overview['unique']:

                        overview['unique'].append(item[overview['key']])

                    overview['sheet']['A'+str(overview['row'])] = domain['name']
                    overview['sheet']['B'+str(overview['row'])] = item[overview['key']]
                    overview['sheet']['C'+str(overview['row'])] = item['count']
                    overview['sheet']['D'+str(overview['row'])] = str('=SUMIF(A:A,A'+str(overview['row'])+',C:C)')
                    overview['sheet']['E'+str(overview['row'])] = str('=ROUND((C'+str(overview['row'])+'/D'+str(overview['row'])+')*100,2)')

                    overview['sheet'].auto_filter.ref = 'A:E'

                    overview['row'] = overview['row']+1

        for overview in overviews:

            sheet = wb.create_sheet(overview['title']+' summary')

            sheet['A1'] = 'Unique'
            sheet['B1'] = 'Total'
            sheet['C1'] = 'Percent'

            row = 2

            for item in overview['unique']:

                sheet['A'+str(row)] = str(item)
                sheet['B'+str(row)] = str('=SUMIF(\''+overview['title']+'\'!B:B,A'+str(row)+',\''+overview['title']+'\'!C:C)')
                sheet['C'+str(row)] = str('=ROUND((B'+str(row)+'/SUM(B:B))*100,2)')

                sheet.auto_filter.ref = 'A:C'

                row = row+1

        # Delete existing file
        if os.path.exists(self.excelOutputPath):

            os.remove(self.excelOutputPath)

        # Save Workbook
        wb.save(self.excelOutputPath)

        self.Log('ExportSpreadsheet : Complete')


        return


    # Export raw json data to file
    # import json
    def ExportJson(self, jsonData):

        jsonData = json.dumps(jsonData)

        f = open(self.rawOutputPath, 'w', encoding='utf-8')
        f.write(jsonData)
        f.close()


        return


    # Check for redirects and link shorteners
    # import requests
    def DirectLink(self, url):

        if not '://' in url:

            url = 'http://'+url

        try:

            response = requests.get(url, allow_redirects=False)

            if 300 <= response.status_code < 400:

                redirect = response.headers['location']

                return redirect

        except Exception as e:

            self.Log('DirectLink : Error - '+str(e))


        return url


    # Get whois info
    # import pythonwhois
    def GetWhois(self, domain):
        
        whois = {}
        
        try:
            
            temp = pythonwhois.get_whois(domain['domain'])
            whois = temp

        except Exception as e:

            self.Log('GetWhois : Error - '+domain['domain']+' '+str(e))


        return whois


    def GetSearchLinks(self, domain):

        searchLinks = {}

        searchLinks['reddit'] = 'https://reddit.com/domain/'+domain['domain']+'/top?t=all'
        searchLinks['twitter'] = 'https://twitter.com/search?q='+domain['http']+'%3A%2F%2F'+domain['domain']
        searchLinks['facebook'] = 'https://facebook.com/search?q='+domain['http']+'%3A%2F%2F'+domain['domain']
        searchLinks['tumblr'] = 'https://tumblr.com/search/'+domain['domain']
        searchLinks['moonsearch'] = 'https://moonsearch.com/report/'+domain['domain']+'.html'
        searchLinks['domaintools'] = 'http://whois.domaintools.com/'+domain['domain']


        return searchLinks


    # Gets the domain of a url
    def GetDomain(self, url):

        domain = {
            'http': 'http',
            'domain': '',
            'subdomain': '',
            'toplevel_domain': '',
            'ip': '0.0.0.0',
            'country': '',
            'city': ''
            }

        # Parse domain name

        domain['domain'] = url

        if 'http://' in url:

            domain['http'] = 'http'

        elif 'https://' in url:

            domain['http'] = 'https'

        if '://' in url:

            domain['domain'] = url[url.find('://')+len('://'):]

        if '/' in domain['domain']:

            domain['domain'] = domain['domain'][0:domain['domain'].find('/')]
            
        domain['subdomain'] = domain['domain']

        if len(domain['domain'].split('.')) > 2:

            if domain['domain'].split('.')[-2] == 'co' or domain['domain'].split('.')[-2] == 'com' or domain['domain'].split('.')[-2] == 'org' or domain['domain'].split('.')[-2] == 'gov':

                domain['toplevel_domain'] = domain['domain'].split('.')[-2]+'.'+domain['domain'].split('.')[-1]

            else:

                domain['toplevel_domain'] = domain['domain'].split('.')[-1]

            base = domain['domain'][0:domain['domain'].find(domain['toplevel_domain'])].strip('.')

            if len(base.split('.')) > 1:

                domain['domain'] = '.'.join([base.split('.')[-1], domain['toplevel_domain']])

                subdomains = []

                for i in range(0, len(base.split('.'))):

                    subdomains.append(base.split('.')[i])

                subdomains.append(domain['toplevel_domain'])

                domain['subdomain'] = '.'.join(subdomains)

        else:

            domain['toplevel_domain'] = domain['domain'].split('.')[-1]

        # Get IP

        domain['ip'] = self.GetDomainIp(domain)

        # Get Location

        location = self.GetLocation(domain['ip'])

        if 'country' in location.keys():

            if not location['country'] == None:

                domain['country'] = location['country']

        if 'city' in location.keys():

            if not location['city'] == None:

                domain['city'] = location['city']


        return domain


    # Get the IP of a domain
    # import socket
    def GetDomainIp(self, domain):
        
        hostIp = '0.0.0.0'
        
        try:

            hostIp = socket.gethostbyname(domain['domain'])

        except:

            try:

                tempIp = socket.gethostbyname(domain['subdomain'])

                hostIp = tempIp

            except:

                self.Log('GetDomainIp : Error - Could not get IP for '+domain['domain'])


        return hostIp


    # Get geo location of an IP
    # import requests
    def GetLocation(self, ip):

        jsonData = {}
        url = 'https://geoip-db.com/json/'+ip

        try:

            response = requests.get(url)

            if response.status_code == requests.codes.ok:

                jsonRaw = response.json()

                if 'country_code' in jsonRaw.keys():

                    jsonData['country'] = jsonRaw['country_code']

                if 'city' in jsonRaw.keys():

                    jsonData['city'] = jsonRaw['city']

            else:

                self.Log('GetLocation : Error ['+ip+'] - Code '+str(response.status_code))

        except Exception as e:

            self.Log('GetLocation : Error ['+ip+'] - '+str(e))


        return jsonData


    # Get Google Analytics and AdSense IDs
    # import re, requests
    def GetTracking(self, domain):

        tracking = {
            'google_analytics': '',
            'google_adsense': ''
            }

        try:

            response = requests.get(domain['http']+'://'+domain['domain'], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})

            if response.status_code == requests.codes.ok:

                html = response.text

                analyticsFinder = re.compile('\'UA-(.*?)-', re.MULTILINE|re.DOTALL)
                analytics = analyticsFinder.findall(html)

                if len(analytics) > 0:

                    tracking['google_analytics'] = analytics[0]

                adsenseFinder = re.compile('data-ad-client="ca-pub-(.*?)"', re.MULTILINE|re.DOTALL)
                adsense = adsenseFinder.findall(html)

                if len(adsense) > 0:

                    tracking['google_adsense'] = adsense[0]

        except Exception as e:

            self.Log('GetTracking : Error - '+str(e))


        return tracking


    # Initialize twitter API
    # import tweepy
    def InitializeTwitter(self):

        global twitterAuthData

        self.twitterAuth = tweepy.OAuthHandler(twitterAuthData['consumer_key'], twitterAuthData['consumer_secret'])
        self.twitterAuth.set_access_token(twitterAuthData['access_token'], twitterAuthData['access_token_secret'])
        self.twitterApi = tweepy.API(self.twitterAuth)

        self.twitterInitialized = True


        return


    # Search twitter for domain
    # import tweepy
    def SearchTwitter(self, domain):

        self.Log('SearchTwitter : Starting '+domain['domain'])

        twitterResults = {
            'users': [],
            'hashtags': []
            }

        if not self.twitterInitialized:

            self.InitializeTwitter()

        results = self.twitterApi.search(domain['domain'])

        for result in results:

            user = {
                'user': result._json['user']['screen_name'],
                'count': 1
                }

            if len(twitterResults['users']) == 0:

                twitterResults['users'].append(user)

            else:

                userFind = list(filter(lambda u: u['user'] == user['user'], twitterResults['users']))

                if len(userFind) == 0:

                    twitterResults['users'].append(user)

                else:

                    userFind[0]['count'] = userFind[0]['count']+1

            for hashtag in result._json['entities']['hashtags']:

                hash = {
                    'hashtag': hashtag['text'],
                    'count': 1
                    }

                if len(twitterResults['hashtags']) == 0:

                    twitterResults['hashtags'].append(hash)

                else:

                    hashFind = list(filter(lambda h: h['hashtag'] == hash['hashtag'], twitterResults['hashtags']))

                    if len(hashFind) == 0:

                        twitterResults['hashtags'].append(hash)

                    else:

                        hashFind[0]['count'] = hashFind[0]['count']+1

        # Sort results
        twitterResults['users'] = sorted(twitterResults['users'], key=lambda k: k['count'], reverse=True)
        twitterResults['hashtags'] = sorted(twitterResults['hashtags'], key=lambda k: k['count'], reverse=True)

        self.Log('SearchTwitter : Completed '+domain['domain'])


        return twitterResults


    # Initialize reddit API
    def InitializeReddit(self):

        self.baseRedditUrl = 'https://www.reddit.com'
        self.lastRedditRequest = 0.0
        self.redditRequestDelay = 2.0
        self.redditHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        self.redditInitialized = True


        return


    # Search reddit for domain
    def SearchReddit(self, domain, maxCalls=0):

        self.Log('SearchReddit : Starting '+domain['domain'])

        redditResults = {
            'communities': [],
            'users': []
            }

        processedThings = []

        listings = [
            {
                'type': 'new',
                'sort': 'new'
                },
            {
                'type': 'hot',
                'sort': 'hot'
                },
            {
                'type': 'top',
                'sort': 'top'
                },
            {
                'type': 'controversial',
                'sort': 'controversial'
                }
            ]

        for listing in listings:

            domainSubmissions = self.CollectRedditListing('/domain/'+domain['domain']+'/'+listing['type'], maxCalls=maxCalls, sort=listing['sort'])

            for domainSubmission in domainSubmissions:

                if not domainSubmission['name'] in processedThings:

                    processedThings.append(domainSubmission['name'])

                    community = {
                        'community': domainSubmission['subreddit'],
                        'count': 1
                        }

                    if len(redditResults['communities']) == 0:

                        redditResults['communities'].append(community)

                    else:

                        communityFind = list(filter(lambda c: c['community'] == community['community'], redditResults['communities']))

                        if len(communityFind) == 0:

                            redditResults['communities'].append(community)

                        else:

                            communityFind[0]['count'] = communityFind[0]['count']+1

                    user = {
                        'user': domainSubmission['author'],
                        'count': 1
                        }

                    if len(redditResults['users']) == 0:

                        redditResults['users'].append(user)

                    else:

                        userFind = list(filter(lambda u: u['user'] == user['user'], redditResults['users']))

                        if len(userFind) == 0:

                            redditResults['users'].append(user)

                        else:

                            userFind[0]['count'] = userFind[0]['count']+1

        redditResults['communities'] = sorted(redditResults['communities'], key=lambda k: k['count'], reverse=True)

        redditResults['users'] = sorted(redditResults['users'], key=lambda k: k['count'], reverse=True)

        self.Log('SearchReddit : Completed '+domain['domain'])


        return redditResults


    # Collect reddit listing
    # import time
    def CollectRedditListing(self, listing, maxCalls=0, sort='new'):

        self.Log('CollectRedditListing : Starting '+listing)

        listingData = []
        collected = []
        calls = 0
        listingArgs = {
            't': 'all',
            'sort': sort,
            'limit': 100
            }
        after = ''

        endCollection = False

        while not endCollection:

            if maxCalls > 0:

                if calls > maxCalls:

                    endCollection = True

            if calls > 0:

                listingArgs['count'] = listingArgs['limit']*calls

            if len(collected) > 0:

                if after == collected[-1]:

                    endCollection = True

                if calls > 1:
                    
                    after = listingArgs['after']

                listingArgs['after'] = collected[-1]

            rawJson = self.GetRedditJson(listing, listingArgs)

            if rawJson == 'error':

                time.sleep(int(self.redditRequestDelay))

            elif 'error' in rawJson.keys():

                endCollection = True

            elif 'data' not in rawJson.keys():

                endCollection = True

            else:

                if rawJson['data']['children']:

                    if len(rawJson['data']['children']) < 1:

                        endCollection = True

                    for item in rawJson['data']['children']:

                        thing = self.FormatRedditThing(item)

                        if not 'error' in thing.keys():

                            if not thing['name'] in collected:

                                collected.append(thing['name'])
                                listingData.append(thing)

                    if len(rawJson['data']['children']) < listingArgs['limit']:
                        
                        endCollection = True

                    calls = calls+1

                else:

                    endCollection = True

        self.Log('CollectRedditListing : Complete '+listing)


        return listingData


    # Format reddit comments and submissions
    def FormatRedditThing(self, thingData):

        thing = {}

        commentKeys = [
            ['archived', 'archived'],
            ['author', 'author'],
            ['body', 'body'],
            ['body_html', 'body_html'],
            ['created', 'created_utc'],
            ['distinguished', 'distinguished'],
            ['edited', 'edited'],
            ['gilded', 'gilded'],
            ['id', 'id'],
            ['submission_author', 'link_author'],
            ['submission_id', 'link_id'],
            ['name', 'name'],
            ['num_s', 'num_s'],
            ['nsfw', 'over_18'],
            ['parent_id', 'parent_id'],
            ['quarantine', 'quarantine'],
            ['replies', 'replies'],
            ['score', 'score'],
            ['stickied', 'stickied'],
            ['subreddit', 'subreddit']
            ]

        submissionKeys = [
            ['archived', 'archived'],
            ['author', 'author'],
            ['category', 'category'],
            ['content_categories', 'content_categories'],
            ['contest', 'contest_mode'],
            ['created', 'created_utc'],
            ['distinguished', 'distinguished'],
            ['domain', 'domain'],
            ['edited', 'edited'],
            ['gilded', 'gilded'],
            ['hidden', 'hidden'],
            ['id', 'id'],
            ['is_meta', 'is_meta'],
            ['is_oc', 'is_original_content'],
            ['is_self', 'is_self'],
            ['locked', 'locked'],
            ['name', 'name'],
            ['num_comments', 'num_comments'],
            ['num_crossposts', 'num_crossposts'],
            ['nsfw', 'over_18'],
            ['parent_whitelist', 'parent_whitelist_status'],
            ['pinned', 'pinned'],
            ['quarantine', 'quarantine'],
            ['score', 'score'],
            ['selftext', 'selftext'],
            ['selftext_html', 'selftext_html'],
            ['spoiler', 'spoiler'],
            ['stickied', 'stickied'],
            ['subreddit', 'subreddit'],
            ['title', 'title'],
            ['url', 'url'],
            ['whitelist', 'whitelist_status']
            ]

        thingKeys = []

        try:

            if thingData['kind'] == 't1':

                thing['type'] = 'comment'
                thingKeys = commentKeys.copy()

            elif thingData['kind'] == 't3':

                thing['type'] = 'submission'
                thingKeys = submissionKeys.copy()

            thingData = thingData['data']

            for thingKey in thingKeys:

                if thingKey[1] in thingData.keys():

                    thing[thingKey[0]] = thingData[thingKey[1]]

            if thing['type'] == 'comment' and 'permalink' in thing.keys() and 'submission_id' in thing.keys():

                thing['permalink'] = 'https://reddit.com/comments/'+thing['submission_id'].split('_')[-1]+'/_/'+thing['id']

            if thing['type'] == 'submission' and 'id' in thing.keys():

                thing['permalink'] = 'https://redd.it/'+thing['id']

        except Exception as e:

            thing['error'] = True
            self.Log('FormatThing : Error - '+str(e))


        return thing


    # Get reddit json
    # import requests, time
    def GetRedditJson(self, url, urlArgs={}):

        if not self.redditInitialized:

            self.InitializeReddit()

        # Assume the worst
        redditJson = {'error': 'error'}

        # Format url arguments
        args = []

        if len(urlArgs.keys()) > 0:

            for key in urlArgs.keys():

                args.append(key+'='+str(urlArgs[key]))

            args = '?'+'&'.join(args)

        else:

            args = ''

        # Format url
        url = self.baseRedditUrl+url+'.json'+args

        self.Log('GetRedditJson : Requesting ['+url+']')

        # API timer
        if self.GetTime(False)-self.lastRedditRequest < self.redditRequestDelay:

            time.sleep(int(self.redditRequestDelay-(self.GetTime(False)-self.lastRedditRequest)))

        self.lastRedditRequest = self.GetTime(False)

        # Make http request
        try:

            response = requests.get(url, headers=self.redditHeaders)

            if response.status_code == requests.codes.ok:

                redditJson = response.json()

            else:

                redditJson = {'error': str(response.status_code)}
                self.Log('GetRedditJson : Error ['+url+'] - Code '+str(response.status_code))

        except Exception as e:

            redditJson = {'error': str(e)}
            self.Log('GetRedditJson : Error ['+url+'] - '+str(e))


        return redditJson


    # Get timestamp
    # import datetime
    def GetTime(self, readable=True):

        timestamp = datetime.datetime.now()

        if readable:
            
            timestamp = timestamp.strftime('%B %d, %Y  %I:%M:%S %p')

        else:

            timestamp = timestamp.timestamp()


        return timestamp


    # Log events
    def Log(self, status, display=False):

        status = self.GetTime()+' | Disinformation '+str(status)

        f = open(self.logPath, 'a', encoding='utf-8')
        f.write(status+'\n')
        f.close()

        if display:

            print(status)


        return


Disinformation()
