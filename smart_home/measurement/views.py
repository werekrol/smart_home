# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorView(APIView):
    def get(self, request):
        sensors = Sensor.objects.all()
        sen = SensorSerializer(sensors, many=True)
        return Response(sen.data)

    def post(self, request):
        data = SensorSerializer(request.data)
        sen = Sensor(name=data.data['name'], description=data.data['description'])
        sen.save()
        return Response(data.data)


class DetailView(APIView):
    def get_object(self, pk):
        return Sensor.objects.get(id=pk)

    def patch(self, request, pk):
        sensor = self.get_object(pk)
        serializer = SensorSerializer(instance=sensor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'Ошибка!': 'Что-то пошло не так...'})

    def get(self, request, pk):
        sensor = self.get_object(pk)
        # sensors = Sensor.objects.all()
        sen = SensorDetailSerializer(sensor, )
        return Response(sen.data)


class MeasurementsView(APIView):
    def post(self, request):
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)