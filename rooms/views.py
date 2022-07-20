from django.views.generic.list import ListView, View
from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404()


class SearchView(View):

    """SearchView Definition"""

    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                filtered_rooms = models.Room.objects.filter(**filter_args)
                for amenity in amenities:
                    filtered_rooms = filtered_rooms.filter(amenities=amenity)

                for facility in facilities:
                    filtered_rooms = filtered_rooms.filter(facilities=facility)

                qs = filtered_rooms.order_by("created")

                paginator = Paginator(qs, 5, orphans=2)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                if room_type is None:
                    room_type = ""
                if price is None:
                    price = ""
                if guests is None:
                    guests = ""
                if bedrooms is None:
                    bedrooms = ""
                if beds is None:
                    beds = ""
                if baths is None:
                    baths = ""

                current_url = f"/rooms/search/?city={city}&country={country}&room_type={room_type}&price={price}&guests={guests}&bedrooms={bedrooms}&beds={beds}&baths={baths}"

                if instant_book is True:
                    current_url = current_url + "&instant_book=on"
                if superhost is True:
                    current_url = current_url + "&superhost=on"

                if len(amenities) > 0:
                    for a in amenities:
                        current_url = current_url + f"&amenities{a.pk}"
                if len(facilities) > 0:
                    for f in facilities:
                        current_url = current_url + f"&facilities{f.pk}"

                return render(
                    request,
                    "rooms/search.html",
                    {
                        "form": form,
                        "rooms": rooms,
                        "path": current_url,
                    },
                )

        else:

            form = forms.SearchForm()
        return render(request, "rooms/search.html", {"form": form})
