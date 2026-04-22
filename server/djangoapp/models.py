from django.db import models


# -------------------------
# CarMake Model
# -------------------------
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# -------------------------
# CarModel Model
# -------------------------
class CarModel(models.Model):

    # choices
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'

    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]

    name = models.CharField(max_length=100)

    # Many-to-one relationship
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    dealer_id = models.IntegerField()

    car_type = models.CharField(
        max_length=20,
        choices=CAR_TYPE_CHOICES,
        default=SEDAN
    )

    year = models.IntegerField()

    def __str__(self):
        return f"{self.car_make.name} - {self.name}"