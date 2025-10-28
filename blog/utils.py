from django.utils.text import slugify


def unique_slugify(
    instance, value, slug_field_name="slug", queryset=None, slug_separator="-"
):
    """
    تولید slug یکتا برای هر پست بر اساس عنوان.
    اگر slug تکراری باشد، عددی به آخر آن اضافه می‌کند.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = slugify(value)
    if not slug:
        slug = "post"

    if queryset is None:
        queryset = instance.__class__.objects.all()

    # اگر نمونه در حال ویرایش است، خودش را از queryset حذف کن
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    original_slug = slug
    counter = 1
    while queryset.filter(**{slug_field_name: slug}).exists():
        slug = f"{original_slug}{slug_separator}{counter}"
        counter += 1

    setattr(instance, slug_field.attname, slug)
