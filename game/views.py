from rest_framework import viewsets, permissions
from rest_framework.decorators import action as drf_action
from rest_framework.response import Response
from .models import Shelter
from .serializers import ShelterSerializer, LeaderboardEntrySerializer


class ShelterViewSet(viewsets.ModelViewSet):
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Mostra solo il rifugio dell'utente loggato
        return Shelter.objects.filter(user=self.request.user)

    @drf_action(detail=False, methods=['get'])
    def status(self, request):
        """Mostra la situazione attuale del rifugio."""
        shelter, created = Shelter.objects.get_or_create(user=request.user)
        serializer = ShelterSerializer(shelter)
        return Response(serializer.data)

    @drf_action(detail=False, methods=['post'])
    def next_day(self, request):
        """Avanza di un giorno e restituisce l'evento casuale."""
        shelter, created = Shelter.objects.get_or_create(user=request.user)
        result = shelter.next_day()
        return Response(result)

    @drf_action(detail=False, methods=['post'])
    def restart(self, request):
        """Riavvia il rifugio ai valori iniziali."""
        shelter, created = Shelter.objects.get_or_create(user=request.user)
        result = shelter.restart()
        return Response(result)
    
    @drf_action(detail=False, methods=['post'])
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
    
    @drf_action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def leaderboard(self, request):
        top = (
            Shelter.objects
            .select_related('user')
            .order_by('-best_day', '-day', 'user__username')[:3]
        )
        data = LeaderboardEntrySerializer(top, many=True).data
        # aggiungo ranking 1..N
        for i, row in enumerate(data, start=1):
            row['rank'] = i
        return Response({"results": data})