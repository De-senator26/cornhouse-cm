# pylint: disable=no-member
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import User
from apps.harvests.models import Harvest, Loss
from apps.finance.models import Grant
from apps.marketplace.models import Listing

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Return analytics metrics for partner and admin users."""
    # Only allow partners and admins
    if request.user.role not in ['partner', 'admin']:
        return Response({'error': 'Permission denied'}, status=403)

    # Total farmers
    total_farmers = User.objects.filter(role='farmer').count()

    # Total harvests
    total_harvests = Harvest.objects.count()
    total_harvest_kg = Harvest.objects.aggregate(total=Sum('quantity_kg'))['total'] or 0

    # Total losses
    total_losses_kg = Loss.objects.aggregate(total=Sum('quantity_kg'))['total'] or 0

    # Grants disbursed
    grants_disbursed = Grant.objects.filter(status='disbursed').aggregate(total=Sum('amount_requested'))['total'] or 0
    grants_pending = Grant.objects.filter(status='pending').count()

    # Active listings
    active_listings = Listing.objects.filter(is_active=True).count()

    # Harvests per month (last 6 months)
    six_months_ago = timezone.now().date() - timedelta(days=180)
    harvests_by_month_qs = (
        Harvest.objects
        .filter(harvest_date__gte=six_months_ago)
        .annotate(month=TruncMonth('harvest_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    harvests_by_month = [
        {'month': item['month'].strftime('%Y-%m') if item['month'] else None, 'count': item['count']}
        for item in harvests_by_month_qs
    ]

    # Losses by type
    losses_by_type = (
        Loss.objects
        .values('loss_type')
        .annotate(total_kg=Sum('quantity_kg'))
        .order_by('-total_kg')
    )

    # Farmer growth (last 6 months)
    farmers_by_month_qs = (
        User.objects
        .filter(role='farmer', date_joined__gte=six_months_ago)
        .annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    farmers_by_month = [
        {'month': item['month'].strftime('%Y-%m') if item['month'] else None, 'count': item['count']}
        for item in farmers_by_month_qs
    ]

    return Response({
        'total_farmers': total_farmers,
        'total_harvests': total_harvests,
        'total_harvest_kg': total_harvest_kg,
        'total_losses_kg': total_losses_kg,
        'grants_disbursed': grants_disbursed,
        'grants_pending': grants_pending,
        'active_listings': active_listings,
        'harvests_by_month': list(harvests_by_month),
        'losses_by_type': list(losses_by_type),
        'farmers_by_month': list(farmers_by_month),
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_page(request):
    """Render the analytics dashboard page for authorized users."""
    if request.user.role not in ['partner', 'admin']:
        return redirect('home')
    return render(request, 'analytics/dashboard.html', {'token': request.session.get('access_token')})
