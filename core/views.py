# chat/views.py
from django.shortcuts import render
from .models import Mensagem, Sala
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import Http404
from .funcoes.criar_hash import gerar_nome_da_sala
from django.contrib.auth.decorators import login_required


# Gerar Hash sempre na orde de: 1-  outro_usuario | 2-  usuario_conectado. Para fins de comparação 

def index(request):
    usuarios = User.objects.all()
    return render(request, "chat/index.html", {
        'usuarios': usuarios
    })


@login_required
def room(request, room_name): 
    
    user = request.GET.get('user') # Id do outro usuario 
    # se o room_name não tiver 32 caracteres não cria a sala mas levanta um erro de não encontrado
    # Ou se a comparação da hash (room_name) for diferente na nova geração dela
    if len(room_name) != 36 or gerar_nome_da_sala(user, request.user.id) != room_name:
        raise Http404
    
    sala_obj = Sala.objects.filter(sala=room_name).first()
    
    mensagens = Mensagem.objects.filter(sala=sala_obj)
    info_user = User.objects.filter(id=user)[0]
    return render(request, "chat/room.html", {
                                "room_name": room_name,
                                'mensagens': mensagens,
                                'user_id': user,
                                'info_user': info_user
                                })


@login_required
def room_redirect(request, id_user):
    if int(id_user) == request.user.id:
        raise Http404

    usuario = get_object_or_404(User, id=id_user)
    room_name = gerar_nome_da_sala(id_user, request.user.id)

    return redirect(f'/chat/{room_name}?user={id_user}')

