#  Copyright (c) 2019, CRS4
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of
#  this software and associated documentation files (the "Software"), to deal in
#  the Software without restriction, including without limitation the rights to
#  use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#  the Software, and to permit persons to whom the Software is furnished to do so,
#  subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db import IntegrityError
from promort.settings import DEFAULT_GROUPS
from slides_manager.models import Case
from reviews_manager.models import ROIsAnnotation, ROIsAnnotationStep

from uuid import uuid4
import logging

logger = logging.getLogger('promort_commands')


class Command(BaseCommand):
    help = 'build first reviewers worklist based on the existing cases and slides'

    def _get_rois_manager_users(self):
        rois_manager_group = Group.objects.get(name=DEFAULT_GROUPS['rois_manager']['name'])
        return rois_manager_group.user_set.all()

    def _get_cases_list(self):
        return Case.objects.all()

    def _create_rois_annotation(self, case_obj, reviewer_obj):
        try:
            annotation_obj = ROIsAnnotation.objects.get(case=case_obj)
            logger.info('There is already a ROIs Annotation object (label %s) and it\'s assigned to %s',
                        annotation_obj.label, annotation_obj.reviewer.username)
        except ROIsAnnotation.DoesNotExist:
            annotation_obj = ROIsAnnotation(case=case_obj, reviewer=reviewer_obj,
                                            label=uuid4().hex)
            annotation_obj.save()
            logger.info('Saved new ROIs Annotation with label %s and assigne to %s',
                        annotation_obj.label, reviewer_obj.username)
        return annotation_obj

    def _get_annotation_step_label(self, annotation_label, slide_label):
        slide_index = slide_label.split('-')[-1]
        return '%s-%s' % (annotation_label, slide_index)

    def _create_rois_annotation_step(self, rois_annotation_obj, slide_obj):
        annotation_step_obj = ROIsAnnotationStep(
            rois_annotation=rois_annotation_obj, slide=slide_obj,
            label=self._get_annotation_step_label(rois_annotation_obj.label, slide_obj.id)
        )
        try:
            annotation_step_obj.save()
            logger.info('Saved new ROIs Annotation Step with label %s', annotation_step_obj.label)
        except IntegrityError:
            annotation_step_obj = ROIsAnnotationStep.objects.get(rois_annotation=rois_annotation_obj, slide=slide_obj)
            logger.info('There is already a ROIs Annotation Step object (label %s)', annotation_step_obj.label)
        return annotation_step_obj

    def handle(self, *args, **opts):
        logger.info('=== Starting ROIs worklist creation ===')
        rois_managers = self._get_rois_manager_users()
        cases = self._get_cases_list()
        for i, case in enumerate(cases):
            logger.info('Processing case %s', case.id)
            annotation_obj = self._create_rois_annotation(case, rois_managers[i % len(rois_managers)])
            for slide in case.slides.all():
                logger.info('Processing slide %s', slide.id)
                self._create_rois_annotation_step(annotation_obj, slide)
        logger.info('=== ROIs worklist creation completed ===')
