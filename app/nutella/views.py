"""Module providing views to app nutella"""
import logging
from sqlite3 import OperationalError

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from off.models import Favorite, Product

logger = logging.getLogger(__name__)

def nutriscore(score):
    
    if score=='a':
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Nutri-score-A.svg/128px-Nutri-score-A.svg.png"
    elif score=='b':
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Nutri-score-B.svg/128px-Nutri-score-B.svg.png"
    elif score=='c':
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Nutri-score-C.svg/128px-Nutri-score-C.svg.png"
    
    elif score=='d':
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Nutri-score-D.svg/128px-Nutri-score-D.svg.png"
    
    else:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Nutri-score-E.svg/128px-Nutri-score-E.svg.png"
    

# Create your views here.
def index(request):
    """generic view"""
    return render(request,'nutella/index.html')

def product(request, pk):
    """detail product view"""
    detail = Product.objects.get(pk=pk)
    context = {"product":detail, "nutriscore": nutriscore(detail.score)}
    return render(request,'nutella/product.html', context)

def search_product(request):
    """search view for index search"""

    logger.info('New search', exc_info=True, extra={
        'request':request,
    })

    search_term = request.GET.get('home_search')
    
    page = request.GET.get('page', 1)
    
  
    result = Product.objects.filter(product__icontains=search_term).order_by('product')

    paginator = Paginator(result, per_page=12)
    
    try:
        page_object = paginator.get_page(page)

    except EmptyPage:

        page_object = paginator.get_page(paginator.num_pages)
        
    context = {
        'product_list':page_object,
        'search_term': search_term,
        'message': None,
    }
    
    if result.count() ==0:
        context['message']="Votre recherche n'a retourn?? aucun r??sultat."
    elif result.count()==1:
        context['message']="Votre recherche a retourn?? 1 r??sultat."
    else:
        context['message']="Votre recherche a retourn?? " + str(result.count()) + ' r??sultats.'

    
    return render(request, 'nutella/product_search.html', context)

def search_replacement(request, pk):
    """search view for product replacement"""
    context={
        'product_list':None,
        'product_name':None,
        'product_score':None,
        'product_image': None,
        'product_id':0,
        'message': None
    }

    base_product = Product.objects.select_related('category_id').get(pk=pk)
    context['product_name']=base_product.product
    context['product_score']=base_product.score
    context['product_image']= base_product.pic_url
    context['product_id']= base_product.id
    
    global_queryset = (Product.objects.select_related('category_id')
                       .filter(category_id__exact=base_product.category_id)
                       .exclude(pk=base_product.pk))
    
    global_queryset = global_queryset.filter(score__lt=base_product.score).order_by('score', 'product')

    
    if global_queryset.count() ==0:
        context['message']=("Je n'ai trouv?? aucun produit dont le Nutriscore est meilleur que celui de "
                           + base_product.product + '(' + base_product.score +')')
    
    elif global_queryset.count()==1:
        context['message']="J'ai trouv?? un produit bien meilleur pour votre sant??."
    
    else:
        context['message']="J'ai trouv?? " + str(global_queryset.count()) + ' produits bien meilleurs pour votre sant??.'

    paginator = Paginator(global_queryset, per_page=12)

    page = request.GET.get('page', 1)
    
    try:
        page_object = paginator.get_page(page)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)


    except EmptyPage:

        page_object = paginator.get_page(paginator.num_pages)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(paginator.num_pages)
        
    except PageNotAnInteger:
        
        page_object = paginator.get_page(1)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(1)
    

    context['product_list'] = page_object

    return render(request, 'nutella/product_replacement.html', context)

@login_required
def save_favorite(request, pk_replaced, pk_replacing):
    """save replacement product in database for the current user"""
    replaced = Product.objects.get(id=pk_replaced)
    replacing = Product.objects.get(id=pk_replacing)
    
    try:
    
        Favorite.objects.create(
            product_id = replaced,
            replacement_id = replacing,
            user_id = request.user)
        
    except:
        pass
    
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)

@login_required
def delete_favorite(request, pk):
    """delete replacement product in database for the current user"""
    Favorite.objects.filter(id__exact=pk).delete()
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)

@login_required
def product_user(request, pk):
    """display favorite recorded product for current user"""
    queryset = Favorite.objects.filter(user_id__exact=pk)
    context={'product_list': queryset, "message": None}
    if queryset.count()==0:
        context['message']=", vous n'avez enregistr?? aucun produit."
    elif queryset.count()==1:
        context['message']=", vous avez enregistr?? 1 produit."
    else:
        context['message']=", vous avez enregistr?? " + str(queryset.count()) + ' produits.'
        
    return render(request, 'nutella/product_user.html', context)

def legal_notice(request):
    """display legal notice"""
    return render(request, 'nutella/legal_notice.html')
