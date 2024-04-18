from django.db import models

class TrainTicket(models.Model):
    departure_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.departure_station} to {self.arrival_station} at £{self.price}"

class TrainStation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)
    location = models.CharField(max_length=200)  # Optional

    def __str__(self):
        return self.name

class TrainFare(models.Model):
    origin = models.ForeignKey(TrainStation, related_name='fare_origin', on_delete=models.CASCADE)
    destination = models.ForeignKey(TrainStation, related_name='fare_destination', on_delete=models.CASCADE)
    date = models.DateField()
    fare = models.DecimalField(max_digits=6, decimal_places=2)  # Adjust precision as necessary

    def __str__(self):
        return f"{self.origin} to {self.destination} on {self.date} - £{self.fare}"

class UserQuery(models.Model):
    query_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)  # To track whether the query has been processed

    def __str__(self):
        return f"Query made at {self.timestamp}"
