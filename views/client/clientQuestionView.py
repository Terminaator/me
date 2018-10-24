from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import langprocessing.chatbot as cbot
from views.json.requestJson import RequestJson

@method_decorator(csrf_exempt, name='dispatch') #Võimalik, et me eemaldame selle ära
class ClientQuestionView(View):
    #def __init__(self):
        #self.__chatbot = chatbot()

    @method_decorator(RequestJson)
    def post(self, request):
        json_data = request.json
        bot = cbot.chatbot()
        answerchat = bot.getResponse(json_data.get('question'))
        return JsonResponse({"answer": answerchat})
