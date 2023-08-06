# Django ListView Filters

[![Documentation Status](https://readthedocs.org/projects/django-listview-filters/badge/?version=latest)](https://django-listview-filters.readthedocs.io/en/latest/?badge=latest)

Add context to list views for sidebar links and modifying querysets with those links.

## Purpose

Attempting to duplicate the functionality of the [`ModelAdmin` List Filter](https://docs.djangoproject.com/en/stable/ref/contrib/admin/filters/) capabilities.

This is largely a copy-paste of the source code for that modified to work outside of the admin interface. For example, references to `model_admin` have been removed.

## Additional Functionality

A few customizations are added.

### Add 'Clear Filter' Context

Allow for replacing the 'All' link with a button that clears the parameter from the query.

### Only List Lookups With Matches

Allow for filtering of list for sidebar to only those with matches. That way empty links aren't taking up valuable space.

### Add Count to Context

Add the count of number of objects to each link that can be shown in the template.

## Configuration

### Model

```python
from django.db import models

class Author(models.Model):
    name = models.CharField("Author's Name", max_length=100)
    birthday = models.DateField("Author's Birthday", blank=True)

class Book(models.Model):
    title = models.CharField("Book Title", max_length=150)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
```

### Class-based View

```python
from django.view.generic import ListView

from django-listview-filters import RelatedFieldListViewFilter

class AuthorListView(ListView):
    context_object_name = "author"
    queryset = Author.objects.order_by("name")

class BookListView(ListView):
    context_object_name = "book"
    queryset = Author.objects.order_by("title")

    list_filter = [
        ('author', RelatedFieldListViewFilter)
    ]
```

### Template

```python
{% for filter_name, filter_objects, clear_fragment in filter_list %}
    <div>
        {{ filter_name|title }}
        <a href="{{ clear_fragment }}">clear filter</a>
    </div>
    <ul>
        {% with filter_objects|dictsort:"display" as display_list %}
            {% for item in display_list %}
                <div>
                    <a href="{{ item.query_string }}">
                        {{ item.display }}
                    </a>
                </div>
            {% endfor %}
        {% endwith %}
    </ul>
</div>
```
