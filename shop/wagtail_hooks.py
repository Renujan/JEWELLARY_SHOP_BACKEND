from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from django.urls import reverse
from django.utils.html import format_html
from .models import Product, Enquiry, BillingInfo
from wagtail.admin.panels import FieldPanel

# 👉 Product Admin ViewSet
class ProductAdmin(SnippetViewSet):
    model = Product
    icon = "tag"
    add_to_admin_menu = True
    inspect_view_enabled = True
    menu_label = "Products"
    list_display = ("name", "price", "category", "in_stock", "color")
    search_fields = ("name", "category", "color")

@hooks.register("register_snippet_viewset")
def register_product_admin():
    return ProductAdmin()

# 👉 Enquiry Admin ViewSet
class EnquiryAdmin(SnippetViewSet):
    model = Enquiry
    icon = "form"
    add_to_admin_menu = True
    inspect_view_enabled = True
    menu_label = "Enquiries"
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")

    panels = [
        FieldPanel('name', read_only=True),
        FieldPanel('email', read_only=True),
        FieldPanel('subject',read_only=True),
        FieldPanel('message',read_only=True),
    ]

@hooks.register("register_snippet_viewset")
def register_enquiry_admin():
    return EnquiryAdmin()

# 👉 BillingInfo Admin ViewSet
class BillingAdmin(SnippetViewSet):
    model = BillingInfo
    icon = "user"
    inspect_view_enabled = True
    add_to_admin_menu = True
    menu_label = "Billing Info"
    list_display = ("full_name", "city", "phone_number", "email", "created_at")
    search_fields = ("full_name", "email", "city")

    panels = [
        FieldPanel('full_name',read_only=True),
        FieldPanel('address',read_only=True),
        FieldPanel('city', read_only=True),
        FieldPanel('phone_number',read_only=True),
        FieldPanel('email', read_only=True),
    ]

@hooks.register("register_snippet_viewset")
def register_billing_admin():
    return BillingAdmin()

# ✅ Custom CSS (Already in your code)
@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="/static/css/custom-admin.css">')

# ✅ Custom Menu Item (Home)
@hooks.register('register_admin_menu_item')
def register_main_admin_menu_item():
    return MenuItem(
        'Home',
        reverse('wagtailadmin_home'),
        icon_name='home',
        order=1
    )

# ✅ Hide unwanted main menu items
@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(request, menu_items):
    new_menu_items = []
    for item in menu_items:
        if item.name not in ['reports', 'help', 'explorer', 'documents', 'images']:
            new_menu_items.append(item)
    menu_items[:] = new_menu_items

# ✅ Hide unwanted settings menu items
@hooks.register('construct_settings_menu')
def hide_settings_items(request, menu_items):
    new_menu_items = []
    for item in menu_items:
        if item.name not in ['redirects', 'sites', 'collections', 'workflows', 'workflow-tasks']:
            new_menu_items.append(item)
    menu_items[:] = new_menu_items
