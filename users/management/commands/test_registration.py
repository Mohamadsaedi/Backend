import io
import re
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.test import Client
from users.utils import activateEmail

class Command(BaseCommand):
    help = 'Tests the user registration and email sending process.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpassword'

        # Clean up any existing test user
        User.objects.filter(username=username).delete()

        self.stdout.write(f"Creating a new inactive user: {username}")
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        self.stdout.write("Sending the activation email...")

        # Capture the email content by redirecting stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        # We still need a request for activateEmail, but it doesn't need messages
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/')
        activateEmail(request, user)

        sys.stdout = old_stdout
        email_content = captured_output.getvalue()

        self.stdout.write("Activation email sent (content captured).")

        # Extract the activation URL from the email content
        match = re.search(r'href="http://example.com(.+?)"', email_content)
        if not match:
            self.stderr.write("Could not find activation URL in email content.")
            user.delete()
            return

        activation_url = match.group(1)
        self.stdout.write(f"Extracted activation URL: {activation_url}")

        self.stdout.write("Simulating user clicking the activation link...")

        client = Client()

        # Capture the welcome email
        sys.stdout = captured_output = io.StringIO()

        response = client.get(activation_url)

        sys.stdout = old_stdout
        welcome_email_content = captured_output.getvalue()

        if response.status_code == 302 and response.url == '/accounts/login/':
             self.stdout.write("✅ Activation successful, redirected to login page.")
        else:
            self.stderr.write(f"❌ Activation failed. Status code: {response.status_code}")
            self.stderr.write(f"Content: {response.content.decode('utf-8')}")


        if "Welcome to Our Website!" in welcome_email_content:
            self.stdout.write("✅ Welcome email sent successfully after activation.")
        else:
            self.stderr.write("❌ Welcome email not found in output after activation.")

        # Verify user is active
        user.refresh_from_db()
        if user.is_active:
            self.stdout.write("✅ User is now active.")
        else:
            self.stderr.write("❌ User is still inactive.")

        # Clean up the created user
        user.delete()
        self.stdout.write("Test finished and test user deleted.")
