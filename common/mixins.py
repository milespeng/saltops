# class AjaxDeleteResponseMixin(object):
#     def form_valid(self, form):
#         response = super(AjaxDeleteResponseMixin, self).form_valid(form)
#         if self.request.is_ajax():
#             data = {
#                 'pk': self.object.pk,
#             }
#             return JsonResponse(data)
#         else:
#             return response
