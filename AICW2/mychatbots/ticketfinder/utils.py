from .models import TrainJourney

def get_train_data():
    # Retrieve data needed for the prediction model
    data = TrainJourney.objects.all().values(
        'rid', 'tpl', 'pta', 'ptd', 'wta', 'wtp', 'wtd', 
        'arr_et', 'arr_wet', 'arr_at', 'dep_et', 'dep_wet', 
        'dep_at', 'pass_et', 'pass_wet', 'arr_removed', 
        'pass_removed', 'cr_code', 'lr_code'
    )
    return list(data)