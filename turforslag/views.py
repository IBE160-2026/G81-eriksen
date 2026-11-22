from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def sok(request):
    """Forsiden Søk. Søkeskjemaet kommer i story 1.9."""
    return render(request, "turforslag/sok.html")
