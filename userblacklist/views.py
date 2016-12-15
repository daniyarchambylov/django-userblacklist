from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST

from .forms import UserBlacklistForm


@login_required
@require_POST
def user_block_toggle(request):
    form = UserBlacklistForm(request.POST or None)

    if form.is_valid():
        result = form.save()
        return JsonResponse({'status': 'success', 'data': result})
    return JsonResponse({'status': 'error', 'errors': form.errors})
