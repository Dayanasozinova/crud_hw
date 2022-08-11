from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
        # extra_kwargs = {'stock': {'required': 'False'}}


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', ]

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)
        for position in positions:
            position_obj = StockProduct.objects.create(stock=stock, **position)
            stock.positions.add(position_obj)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for a, position in positions:
            position_obj = StockProduct.objects.update(stock=stock, **position)
            stock.positions.add(position_obj)
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    # def update_or_create(self, instance, validated_data):
    #     positions = validated_data.pop('positions')
    #     stock = super().update_or_create(instance, validated_data)
    #     for position in positions:
    #         position_obj = StockProduct.objects.update_or_create(stock=stock, **position)
    #         stock.positions.add(position_obj)
    #
    #     return stock
