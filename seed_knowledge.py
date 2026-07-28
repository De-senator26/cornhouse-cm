from apps.knowledge.models import Category, Article
from apps.users.models import User

cat1, _ = Category.objects.get_or_create(name='Climate-Smart Agriculture')
cat2, _ = Category.objects.get_or_create(name='Post-Harvest Storage')
cat3, _ = Category.objects.get_or_create(name='Financial Literacy')
cat4, _ = Category.objects.get_or_create(name='Soil Health')

admin = User.objects.filter(username='Admin').first()
if not admin:
    admin = User.objects.filter(is_superuser=True).first()

if admin:
    article1, _ = Article.objects.get_or_create(
        title='Climate-Smart Maize Farming',
        defaults={
            'content': 'Use drought-tolerant varieties and practice intercropping with legumes to improve soil fertility.',
            'category': cat1,
            'author': admin,
            'is_featured': True
        }
    )
    article2, _ = Article.objects.get_or_create(
        title='Hermetic Storage Bags',
        defaults={
            'content': 'Airtight bags protect maize from weevils and reduce losses by up to 90%.',
            'category': cat2,
            'author': admin,
            'is_featured': False
        }
    )
    print('✅ Seeded successfully.')
else:
    print('❌ No admin user found. Create one with: python manage.py createsuperuser')
