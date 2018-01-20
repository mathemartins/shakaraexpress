from django.shortcuts import render

# Create your views here.

def homepage(request):
	query = request.GET.get("q")
	query2 = request.GET.get("q2")
	if query and query2:
		if len(query) == 0:
			if len(query2) == 0:
				raise ValidationError("Either fields cannot be empty!")
				qs = qs.filter(
						Q(business_name__icontains=query)|
						Q(profession__icontains=query) |
						Q(category__icontains=query) |
						Q(address__icontains=query2)
					)
	template = "core/index.html"
	context = {}
	return render(request, template, context)