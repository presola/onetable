from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.core import serializers
import uuid

from .models import Organization, OrganizationUser, App, AppUser, Menu, List, ListField, Record, RecordField
from .forms import OrganizationForm, AppForm, ListForm, ListFieldFormset

# TODO
# On all views, @login_required prevents users not logged in, but need method and
# approach for making sure users are viewing / editing / creating / etc. only in
# the apps and organizations they have been added to and (eventually) have the
# correct permissions for.


# TODO
# Urls for template / page rendering and ajax are mixed in together, messy and
# hard to organize. Need to split somehow into ajax/ url or organize so it's clear
# which url routes are used for ajax, and what is used for page template rendering



#===============================================================================
# Static Pages / Home Page Setup
#===============================================================================

def home(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/home.html', context=context)

def terms(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/terms.html', context=context)

def privacy(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/privacy.html', context=context)

def about(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/about.html', context=context)

#===============================================================================
# Organizations
#===============================================================================

@login_required
def organizations(request):

    userOrganizations = OrganizationUser.objects.filter(user=request.user, status__exact='active', organization__status__exact="active").order_by('organization__name',)
    organizations = []
    for userOrganization in userOrganizations:
        organizations.append(userOrganization.organization)

    context = {
        'organizations': organizations
    }

    return render(request, 'home/organizations.html', context=context)

@login_required
def add_organization(request):

    # Uses standard django forms

    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():

            # Save the new project
            organization = form.save(commit=False)
            organization.created_user = request.user
            organization.created_at = timezone.now()
            organization.save()

            # Save the new user <> project relation
            organizationUser = OrganizationUser()
            organizationUser.user = request.user
            organizationUser.organization = organization
            organizationUser.status = "active"
            organizationUser.role = "admin"
            organizationUser.save()

            return redirect('apps', organization_pk=organization.pk)

    else:
        form = OrganizationForm()

        return render(request, 'home/organization-form.html', {'form': form})

@login_required
def edit_organization(request, organization_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)

    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.last_updated = timezone.now()
            organization.save()
            return redirect('organizations')
    else:
        form = OrganizationForm(instance=organization)

        context = {
            'organization': organization,
            'form': form
        }

        return render(request, 'home/organization-form.html', {'form': form})

@login_required
def archive_organization(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)

    organization.status = "archived"
    organization.save()

    return redirect('organizations')

@login_required
def organization_settings(request, organization_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)

    form = OrganizationForm(instance=organization)

    context = {
        'organization': organization,
        'form': form
    }

    return render(request, 'home/organization-settings.html', context=context)

#===============================================================================
# Apps (Workspaces)
#===============================================================================

@login_required
def apps(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    userApps = AppUser.objects.filter(user=request.user, status__exact='active', app__status__exact="active", app__organization=organization).order_by('app__name',)
    apps = []
    for userApp in userApps:
        apps.append(userApp.app)

    context = {
        'organization': organization,
        'apps': apps
    }

    return render(request, 'home/apps.html', context=context)

@login_required
def add_app(request, organization_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)

    if request.method == "POST":
        form = AppForm(request.POST)
        if form.is_valid():

            # Save the new project
            app = form.save(commit=False)
            app.organization = organization
            app.created_user = request.user
            app.created_at = timezone.now()
            app.save()

            # Save the new user <> project relation
            appUser = AppUser()
            appUser.user = request.user
            appUser.app = app
            appUser.status = "active"
            appUser.role = "admin"
            appUser.save()

            return redirect('app_details', organization_pk=organization_pk, app_pk=app.pk)

    else:

        form = AppForm()
        context = {
            'form': form,
            'organization': organization
        }

        return render(request, 'home/app-form.html', {'form': form})

@login_required
def edit_app(request, organization_pk, app_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.method == "POST":
        form = AppForm(request.POST, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
            app.last_updated = timezone.now()
            app.save()
            return redirect('apps', organization_pk=organization_pk)
    else:
        form = AppForm(instance=app)

        context = {
            'organization': organization,
            'app': app,
            'form': form
        }

        return render(request, 'home/app-form.html', {'form': form})

@login_required
def archive_app(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    app.status = "archived"
    app.save()

    return redirect('apps', organization_pk=organization_pk)

@login_required
def app_settings(request, organization_pk, app_pk):

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    form = AppForm(instance=app)

    context = {
        'organization': organization,
        'app': app,
        'form': form
    }

    return render(request, 'home/app-settings.html', context=context)

@login_required
def app_details(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    context = {
        'organization': organization,
        'app': app,
        'type': 'dashboard'
    }

    # Always loads the full workspace here (no ajax), defaults to dashboard content
    # in the template file
    return render(request, 'home/workspace.html', context=context)


#===============================================================================
# Workspace Pages
#===============================================================================

@login_required
def dashboard(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/dashboard.html",
            context={
                'organization': organization,
                'app': app
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'type': 'dashboard'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def tasks(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/tasks.html",
            context={
                'organization': organization,
                'app': app
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'type': 'tasks'
        }

        return render(request, 'home/workspace.html', context=context)


@login_required
def notes(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/notes.html",
            context={
                'organization': organization,
                'app': app
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'type': 'notes'
        }

        return render(request, 'home/workspace.html', context=context)


#===============================================================================
# Lists
#===============================================================================

@login_required
def lists(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    lists = List.objects.all().filter(status='active', app=app)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/lists.html",
            context={
                'organization': organization,
                'app': app,
                'lists': lists
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'lists': lists,
            'type': 'lists'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    records = Record.objects.all().filter(status='active', list=list)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/list.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'records': records
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'records': records,
            'type': 'list'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def create_list(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    lists = List.objects.all().filter(status='active', app=app)

    # Django formset stuff

    # Use model formset and not inline formset for more control over the data
    # being saved (i.e. setting and checking primary fields, etc.)

    if request.method == 'GET':
        listform = ListForm(request.GET or None)
        formset = ListFieldFormset(queryset=List.objects.none())

    elif request.method == 'POST':
        listform = ListForm(request.POST)
        formset = ListFieldFormset(request.POST)

        print(request.POST)

        # Verify the form submitted is valid
        if listform.is_valid() and formset.is_valid():

            list = listform.save(commit=False)
            list.app = app
            list.created_user = request.user
            list.created_at = timezone.now()
            list.save() # Save here then update primary field once field is saved
            # Loop through the list field forms submitted
            for index, form in enumerate(formset):

                print('--------') # Just for testing
                print(form.cleaned_data) # Just for testing

                # Save the list field
                list_field = form.save(commit=False)
                list_field.list = list
                list_field.created_user = request.user
                list_field.created_at = timezone.now()
                
                if index == 0:
                    list_field.primary = True
                    list_field.required = True
                    list_field.visible = True
                list_field.save()

            return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)

    context={
        'organization': organization,
        'app': app,
        'lists': lists,
        'listform': listform,
        'formset': formset,
        'type': 'list-create'
    }

    # TODO eventually handle ajax calls vs. direct link call

    return render(request, 'home/workspace.html', context=context)

@login_required
def edit_list(request, organization_pk, app_pk, list_pk):

    # TODO Implement django formset here and replace below

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    # We need to get the existing list fields
    # Keeping as object not django model because easier to manage here / local storage
    # needs this json format
    fields = ListField.objects.all().filter(status='active', list=list).order_by('order')

    list_fields = []
    for field in fields:

        field_object = {}
        field_object['id'] = field.field_id
        field_object['fieldLabel'] = field.field_label
        field_object['fieldType'] = field.field_type
        if field.select_list:
            field_object['fieldList'] = field.select_list.id
            field_object['fieldListName'] = field.select_list.name
        field_object['required'] = field.required
        field_object['primary'] = field.primary
        field_object['visible'] = field.visible
        field_object['order'] = field.order

        list_fields.append(field_object)

    # We need the available lists for edit mode choose from list dropdowns
    # Keeping as object not django model because easier to manage here / local storage
    # needs this json format
    lists = List.objects.all().filter(status='active', app=app)

    app_lists = []
    for list in lists:

        list_object = {}
        list_object['id'] = list.id
        list_object['name'] = list.name

        app_lists.append(list_object)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/list-create.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'app_lists': app_lists,
                'list_fields': list_fields
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'app_lists': app_lists,
            'list_fields': list_fields,
            'type': 'edit-list'
        }

        # Note this screen will also call the list_fields view below once loaded
        # in order to get / render the actual list fields for editing

        return render(request, 'home/workspace.html', context=context)


@login_required
def save_list(request, organization_pk, app_pk):

    # TODO Implement django formset here and replace below

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax and request.method == "POST":

        list_name = request.POST.get('list_name', None)

        field_list = json.loads(request.POST['fields'])

        list = List.objects.create(
            name=list_name,
            app=app,
            status='active',
            created_at=timezone.now(),
            created_user=request.user)
        list.save();

        for field in field_list:
            list_field = ListField.objects.create(
                list=list,
                field_id=field['id'],
                field_label=field['fieldLabel'],
                field_type=field['fieldType'],
                required=field['required'],
                visible=field['visible'],
                primary=field['primary'],
                order=field['order'],
                status='active',
                created_at=timezone.now(),
                created_user=request.user)

            # Add the embedded list here if embedded list type
            if field['fieldType'] == 'choose-from-list' or field['fieldType'] == 'choose-multiple-from-list':
                # Look up the field list
                list = get_object_or_404(List, pk=field['fieldList'])
                list_field.select_list=list

            list_field.save();

        # Redirect based on ajax call from frontend on success

        # TODO Need error handling here for fail
        data_dict = {"success": True}

        return JsonResponse(data=data_dict, safe=False)

@login_required
def update_list(request, organization_pk, app_pk, list_pk):

    # TODO Implement django formset here and replace below

    # TODO combine with save_list above to consolidate

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    if request.is_ajax and request.method == "POST":

        list_name = request.POST.get('list_name', None)
        if list_name is not list.name:
            list.name=list_name
            list.last_updated = timezone.now()
            list.save();

        field_list = json.loads(request.POST['fields'])
        removed_fields = json.loads(request.POST['removed'])

        # Loop through and update or add the fields
        for field in field_list:
            try:
                list_field = ListField.objects.get(status='active', field_id=field['id'], list=list)
                # Update the old list field database record
                list_field.field_label = field['fieldLabel']
                list_field.fieldType = field['fieldType']
                list_field.required = field['required']
                list_field.visible = field['visible']
                list_field.primary = field['primary']
                list_field.order = field['order']
                list_field.save()
            except ListField.DoesNotExist:
                # Create a new list field in the database
                list_field = ListField.objects.create(
                    list=list,
                    field_id=field['id'],
                    field_label=field['fieldLabel'],
                    field_type=field['fieldType'],
                    required=field['required'],
                    visible=field['visible'],
                    primary=field['primary'],
                    order=field['order'],
                    status='active',
                    created_at=timezone.now(),
                    created_user=request.user)
                list_field.save();

        for field_id in removed_fields:
            try:
                list_field = ListField.objects.get(status='active', field_id=field_id, list=list)
                list_field.status = "deleted"
                list_field.save()
            except ListField.DoesNotExist:
                # Do nothing - field already removed somehow
                pass

        # Redirect based on ajax call from frontend on success

        # TODO Need error handling here for fail
        data_dict = {"success": True}

        return JsonResponse(data=data_dict, safe=False)

@login_required
def archive_list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    list.status = "archived"
    list.save()

    # Able to use a redirect here because we did a direct POST request
    return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)

@login_required
def list_settings(request, organization_pk, app_pk, list_pk):

    # Does not / will not use the standard django forms per the comments noted
    # above

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    context = {
        'organization': organization,
        'app': app,
        'list': list
    }

    return render(request, 'home/list-settings.html', context=context)


#===============================================================================
# Records
#===============================================================================

@login_required
def add_record(request, organization_pk, app_pk, list_pk):

    # Very similar to the edit_record view, but includes the field values previously saved
    # Probably a way to combine these views to consolidate

    # We are not using the following here:
    # 1) Django form.Forms (couldn't find a way to create dynamic forms this approach,
    # but we may be able to find eventually)
    # 2) the models.Model @property for list.list_fields or the record.record_fields >>
    # needed an object with both the field inforation and value included so we can edit prvious values here

    # Instead, only approach could find is building an object here then passing it to the frontend
    # template for rending the form

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    fields = []
    for list_field in list.list_fields:

        field_object = {}
        field_object['field_id'] = list_field.field_id
        field_object['field_label'] = list_field.field_label
        field_object['field_type'] = list_field.field_type
        field_object['required'] = list_field.required
        field_object['primary'] = list_field.primary
        field_object['visible'] = list_field.visible
        field_object['order'] = list_field.order

        fields.append(field_object)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-create.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'fields': fields
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'fields': fields,
            'type': 'edit-record'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def save_record(request, organization_pk, app_pk, list_pk):

    # This handles both saving and updating a record

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    record_id = request.POST.get('record_id', None)
    fields = json.loads(request.POST['field_values'])

    # TODO
    # Needs error handling here verify if the form is valid (i.e. all required fields, acceptable data types, etc)

    record = None # Create object globally outside of the if/else
    if record_id is not None:
        # Get the existing record / this is a record being edited
        record = get_object_or_404(Record, pk=record_id)
    else:
        # Add a new record
        record = Record.objects.create(
            list=list,
            status='active',
            created_at=timezone.now(),
            last_updated=timezone.now(),
            created_user=request.user)
        record.save();

    for field in fields:

            # Print for testing / temporary
            print('---------------')
            print(field['fieldId'])
            print(field['fieldValue'])

            if field['fieldValue'] is not None:
                # Only save a RecordField object if there is a value

                if record_id is not None:

                    try:
                        # Update existing record field
                        record_field = RecordField.objects.get(status='active', list_field__field_id=field['fieldId'], record=record)
                        record_field.value = field['fieldValue']
                        record_field.last_updated = timezone.now()
                        record_field.save()

                    except RecordField.DoesNotExist:

                        # This record field has not been saved before, so create it
                        # Note this is redundant with below / can be consolidated eventually
                        try:

                            list_field = ListField.objects.get(status='active', field_id=field['fieldId'], list=list)

                            record_field = RecordField.objects.create(
                                record=record,
                                list_field=list_field,
                                value=field['fieldValue'],
                                status='active',
                                created_at=timezone.now(),
                                created_user=request.user)
                            record_field.save()

                        except ListField.DoesNotExist:
                            # Easy error handling for now
                            pass

                else:

                    try:

                        # Create new record field

                        list_field = ListField.objects.get(status='active', field_id=field['fieldId'], list=list)

                        record_field = RecordField.objects.create(
                            record=record,
                            list_field=list_field,
                            value=field['fieldValue'],
                            status='active',
                            created_at=timezone.now(),
                            created_user=request.user)
                        record_field.save()

                    except ListField.DoesNotExist:
                        # Easy error handling for now
                        pass

    # Using ajax here to save because cannot do a POST request and get the field values
    # from a dynamically created form (or at least I couldn't figure out how to
    # do this, although there may be a way to!)

    # Redirect based on ajax call from frontend on success

    data_dict = {"success": True}

    return JsonResponse(data=data_dict, safe=False)

@login_required
def record(request, organization_pk, app_pk, list_pk, record_pk):

    # Record details page (placeholder for now)
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'record': record
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'type': 'record',
            'record_view': 'record-details'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def record_details(request, organization_pk, app_pk, list_pk, record_pk):

    # Record details page (placeholder for now)

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-details.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'record': record

            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    # TODO add access here for direct link
    # For now just return record details
    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'type': 'record',
            'record_view': 'record-details'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def record_notes(request, organization_pk, app_pk, list_pk, record_pk):

    # Record details page (placeholder for now)

    record = get_object_or_404(Record, pk=record_pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-notes.html",
            context={
                'record': record

            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    # TODO add access here for direct link
    # For now just return record details
    else:

        # If accessing the url directly, load full page
        organization = get_object_or_404(Organization, pk=organization_pk)
        app = get_object_or_404(App, pk=app_pk)
        list = get_object_or_404(List, pk=list_pk)

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'type': 'record',
            'record_view': 'record-notes'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def record_tasks(request, organization_pk, app_pk, list_pk, record_pk):

    # Record details page (placeholder for now)
    record = get_object_or_404(Record, pk=record_pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-tasks.html",
            context={
                'record': record
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page
        organization = get_object_or_404(Organization, pk=organization_pk)
        app = get_object_or_404(App, pk=app_pk)
        list = get_object_or_404(List, pk=list_pk)

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'type': 'record',
            'record_view': 'record-tasks'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def edit_record(request, organization_pk, app_pk, list_pk, record_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)

    # Very similar to the add_record view, but includes the field values previously saved
    # Probably a way to combine these views to consolidate

    # We are not using the following here:
    # 1) Django form.Forms (couldn't find a way to create dynamic forms this approach,
    # but we may be able to find eventually)
    # 2) the models.Model @property for list.list_fields or the record.record_fields >>
    # needed an object with both the field inforation and value included so we can edit prvious values here

    # Instead, only approach could find is building an object here then passing it to the frontend
    # template for rending the form

    fields = []
    for list_field in list.list_fields:

        field_object = {}
        field_object['field_id'] = list_field.field_id
        field_object['field_label'] = list_field.field_label
        field_object['field_type'] = list_field.field_type
        field_object['required'] = list_field.required
        field_object['primary'] = list_field.primary
        field_object['visible'] = list_field.visible
        field_object['order'] = list_field.order

        # Get the field value if it exists
        for record_field in record.record_fields:
            if list_field.id == record_field.list_field.id:
                field_object['value'] = record_field.value

        fields.append(field_object)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-create.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'fields': fields,
                'record': record
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'fields': fields,
            'type': 'edit-record'
        }

        return render(request, 'home/workspace.html', context=context)


# TODO need view for archiving records

# TODO need view for create task, edit task, archive task, get tasks (will use
# standard django forms for this)

# TODO need view for create note, edit note, archive note, get notes (will use
# standard django forms for this)

#===============================================================================
# Records
#===============================================================================

# Will be used later for replacing the default django pk / id's in urls
def generate_random_string(string_length=10):
    # Not sure this is the best approach, but works okay for now

    random = str(uuid.uuid4()) # Make into string
    random = random.replace("-","") # Just letters and numbers
    return random[0:string_length] # Truncate to correct length
