def send_notification(title, message, duration, callback):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=duration, callback_on_click=callback, threaded=False)
