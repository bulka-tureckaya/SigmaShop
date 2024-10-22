from django.core.mail import send_mail
from myshop.settings import EMAIL_HOST_USER

def send_created(order, form):
    message = "Ваш заказ успешно сформирован.\n" \
             f"Номер заказa: {order.id}\n" \
             f"Адрес: {form.cleaned_data['address']}\n" \
             f"Индекс: {form.cleaned_data['postal_code']}\n" \
             f"Город: {form.cleaned_data['city']}"
            
    send_mail("Заказ сформирован",
              message,
              EMAIL_HOST_USER,
              [form.cleaned_data['email']],
              fail_silently=False,
    )