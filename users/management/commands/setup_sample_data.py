from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
import random
from decimal import Decimal

from users.models import User
from fishing.models import Catch
from content.models import TimelinePost, EducationalContent, PostLike


class Command(BaseCommand):
    help = 'Setup sample data for the Sustainable Fishing platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=20,
            help='Number of users to create',
        )
        parser.add_argument(
            '--catches',
            type=int,
            default=50,
            help='Number of catch records to create',
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=30,
            help='Number of timeline posts to create',
        )
        parser.add_argument(
            '--educational',
            type=int,
            default=15,
            help='Number of educational content items to create',
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create superuser if it doesn't exist
            if not User.objects.filter(username='admin').exists():
                admin_user = User.objects.create_superuser(
                    username='admin',
                    email='admin@sustainablefishing.com',
                    password='admin123',
                    full_name='System Administrator',
                    role='admin'
                )
                self.stdout.write(self.style.SUCCESS(f'Created superuser: admin'))
            else:
                admin_user = User.objects.get(username='admin')

            # Create sample users
            self.create_users(options['users'])
            
            # Create sample catches
            self.create_catches(options['catches'])
            
            # Create sample posts
            self.create_posts(options['posts'])
            
            # Create sample educational content
            self.create_educational_content(options['educational'])
            
            # Create sample likes
            self.create_likes()
            
            self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_users(self, count):
        """Create sample users"""
        fishermen_names = [
            'John Fisher', 'Maria Santos', 'David Ocean', 'Lisa Wave',
            'Carlos Tide', 'Anna Deep', 'Miguel Shore', 'Sofia Blue',
            'Pedro Coast', 'Elena Marina', 'Roberto Bay', 'Carmen Sea',
            'Juan Reef', 'Isabella Current', 'Diego Anchor'
        ]
        
        educator_names = [
            'Dr. Sarah Marine', 'Prof. James Sustainable', 'Dr. Emily Conservation',
            'Prof. Michael Ecology', 'Dr. Linda Environmental'
        ]
        
        locations = [
            'Atlantic Coast', 'Pacific Shore', 'Gulf of Mexico', 'Caribbean Sea',
            'Mediterranean', 'Baltic Sea', 'Indian Ocean', 'Arctic Waters',
            'Coral Reef Area', 'Deep Sea Region'
        ]
        
        # Create fishermen
        for i in range(min(count - 5, len(fishermen_names))):
            name = fishermen_names[i]
            username = name.lower().replace(' ', '_')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    full_name=name,
                    role='fisherman',
                    location=random.choice(locations),
                    bio=f'Experienced fisherman from {random.choice(locations)}. Passionate about sustainable fishing practices.',
                    created_at=timezone.now() - timedelta(days=random.randint(1, 365))
                )
                self.stdout.write(f'Created fisherman: {name}')
        
        # Create educators
        for i in range(min(5, len(educator_names))):
            name = educator_names[i]
            username = name.lower().replace(' ', '_').replace('.', '')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    full_name=name,
                    role='educator',
                    location=random.choice(locations),
                    bio=f'Marine biologist and educator specializing in sustainable fishing practices.',
                    created_at=timezone.now() - timedelta(days=random.randint(1, 365))
                )
                self.stdout.write(f'Created educator: {name}')

    def create_catches(self, count):
        """Create sample catch records"""
        fish_types = [
            'Tuna', 'Salmon', 'Cod', 'Mackerel', 'Sardine', 'Anchovy',
            'Bass', 'Snapper', 'Grouper', 'Mahi-mahi', 'Halibut', 'Flounder',
            'Shrimp', 'Lobster', 'Crab', 'Squid'
        ]
        
        locations = [
            'Deep Sea Area A', 'Coastal Zone B', 'Reef Region C', 'Open Ocean D',
            'Fishing Ground E', 'Marine Protected Area F', 'Traditional Spot G'
        ]
        
        statuses = ['sold', 'unsold', 'donated']
        
        fishermen = User.objects.filter(role='fisherman')
        
        for i in range(count):
            catch = Catch.objects.create(
                fisher=random.choice(fishermen),
                fish_type=random.choice(fish_types),
                weight=Decimal(str(random.uniform(0.5, 50.0))),
                location=random.choice(locations),
                catch_date=timezone.now().date() - timedelta(days=random.randint(1, 90)),
                status=random.choice(statuses),
                price=Decimal(str(random.uniform(10.0, 500.0))) if random.choice([True, False]) else None,
                notes=f'Good quality {random.choice(fish_types).lower()} caught in {random.choice(locations)}',
                created_at=timezone.now() - timedelta(days=random.randint(1, 90))
            )
            
        self.stdout.write(f'Created {count} catch records')

    def create_posts(self, count):
        """Create sample timeline posts"""
        post_titles = [
            'Great day on the water!', 'Sustainable fishing tips', 'Today\'s catch',
            'Beautiful sunset fishing', 'New fishing techniques', 'Conservation awareness',
            'Community fishing event', 'Weather report update', 'Seasonal fishing guide',
            'Equipment maintenance tips', 'Fish species identification', 'Safety first!',
            'Local fishing regulations', 'Catch and release best practices'
        ]
        
        post_contents = [
            'Had an amazing day fishing today. The weather was perfect and the fish were biting!',
            'Here are some tips for sustainable fishing that everyone should know...',
            'Today\'s catch was exceptional. Remember to follow local regulations!',
            'The sunset was absolutely beautiful during our evening fishing trip.',
            'Learning new techniques helps improve both catch rates and sustainability.',
            'It\'s important to be aware of conservation efforts in our fishing areas.',
            'Join us for our community fishing event next weekend!',
            'Weather conditions are looking great for fishing this week.',
            'Here\'s a guide to seasonal fishing in our local waters.',
            'Regular equipment maintenance ensures safe and effective fishing.'
        ]
        
        post_types = ['general', 'catch_share', 'education', 'tip']
        
        users = User.objects.all()
        
        for i in range(count):
            post = TimelinePost.objects.create(
                author=random.choice(users),
                title=random.choice(post_titles),
                content=random.choice(post_contents),
                post_type=random.choice(post_types),
                likes_count=random.randint(0, 50),
                created_at=timezone.now() - timedelta(days=random.randint(1, 60))
            )
            
        self.stdout.write(f'Created {count} timeline posts')

    def create_educational_content(self, count):
        """Create sample educational content"""
        content_titles = [
            'Sustainable Fishing Practices 101', 'Understanding Fish Habitats',
            'Seasonal Fishing Patterns', 'Marine Conservation Basics',
            'Fishing Equipment and Safety', 'Catch and Release Techniques',
            'Local Fishing Regulations Guide', 'Weather and Fishing Conditions',
            'Fish Species Identification', 'Sustainable Seafood Choices',
            'Ocean Health and Fishing', 'Traditional Fishing Methods',
            'Modern Fishing Technology', 'Community-Based Fishing Management'
        ]
        
        content_bodies = [
            'Sustainable fishing is crucial for maintaining healthy marine ecosystems...',
            'Understanding fish habitats helps fishermen make better decisions...',
            'Different seasons bring different fishing opportunities and challenges...',
            'Marine conservation is essential for the future of fishing...',
            'Proper equipment and safety measures are vital for successful fishing...',
            'Catch and release techniques help preserve fish populations...',
            'Understanding local regulations ensures compliance and sustainability...',
            'Weather conditions significantly impact fishing success and safety...',
            'Proper fish identification helps with conservation and regulations...',
            'Making sustainable seafood choices supports healthy ocean ecosystems...'
        ]
        
        categories = ['sustainability', 'techniques', 'regulations', 'conservation']
        difficulty_levels = ['beginner', 'intermediate', 'advanced']
        
        educators = User.objects.filter(role='educator')
        
        for i in range(count):
            content = EducationalContent.objects.create(
                author=random.choice(educators),
                title=random.choice(content_titles),
                content=random.choice(content_bodies),
                category=random.choice(categories),
                difficulty_level=random.choice(difficulty_levels),
                is_published=random.choice([True, True, False]),  # 2/3 chance of being published
                featured=random.choice([True, False, False, False]),  # 1/4 chance of being featured
                read_count=random.randint(0, 1000),
                created_at=timezone.now() - timedelta(days=random.randint(1, 180))
            )
            
        self.stdout.write(f'Created {count} educational content items')

    def create_likes(self):
        """Create sample likes for posts"""
        posts = TimelinePost.objects.all()
        users = User.objects.all()
        
        for post in posts:
            # Randomly assign likes to posts
            num_likes = random.randint(0, min(post.likes_count, len(users)))
            liked_users = random.sample(list(users), num_likes)
            
            for user in liked_users:
                PostLike.objects.get_or_create(
                    user=user,
                    post=post,
                    defaults={
                        'created_at': timezone.now() - timedelta(days=random.randint(1, 30))
                    }
                )
        
        self.stdout.write('Created sample likes for posts')
