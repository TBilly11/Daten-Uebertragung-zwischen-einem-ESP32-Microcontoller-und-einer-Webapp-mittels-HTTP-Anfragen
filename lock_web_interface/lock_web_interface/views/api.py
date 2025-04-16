import base64
import logging
import random
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from lock_web_interface.models import LoginEntry, MyUser, RecordConfig
from django.shortcuts import render
from django.core.paginator import Paginator


logger = logging.getLogger(__name__)


def send_mail_with_login_code(request):
    if request.method == "POST":
        try:
            nfc = request.POST.get('nfc')
            print(nfc)
            user = MyUser.objects.get(nfc=nfc)
            password = ''.join([str(random.randint(0, 9)) for i in range(6)])
            send_mail(
                subject="Code d'authentification",
                from_email="",
                recipient_list=[user.email],
                message=f"Votre code d'authentification est le suivant: {password}",
                fail_silently=True
            )
            return JsonResponse(status=200, data={
                'msg': "mail with login code sent with success",
                'password': password  # not safe must encrypt this password before sending over the network
            })
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                'msg': 'an error has occured on our end'
            })
    else:
        return JsonResponse(status=405, data={
            'msg': 'method not allowed'
        })


# cette fonction est appelée quand tu tapes l'url "api/one_factor_auth"
def can_authenticate_with_one_factor(request):
    if request.method == "POST": # type de la requête
        try:
            # les paramètres de la requête de type POST sont dans request.POST
            # username est un paramètre que tu passes depuis ton hardware
            one_factor_code = request.POST.get('one_factor_code')
            one_factor_code = base64.b64encode(bytes(one_factor_code, 'utf-8'))
            # ici on fait une requête vers la base de données pour récupérer l'utilisateur
            # si tu veux plus d'informations sur comment faire des requête regarde la doc de django sur les "requêtes"
            user = MyUser.objects.get(one_factor_code=one_factor_code, one_factor_auth_enabled=True)
            if user:
                # ici on retourne la réponse en passant des paramètres que tu vas pouvoir récupérer côté hardware
                return JsonResponse(status=200, data={
                    'msg': 'one factor authentication enabled',
                    'one_factor': True,
                    'one_factor_code': base64.b64decode(bytes(user.one_factor_code[1:], 'utf-8')).decode()
                })
            else:
                return JsonResponse(status=200, data={
                    'msg': 'one factor authentication disabled',
                    'one_factor': False
                })
        except User.DoesNotExist:
            return JsonResponse(status=404, data={
                'msg': "a user with this username doesn't exist"
            })
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                'msg': 'an error has occured on our end'
            })
    else:
        return JsonResponse(status=405, data={
            'msg': 'method not allowed'
        })


def add_login_entry(request):
    #login_records(request)
    check_login_entries(request)  
    if request.method == "POST":
        try:
            one_factor_code = request.POST.get('code')
            if(one_factor_code.isdigit()): 
              one_factor_code = base64.b64encode(bytes(one_factor_code, 'utf-8'))
              print(one_factor_code)
              auth_type = request.POST.get('auth_type')
              print(auth_type)
              user = MyUser.objects.get(one_factor_code=one_factor_code)
              print(user)
              LoginEntry(
                user=user,
                auth_type=auth_type
                ).save()
            else:
              nfc=one_factor_code
              #nfc = base64.b64encode(bytes(one_factor_code, 'utf-8'))
              print(nfc)
              auth_type = request.POST.get('auth_type')
              print(auth_type)
              user = MyUser.objects.get(nfc=nfc)

              LoginEntry(
                user=user,
                auth_type=auth_type
                ).save()
            
            return JsonResponse(status=200, data={
                'msg': 'log entry saved with success'
            })
        except User.DoesNotExist:
            return JsonResponse(status=404, data={
                'msg': "a user with this username doesn't exist"
            })
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                'msg': 'an error has occured on our end',
                'error': e
            })
    else:
        return JsonResponse(status=405, data={
            'msg': 'method not allowed'
        })

def check_login_entries(request):
    print("nb1")
    if request.method == 'POST':
      nb_records=RecordConfig.objects.get()
      nb = LoginEntry.objects.count()
      print("nb2")
      print(nb_records)
      print("nb-records :", nb_records)
      print(nb)
    if nb == nb_records:
        # je supprime la dernière entrée
        print("nb3")
        LoginEntry.objects.latest('date').delete()
        print("nb4")
    if nb>=nb_records:
       print("nb5")
       entries_to_delete = LoginEntry.objects.order_by('-date')[nb - nb_records:]
       print("nb6")
    for entry in entries_to_delete:
        entry.delete()
    #return render(request, 'lock_web_interface/login_records.html', context)
  
'''import base64
import logging

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from lock_web_interface.models import LoginEntry, MyUser, RecordConfig

logger = logging.getLogger(__name__)


def send_mail_with_login_code(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            user = MyUser.objects.get(username=username)
            password = MyUser.generate_random_etan_password()
            send_mail(
                subject="Code d'authentification",
                from_email="",
                recipient_list=[user.email],
                message=f"Votre code d'authentification est le suivant: {password}",
                fail_silently=True
            )
            return JsonResponse(status=200, data={
                'msg': "mail with login code sent with success",
                'password': password  # not safe must encrypt this password before sending over the network
            })
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                'msg': 'an error has occured on our end'
            })
    else:
        return JsonResponse(status=405, data={
            'msg': 'method not allowed'
        })


# cette fonction est appelée quand tu tapes l'url "api/one_factor_auth"
def can_authenticate_with_one_factor(request):
    if request.method == "POST": # type de la requête
        try:
            # les paramètres de la requête de type POST sont dans request.POST
            # username est un paramètre que tu passes depuis ton hardware
            one_factor_code = request.POST.get('one_factor_code')
            one_factor_code = base64.b64encode(bytes(one_factor_code, 'utf-8'))
            # ici on fait une requête vers la base de données pour récupérer l'utilisateur
            # si tu veux plus d'informations sur comment faire des requête regarde la doc de django sur les "requêtes"
            user = MyUser.objects.get(one_factor_code=one_factor_code, one_factor_auth_enabled=False)
            if user:
                # ici on retourne la réponse en passant des paramètres que tu vas pouvoir récupérer côté hardware
                return JsonResponse(status=200, data={
                    'msg': 'one factor authentication enabled',
                    'one_factor': True,
                    'one_factor_code': base64.b64decode(bytes(user.one_factor_code[1:], 'utf-8')).decode()
                })
            else:
                return JsonResponse(status=200, data={
                    'msg': 'one factor authentication disabled',
                    'one_factor': False
                })
        except User.DoesNotExist:
            return JsonResponse(status=404, data={
                'msg': "a user with this username doesn't exist"
            }) 
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                'msg': 'an error has occured on our end'
            })
    else:
        return JsonResponse(status=405, data={
            'msg': 'method not allowed'
        })


def add_login_entry(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            auth_type = request.POST.get('auth_type')
            nb_records=RecordConfig.objects.get()
            user = MyUser.objects.get(username=username)
            LoginEntry(
                user=user,
                auth_type=auth_type
            ).save()
            return JsonResponse(status=200, data={
                'msg': 'log entry saved with success'
            })
        except User.DoesNotExist:
            return JsonResponse(status=404, data={
                'msg': "a user with this username doesn't exist"
            })
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                'msg': 'an error has occured on our end',
                'error': e
            })
    else:
        return JsonResponse(status=405, data={
            'msg': 'method not allowed'
        })
 '''   
    
