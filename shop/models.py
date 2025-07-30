from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.snippets.models import register_snippet

# ---------- Page Model ----------
from django.db import models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from taggit.managers import TaggableManager

@register_snippet
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = RichTextField()
    category = models.CharField(max_length=100, choices=[
        ('ring', 'Ring'),
        ('necklace', 'Necklace'),
        ('bracelet', 'Bracelet'),
        ('earring', 'Earring'),
    ])
    in_stock = models.BooleanField(default=True)
    color = models.CharField(max_length=50, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = TaggableManager(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('price'),
        FieldPanel('description'),
        FieldPanel('category'),
        FieldPanel('in_stock'),
        FieldPanel('color'),
        FieldPanel('image'),
        FieldPanel('tags'),
    ]

    def __str__(self):
        return self.name

# ---------- Cart ----------



# ---------- Enquiry ----------
@register_snippet
class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
# 👉 Enquiry Admin ViewSet
class EnquiryAdmin(models.Model):
    model = Enquiry
    icon = "form"
    add_to_admin_menu = True
    inspect_view_enabled = True
    menu_label = "Enquiries"
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")

    # ❌ Disable Add, Edit, Delete
    add_view_enabled = False
    edit_view_enabled = False
    delete_view_enabled = False


# ---------- Billing ----------
@register_snippet
class BillingInfo(models.Model):
    
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
        return self.full_name
class Order(models.Model):
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.billing_info.full_name}"

class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.product.price
