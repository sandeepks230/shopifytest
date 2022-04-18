from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.template import RequestContext
from django.apps import apps
import hmac, base64, hashlib, binascii, os
import shopify

def _new_session(shop_url):
    print("new session!!!!")
    api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION
    print("api_version::")
    print(api_version)
    return shopify.Session(shop_url, api_version)

# Ask user for their ${shop}.myshopify.com address
def login(request):
    print("session body !!!")
    request.session.pop('shopify', None)
    # If the ${shop}.myshopify.com address is already provided in the URL,
    # just skip to authenticate
    store_url = ''
    shop = request.GET.get('shop')
    print("LOGIN SESSION",request.session.__dict__)
    if 'return_to' in request.session and  request.session['return_to'] != '/':
        retstr = request.session['return_to']
        print("RETURN TO ",retstr)
        retstr_list = retstr.split('&')
        print("retstr_list")
        print(retstr_list)
        # shop=shoeshop16.myshopify.com'
        with_s = list(filter(lambda x: x.startswith('shop='), retstr_list))
        print("with_s!!")
        print(with_s)
        if with_s:
            store_url =with_s[0].replace("shop=","")
            print(store_url)
    else:
        if request.GET.get('shop'):
            print("SHOP",shop)
            return authenticate(request)
        # return render(request, 'home/index.html', {})
        return render(request, 'shopify_app/login.html', {})


    shop_url = store_url
    if not shop_url:
        # messages.error(request, "A shop param is required")
        return render(request, 'home/index.html', {})
    scope = apps.get_app_config('shopify_app').SHOPIFY_API_SCOPE
    redirect_uri = request.build_absolute_uri(reverse(finalize))
    print("LOGIN REDIRECT URI",redirect_uri)
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    print("LOGIN STATE",state)
    request.session['shopify_oauth_state_param'] = state
    permission_url = _new_session(shop_url).create_permission_url(scope, redirect_uri, state)
    print("LOGIN PERMISSION",permission_url)
    return redirect(permission_url)



    # ---------------
    # if request.GET.get('shop'):
    #     return authenticate(request)
    # return render(request, 'shopify_app/login.html', {})

def authenticate(request):
    shop_url = request.GET.get('shop', request.POST.get('shop')).strip()
    if not shop_url:
        messages.error(request, "A shop param is required")
        return render(request, 'home/index.html', {})
    scope = apps.get_app_config('shopify_app').SHOPIFY_API_SCOPE
    redirect_uri = request.build_absolute_uri(reverse(finalize))
    print("AUTHENTICATE REDIRECT URI",redirect_uri)
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    request.session['shopify_oauth_state_param'] = state
    permission_url = _new_session(shop_url).create_permission_url(scope, redirect_uri, state)
    print("Authenticate", permission_url)
    return redirect(permission_url)

def finalize(request):
    api_secret = apps.get_app_config('shopify_app').SHOPIFY_API_SECRET
    # api_secret = '4364c39c5a1d5197cef8017eb63714e0'
    params = request.GET.dict()
    print("FINALIZE PARAMS",params)
    print("FINALIZE SESSION ATTRS",request.session.__dict__)
    if request.session['shopify_oauth_state_param'] != params['state']:
        messages.error(request, 'Anti-forgery state token does not match the initial request.')
        return render(request, 'home/index.html', {})
    else:
        request.session.pop('shopify_oauth_state_param', None)

    myhmac = params.pop('hmac')
    line = '&'.join([
        '%s=%s' % (key, value)
        for key, value in sorted(params.items())
    ])
    print("APISECRET",api_secret)
    h = hmac.new(api_secret.encode('utf-8'), line.encode('utf-8'), hashlib.sha256)
    if hmac.compare_digest(h.hexdigest(), myhmac) == False:
        messages.error(request, "Could not verify a secure login")
        return render(request, 'home/index.html', {})

    try:
        shop_url = params['shop']
        session = _new_session(shop_url)
        request.session['shopify'] = {
            "shop_url": shop_url,
            "access_token": session.request_token(request.GET)
        }
        print("access_token::::")
        print(session.request_token(request.GET))

    except Exception:
        messages.error(request, "Could not log in to Shopify store.")
        return redirect(reverse(login))
    messages.info(request, "Logged in to shopify store.")
    store_url = request.GET.get('shop')
    print(store_url)



    request.session.pop('return_to', None)
    # return redirect(request.session.get('return_to', reverse('root_path')))
    return redirect('https://'+store_url+'/admin/apps/demoapp-269')

def logout(request):
    request.session.pop('shopify', None)
    messages.info(request, "Successfully logged out.")
    return render(request, 'home/index.html', {})
