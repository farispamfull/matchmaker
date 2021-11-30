from PIL import Image, ImageDraw, ImageFont


class Util:
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
    def compress_image(photo, text='Matchmaker Copyright', size=40):
        upload = 'media/' + photo
        image = Image.open(upload)
        width, height = image.size

        draw = ImageDraw.Draw(image)
        text = text

        font = ImageFont.truetype('arial.ttf', size)
        textwidth, textheight = draw.textsize(text, font)

        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin

        draw.text((x, y), text, font=font)

        image.save(upload)

