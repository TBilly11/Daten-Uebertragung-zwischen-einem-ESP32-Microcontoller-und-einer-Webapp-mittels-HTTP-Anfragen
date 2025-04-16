import base64

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
import logging

from lock_web_interface.forms.user_form import UserForm
from lock_web_interface.models import MyUser, LoginEntry, RecordConfig

logger = logging.getLogger(__name__)


class ManagementView(View):

    @classmethod
    def get(cls, request):
        user_page = request.GET.get('page', 1)
        action = request.GET.get('action')
        if action:
            if action == "next":
                user_page = int(user_page) + 1
            else:
                user_page = int(user_page) - 1

        regular_users = MyUser.objects.filter(user_type="REGULAR").order_by('username')
        paginator = Paginator(regular_users, 10)  # 5 liens par page
        try:
            # La définition de nos URL autorise comme argument « page » uniquement
            # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
            user_pages = paginator.page(user_page)
        except EmptyPage:
            # Nous vérifions toutefois que nous ne dépassons pas la limite de page
            # Par convention, nous renvoyons la dernière page dans ce cas
            user_pages = paginator.page(paginator.num_pages)

        form = UserForm(user_id=None)
        context = {
            "user_pages": user_pages,
            "form": form,
            "action_form": "Ajouter"
        }
        return render(request, 'lock_web_interface/management.html', context=context)



class UserView(View):
    template_name = "lock_web_interface/management/user_template.html"

    @classmethod
    def get(cls, request):
        try:
            user_id = request.GET.get('id')
            user = MyUser.objects.get(id=user_id)
            logger.info(type(user.one_factor_code))
            logger.info(user.one_factor_code)
            initials = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'one_factor_code': base64.b64decode(bytes(user.one_factor_code[1:], 'utf-8')).decode(),
                'nfc': user.nfc
            }

            context = {
                "form": UserForm(initial=initials, user_id=user_id),
                "action_form": "Modifier"
            } 
            template = render_to_string(
                template_name=cls.template_name,
                request=request,
                context=context
            )
            return JsonResponse(status=200, data={'html': template})
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                "msg": "an error has occured on our end"
            })

    @classmethod
    def post(cls, request):
        try:
            form = UserForm(data=request.POST, user_id=request.POST.get('user_id'))
            logger.info(form.is_bound)
            context = {
                "form": form,
                "action_form": "Modifier" if request.POST.get('user_id') else "Ajouter"
            }
            if form.is_valid():
                form.save()
                return JsonResponse(status=200, data={
                    'msg': "user updated with success"
                })
            else:
                logger.error(form.errors)
                template = render_to_string(
                    template_name=cls.template_name,
                    request=request,
                    context=context
                )
                return JsonResponse(status=400, data={
                    'msg': "form errors",
                    "html": template
                })
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                "msg": "an error has occured on our end"
            })

    @classmethod
    def delete(cls, request):
        try:
            user_id = QueryDict(request.body).get('id')

            MyUser.objects.get(id=user_id).delete()
            return JsonResponse(status=200, data={
                'msg': "user deleted with success"
            })
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                "msg": "an error has occured on our end"
            })


class OneAuthUsersView(View):

    @classmethod
    def post(cls, request):
        try:
            user_id = request.POST.get('id')
            action = request.POST.get('toggled')
            user = MyUser.objects.get(id=user_id)
            logger.info(action)
            if action == 'False':
                user.one_factor_auth_enabled = True

            else:
                user.one_factor_auth_enabled = False
            user.save()
            return JsonResponse(status=200, data={'msg': "factor authentication toggled with success"})
        except User.DoesNotExist:
            return JsonResponse(status=404, data={"msg": "an error has occured on our end"})
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={
                "msg": "an error has occured on our end"
            })


class LogEntryView(View):

    @classmethod
    def get(cls, request):
        page = request.GET.get('page', 1)
        action = request.GET.get('action')
        if action:
            if action == "next":
                page = int(page) + 1
            else:
                page = int(page) - 1

        entries = LoginEntry.objects.order_by('-date')

        nb_records = request.session.get('nb_records', 5)
        paginator = Paginator(entries, nb_records)  # 5 liens par page
        try:
            entries_pages = paginator.page(page)
        except EmptyPage:
            entries_pages = paginator.page(paginator.num_pages)

        context = {
            'entries_pages': entries_pages,
        }
        return render(template_name='lock_web_interface/login_entries.html', request=request, context=context)

    @classmethod
    def post(cls, request):
        try:
            nb_records = request.POST.get('nb-records', 10)
            logger.info(nb_records)
            try:
                config = RecordConfig.objects.get()               #ici
            except RecordConfig.DoesNotExist:
                config = RecordConfig(nb_records=nb_records)
            config.save()
            logger.info(request.session['nb_records'])
            return cls.get(request)
        except Exception as e:
            logger.error(e)
            return JsonResponse(status=500, data={})