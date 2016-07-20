import datetime

def checkiftimestamp(tmstamp):
    try:
        date = datetime.datetime.fromtimestamp(int(tmstamp)).strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        print('Not a timestamp')
        return False
    return True

# def validate_parameters(pid, start, end, hashtags, pages, sources, infmode, languages):
#
#     return True

def validate_parameters(request):
    parameters = {}
    start = request.args.get('start')
    end = request.args.get('end')
    keywords = request.args.get('hashtags')
    accounts = request.args.get('pages')
    sources = request.args.get('sources')
    project = request.args.get('pid')
    languages = request.args.get('language')
    if project is None:
	    return {"error":"Hey...give me a pid, I don't know which project to look for"}
    if start is None:
	    return {"error":"No start timestamp provided"}
    else:
        if not checkiftimestamp(start):
            return {"error":"Invalid start timestamp"}
    if end is None:
	    return {"error":"No end timestamp provided"}
    else:
        if not checkiftimestamp(end):
            return {"error":"Invalid end timestamp"}
    if keywords is None:
        return {"error":"No search keywords given"}
    if (not (keywords.startswith("\"") and keywords.endswith("\""))):
        return {"error":"Search keywords should be given in quotes"}
    if accounts is None:
        return {"error":"No search accounts given"}
    else:
        try:
            if (not (accounts.startswith("\"") and accounts.endswith("\""))):
                return {"error":"Pages should be given in quotes"}
            accounts = accounts.replace(',','","')
        except:
            return {"error":"Something is wrong with the format of the provided accounts"}
    if sources is None:
        sources = "\"twitter\",\"facebook\",\"instagram\""
    else:
        try:
            if (not (sources.startswith("\"") and sources.endswith("\""))):
                return {"error":"Sources should be given in quotes"}
            sources = sources.replace(',','","')
        except:
            return {"error":"Something is wrong with the sources"}
    if languages is None:
        languages = "\"en\",\"es\""
    else:
        try:
            if (not (languages.startswith("\"") and languages.endswith("\""))):
                return {"error":"Languages should be given in quotes"}
            languages = languages.replace(',','","')
        except:
            return {"error":"Something is wrong with the languages"}
    parameters["project"] = project
    parameters["start"] = start + "000"
    parameters["end"] = end + "000"
    parameters["keywords"] = keywords
    parameters["accounts"] = accounts
    parameters["sources"] = sources
    parameters["languages"] = languages
    return parameters
