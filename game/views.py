from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Shelter
from .serializers import ShelterSerializer


class ShelterViewSet(viewsets.ModelViewSet):
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Mostra solo il rifugio dell'utente loggato
        return Shelter.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def status(self, request):
        """Mostra la situazione attuale del rifugio."""
        shelter, created = Shelter.objects.get_or_create(user=request.user)
        serializer = ShelterSerializer(shelter)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def next_day(self, request):
        """Avanza di un giorno e restituisce l'evento casuale."""
        shelter, created = Shelter.objects.get_or_create(user=request.user)
        result = shelter.next_day()
        return Response(result)

    @action(detail=False, methods=['post'])
    def restart(self, request):
        """Riavvia il rifugio ai valori iniziali."""
        shelter, created = Shelter.objects.get_or_create(user=request.user)
        result = shelter.restart()
        return Response(result)
    
    @action(detail=False, methods=['post'])
    def action(self, request):
        """Esegue l'azione di giorno, poi passa la notte (evento casuale)."""
        shelter, created = Shelter.objects.get_or_create(user=request.user)
        action_type = request.data.get("action")

        # Giorno
        day_result = shelter.perform_action(action_type)

        # Notte
        night_result = shelter.next_day()

        return Response({
            "day": night_result["day"],
            "day_action": day_result["event"],
            "night_event": night_result["event"],
            "status": night_result["status"]
        })