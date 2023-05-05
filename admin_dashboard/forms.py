from django.forms import ModelForm
from frontend.models import BookDelivery


class EditDeliveryForm(ModelForm):
    
    class Meta:
        model = BookDelivery
        fields = ['rider', 'pickup_location', 'destination_location',
                'reciever_contact', 'sender_contact', 'order_status']
        labels = {
            'rider':'Assign Rider'
        }
        
    def __init__(self, *args, **kwargs):
        super(EditDeliveryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
        self.fields['rider'].widget.attrs.update({'class': 'form-control form-select select2'})
        self.fields['order_status'].widget.attrs.update({'class': 'form-control form-select select2'})
            
            
 
            
            
class BookDeliveryForm(ModelForm):
    
    class Meta:
        model = BookDelivery
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(BookDeliveryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control '})

            self.fields["rider"].widget.attrs.update({'class': 'form-control form-select select2'})
            self.fields["profile"].widget.attrs.update({'class': 'form-control form-select select2'})   
            self.fields["order_status"].widget.attrs.update({'class': 'form-control form-select select2'})
        
