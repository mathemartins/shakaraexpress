import json
from django.shortcuts import render, Http404, HttpResponseRedirect, redirect, get_object_or_404

# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

@login_required
def all_note(request):
    notifications = Notification.objects.all_for_user(request.user)
    context = {
        "notifications":notifications
    }
    return render(request, "notifications/notify_all.html", context)

@login_required
def read(request, id):
    notification = get_object_or_404(Notification, id=id)
    try:
        next = request.GET.get('next', None)
        if notification.recipient == request.user:
            notification.read = True
            notification.save()
            if next is not None:
                return HttpResponseRedirect(next)
            else:
                return redirect("notify:notifications_all")
        else:
            raise Http404
    except:
        raise redirect("notify:notifications_all")

@login_required
def get_notifications_ajax(request):
	if request.is_ajax() and request.method == "POST":
		notifications = Notification.objects.all_for_user(request.user).recent()
		count = notifications.count()
		notes = []
		for note in notifications:
			notes.append(str(note.get_link))
		data = {
			"notifications": notes,
			"count": count,
		}
		print (data)
		json_data = json.dumps(data)
		print (json_data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404
