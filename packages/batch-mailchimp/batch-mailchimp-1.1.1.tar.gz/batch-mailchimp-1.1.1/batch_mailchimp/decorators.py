def no_batch(func):
    def wrapper_no_batch(self, *args, **kwargs):
        batch_mode = self.api_client.batch_mode
        self.api_client.set_batch_mode(False)
        try:
            response = func(self, *args, **kwargs)
        finally:
            self.api_client.set_batch_mode(batch_mode)
        return response
    return wrapper_no_batch
