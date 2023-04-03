# chat/views.py
from django.shortcuts import render
from .models import Mensagem, Sala
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import redirect
import hashlib
from django.http import Http404
from django.urls import reverse


# Gerar Hash sempre na orde de: 1-  outro_usuario | 2-  usuario_conectado. Para fins de comparação 

def index(request):
    usuarios = User.objects.all()
    return render(request, "chat/index.html", {
        'usuarios': usuarios
    })


def room(request, room_name): 
    
    user = request.GET.get('user') # Id do outro usuario 
    # se o room_name não tiver 32 caracteres não cria a sala mas levanta um erro de não encontrado
    # Ou se a comparação da hash (room_name) for diferente na nova geração dela
    if len(room_name) != 32 or hashlib.md5(f'{int(user) + request.user.id}'.encode()).hexdigest() != room_name:
        raise Http404
    
    try:
        sala = get_object_or_404(Sala, sala=room_name)
    
    except Http404:
        pass
        
    mensagens = Mensagem.objects.filter(
        Q(destinatario__id=request.user.id) | Q(remetente__id=request.user.id)
        )

    return render(request, "chat/room.html", {
                                "room_name": room_name,
                                'mensagens': mensagens,
                                'user_id': user
                                })


def room_redirect(request, id_user):
    if int(id_user) == request.user.id:
        raise Http404

    usuario = get_object_or_404(User, id=id_user)

    room_name = hashlib.md5(f'{int(id_user) + request.user.id}'.encode()).hexdigest()

    if Sala.objects.filter(sala=room_name).exists():
        pass

    # return redirect(f'/chat/{room_name}?user={id_user}')


    url = reverse('room', kwargs={'room_name': room_name})
    url += f'?user={id_user}'

    return redirect(url)

