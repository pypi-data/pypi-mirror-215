class MongeasyTestPlugin:
    def before_connect(self):
        print("before_connect_plugin: before_connect")
        return True

    def after_connect(self):
        print("after_connect_plugin: after_connect")
        return True
    
    def before_close(self):
        print("before_close_plugin: before_close")
        return True
    
    def after_close(self):
        print("after_close_plugin: after_close")
        return True
    
    def before_delete_document(self, *args, **kwargs):
        print(f"before_delete_document_plugin: before_delete_document")
        return True
        
    def after_delete_document(self, *args, **kwargs):
        print(f"after_delete_document_plugin: after_delete_document")
        return True

    def before_init_document(self, *args, **kwargs):
        print(f"before_init_document_plugin: before_init_document, data: {args}, {kwargs}")
        return True
        
    def after_init_document(self, data):
        print(f"after_init_document_plugin: after_init_document, data: {data}")
        return True

    def before_query_document(self, cls, *args, **kwargs):
        print(f"before_query_document_plugin: before_query_document, data: {cls}, {args}, {kwargs}")
        return True        
    
    def after_query_document(self, cls, *args, **kwargs):
        print(f"after_query_document_plugin: after_query_document, data: {cls}, {args}, {kwargs}")
        return True        

    def before_save_document(self, *args, **kwargs):
        print(f"before_save_plugin: before_save, data: {args}, {kwargs}")
        return True        
            
    def after_save_document(self, data):
        print(f"after_save_plugin: after_save, data: {data}")
        return True        
    
    def validate_document(self, *args, **kwargs):
        print(f"validate_document_plugin: validate_document, data: {args}, {kwargs}")
        return True        
            
    def on_document_validation_error(self, *args, **kwargs):
        print(f"on_document_validation_error_plugin: on_document_validation_error, data: {args}, {kwargs}")
        return True        


