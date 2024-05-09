from .models import TrainJourney
from django.core.paginator import Paginator


def get_train_data():
    # Ensure this function is fetching the correct columns and that they are correctly typed.
    # Debugging: log the data fetched
    data = TrainJourney.objects.all().values(
        'rid', 'tpl', 'pta', 'ptd', 'wta', 'wtp', 'wtd',
        'arr_et', 'arr_wet', 'arr_at', 'dep_et', 'dep_wet',
        'dep_at', 'pass_et', 'pass_wet', 'pass_at',
        'arr_removed', 'pass_removed', 'cr_code', 'lr_code'
    )
    print(f"Data fetched: {list(data[:5])}")  # Print first 5 rows to inspect
    return list(data)
# def get_train_data(page=1, per_page=1000):
#     query = TrainJourney.objects.all().order_by('rid').values(
#         'rid', 'tpl', 'pta', 'ptd', 'wta', 'wtp', 'wtd',
#         'arr_et', 'arr_wet', 'arr_at', 'dep_et', 'dep_wet',
#         'dep_at', 'pass_et', 'pass_wet', 'pass_at',
#         'arr_removed', 'pass_removed', 'cr_code', 'lr_code'
#     )
#     paginator = Paginator(query, per_page)
#     page_obj = paginator.page(page)
#     print(f"Total records fetched: {paginator.count}, Page size: {len(page_obj)}")  # Improved debugging
#     return list(page_obj)