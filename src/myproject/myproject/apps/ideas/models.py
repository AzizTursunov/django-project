import contextlib
import os
import uuid

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now as timezone_now

from myproject.apps.core.models import (
    CreationModificationDateBase,
    MetaTagsBase,
    UrlBase,
    object_relation_base_factory as generic_relation
)
from myproject.apps.core.model_field import (
    MultilingualCharField,
    MultilingualTextField,
    TranslatedField
)

RATING_CHOICES = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

FavoriteObjectBase = generic_relation(is_required=True)

OwnerBase = generic_relation(
    prefix='owner',
    prefix_verbose=_('Owner'),
    is_required=True,
    add_related_name=True,
    limit_content_type_choices_to={
        'model': 'user'
    }
)


def upload_to(instance, filename):
    now = timezone_now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f'ideas/{now:%Y/%m}/{instance.pk}{extension}'


class Like(FavoriteObjectBase, OwnerBase):
    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    def __str__(self):
        return _('{owner} likes {object}').format(
            owner=self.owner_content_object,
            object=self.content_object
        )


class Idea(CreationModificationDateBase,
           MetaTagsBase,
           UrlBase):
    title = MultilingualCharField(
        _('Title'),
        max_length=200
    )
    content = MultilingualTextField(
        _('Content')
    )

    # To avoid circular dependencies use <app_label>.<model> for FK
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        default=None
    )

    category = models.ForeignKey(
        'categories.Category',
        verbose_name=_('Category'),
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        verbose_name = _('Idea')
        verbose_name_plural = _('Ideas')

    def __str__(self):
        return self.title

    def get_url_path(self):
        return reverse('idea-detail', kwargs={'idea_id': self.id})


CommentObject = generic_relation(
    is_required=True,
    limit_content_type_choices_to={
        # 'app_label': 'ideas',
        'model__in': ('idea', 'newsarticle')
    }
)

CommentOwner = generic_relation(
    prefix='commentator',
    prefix_verbose=_('Commentator'),
    is_required=True,
    add_related_name=True,
    limit_content_type_choices_to={
        'model': 'user'
    }
)


class Comment(CommentObject, CommentOwner):

    text = models.CharField(
        max_length=255,
        verbose_name=_('Comment text'),
        help_text=_('Enter your comment'),
        null=True
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return _('{owner} comments {object}').format(
            owner=self.commentator_content_object,
            object=self.content_object
        )


class IdeaWithTranslatedFields(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        max_length=36
    )
    title = models.CharField(
        _('Title'),
        max_length=200
    )
    content = models.TextField(
        _('Content')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='authored_ideas'
    )
    # 12M relation can be deleted after adding M2M and steps with migrations
    # category = models.ForeignKey(
    #     'categories.Category',
    #     verbose_name=_('Category'),
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name='category_ideas'
    # )
    categories = models.ManyToManyField(
        'categories.Category',
        verbose_name=_('Categories'),
        blank=True,
        related_name='category_ideas'
    )
    rating = models.PositiveSmallIntegerField(
        _('Rating'),
        choices=RATING_CHOICES,
        blank=True,
        null=True
    )
    translated_title = TranslatedField('title')
    translated_content = TranslatedField('content')

    picture = models.ImageField(
        _('Picture'),
        upload_to=upload_to,
        blank=True,
        null=True
    )
    picture_social = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(1024, 512)],
        format='JPEG',
        options={'quality': 100}
    )
    picture_large = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(800, 400)],
        format='PNG'
    )
    picture_thumbnail = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(728, 250)],
        format='PNG'
    )

    class Meta:
        verbose_name = _('Idea With Translations')
        verbose_name_plural = _('Ideas With Translations')
        # unique title for each author,
        # but title can be repeated if author is not set
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                condition=~models.Q(author=None),
                name='unique_title_for_each_author'
            ),
            # uniqe title for single author
            # constraints = [
            #     models.UniqueConstraint(
            #         fields=['title', 'author'],
            #         name='uniqe_title_for_single_author'
            #     )
            # ]
            models.CheckConstraint(
                check=models.Q(
                    title__iregex=r'^\S.*\S$'
                    # starts with non-whitespace,
                    # ends with non-whitespace,
                    # anything in the middle
                ),
                name='title_has_no_leading_and_traling_whitespaces'
            )
        ]

    def __str__(self):
        return self.title

    def clean(self):
        '''
        Implement the validation to have data validated at the forms.
        '''
        import re
        if self.author and IdeaWithTranslatedFields.objects.exclude(pk=self.pk).filter(
            title=self.title
        ).exists():
            raise ValidationError(
                _('Each idea of some user should have a unique title.')
            )
        if not re.match(r'^\S.*\S$', self.title):
            raise ValidationError(
                _('The title cannot start or end with a whitespace.')
            )

    def get_url_path(self):
        return reverse('ideas:idea_detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage
        if self.picture:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(
                    self.picture_social.path
                )
                default_storage.delete(
                    self.picture_large.path
                )
                default_storage.delete(
                    self.picture_thumbnail.path
                )
            self.picture.delete()
        super().delete(*args, **kwargs)


class IdeaTranslations(models.Model):
    idea = models.ForeignKey(
        IdeaWithTranslatedFields,
        verbose_name=_('Idea'),
        on_delete=models.CASCADE,
        related_name='translations'
    )
    language = models.CharField(
        _('Language'),
        max_length=7
    )
    title = models.CharField(
        _('Title'),
        max_length=200
    )
    content = models.TextField(
        _('Content')
    )

    class Meta:
        verbose_name = _('Idea Translations')
        verbose_name_plural = _('Idea Translations')
        ordering = ['language']
        unique_together = [('idea', 'language')]

    def __str__(self):
        return self.title
