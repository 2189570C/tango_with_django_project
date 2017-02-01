from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm

def index(request):
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key to boldmessage is the same as {{ boldmessage }} in the template!
        category_list = Category.objects.order_by('-likes')[:5]
        pages_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': pages_list}
	
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render(request, 'rango/index.html', context=context_dict)


	
def about(request):
        return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
        context_dict = {}

        try:
                # Find the Category with the given slug
                category = Category.objects.get(slug=category_name_slug)

                # Retrieve all associated pages
                pages = Page.objects.filter(category=category)

                # Adds pages list to template under name pages
                context_dict['pages'] = pages

                # Add the category in object form from the database
                # Use this to verify that the category exists
                context_dict['category'] = category

        except Category.DoesNotExist:
                # if category does not exist then do nothing
                context_dict['category'] = None
                context_dict['pages'] = None

        return render(request, 'rango/category.html', context_dict)


def add_category(request):
        form = CategoryForm()

        # A HTTP POST?
        if request.method == 'POST':
                form = CategoryForm(request.POST)

                # Is the form valid?
                if form.is_valid():
                        # Save the new category to the database
                        form.save(commit=True)
                        # Direct back to index page
                        return index(request)
                else:
                        # The form has errors so print to terminal
                        print(form.errors)

        return render(request, 'rango/add_category.html', {'form':form})
		
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None
	
	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
            print(form.errors)
	
	context_dict = {'form':form, 'category':category}
	return render(request, 'rango/add_page.html', context_dict)
