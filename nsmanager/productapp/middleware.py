class SetCompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            company = getattr(request.user, 'company', None)
            request.company = company
        else:
            request.company = None
        
        response = self.get_response(request)
        return response
users = forms.ModelMultipleChoiceField(
    queryset=User.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False
)
