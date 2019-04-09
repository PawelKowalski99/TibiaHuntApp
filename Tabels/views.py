from django.shortcuts import render
from .models import Character, Servers, Post
from django.views import View
from .forms import LevelForm
from django.views.generic.edit import FormView


class IndexView(View):
    template_name = 'register/layout.html'
    def get(self, request):
        servers = Servers.objects.all()
        return render(request, self.template_name, context={
            'servers': servers,
        })


class HomeView(FormView):
    template_name = 'register/level_block.html'

    def get(self, request, name, ):
        form = LevelForm
        characters = Character.objects.filter(server_name=name, ).order_by('name')
        server_onl_pl = Servers.objects.get(name=name,)
        servers = Servers.objects.all()
        args = {'form': form, 'characters': characters, 'servers': servers, 'server_onl_pl': server_onl_pl}
        return render(request, self.template_name, args)

    def post(self, request, name):
        form = LevelForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['level']
            lower_nomber = int(number) * 0.7
            higher_number = int(number) * 1.3
            Post.objects.all().delete()
            text = form.cleaned_data['level']
            characters = Character.objects.filter(server_name=name, level__gt=lower_nomber,
                                                  level__lte=higher_number).order_by('level')
            ppl_count = len(characters)
            servers = Servers.objects.all()
            args = {'form': form, 'text': text, 'characters': characters, 'servers': servers,
                    'ppl_count': ppl_count}
            return render(request, self.template_name, args)
        else:
            form = LevelForm
            characters = Character.objects.filter(server_name=name, ).order_by('name')
            servers = Servers.objects.all()
            args = {'form': form, 'characters': characters, 'servers': servers}
            return render(request, self.template_name, args)