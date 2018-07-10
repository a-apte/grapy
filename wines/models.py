from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


def validate_volume(value):
    if value not in [0.2, 0.25, 0.375, 0.5, 0.75, 1, 1.5, 3, 5, 6]:
        raise ValidationError(
            _('%(value)s is not a valid volume'),
            params={'value': value},
        )


class Country(models.Model):
    name = models.CharField(max_length=50)
    code_iso2 = models.CharField(max_length=2, primary_key=True)
    code_iso3 = models.CharField(max_length=3)
    url = models.URLField(blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['code_iso2']


class Grape(models.Model):
    name = models.CharField(max_length=150, unique=True)
    url = models.URLField(blank=True, default='')

    def __str__(self):
        return self.name


class WineStyle(models.Model):
    name = models.CharField(max_length=150, unique=True)
    url = models.URLField(blank=True, default='')
    acidity = models.CharField(max_length=50, blank=True, default='')
    body = models.CharField(max_length=50, blank=True, default='')
    color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class ActiveVendorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Vendor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    is_test = models.BooleanField(default=False)
    plugin = models.CharField(max_length=150)
    page = models.CharField(max_length=150)
    max_pages = models.PositiveSmallIntegerField(default=1)
    product = models.CharField(max_length=150)
    stopwords = models.CharField(max_length=250, blank=True, default='')

    objects = models.Manager()
    active = ActiveVendorManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Wine(models.Model):
    name = models.CharField(max_length=150)
    style = models.ForeignKey(
        WineStyle, blank=True, null=True, on_delete=models.PROTECT,
        related_name='wines')
    grapes = models.ManyToManyField(
        Grape, blank=True, null=True, related_name='wines')
    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.PROTECT,
        related_name='wines')
    region = models.CharField(max_length=150, null=True, blank=True)
    winery = models.CharField(max_length=150, null=True, blank=True)
    url = models.URLField(unique=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def color(self):
        return self.style.color if self.style else 'Unknown'

    @property
    def num_vendors(self):
        return self.vendors.count()

    @property
    def num_ratings(self):
        return self.ratings.aggregate(
            models.Sum('num_ratings'))['num_ratings__sum'] or 0

    @property
    def min_rating(self):
        return self.ratings.aggregate(
            models.Min('rating'))['rating__min'] or 0

    @property
    def min_price(self):
        return self.vendors.aggregate(
            models.Min('price'))['price__min'] or 0

    def latest_rating(self, rater):
        return self.ratings.filter(rater=rater).first().modified

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class VendorWine(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='vendors')
    wine = models.ForeignKey(
        Wine, blank=True, null=True, on_delete=models.CASCADE,
        related_name='vendors')
    vendor_code = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=250, blank=True, default='')
    volume = models.DecimalField(
        max_digits=5, decimal_places=3, default=0.75,
        validators=[validate_volume])
    quantity = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0,
        validators=[MinValueValidator(1)])
    url = models.URLField(unique=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def total_volume(self):
        return round(self.volume * self.quantity, 2)

    @property
    def price_per_75cl(self):
        res = 0
        if self.total_volume != 0:
            res = round(
                Decimal(self.price / self.total_volume) * Decimal(0.75), 2)
        return res


class ActiveRaterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Rater(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    is_test = models.BooleanField(default=False)
    plugin = models.CharField(max_length=150)
    page = models.CharField(max_length=150)
    limit = models.PositiveSmallIntegerField(default=1)

    objects = models.Manager()
    active = ActiveRaterManager()

    def __str__(self):
        return self.name


class WineRating(models.Model):
    wine = models.ForeignKey(
        Wine, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(
        Rater, on_delete=models.CASCADE, related_name='ratings')
    url = models.URLField(blank=True, default='')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    num_ratings = models.PositiveSmallIntegerField(default=1)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.rater.name, self.wine.name)

    class Meta:
        unique_together = (('wine', 'rater'),)
