.. Django ListView Filters documentation master file, created by
   sphinx-quickstart on Tue Aug 30 13:32:06 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django ListView Filters's documentation!
===================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   settings
   classes
   miscellaneous

Purpose
=======

Attempting to duplicate the functionality of the `ModelAdmin List Filter <https://docs.djangoproject.com/en/stable/ref/contrib/admin/filters/>`_ capabilities.

This is largely a copy-paste of the source code for that modified to work outside of the admin interface. For example, references to ``model_admin`` have been removed.

Installation
============

.. substitution-code-block:: console

   python -m pip install django_listview_filters==|ProjectVersion|

Additional Functionality
========================

A few customizations are added.

Add 'Clear Filter' Context
--------------------------

Adds :ref:`setting <show_all_setting>` for replacing the 'All' link with a button that clears the parameter from the query.

Only List Lookups With Matches
------------------------------

Adds :ref:`setting <show_unused_setting>` for filtering of list for sidebar to only those with matches. That way empty links aren't taking up valuable space.

Add Count to Context (Future)
-----------------------------

Add the count of number of objects to each link that can be shown in the template.

Configuration
=============

Basics
------

Filter choices should be sorted at the template or context level.

*Example:*

*In your class-based view:*

.. code-block:: python

   def get_context_data(self, **kwargs)
      # super() is import for all of the other context gathering in FilterViewMixin
      context = super().get_context_data(**kwargs)

      # This matches the name defined in `list_filters` in the view definition.
      filter_name = 'author'

      # Method of FilterViewMixin
      filter = self.get_filter_by_name(filter_name)

      # Sort by lowercase of second object of tuples (display name)
      filter.lookup_choices = sorted(filter.lookup_choices, key = lambda x: x[1].lower())

      return context

or in your template using the built-in `dictsort <https://docs.djangoproject.com/en/stable/ref/templates/builtins/#dictsort>`_ filter:

.. code-block:: html+django

   {% with filter_objects|dictsort:"display" as display_list %}
      {% for item in display_list %}
         <div class="row">
            <a href="{{ item.query_string }}" class="col-auto nav-link link-dark py-0{% if item.selected %} active{% endif %}">
               {{ item.display|truncatechars:20 }}
            </a>
         </div>
      {% endfor %}
   {% endwith %}

Examples
========

Model
-----

.. code-block:: python

   from django.db import models

   class Author(models.Model):
      name = models.CharField("Author's Name", max_length=100)
      birthday = models.DateField("Author's Birthday", blank=True)

   class Book(models.Model):
      title = models.CharField("Book Title", max_length=150)
      author = models.ForeignKey(Author, on_delete=models.PROTECT)

Class-based View
----------------

.. code-block:: python

   from django.view.generic import ListView

   from django_listview_filters.filters import RelatedFieldListViewFilter
   from django_listview_filters.mixins import FilterViewMixin

   class AuthorListView(ListView):
      context_object_name = "author"
      queryset = Author.objects.order_by("name")

   class BookListView(FilterViewMixin, ListView):
      context_object_name = "book"
      queryset = Author.objects.order_by("title")

      list_filter = [
         ('author', RelatedFieldListViewFilter)
      ]

Template
--------

.. code-block:: html+django

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

.. Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
