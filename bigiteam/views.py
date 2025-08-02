from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import BigItemService, BigItemStop

class BigItemServiceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        services = BigItemService.objects.all().order_by('-created_at')  # reverse() replaced with order_by for clarity
        if not services.exists():
            return Response({'message': 'No big item services found.'}, status=status.HTTP_404_NOT_FOUND)

        service_data = []
        for service in services:
            stops = BigItemStop.objects.filter(service=service)
            stop_data = [
                {
                    'id': stop.id,
                    'location': stop.stop_location,
                    'address_line_2': stop.stop_address_line_2
                } for stop in stops
            ]
            service_data.append({
                'id': service.id,
                'user': service.user.mobile_number,
                'pickup_location': service.pickup_location,
                'pickup_address_line_2': service.pickup_address_line_2,
                'dropoff_location': service.dropoff_location,
                'dropoff_address_line_2': service.dropoff_address_line_2,
                'service_time': service.service_time,
                'scheduled_time': service.scheduled_time,
                'loading_help': service.loading_help,
                'payment_method': service.payment_method,
                'stops': stop_data
            })
        return Response(service_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        
        try:
            service = BigItemService.objects.create(
                user=request.user,
                pickup_location=data['pickup_location'],
                pickup_address_line_2=data.get('pickup_address_line_2', ''),
                dropoff_location=data['dropoff_location'],
                dropoff_address_line_2=data.get('dropoff_address_line_2', ''),
                service_time=data['service_time'],
                scheduled_time=data.get('scheduled_time', None),
                loading_help=data['loading_help'],
                payment_method=data['payment_method']
            )

            stops_data = data.get('stops', [])
            for stop in stops_data:
                BigItemStop.objects.create(
                    service=service,
                    stop_location=stop['stop_location'],
                    stop_address_line_2=stop.get('stop_address_line_2', ''),
                    order=stop.get('order', 0)
                )

            return Response({'message': 'Big item service created successfully.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)