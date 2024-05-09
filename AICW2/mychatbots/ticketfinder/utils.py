from .models import TrainJourney
from django.core.paginator import Paginator


def get_train_data():
    
    data = TrainJourney.objects.all().values(
        'rid', 'tpl', 'pta', 'ptd', 'wta', 'wtp', 'wtd',
        'arr_et', 'arr_wet', 'arr_at', 'dep_et', 'dep_wet',
        'dep_at', 'pass_et', 'pass_wet', 'pass_at',
        'arr_removed', 'pass_removed', 'cr_code', 'lr_code'
    )
    # debugging 
    print(f"Data fetched: {list(data[:5])}")  
    return list(data)
