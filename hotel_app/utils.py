from .models import Room, Booking, Category
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateRooms(request, rooms):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 2))

    paginator = Paginator(rooms, size)

    try:
        paginated_rooms = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        paginated_rooms = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        paginated_rooms = paginator.page(page)

    return {
        "rooms": paginated_rooms.object_list,
        "current_page": page,
        "total_pages": paginator.num_pages,
        "total_rooms": paginator.count,
    }



def searchRooms(request):
    if request.GET.get('search'):
        search = request.GET.get('search', '')

        rooms = Room.objects.distinct().filter(
            Q(title__icontains=search) |
            Q(capacity__icontains=search)|
            Q(room_size__icontains=search) |
            Q(room_slug__icontains=search)
        )

        return rooms, search

    elif request.GET.get('filter'):
        search = request.GET.get('filter', '')

        category = Category.objects.filter(category_name__icontains=search)

        rooms = Room.objects.distinct().filter(
            Q(category__in=category)
        )

        return rooms, search
    else:
        rooms = Room.objects.all()
        return rooms, ''
