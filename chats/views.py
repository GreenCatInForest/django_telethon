from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from telethon.errors import PhoneCodeInvalidError
from django_telethon.models import TelegramSession
from .utils.telethon_util import get_telegram_client
from asyncio import TimeoutError, wait_for
from telethon.errors import AuthRestartError

async def telegram_login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        session_name = f"{request.user.username}_{phone}"
        client = get_telegram_client(session_name)

        try:
            async with client:
                await wait_for(client.send_code_request(phone), timeout=10)
                request.session['phone'] = phone
                request.session['session_name'] = session_name
        except AuthRestartError:
            return render(request, 'telegram_login.html', {'error': 'Telegram requires you to restart the login process. Please try again.'})
        except TimeoutError:
            return render(request, 'telegram_login.html', {'error': 'Request timed out. Please try again.'})
        except Exception as e:
            return render(request, 'telegram_login.html', {'error': str(e)})

        return redirect('telegram_verify')
    return render(request, 'telegram_login.html')

     
def telegram_verify_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        phone = request.session.get('phone')
        session_name = request.session.get('session_name')
        client = get_telegram_client(session_name)
        client.connect()
        try:
            client.sign_in(phone, code)
            # Store session in DB
            TelegramSession.objects.get_or_create(
                user=request.user,
                phone_number=phone,
                defaults={'session_name': session_name}
            )
            return redirect('telegram_chats')
        except PhoneCodeInvalidError:
            return render(request, 'telegram_verify.html', {'error': 'Invalid code'})
    return render(request, 'telegram_verify.html')

def telegram_chats_view(request):
    phone = request.session.get('phone')
    session_name = f"{request.user.username}_{phone}"
    client = get_telegram_client(session_name)
    client.connect()
    dialogs = client.get_dialogs()  # Synchronous version
    return render(request, 'telegram_chats.html', {'dialogs': dialogs})