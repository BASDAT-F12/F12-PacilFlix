from django.shortcuts import render
from user.queries import get_all_packages, get_active_subscription, get_transaction_history, get_package_by_name

# Create your views here.
def list_package(request):
    packages = get_all_packages()
    active = get_active_subscription(request.session['username'])
    histories = get_transaction_history(request.session['username'])
    return render(request, "daftar-langganan.html", {
        'packages': packages,
        'active': active,
        'histories': histories
    })

def buy_page(request, id):
    buy_package = get_package_by_name(id)
    context = {
        'buy_package': buy_package
    }
    return render(request, "halaman-beli.html", context)