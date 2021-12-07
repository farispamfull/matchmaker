from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


class Util:
    @staticmethod
    def send_match_for_email(request, from_user, match_user):
        mail_subject = get_current_site(request).domain
        send_mail(f'find match from {mail_subject}',

                  f'У вас появилась взаимная симпатия:\n'
                  f'{match_user.first_name} {match_user.last_name}\n'
                  f'{match_user.email}\n'
                  f'Удачного вам знакомства, {from_user.first_name}',

                  f'{settings.EMAIL_HOST_USER}',

                  [from_user.email],
                  fail_silently=False, )

    @staticmethod
    def normalize_email(email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """

        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name.lower() + '@' + domain_part.lower()
        return email

    @staticmethod
    def compress_image(photo, text='Matchmaker Copyright', size=100):
        upload = 'media/' + photo
        image = Image.open(upload)
        width, height = image.size

        draw = ImageDraw.Draw(image)
        text = text

        font = ImageFont.load_default()
        textwidth, textheight = draw.textsize(text, font)

        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin

        draw.text((x, y), text, font=font)

        image.save(upload)
